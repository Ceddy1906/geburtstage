"""Integration tests (need pytest-homeassistant-custom-component)."""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.setup import async_setup_component
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_capture_events,
    async_mock_service,
)

from custom_components.geburtstage.calendar import GeburtstageCalendar
from custom_components.geburtstage.const import DOMAIN, EVENT_BIRTHDAY, EVENT_REMINDER


async def _setup(hass: HomeAssistant) -> MockConfigEntry:
    # Skip loading the real http/frontend stack – it is not what we test here.
    for component in ("http", "frontend", "panel_custom", "websocket_api"):
        hass.config.components.add(component)
    entry = MockConfigEntry(domain=DOMAIN, data={}, title="Geburtstage")
    entry.add_to_hass(hass)
    with patch("custom_components.geburtstage._async_setup_frontend", AsyncMock()):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    return entry


def _born(offset_days: int = 0, year: int = 1992) -> str:
    """Birthdate (leap year, so every day exists) whose birthday is today + offset."""
    day = dt_util.now().date() + timedelta(days=offset_days)
    return date(year, day.month, day.day).isoformat()


async def test_add_person_and_sensor(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    await hass.services.async_call(
        DOMAIN,
        "add_person",
        {"first_name": "Max", "last_name": "Müller", "birthdate": _born(5), "salutation": "herr"},
        blocking=True,
    )
    registry = er.async_get(hass)
    entity_id = registry.async_get_entity_id("sensor", DOMAIN, f"{entry.entry_id}_upcoming")
    state = hass.states.get(entity_id)
    assert state.state == "1"
    item = state.attributes["birthdays"][0]
    assert item["name"] == "Max Müller"
    assert item["days_until"] == 5
    assert item["turning_age"] == (dt_util.now().date() + timedelta(days=5)).year - 1992
    assert "greeting_notify" not in item  # private data stays out of the attribute


async def test_validation_errors(hass: HomeAssistant) -> None:
    await _setup(hass)
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            "add_person",
            {"first_name": "Max", "birthdate": _born(1), "greeting_enabled": True},
            blocking=True,
        )


async def test_birthday_greeting_is_sent_once(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    calls = async_mock_service(hass, "notify", "test_target")
    events = async_capture_events(hass, EVENT_BIRTHDAY)
    await hass.services.async_call(
        DOMAIN,
        "add_person",
        {
            "first_name": "Anna",
            "last_name": "Meier",
            "salutation": "frau",
            "birthdate": _born(0),
            "greeting_enabled": True,
            "greeting_notify": "notify.test_target",
        },
        blocking=True,
    )
    manager = entry.runtime_data
    await manager.async_run_daily()
    await manager.async_run_daily()  # second run must not send again
    await hass.async_block_till_done()

    assert len(calls) == 1
    assert "Anna" in calls[0].data["message"]
    assert calls[0].data["title"]
    assert len(events) == 1
    assert events[0].data["name"] == "Anna Meier"
    assert events[0].data["sent"] is True


async def test_greeting_event_only_when_auto_send_disabled(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    calls = async_mock_service(hass, "notify", "test_target")
    events = async_capture_events(hass, EVENT_BIRTHDAY)
    await hass.services.async_call(
        DOMAIN,
        "add_person",
        {"first_name": "Bob", "birthdate": _born(0), "greeting_notify": "notify.test_target"},
        blocking=True,
    )
    await entry.runtime_data.async_run_daily()
    await hass.async_block_till_done()
    assert not calls
    assert len(events) == 1 and events[0].data["auto_send"] is False
    assert events[0].data["message"]


async def test_reminders(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    calls = async_mock_service(hass, "notify", "me")
    events = async_capture_events(hass, EVENT_REMINDER)
    manager = entry.runtime_data
    manager.async_set_settings({"reminder_notify": "notify.me"})
    await hass.services.async_call(
        DOMAIN,
        "add_person",
        {"first_name": "Cleo", "last_name": "K", "birthdate": _born(2), "reminder_days_1": 1, "reminder_days_2": 2},
        blocking=True,
    )
    await manager.async_run_daily()
    await hass.async_block_till_done()
    assert len(calls) == 1  # only the 2-days reminder is due today
    assert "übermorgen" in calls[0].data["message"] or "day after" in calls[0].data["message"] or "in 2" in calls[0].data["message"]
    assert events[0].data["days_until"] == 2


async def test_calendar_events(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    await hass.services.async_call(
        DOMAIN, "add_person", {"first_name": "Dora", "birthdate": _born(3)}, blocking=True
    )
    # The calendar component needs a real HTTP server, so test the entity directly.
    entity = GeburtstageCalendar(entry.runtime_data, entry.entry_id)
    start = dt_util.now()
    events = await entity.async_get_events(hass, start, start + timedelta(days=10))
    assert len(events) == 1 and "Dora" in events[0].summary
    assert entity.event.summary.startswith("🎂 Dora")


async def test_persistence_roundtrip(hass: HomeAssistant, hass_storage) -> None:
    entry = await _setup(hass)
    await hass.services.async_call(
        DOMAIN, "add_person", {"first_name": "Emil", "birthdate": _born(9)}, blocking=True
    )
    manager = entry.runtime_data
    await manager._store.async_save(manager._data_to_save())
    saved = hass_storage["geburtstage.data"]["data"]
    assert saved["persons"][0]["first_name"] == "Emil"


async def test_import_skips_duplicates_and_reports_errors(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    manager = entry.runtime_data
    rows = [
        {"first_name": "Fritz", "last_name": "A", "birthdate": "1980-05-05", "year_known": True},
        {"first_name": "Fritz", "last_name": "A", "birthdate": "1980-05-05", "year_known": True},
        {"first_name": "", "birthdate": "1980-05-05"},
        {"first_name": "Gerda", "birthdate": "2000-02-29", "year_known": False},
    ]
    result = manager.async_import_persons(rows)
    assert result["added"] == 2 and result["skipped"] == 1 and len(result["errors"]) == 1


async def test_update_and_remove_by_name(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    await hass.services.async_call(
        DOMAIN, "add_person", {"first_name": "Hans", "last_name": "Z", "birthdate": _born(4)}, blocking=True
    )
    await hass.services.async_call(
        DOMAIN, "update_person", {"person": "hans z", "last_name": "Y"}, blocking=True
    )
    assert next(iter(entry.runtime_data.persons.values()))["last_name"] == "Y"
    await hass.services.async_call(DOMAIN, "remove_person", {"person": "Hans Y"}, blocking=True)
    assert not entry.runtime_data.persons


async def test_get_upcoming_response(hass: HomeAssistant) -> None:
    await _setup(hass)
    await hass.services.async_call(
        DOMAIN, "add_person", {"first_name": "Ida", "birthdate": _born(6)}, blocking=True
    )
    result = await hass.services.async_call(
        DOMAIN, "get_upcoming", {"days": 10}, blocking=True, return_response=True
    )
    assert [p["name"] for p in result["birthdays"]] == ["Ida"]

"""Tests for the websocket API used by the sidebar panel."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from homeassistant.exceptions import Unauthorized

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import async_mock_service

from custom_components.geburtstage import websocket as ws

from .test_integration import _born, _setup


def _conn(admin: bool = True) -> MagicMock:
    conn = MagicMock()
    conn.user.is_admin = admin
    return conn


async def _call(hass: HomeAssistant, handler, conn, payload: dict) -> None:
    # HA validates incoming messages with the command schema (this also applies defaults).
    msg = {"id": 1, **payload}
    schema = getattr(handler, "_ws_schema", None)
    if callable(schema):
        msg = schema(msg)
    handler(hass, conn, msg)
    await hass.async_block_till_done()


async def test_non_admin_is_rejected(hass: HomeAssistant) -> None:
    await _setup(hass)
    conn = _conn(admin=False)
    with pytest.raises(Unauthorized):
        await _call(hass, ws.ws_list, conn, {"type": "geburtstage/list"})
    conn.send_result.assert_not_called()


async def test_upsert_list_delete(hass: HomeAssistant) -> None:
    await _setup(hass)
    conn = _conn()
    person = {
        "first_name": "Max",
        "last_name": "Müller",
        "salutation": "herr",
        "style": "formal",
        "birthdate": _born(3),
        "year_known": True,
        "greeting_enabled": False,
        "greeting_notify": "",
        "reminder_days_1": 1,
        "reminder_days_2": None,
    }
    await _call(hass, ws.ws_upsert, conn, {"type": "geburtstage/upsert", "person": person})
    result = conn.send_result.call_args[0][1]["person"]
    pid = result["id"]
    assert result["name"] == "Max Müller" and result["days_until"] == 3

    # edit
    conn = _conn()
    await _call(hass, ws.ws_upsert, conn, {"type": "geburtstage/upsert", "person": {**person, "id": pid, "first_name": "Moritz"}})
    assert conn.send_result.call_args[0][1]["person"]["name"] == "Moritz Müller"

    conn = _conn()
    await _call(hass, ws.ws_list, conn, {"type": "geburtstage/list"})
    data = conn.send_result.call_args[0][1]
    assert len(data["persons"]) == 1
    assert len(data["settings"]["texts_personal"]) == 10
    assert data["settings"]["texts_personal_is_default"] is True

    conn = _conn()
    await _call(hass, ws.ws_delete, conn, {"type": "geburtstage/delete", "person_id": pid})
    conn.send_result.assert_called_once_with(1)
    conn = _conn()
    await _call(hass, ws.ws_delete, conn, {"type": "geburtstage/delete", "person_id": pid})
    assert conn.send_error.call_args[0][1] == "not_found"


async def test_upsert_validation_error(hass: HomeAssistant) -> None:
    await _setup(hass)
    conn = _conn()
    await _call(
        hass,
        ws.ws_upsert,
        conn,
        {"type": "geburtstage/upsert", "person": {"first_name": "", "birthdate": "2000-01-01"}},
    )
    assert conn.send_error.call_args[0][1] == "invalid_format"


async def test_settings_and_preview(hass: HomeAssistant) -> None:
    await _setup(hass)
    conn = _conn()
    await _call(
        hass,
        ws.ws_settings_set,
        conn,
        {
            "type": "geburtstage/settings_set",
            "settings": {"send_time": "09:30:00", "texts_personal": ["{gruss}, Prost!"], "reminder_template": None},
        },
    )
    settings = conn.send_result.call_args[0][1]["settings"]
    assert settings["send_time"] == "09:30:00"
    assert settings["texts_personal"] == ["{gruss}, Prost!"]
    assert settings["texts_personal_is_default"] is False
    assert settings["texts_formal_is_default"] is True

    conn = _conn()
    await _call(
        hass,
        ws.ws_preview,
        conn,
        {
            "type": "geburtstage/preview",
            "person": {"first_name": "Anna", "salutation": "frau", "birthdate": "1990-05-05"},
        },
    )
    assert conn.send_result.call_args[0][1]["message"] == "Liebe Anna, Prost!" or "Anna" in conn.send_result.call_args[0][1]["message"]

    conn = _conn()
    await _call(
        hass,
        ws.ws_settings_set,
        conn,
        {"type": "geburtstage/settings_set", "settings": {"send_time": "25:99"}},
    )
    assert conn.send_error.call_args[0][1] == "invalid_format"


async def test_notify_targets_listed(hass: HomeAssistant) -> None:
    await _setup(hass)
    async_mock_service(hass, "notify", "mein_handy")
    conn = _conn()
    await _call(hass, ws.ws_notify_targets, conn, {"type": "geburtstage/notify_targets"})
    values = [t["value"] for t in conn.send_result.call_args[0][1]["targets"]]
    assert "notify.mein_handy" in values


async def test_send_test_goes_to_admin_target_never_to_the_person(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    mine = async_mock_service(hass, "notify", "mein_handy")
    persons = async_mock_service(hass, "notify", "person_target")
    entry.runtime_data.async_set_settings({"reminder_notify": "notify.mein_handy"})
    desc = entry.runtime_data.async_upsert_person(
        {
            "first_name": "Test",
            "birthdate": "1990-01-01",
            "greeting_enabled": True,
            "greeting_notify": "notify.person_target",
        }
    )
    # stored person
    conn = _conn()
    await _call(hass, ws.ws_send_test, conn, {"type": "geburtstage/send_test", "person_id": desc["id"]})
    assert len(mine) == 1 and mine[0].data["message"].startswith("[Test für Test]")
    assert not persons
    assert conn.send_result.call_args[0][1]["notify"] == "notify.mein_handy"

    # unsaved form data, person without own target
    conn = _conn()
    await _call(
        hass,
        ws.ws_send_test,
        conn,
        {"type": "geburtstage/send_test", "person": {"first_name": "Neu", "birthdate": "1990-01-01"}},
    )
    assert len(mine) == 2 and "Neu" in mine[1].data["message"]
    assert not persons


async def test_send_test_without_admin_target_is_an_error(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    person_calls = async_mock_service(hass, "notify", "person_target")
    conn = _conn()
    await _call(
        hass,
        ws.ws_send_test,
        conn,
        {
            "type": "geburtstage/send_test",
            "person": {
                "first_name": "Neu",
                "birthdate": "1990-01-01",
                "greeting_notify": "notify.person_target",
            },
        },
    )
    assert conn.send_error.call_args[0][1] == "no_target"
    assert not person_calls  # even though the person has a target, nothing was sent


async def test_settings_equal_to_defaults_are_stored_as_default(hass: HomeAssistant) -> None:
    entry = await _setup(hass)
    manager = entry.runtime_data
    view = manager.settings_view()
    manager.async_set_settings(
        {
            "texts_personal": view["texts_personal"],
            "reminder_template": view["reminder_template"],
            "greeting_title": view["greeting_title"],
        }
    )
    assert manager.settings["texts_personal"] is None
    assert manager.settings["reminder_template"] is None
    assert manager.settings["greeting_title"] == ""

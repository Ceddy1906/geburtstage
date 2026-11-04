"""Sensors for Geburtstage."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GeburtstageConfigEntry
from .const import UPCOMING_WINDOW_DAYS
from .entity import GeburtstageEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GeburtstageConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensors."""
    manager = entry.runtime_data
    async_add_entities(
        [
            UpcomingBirthdaysSensor(manager, entry.entry_id),
            NextBirthdaySensor(manager, entry.entry_id),
            TodayBirthdaysSensor(manager, entry.entry_id),
        ]
    )


class UpcomingBirthdaysSensor(GeburtstageEntity, SensorEntity):
    """Number of birthdays in the next 30 days; attribute ``birthdays`` feeds the card."""

    _attr_icon = "mdi:cake-variant"
    _attr_native_unit_of_measurement = None
    # The list can get long – keep it out of the recorder database.
    _unrecorded_attributes = frozenset({"birthdays"})

    def __init__(self, manager, entry_id: str) -> None:
        super().__init__(manager, entry_id, "upcoming")

    @property
    def native_value(self) -> int:
        return sum(
            1 for p in self._manager.public_list() if p["days_until"] <= UPCOMING_WINDOW_DAYS
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        items = self._manager.public_list()
        return {"birthdays": items, "total": len(items), "window_days": UPCOMING_WINDOW_DAYS}


class NextBirthdaySensor(GeburtstageEntity, SensorEntity):
    """The person whose birthday comes next."""

    _attr_icon = "mdi:calendar-star"

    def __init__(self, manager, entry_id: str) -> None:
        super().__init__(manager, entry_id, "next_birthday")

    def _first(self) -> dict[str, Any] | None:
        items = self._manager.public_list()
        return items[0] if items else None

    @property
    def native_value(self) -> str | None:
        first = self._first()
        return first["name"] if first else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        first = self._first()
        if not first:
            return {}
        return {
            "person_id": first["id"],
            "date": first["next_date"],
            "days_until": first["days_until"],
            "age": first["turning_age"],
            "is_today": first["is_today"],
        }


class TodayBirthdaysSensor(GeburtstageEntity, SensorEntity):
    """Number of birthdays today; attribute ``names`` lists them."""

    _attr_icon = "mdi:party-popper"

    def __init__(self, manager, entry_id: str) -> None:
        super().__init__(manager, entry_id, "today")

    def _today(self) -> list[dict[str, Any]]:
        return [p for p in self._manager.public_list() if p["is_today"]]

    @property
    def native_value(self) -> int:
        return len(self._today())

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        today = self._today()
        return {
            "names": [p["name"] for p in today],
            "birthdays": today,
        }

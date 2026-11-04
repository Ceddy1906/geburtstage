"""Calendar platform for Geburtstage."""

from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from . import GeburtstageConfigEntry
from .entity import GeburtstageEntity
from .logic import describe, occurrence


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GeburtstageConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the calendar."""
    async_add_entities([GeburtstageCalendar(entry.runtime_data, entry.entry_id)])


class GeburtstageCalendar(GeburtstageEntity, CalendarEntity):
    """All birthdays as all-day events."""

    _attr_icon = "mdi:cake-variant"

    def __init__(self, manager, entry_id: str) -> None:
        super().__init__(manager, entry_id, "calendar")

    @staticmethod
    def _summary(name: str, age: int | None) -> str:
        return f"🎂 {name} ({age})" if age is not None else f"🎂 {name}"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the current or next birthday."""
        items = self._manager.describe_all()
        if not items:
            return None
        first = items[0]
        day = dt_util.parse_date(first["next_date"])
        return CalendarEvent(
            start=day,
            end=day + timedelta(days=1),
            summary=self._summary(first["name"], first["turning_age"]),
            uid=f"{first['id']}-{first['next_date']}",
        )

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Return birthdays between two datetimes (end exclusive)."""
        start = dt_util.as_local(start_date).date()
        end = dt_util.as_local(end_date).date()
        events: list[CalendarEvent] = []
        for person in self._manager.persons.values():
            desc = describe(person, start)
            for year in range(start.year, end.year + 1):
                occ = occurrence(desc["month"], desc["day"], year)
                if not start <= occ < end:
                    continue
                age = None
                if desc["year_known"]:
                    age = year - int(person["birthdate"][:4])
                    if age < 0:
                        continue
                events.append(
                    CalendarEvent(
                        start=occ,
                        end=occ + timedelta(days=1),
                        summary=self._summary(desc["name"], age),
                        uid=f"{person['id']}-{occ.isoformat()}",
                    )
                )
        events.sort(key=lambda e: (e.start, e.summary))
        return events

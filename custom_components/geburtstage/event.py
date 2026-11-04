"""Event entity for Geburtstage – usable as trigger in the automation editor."""

from __future__ import annotations

from typing import Any

from homeassistant.components.event import EventEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GeburtstageConfigEntry
from .const import EVENT_TYPE_BIRTHDAY, EVENT_TYPE_REMINDER
from .entity import GeburtstageEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GeburtstageConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the event entity."""
    async_add_entities([GeburtstageEventEntity(entry.runtime_data, entry.entry_id)])


class GeburtstageEventEntity(GeburtstageEntity, EventEntity):
    """Fires ``birthday`` and ``reminder`` events with all details as attributes."""

    _attr_icon = "mdi:cake-variant"
    _attr_event_types = [EVENT_TYPE_BIRTHDAY, EVENT_TYPE_REMINDER]

    def __init__(self, manager, entry_id: str) -> None:
        super().__init__(manager, entry_id, "events")

    async def async_added_to_hass(self) -> None:
        """Register with the manager."""
        await super().async_added_to_hass()
        self._manager.event_entity = self

    async def async_will_remove_from_hass(self) -> None:
        """Unregister from the manager."""
        if self._manager.event_entity is self:
            self._manager.event_entity = None

    @callback
    def fire(self, event_type: str, data: dict[str, Any]) -> None:
        """Trigger the event."""
        self._trigger_event(event_type, data)
        self.async_write_ha_state()

    @callback
    def _handle_update(self) -> None:
        # Nothing to refresh – the state only changes when an event fires.
        return

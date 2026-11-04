"""Base entity for Geburtstage."""

from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .manager import GeburtstageManager


class GeburtstageEntity(Entity):
    """Common behaviour: one device, refresh when the manager changes."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, manager: GeburtstageManager, entry_id: str, key: str) -> None:
        self._manager = manager
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name="Geburtstage",
            entry_type=DeviceEntryType.SERVICE,
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to manager updates."""
        self.async_on_remove(self._manager.async_add_listener(self._handle_update))

    @callback
    def _handle_update(self) -> None:
        self.async_write_ha_state()

"""Geburtstage – birthday management for Home Assistant."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import async_get_integration

from .const import DOMAIN, PANEL_URL_PATH, PLATFORMS, STATIC_URL
from .manager import GeburtstageManager
from .services import async_register_services
from .websocket import async_register_websocket

_LOGGER = logging.getLogger(__name__)

type GeburtstageConfigEntry = ConfigEntry[GeburtstageManager]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register services and the websocket API (once)."""
    async_register_services(hass)
    async_register_websocket(hass)
    return True


def _frontend_stamp(path: Path) -> str:
    """Return a cache-busting stamp that changes whenever a frontend file changes."""
    return str(int(max(f.stat().st_mtime for f in path.glob("*.js"))))


async def _async_setup_frontend(hass: HomeAssistant) -> None:
    """Serve the bundled frontend files, load the card and add the sidebar panel."""
    integration = await async_get_integration(hass, DOMAIN)
    frontend_dir = Path(__file__).parent / "frontend"
    stamp = await hass.async_add_executor_job(_frontend_stamp, frontend_dir)
    version = f"{integration.version}-{stamp}"
    domain_data = hass.data.setdefault(DOMAIN, {})

    if not domain_data.get("static_registered"):
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    STATIC_URL,
                    str(frontend_dir),
                    cache_headers=False,
                )
            ]
        )
        frontend.add_extra_js_url(hass, f"{STATIC_URL}/geburtstage-card.js?v={version}")
        domain_data["static_registered"] = True

    try:
        await panel_custom.async_register_panel(
            hass,
            webcomponent_name="geburtstage-panel",
            frontend_url_path=PANEL_URL_PATH,
            module_url=f"{STATIC_URL}/geburtstage-panel.js?v={version}",
            sidebar_title="Geburtstage",
            sidebar_icon="mdi:cake-variant",
            require_admin=True,
            config={},
        )
    except ValueError:
        _LOGGER.debug("Panel %s is already registered", PANEL_URL_PATH)


async def async_setup_entry(hass: HomeAssistant, entry: GeburtstageConfigEntry) -> bool:
    """Set up Geburtstage from a config entry."""
    manager = GeburtstageManager(hass)
    await manager.async_load()
    entry.runtime_data = manager

    await _async_setup_frontend(hass)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    manager.async_start()
    entry.async_on_unload(manager.async_stop)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: GeburtstageConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        frontend.async_remove_panel(hass, PANEL_URL_PATH)
    return unload_ok

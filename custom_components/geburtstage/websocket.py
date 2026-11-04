"""Websocket API used by the sidebar panel (admin only)."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError

from .manager import get_manager


@callback
def async_register_websocket(hass: HomeAssistant) -> None:
    """Register the websocket commands."""
    for handler in (
        ws_list,
        ws_upsert,
        ws_delete,
        ws_import,
        ws_settings_set,
        ws_notify_targets,
        ws_preview,
        ws_send_test,
    ):
        websocket_api.async_register_command(hass, handler)


def _manager(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]):
    try:
        return get_manager(hass)
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "not_loaded", str(err))
        return None


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "geburtstage/list"})
@websocket_api.async_response
async def ws_list(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Return persons and settings."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    connection.send_result(
        msg["id"],
        {
            "persons": manager.describe_all(),
            "settings": manager.settings_view(),
            "language": manager.lang,
        },
    )


@websocket_api.require_admin
@websocket_api.websocket_command(
    {vol.Required("type"): "geburtstage/upsert", vol.Required("person"): dict}
)
@websocket_api.async_response
async def ws_upsert(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Create or update a person."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    try:
        desc = manager.async_upsert_person(msg["person"])
    except ValueError as err:
        connection.send_error(msg["id"], "invalid_format", str(err))
        return
    connection.send_result(msg["id"], {"person": desc})


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "geburtstage/delete", vol.Required("person_id"): str})
@websocket_api.async_response
async def ws_delete(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Delete a person."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    try:
        manager.async_remove_person(msg["person_id"])
    except HomeAssistantError as err:
        connection.send_error(msg["id"], "not_found", str(err))
        return
    connection.send_result(msg["id"])


@websocket_api.require_admin
@websocket_api.websocket_command(
    {vol.Required("type"): "geburtstage/import", vol.Required("rows"): [dict]}
)
@websocket_api.async_response
async def ws_import(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Import several persons."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    connection.send_result(msg["id"], manager.async_import_persons(msg["rows"]))


@websocket_api.require_admin
@websocket_api.websocket_command(
    {vol.Required("type"): "geburtstage/settings_set", vol.Required("settings"): dict}
)
@websocket_api.async_response
async def ws_settings_set(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """Save settings."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    try:
        manager.async_set_settings(msg["settings"])
    except ValueError as err:
        connection.send_error(msg["id"], "invalid_format", str(err))
        return
    connection.send_result(msg["id"], {"settings": manager.settings_view()})


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "geburtstage/notify_targets"})
@websocket_api.async_response
async def ws_notify_targets(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]
) -> None:
    """List notify services and entities."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    connection.send_result(msg["id"], {"targets": manager.notify_targets()})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "geburtstage/preview",
        vol.Required("person"): dict,
        vol.Optional("kind", default="greeting"): vol.In(["greeting", "reminder"]),
        vol.Optional("days", default=1): vol.Coerce(int),
    }
)
@websocket_api.async_response
async def ws_preview(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Render an example message for unsaved form data."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    from .manager import normalize_person  # noqa: PLC0415

    try:
        person = normalize_person({**msg["person"], "greeting_enabled": False})
    except ValueError as err:
        connection.send_error(msg["id"], "invalid_format", str(err))
        return
    if msg["kind"] == "greeting":
        text = manager.greeting_text(person)
    else:
        text = manager.reminder_text(person, msg["days"])
    connection.send_result(msg["id"], {"message": text})


@websocket_api.require_admin
@websocket_api.websocket_command(
    {
        vol.Required("type"): "geburtstage/send_test",
        vol.Optional("person_id"): str,
        vol.Optional("person"): dict,
        vol.Optional("kind", default="greeting"): vol.In(["greeting", "reminder"]),
    }
)
@websocket_api.async_response
async def ws_send_test(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    """Send a test message for a stored person or for the (unsaved) form data."""
    if (manager := _manager(hass, connection, msg)) is None:
        return
    from .manager import normalize_person  # noqa: PLC0415

    try:
        if "person" in msg:
            person = normalize_person({**msg["person"], "greeting_enabled": False})
        elif "person_id" in msg:
            person = manager.find_person(msg["person_id"])
        else:
            raise ValueError("person or person_id is required")
    except (ValueError, HomeAssistantError) as err:
        connection.send_error(msg["id"], "invalid_format", str(err))
        return
    if msg["kind"] == "greeting":
        target = person.get("greeting_notify", "")
        text = manager.greeting_text(person)
        title = manager.greeting_title
    else:
        target = manager.settings.get("reminder_notify", "")
        text = manager.reminder_text(person, 1)
        title = manager.reminder_title
    if not target:
        connection.send_error(msg["id"], "no_target", "No notify target configured")
        return
    ok = await manager.async_send(target, f"[Test] {text}", title)
    if not ok:
        connection.send_error(msg["id"], "send_failed", f"Sending via {target} failed")
        return
    connection.send_result(msg["id"], {"message": text, "notify": target})

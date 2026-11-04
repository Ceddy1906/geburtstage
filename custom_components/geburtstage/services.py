"""Services for Geburtstage."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse, callback
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, MAX_REMINDER_DAYS, SALUTATIONS, STYLES
from .manager import get_manager

_PERSON_FIELDS = {
    vol.Optional("first_name"): cv.string,
    vol.Optional("last_name"): cv.string,
    vol.Optional("salutation"): vol.In(SALUTATIONS),
    vol.Optional("style"): vol.In(STYLES),
    vol.Optional("birthdate"): cv.date,
    vol.Optional("year_known"): cv.boolean,
    vol.Optional("greeting_enabled"): cv.boolean,
    vol.Optional("greeting_notify"): cv.string,
    vol.Optional("reminder_days_1"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(0, MAX_REMINDER_DAYS))),
    vol.Optional("reminder_days_2"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(0, MAX_REMINDER_DAYS))),
}

ADD_SCHEMA = vol.Schema(
    {
        vol.Required("first_name"): cv.string,
        vol.Required("birthdate"): cv.date,
        **{k: v for k, v in _PERSON_FIELDS.items() if k not in ("first_name", "birthdate")},
    }
)
UPDATE_SCHEMA = vol.Schema({vol.Required("person"): cv.string, **_PERSON_FIELDS})
REMOVE_SCHEMA = vol.Schema({vol.Required("person"): cv.string})
SEND_SCHEMA = vol.Schema(
    {
        vol.Required("person"): cv.string,
        vol.Optional("message"): cv.string,
        vol.Optional("notify"): cv.string,
        vol.Optional("title"): cv.string,
    }
)
UPCOMING_SCHEMA = vol.Schema({vol.Optional("days", default=30): vol.All(vol.Coerce(int), vol.Range(0, 366))})


def _as_error(err: ValueError) -> ServiceValidationError:
    return ServiceValidationError(str(err))


@callback
def async_register_services(hass: HomeAssistant) -> None:
    """Register all services."""

    async def add_person(call: ServiceCall) -> dict[str, Any]:
        manager = get_manager(hass)
        try:
            desc = manager.async_upsert_person(dict(call.data))
        except ValueError as err:
            raise _as_error(err) from err
        return {"person": desc}

    async def update_person(call: ServiceCall) -> dict[str, Any]:
        manager = get_manager(hass)
        person = manager.find_person(call.data["person"])
        data = {k: v for k, v in call.data.items() if k != "person"}
        try:
            desc = manager.async_upsert_person({**data, "id": person["id"]})
        except ValueError as err:
            raise _as_error(err) from err
        return {"person": desc}

    async def remove_person(call: ServiceCall) -> None:
        manager = get_manager(hass)
        person = manager.find_person(call.data["person"])
        manager.async_remove_person(person["id"])

    async def send_greeting(call: ServiceCall) -> dict[str, Any]:
        manager = get_manager(hass)
        person = manager.find_person(call.data["person"])
        message = call.data.get("message") or manager.greeting_text(person)
        target = call.data.get("notify") or person.get("greeting_notify")
        if not target:
            raise ServiceValidationError("No notify target given and none stored for the person")
        title = call.data.get("title") or manager.greeting_title
        if not await manager.async_send(target, message, title):
            raise HomeAssistantError(f"Sending via {target} failed")
        return {"message": message, "notify": target}

    async def get_upcoming(call: ServiceCall) -> dict[str, Any]:
        manager = get_manager(hass)
        limit = call.data["days"]
        return {"birthdays": [p for p in manager.public_list() if p["days_until"] <= limit]}

    hass.services.async_register(
        DOMAIN, "add_person", add_person, ADD_SCHEMA, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, "update_person", update_person, UPDATE_SCHEMA, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(DOMAIN, "remove_person", remove_person, REMOVE_SCHEMA)
    hass.services.async_register(
        DOMAIN, "send_greeting", send_greeting, SEND_SCHEMA, supports_response=SupportsResponse.OPTIONAL
    )
    hass.services.async_register(
        DOMAIN, "get_upcoming", get_upcoming, UPCOMING_SCHEMA, supports_response=SupportsResponse.ONLY
    )

"""Constants for the Geburtstage integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "geburtstage"
PLATFORMS: list[Platform] = [Platform.CALENDAR, Platform.SENSOR, Platform.EVENT]

STORAGE_KEY = "geburtstage.data"
STORAGE_VERSION = 1

PANEL_URL_PATH = "geburtstage"
STATIC_URL = "/geburtstage_static"

SALUTATIONS = ("herr", "frau", "")
STYLES = ("personal", "formal")

EVENT_BIRTHDAY = f"{DOMAIN}_birthday"
EVENT_REMINDER = f"{DOMAIN}_reminder"
EVENT_TYPE_BIRTHDAY = "birthday"
EVENT_TYPE_REMINDER = "reminder"

UPCOMING_WINDOW_DAYS = 30
MAX_REMINDER_DAYS = 60

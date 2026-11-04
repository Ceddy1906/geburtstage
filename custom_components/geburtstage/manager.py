"""Data manager for Geburtstage: storage, validation, scheduling and notifications."""

from __future__ import annotations

import logging
import random
import uuid
from collections.abc import Callable
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.event import async_track_point_in_time, async_track_time_change
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    EVENT_BIRTHDAY,
    EVENT_REMINDER,
    EVENT_TYPE_BIRTHDAY,
    EVENT_TYPE_REMINDER,
    MAX_REMINDER_DAYS,
    SALUTATIONS,
    STORAGE_KEY,
    STORAGE_VERSION,
    STYLES,
)
from .logic import (
    DEFAULT_REMINDER_TEMPLATE,
    DEFAULT_TEXTS,
    DEFAULT_TITLES,
    build_greeting_message,
    build_reminder_message,
    describe,
    greeting_for,
    norm_lang,
    random_offset,
    sort_key,
)

if TYPE_CHECKING:
    from .event import GeburtstageEventEntity

_LOGGER = logging.getLogger(__name__)

DEFAULT_SETTINGS: dict[str, Any] = {
    "send_time": "08:00:00",
    "send_time_end": "",
    "reminder_notify": "",
    "auto_reminders": True,
    "greeting_title": "",
    "reminder_title": "",
    "texts_personal": None,
    "texts_formal": None,
    "reminder_template": None,
}

# Fields of a person that are exposed to every user (card / sensors).
PUBLIC_FIELDS = (
    "id",
    "name",
    "first_name",
    "last_name",
    "salutation",
    "month",
    "day",
    "year_known",
    "next_date",
    "days_until",
    "turning_age",
    "current_age",
    "is_today",
    "is_round",
)


def get_manager(hass: HomeAssistant) -> GeburtstageManager:
    """Return the manager of the loaded config entry."""
    entries = hass.config_entries.async_loaded_entries(DOMAIN)
    if not entries:
        raise HomeAssistantError("Geburtstage is not set up")
    return entries[0].runtime_data


def _parse_time(value: str) -> time:
    parts = [int(p) for p in str(value).split(":")]
    while len(parts) < 3:
        parts.append(0)
    return time(parts[0], parts[1], parts[2])


def _clean_str(value: Any, field: str, max_len: int = 120) -> str:
    text = "" if value is None else str(value).strip()
    if len(text) > max_len:
        raise ValueError(f"{field} is too long")
    return text


def _clean_days(value: Any, field: str) -> int | None:
    if value in (None, "", 0, "0"):
        return None
    try:
        days = int(value)
    except (TypeError, ValueError) as err:
        raise ValueError(f"{field} must be a number") from err
    if not 1 <= days <= MAX_REMINDER_DAYS:
        raise ValueError(f"{field} must be between 1 and {MAX_REMINDER_DAYS}")
    return days


def normalize_person(data: dict[str, Any], base: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate and normalise person data. ``base`` provides defaults when updating."""
    merged = {**(base or {}), **data}
    first = _clean_str(merged.get("first_name"), "first_name")
    if not first:
        raise ValueError("first_name is required")
    last = _clean_str(merged.get("last_name"), "last_name")
    salutation = _clean_str(merged.get("salutation"), "salutation").lower()
    if salutation not in SALUTATIONS:
        raise ValueError("salutation must be 'herr', 'frau' or empty")
    style = _clean_str(merged.get("style") or "personal", "style").lower()
    if style not in STYLES:
        raise ValueError("style must be 'personal' or 'formal'")
    raw_date = merged.get("birthdate")
    if isinstance(raw_date, date):
        born = raw_date
    else:
        try:
            born = date.fromisoformat(str(raw_date))
        except ValueError as err:
            raise ValueError("birthdate must be a valid date (YYYY-MM-DD)") from err
    year_known = bool(merged.get("year_known", True))
    if year_known and born > dt_util.now().date():
        raise ValueError("birthdate must not be in the future")
    greeting_enabled = bool(merged.get("greeting_enabled", False))
    notify = _clean_str(merged.get("greeting_notify"), "greeting_notify", 200)
    if greeting_enabled and not notify:
        raise ValueError("greeting_notify is required when greeting_enabled is set")
    return {
        "id": merged.get("id") or uuid.uuid4().hex,
        "first_name": first,
        "last_name": last,
        "salutation": salutation,
        "style": style,
        "birthdate": born.isoformat(),
        "year_known": year_known,
        "greeting_enabled": greeting_enabled,
        "greeting_notify": notify,
        "reminder_days_1": _clean_days(merged.get("reminder_days_1"), "reminder_days_1"),
        "reminder_days_2": _clean_days(merged.get("reminder_days_2"), "reminder_days_2"),
    }


def normalize_settings(data: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """Validate settings."""
    merged = {**base, **data}
    try:
        send_time = _parse_time(merged.get("send_time") or "08:00:00")
    except (TypeError, ValueError) as err:
        raise ValueError("send_time must be HH:MM[:SS]") from err
    end_raw = merged.get("send_time_end") or ""
    send_time_end = ""
    if end_raw:
        try:
            end_time = _parse_time(end_raw)
        except (TypeError, ValueError) as err:
            raise ValueError("send_time_end must be HH:MM[:SS]") from err
        if end_time <= send_time:
            raise ValueError("send_time_end must be later than send_time")
        send_time_end = end_time.strftime("%H:%M:%S")

    def _texts(key: str) -> list[str] | None:
        value = merged.get(key)
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError(f"{key} must be a list")
        items = [str(v).strip() for v in value if str(v).strip()]
        if len(items) > 50 or any(len(v) > 600 for v in items):
            raise ValueError(f"{key} is too long")
        return items or None

    template = merged.get("reminder_template")
    template = str(template).strip() if template else None
    return {
        "send_time": send_time.strftime("%H:%M:%S"),
        "send_time_end": send_time_end,
        "reminder_notify": _clean_str(merged.get("reminder_notify"), "reminder_notify", 200),
        "auto_reminders": bool(merged.get("auto_reminders", True)),
        "greeting_title": _clean_str(merged.get("greeting_title"), "greeting_title", 100),
        "reminder_title": _clean_str(merged.get("reminder_title"), "reminder_title", 100),
        "texts_personal": _texts("texts_personal"),
        "texts_formal": _texts("texts_formal"),
        "reminder_template": template,
    }


class GeburtstageManager:
    """Owns all persons/settings and drives reminders and congratulations."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._store: Store[dict[str, Any]] = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.persons: dict[str, dict[str, Any]] = {}
        self.settings: dict[str, Any] = dict(DEFAULT_SETTINGS)
        self.sent: dict[str, str] = {}
        self.event_entity: GeburtstageEventEntity | None = None
        self._listeners: list[CALLBACK_TYPE] = []
        self._unsubs: list[CALLBACK_TYPE] = []
        self._daily_unsub: CALLBACK_TYPE | None = None
        self._pending: dict[str, CALLBACK_TYPE] = {}
        self._rng = random.Random()

    # ------------------------------------------------------------------ #
    # Persistence
    # ------------------------------------------------------------------ #

    async def async_load(self) -> None:
        """Load data from storage."""
        data = await self._store.async_load() or {}
        self.persons = {p["id"]: p for p in data.get("persons", []) if "id" in p}
        try:
            self.settings = normalize_settings(data.get("settings", {}), DEFAULT_SETTINGS)
        except ValueError:
            _LOGGER.warning("Invalid stored settings, using defaults")
            self.settings = dict(DEFAULT_SETTINGS)
        self.sent = dict(data.get("sent", {}))

    @callback
    def _save(self) -> None:
        self._store.async_delay_save(self._data_to_save, 1)

    @callback
    def _data_to_save(self) -> dict[str, Any]:
        return {
            "persons": list(self.persons.values()),
            "settings": self.settings,
            "sent": self.sent,
        }

    # ------------------------------------------------------------------ #
    # Listeners (entities)
    # ------------------------------------------------------------------ #

    @callback
    def async_add_listener(self, update: CALLBACK_TYPE) -> CALLBACK_TYPE:
        """Register an entity update callback."""
        self._listeners.append(update)

        @callback
        def _remove() -> None:
            if update in self._listeners:
                self._listeners.remove(update)

        return _remove

    @callback
    def _notify_listeners(self) -> None:
        for update in list(self._listeners):
            update()

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @property
    def lang(self) -> str:
        """Language used for generated texts."""
        return norm_lang(self.hass.config.language)

    @property
    def today(self) -> date:
        """Today in the local time zone."""
        return dt_util.now().date()

    def find_person(self, ident: str) -> dict[str, Any]:
        """Find a person by id or (case-insensitive) full name."""
        if ident in self.persons:
            return self.persons[ident]
        needle = str(ident).strip().lower()
        for person in self.persons.values():
            full = " ".join(p for p in (person["first_name"], person["last_name"]) if p).lower()
            if full == needle:
                return person
        raise HomeAssistantError(f"Person '{ident}' not found")

    def describe_all(self, today: date | None = None) -> list[dict[str, Any]]:
        """Return all persons with computed fields, sorted by next birthday."""
        today = today or self.today
        items = [describe(p, today) for p in self.persons.values()]
        items.sort(key=sort_key)
        return items

    def public_list(self, today: date | None = None) -> list[dict[str, Any]]:
        """Return the list exposed on entities (no notify targets)."""
        return [{k: item[k] for k in PUBLIC_FIELDS} for item in self.describe_all(today)]

    def settings_view(self) -> dict[str, Any]:
        """Return settings including the effective (default) texts."""
        lang = self.lang
        view = dict(self.settings)
        for key, style in (("texts_personal", "personal"), ("texts_formal", "formal")):
            view[f"{key}_is_default"] = self.settings.get(key) is None
            view[key] = self.settings.get(key) or list(DEFAULT_TEXTS[lang][style])
        view["reminder_template_is_default"] = not self.settings.get("reminder_template")
        view["reminder_template"] = self.settings.get("reminder_template") or (
            DEFAULT_REMINDER_TEMPLATE[lang]
        )
        view["greeting_title"] = self.settings["greeting_title"] or DEFAULT_TITLES[lang]["greeting"]
        view["reminder_title"] = self.settings["reminder_title"] or DEFAULT_TITLES[lang]["reminder"]
        return view

    def notify_targets(self) -> list[dict[str, str]]:
        """Return available notify services and notify entities."""
        targets: list[dict[str, str]] = []
        services = self.hass.services.async_services_for_domain("notify")
        for name in sorted(services):
            if name == "send_message":
                continue
            targets.append(
                {
                    "value": f"notify.{name}",
                    "label": name.replace("_", " ").title(),
                    "kind": "service",
                }
            )
        for state in sorted(self.hass.states.async_all("notify"), key=lambda s: s.entity_id):
            targets.append(
                {"value": state.entity_id, "label": state.name, "kind": "entity"}
            )
        return targets

    # ------------------------------------------------------------------ #
    # CRUD
    # ------------------------------------------------------------------ #

    @callback
    def async_upsert_person(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create or update a person. Raises ValueError on invalid input."""
        base = self.persons.get(data.get("id") or "")
        person = normalize_person(data, base)
        self.persons[person["id"]] = person
        self._save()
        self._notify_listeners()
        return describe(person, self.today)

    @callback
    def async_remove_person(self, person_id: str) -> None:
        """Delete a person."""
        if person_id not in self.persons:
            raise HomeAssistantError(f"Person '{person_id}' not found")
        del self.persons[person_id]
        self.sent = {k: v for k, v in self.sent.items() if f":{person_id}" not in k}
        self._save()
        self._notify_listeners()

    @callback
    def async_import_persons(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        """Import several persons, skipping duplicates and reporting errors."""
        existing = {
            (p["first_name"].lower(), p["last_name"].lower(), p["birthdate"][5:])
            for p in self.persons.values()
        }
        added = skipped = 0
        errors: list[dict[str, Any]] = []
        for index, row in enumerate(rows):
            try:
                row = {k: v for k, v in row.items() if k != "id"}
                person = normalize_person(row)
            except ValueError as err:
                errors.append({"row": index + 1, "error": str(err)})
                continue
            key = (person["first_name"].lower(), person["last_name"].lower(), person["birthdate"][5:])
            if key in existing:
                skipped += 1
                continue
            existing.add(key)
            self.persons[person["id"]] = person
            added += 1
        if added:
            self._save()
            self._notify_listeners()
        return {"added": added, "skipped": skipped, "errors": errors}

    @callback
    def async_set_settings(self, data: dict[str, Any]) -> None:
        """Update settings. Raises ValueError on invalid input."""
        settings = normalize_settings(data, self.settings)
        # Values equal to the defaults are stored as "default", so they follow the language.
        lang = self.lang
        for style in ("personal", "formal"):
            if settings[f"texts_{style}"] == DEFAULT_TEXTS[lang][style]:
                settings[f"texts_{style}"] = None
        if settings["reminder_template"] == DEFAULT_REMINDER_TEMPLATE[lang]:
            settings["reminder_template"] = None
        for kind in ("greeting", "reminder"):
            if settings[f"{kind}_title"] == DEFAULT_TITLES[lang][kind]:
                settings[f"{kind}_title"] = ""
        timing_changed = (settings["send_time"], settings["send_time_end"]) != (
            self.settings["send_time"],
            self.settings["send_time_end"],
        )
        self.settings = settings
        self._save()
        if timing_changed:
            self._cancel_pending()
            self._schedule_daily()
            if dt_util.now().time() >= _parse_time(settings["send_time"]):
                self.hass.async_create_task(self.async_run_daily())
        self._notify_listeners()

    # ------------------------------------------------------------------ #
    # Messages
    # ------------------------------------------------------------------ #

    def greeting_text(self, person: dict[str, Any], today: date | None = None) -> str:
        """Return a random congratulation text for a person."""
        lang = self.lang
        desc = describe(person, today or self.today)
        style = person.get("style", "personal")
        texts = self.settings.get(f"texts_{style}") or DEFAULT_TEXTS[lang][style]
        return build_greeting_message(person, desc, texts, lang, self._rng)

    def reminder_text(self, person: dict[str, Any], days: int, today: date | None = None) -> str:
        """Return the reminder text for a person."""
        lang = self.lang
        desc = describe(person, today or self.today)
        template = self.settings.get("reminder_template") or DEFAULT_REMINDER_TEMPLATE[lang]
        return build_reminder_message(person, desc, template, lang, days)

    @property
    def greeting_title(self) -> str:
        """Title used for congratulations."""
        return self.settings["greeting_title"] or DEFAULT_TITLES[self.lang]["greeting"]

    @property
    def reminder_title(self) -> str:
        """Title used for reminders."""
        return self.settings["reminder_title"] or DEFAULT_TITLES[self.lang]["reminder"]

    # ------------------------------------------------------------------ #
    # Sending
    # ------------------------------------------------------------------ #

    async def async_send(self, target: str, message: str, title: str | None = None) -> bool:
        """Send via a notify service or notify entity. Never raises."""
        if not target:
            return False
        domain, _, name = target.partition(".")
        if domain != "notify" or not name:
            _LOGGER.warning("Invalid notify target: %s", target)
            return False
        try:
            if name != "send_message" and self.hass.services.has_service("notify", name):
                data: dict[str, Any] = {"message": message}
                if title:
                    data["title"] = title
                await self.hass.services.async_call("notify", name, data, blocking=True)
            elif self.hass.states.get(target) is not None:
                data = {"entity_id": target, "message": message}
                if title:
                    data["title"] = title
                await self.hass.services.async_call("notify", "send_message", data, blocking=True)
            else:
                _LOGGER.warning("Notify target %s does not exist", target)
                return False
        except Exception:  # noqa: BLE001 - a failing notifier must not break the job
            _LOGGER.exception("Sending notification via %s failed", target)
            return False
        return True

    @callback
    def _fire(self, event_type: str, payload: dict[str, Any]) -> None:
        bus_event = EVENT_BIRTHDAY if event_type == EVENT_TYPE_BIRTHDAY else EVENT_REMINDER
        self.hass.bus.async_fire(bus_event, payload)
        if self.event_entity is not None:
            self.event_entity.fire(event_type, payload)

    # ------------------------------------------------------------------ #
    # Daily job
    # ------------------------------------------------------------------ #

    @callback
    def async_start(self) -> None:
        """Start schedules."""
        self._schedule_daily()
        self._unsubs.append(
            async_track_time_change(self.hass, self._async_midnight, hour=0, minute=0, second=10)
        )
        if unsub := async_at_started(self.hass, self._async_started):
            self._unsubs.append(unsub)

    @callback
    def async_stop(self) -> None:
        """Stop schedules."""
        if self._daily_unsub:
            self._daily_unsub()
            self._daily_unsub = None
        self._cancel_pending()
        for unsub in self._unsubs:
            unsub()
        self._unsubs.clear()

    @callback
    def _cancel_pending(self) -> None:
        """Cancel timers of messages that are planned for later today."""
        for unsub in self._pending.values():
            unsub()
        self._pending.clear()

    @callback
    def _schedule_daily(self) -> None:
        if self._daily_unsub:
            self._daily_unsub()
        send = _parse_time(self.settings["send_time"])
        self._daily_unsub = async_track_time_change(
            self.hass,
            self._async_scheduled,
            hour=send.hour,
            minute=send.minute,
            second=send.second,
        )

    async def _async_midnight(self, _now: datetime) -> None:
        self._notify_listeners()

    async def _async_started(self, _hass: HomeAssistant) -> None:
        """Catch up after a restart if today's send time has already passed."""
        if dt_util.now().time() >= _parse_time(self.settings["send_time"]):
            await self.async_run_daily()

    async def _async_scheduled(self, _now: datetime) -> None:
        await self.async_run_daily()

    def _send_moment(self, key: str, today: date) -> datetime:
        """Return when a message is sent today: the start time or a random time in the window."""
        tz = dt_util.get_default_time_zone()
        start = datetime.combine(today, _parse_time(self.settings["send_time"]), tzinfo=tz)
        end_raw = self.settings.get("send_time_end")
        window = 0
        if end_raw:
            end = datetime.combine(today, _parse_time(end_raw), tzinfo=tz)
            window = int((end - start).total_seconds())
        return start + timedelta(seconds=random_offset(key, today, window))

    async def async_run_daily(self) -> None:
        """Send what is due now and plan what is due later today (idempotent)."""
        today = self.today
        now = dt_util.now()
        for person in list(self.persons.values()):
            desc = describe(person, today)
            if desc["days_until"] == 0:
                await self._async_dispatch("greet", person["id"], 0, today.isoformat(), today, now)
            for days in desc["reminder_days"]:
                if desc["days_until"] == days:
                    await self._async_dispatch("rem", person["id"], days, desc["next_date"], today, now)
        cutoff = today - timedelta(days=2)
        self.sent = {
            key: value for key, value in self.sent.items() if date.fromisoformat(value) >= cutoff
        }
        self._save()
        self._notify_listeners()

    async def _async_dispatch(
        self, kind: str, pid: str, days: int, marker: str, today: date, now: datetime
    ) -> None:
        """Send an item now if its moment has come, otherwise plan a timer for it."""
        key = f"greet:{pid}" if kind == "greet" else f"rem:{days}:{pid}"
        if self.sent.get(key) == marker:
            return
        when = self._send_moment(key, today)
        if when <= now:
            if unsub := self._pending.pop(key, None):
                unsub()
            await self._async_fire_item(kind, pid, days)
            return
        if key in self._pending:
            return

        async def _fire(_now: datetime) -> None:
            self._pending.pop(key, None)
            await self._async_fire_item(kind, pid, days)

        self._pending[key] = async_track_point_in_time(self.hass, _fire, when)

    async def _async_fire_item(self, kind: str, pid: str, days: int) -> None:
        """Send one item after re-checking that it is still due (person may have changed)."""
        person = self.persons.get(pid)
        if person is None:
            return
        today = self.today
        desc = describe(person, today)
        if kind == "greet":
            if desc["days_until"] != 0:
                return
            await self._async_handle_birthday(person, desc, today)
        else:
            if desc["days_until"] != days or days not in desc["reminder_days"]:
                return
            await self._async_handle_reminder(person, desc, days, today)
        self._save()
        self._notify_listeners()

    async def _async_handle_birthday(
        self, person: dict[str, Any], desc: dict[str, Any], today: date
    ) -> None:
        key = f"greet:{person['id']}"
        if self.sent.get(key) == today.isoformat():
            return
        self.sent[key] = today.isoformat()
        message = self.greeting_text(person, today)
        auto = bool(person.get("greeting_enabled") and person.get("greeting_notify"))
        sent = False
        if auto:
            sent = await self.async_send(person["greeting_notify"], message, self.greeting_title)
        self._fire(
            EVENT_TYPE_BIRTHDAY,
            {
                **self._event_person(person, desc),
                "days_until": 0,
                "message": message,
                "notify": person.get("greeting_notify", ""),
                "auto_send": auto,
                "sent": sent,
            },
        )

    async def _async_handle_reminder(
        self, person: dict[str, Any], desc: dict[str, Any], days: int, today: date
    ) -> None:
        key = f"rem:{days}:{person['id']}"
        if self.sent.get(key) == desc["next_date"]:
            return
        self.sent[key] = desc["next_date"]
        message = self.reminder_text(person, days, today)
        target = self.settings.get("reminder_notify", "")
        auto = bool(self.settings.get("auto_reminders") and target)
        sent = False
        if auto:
            sent = await self.async_send(target, message, self.reminder_title)
        self._fire(
            EVENT_TYPE_REMINDER,
            {
                **self._event_person(person, desc),
                "days_until": days,
                "message": message,
                "notify": target,
                "auto_send": auto,
                "sent": sent,
            },
        )

    def _event_person(self, person: dict[str, Any], desc: dict[str, Any]) -> dict[str, Any]:
        return {
            "person_id": desc["id"],
            "name": desc["name"],
            "first_name": desc["first_name"],
            "last_name": desc["last_name"],
            "salutation": desc["salutation"],
            "style": desc["style"],
            "greeting": greeting_for(person, self.lang),
            "age": desc["turning_age"],
            "birthdate": desc["birthdate"],
            "date": desc["next_date"],
        }

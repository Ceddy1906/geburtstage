"""Pure helper logic for Geburtstage (no Home Assistant imports, easy to test)."""

from __future__ import annotations

import calendar
import random
import re
from datetime import date
from typing import Any

# --------------------------------------------------------------------------- #
# Default texts
# --------------------------------------------------------------------------- #

DEFAULT_TEXTS: dict[str, dict[str, list[str]]] = {
    "de": {
        "personal": [
            "{gruss}, alles Gute zum {alter}. Geburtstag! 🎂 Bleib gesund und lass dich heute richtig feiern!",
            "{gruss}, herzlichen Glückwunsch zum Geburtstag! 🎉 Ich wünsche dir ein wunderbares neues Lebensjahr.",
            "{gruss}, zum {alter}. Geburtstag wünsche ich dir von Herzen alles Liebe, Glück und Gesundheit! 🎈",
            "Happy Birthday, {name}! 🥳 Genieße deinen Ehrentag und lass es dir richtig gut gehen!",
            "{gruss}, ein neues Lebensjahr beginnt – ich wünsche dir, dass all deine Wünsche in Erfüllung gehen. 🎁 Alles Gute!",
            "{gruss}, heute ist dein Ehrentag! 🎂 Alles Liebe zum Geburtstag und einen tollen Tag.",
            "{gruss}, {alter} Jahre jung – alles Gute zum Geburtstag! 🥂",
            "{gruss}, ich denke heute besonders an dich und wünsche dir einen wunderschönen Geburtstag! 💐",
            "{gruss}, auf dich und auf das neue Lebensjahr: Prost und alles Gute zum Geburtstag! 🥂",
            "{gruss}, Glück, Gesundheit und viele schöne Momente – das wünsche ich dir zum Geburtstag! 🍀",
        ],
        "formal": [
            "{gruss}, zu Ihrem Geburtstag gratuliere ich Ihnen sehr herzlich und wünsche Ihnen alles Gute, Gesundheit und Erfolg.",
            "{gruss}, zum {alter}. Geburtstag übermittle ich Ihnen meine herzlichsten Glückwünsche.",
            "{gruss}, ich wünsche Ihnen zu Ihrem Geburtstag einen schönen Tag im Kreise Ihrer Liebsten und für das neue Lebensjahr alles Gute.",
            "{gruss}, herzliche Glückwünsche zum Geburtstag! Bleiben Sie gesund und zuversichtlich.",
            "{gruss}, zu Ihrem Ehrentag sende ich Ihnen die besten Wünsche für Glück, Gesundheit und Zufriedenheit.",
            "{gruss}, alles Gute zum Geburtstag! Mögen sich im neuen Lebensjahr all Ihre Wünsche erfüllen.",
            "{gruss}, anlässlich Ihres Geburtstags wünsche ich Ihnen von Herzen alles Gute und viel Freude.",
            "{gruss}, ich gratuliere Ihnen herzlich zum {alter}. Geburtstag und wünsche Ihnen ein erfolgreiches neues Lebensjahr.",
            "{gruss}, zu Ihrem Geburtstag die besten Wünsche – genießen Sie diesen besonderen Tag.",
            "{gruss}, ich wünsche Ihnen einen wunderschönen Geburtstag sowie Gesundheit und Wohlergehen im kommenden Lebensjahr.",
        ],
    },
    "en": {
        "personal": [
            "{greeting}, happy {age_ordinal} birthday! 🎂 Stay healthy and enjoy your day!",
            "{greeting}, congratulations on your birthday! 🎉 I wish you a wonderful new year of life.",
            "{greeting}, all the best for your birthday – love, luck and good health! 🎈",
            "Happy Birthday, {first_name}! 🥳 Enjoy your special day!",
            "{greeting}, a new year begins – may all your wishes come true. 🎁 Happy birthday!",
            "{greeting}, today is your day! 🎂 Wishing you a fantastic birthday.",
            "{greeting}, {age} years young – happy birthday! 🥂",
            "{greeting}, I'm thinking of you today and wish you a wonderful birthday! 💐",
            "{greeting}, cheers to you and the year ahead – happy birthday! 🥂",
            "{greeting}, luck, health and lots of beautiful moments – that's what I wish you for your birthday! 🍀",
        ],
        "formal": [
            "{greeting}, please accept my warmest congratulations on your birthday and my best wishes for health and success.",
            "{greeting}, on the occasion of your {age_ordinal} birthday I send you my very best wishes.",
            "{greeting}, I wish you a lovely day among your loved ones and all the best for the coming year.",
            "{greeting}, warmest birthday wishes! May you stay healthy and confident.",
            "{greeting}, on your special day I send you my best wishes for happiness, health and contentment.",
            "{greeting}, happy birthday! May all your wishes come true in the coming year.",
            "{greeting}, on your birthday I sincerely wish you all the best and much joy.",
            "{greeting}, congratulations on your {age_ordinal} birthday – I wish you a successful year ahead.",
            "{greeting}, best wishes on your birthday – please enjoy this special day.",
            "{greeting}, I wish you a wonderful birthday as well as health and well-being in the year to come.",
        ],
    },
}

DEFAULT_REMINDER_TEMPLATE = {
    "de": "🎂 Erinnerung: {vollername} hat {wann} Geburtstag {wird}.",
    "en": "🎂 Reminder: {full_name} has a birthday {when} {turning}.",
}

DEFAULT_TITLES = {
    "de": {"greeting": "Geburtstag 🎂", "reminder": "Geburtstags-Erinnerung"},
    "en": {"greeting": "Birthday 🎂", "reminder": "Birthday reminder"},
}

GREETINGS: dict[str, dict[tuple[str, str], str]] = {
    "de": {
        ("personal", "herr"): "Lieber {first}",
        ("personal", "frau"): "Liebe {first}",
        ("personal", ""): "Hallo {first}",
        ("formal", "herr"): "Sehr geehrter Herr {surname}",
        ("formal", "frau"): "Sehr geehrte Frau {surname}",
        ("formal", ""): "Guten Tag {full}",
    },
    "en": {
        ("personal", "herr"): "Dear {first}",
        ("personal", "frau"): "Dear {first}",
        ("personal", ""): "Hi {first}",
        ("formal", "herr"): "Dear Mr. {surname}",
        ("formal", "frau"): "Dear Ms. {surname}",
        ("formal", ""): "Dear {full}",
    },
}

_AGE_PLACEHOLDERS = ("{alter}", "{age}", "{age_ordinal}")
_PLACEHOLDER = re.compile(r"\{(\w+)\}")


def random_offset(key: str, day: date, window_seconds: int) -> int:
    """Return a reproducible random second offset (0..window) for a message on a day.

    The value only depends on ``key`` and ``day`` so that a restart of Home Assistant
    does not move the planned send time.
    """
    if window_seconds <= 0:
        return 0
    return random.Random(f"{key}|{day.isoformat()}").randint(0, window_seconds)


def norm_lang(language: str | None) -> str:
    """Return 'de' for German locales, otherwise 'en'."""
    return "de" if (language or "").lower().startswith("de") else "en"


# --------------------------------------------------------------------------- #
# Dates and ages
# --------------------------------------------------------------------------- #


def occurrence(month: int, day: int, year: int) -> date:
    """Return the birthday date in a given year (29 Feb -> 1 Mar in non-leap years)."""
    if month == 2 and day == 29 and not calendar.isleap(year):
        return date(year, 3, 1)
    return date(year, month, day)


def next_occurrence(month: int, day: int, today: date) -> date:
    """Return the next date (today included) on which the birthday is celebrated."""
    occ = occurrence(month, day, today.year)
    if occ < today:
        occ = occurrence(month, day, today.year + 1)
    return occ


def full_name(person: dict[str, Any]) -> str:
    """Return 'First Last'."""
    return " ".join(p for p in (person.get("first_name"), person.get("last_name")) if p)


def is_round_age(age: int | None) -> bool:
    """Round birthdays are multiples of ten."""
    return bool(age) and age % 10 == 0


def describe(person: dict[str, Any], today: date) -> dict[str, Any]:
    """Return the person plus computed fields relative to ``today``."""
    born = date.fromisoformat(person["birthdate"])
    year_known = bool(person.get("year_known", True))
    nxt = next_occurrence(born.month, born.day, today)
    days_until = (nxt - today).days
    turning = nxt.year - born.year if year_known else None
    current = None
    if turning is not None:
        current = turning if days_until == 0 else turning - 1
    reminders = sorted(
        {d for d in (person.get("reminder_days_1"), person.get("reminder_days_2")) if d}
    )
    return {
        "id": person["id"],
        "name": full_name(person),
        "first_name": person.get("first_name", ""),
        "last_name": person.get("last_name", ""),
        "salutation": person.get("salutation", ""),
        "style": person.get("style", "personal"),
        "birthdate": person["birthdate"],
        "year_known": year_known,
        "month": born.month,
        "day": born.day,
        "next_date": nxt.isoformat(),
        "days_until": days_until,
        "turning_age": turning,
        "current_age": current,
        "is_today": days_until == 0,
        "is_round": is_round_age(turning),
        "greeting_enabled": bool(person.get("greeting_enabled")),
        "greeting_notify": person.get("greeting_notify", ""),
        "reminder_days_1": person.get("reminder_days_1"),
        "reminder_days_2": person.get("reminder_days_2"),
        "reminder_days": reminders,
    }


def sort_key(desc: dict[str, Any]) -> tuple[int, str]:
    """Sort by days until the next birthday, then by name."""
    return (desc["days_until"], desc["name"].lower())


# --------------------------------------------------------------------------- #
# Message building
# --------------------------------------------------------------------------- #


def render(template: str, context: dict[str, Any]) -> str:
    """Replace {placeholders}; unknown ones are left untouched. Tidy up spacing."""
    text = _PLACEHOLDER.sub(
        lambda m: str(context[m.group(1)]) if m.group(1) in context else m.group(0),
        template,
    )
    text = re.sub(r"[ \t]+([.,!?;:])", r"\1", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def greeting_for(person: dict[str, Any], lang: str) -> str:
    """Build the salutation line, e.g. 'Lieber Max' or 'Sehr geehrte Frau Müller'."""
    first = person.get("first_name", "")
    last = person.get("last_name", "")
    table = GREETINGS[lang]
    style = person.get("style", "personal")
    sal = person.get("salutation", "")
    pattern = table.get((style, sal)) or table[("personal", "")]
    return pattern.format(
        first=first, surname=last or first, full=full_name(person) or first
    )


def when_text(days: int, lang: str) -> str:
    """Return 'heute' / 'morgen' / 'in 3 Tagen' (or English)."""
    if lang == "de":
        if days == 0:
            return "heute"
        if days == 1:
            return "morgen"
        if days == 2:
            return "übermorgen"
        return f"in {days} Tagen"
    if days == 0:
        return "today"
    if days == 1:
        return "tomorrow"
    return f"in {days} days"


def ordinal_en(n: int) -> str:
    """Return the English ordinal (1st, 2nd, 3rd, 4th, 11th ...)."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def format_short_date(d: date, lang: str) -> str:
    """Return a compact day.month representation."""
    return f"{d.day:02d}.{d.month:02d}." if lang == "de" else f"{d.month:02d}/{d.day:02d}"


def build_context(
    person: dict[str, Any], desc: dict[str, Any], lang: str, days: int = 0
) -> dict[str, Any]:
    """Return all placeholder values for a person (German and English aliases)."""
    age = desc["turning_age"]
    age_text = "" if age is None else str(age)
    if age is None:
        turning = ""
    elif lang == "de":
        turning = f"und wird {age}"
    else:
        turning = f"(turning {age})"
    salutation_word = {
        "de": {"herr": "Herr", "frau": "Frau", "": ""},
        "en": {"herr": "Mr.", "frau": "Ms.", "": ""},
    }[lang][person.get("salutation", "")]
    greeting = greeting_for(person, lang)
    first = person.get("first_name", "")
    last = person.get("last_name", "")
    nxt = date.fromisoformat(desc["next_date"])
    when = when_text(days, lang)
    return {
        "gruss": greeting,
        "greeting": greeting,
        "name": first,
        "vorname": first,
        "first_name": first,
        "nachname": last,
        "last_name": last,
        "vollername": full_name(person),
        "full_name": full_name(person),
        "alter": age_text,
        "age": age_text,
        "age_ordinal": "" if age is None else ordinal_en(age),
        "anrede": salutation_word,
        "salutation": salutation_word,
        "datum": format_short_date(nxt, lang),
        "date": format_short_date(nxt, lang),
        "wann": when,
        "when": when,
        "tage": days,
        "days": days,
        "wird": turning,
        "turning": turning,
    }


def pick_text(
    texts: list[str], has_age: bool, lang: str, style: str, rng: random.Random | None = None
) -> str:
    """Pick a random text; ignore texts that need an age when it is unknown."""
    rng = rng or random
    candidates = [t for t in texts if t and t.strip()]
    if not has_age:
        candidates = [t for t in candidates if not any(p in t for p in _AGE_PLACEHOLDERS)]
    if not candidates:
        pool = DEFAULT_TEXTS[lang][style]
        candidates = (
            pool if has_age else [t for t in pool if not any(p in t for p in _AGE_PLACEHOLDERS)]
        )
    return rng.choice(candidates)


def build_greeting_message(
    person: dict[str, Any],
    desc: dict[str, Any],
    texts: list[str],
    lang: str,
    rng: random.Random | None = None,
) -> str:
    """Render a random congratulation text for a person."""
    template = pick_text(
        texts, desc["turning_age"] is not None, lang, person.get("style", "personal"), rng
    )
    return render(template, build_context(person, desc, lang, 0))


def build_reminder_message(
    person: dict[str, Any], desc: dict[str, Any], template: str, lang: str, days: int
) -> str:
    """Render the reminder text."""
    return render(template, build_context(person, desc, lang, days))

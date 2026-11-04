"""Tests for the pure logic module."""

from __future__ import annotations

import importlib.util
import random
import sys
from datetime import date
from pathlib import Path

# Load logic.py directly so that the tests run without Home Assistant installed.
_spec = importlib.util.spec_from_file_location(
    "geburtstage_logic",
    Path(__file__).parents[1] / "custom_components" / "geburtstage" / "logic.py",
)
logic = importlib.util.module_from_spec(_spec)
sys.modules["geburtstage_logic"] = logic
_spec.loader.exec_module(logic)


def person(**kw):
    base = {
        "id": "1",
        "first_name": "Max",
        "last_name": "Müller",
        "salutation": "herr",
        "style": "personal",
        "birthdate": "1985-11-04",
        "year_known": True,
    }
    base.update(kw)
    return base


def test_next_occurrence_today_and_past():
    assert logic.next_occurrence(11, 4, date(2026, 11, 4)) == date(2026, 11, 4)
    assert logic.next_occurrence(11, 3, date(2026, 11, 4)) == date(2027, 11, 3)
    assert logic.next_occurrence(1, 1, date(2026, 12, 31)) == date(2027, 1, 1)


def test_leap_day_is_celebrated_on_first_of_march():
    assert logic.occurrence(2, 29, 2027) == date(2027, 3, 1)
    assert logic.occurrence(2, 29, 2028) == date(2028, 2, 29)
    assert logic.next_occurrence(2, 29, date(2027, 2, 1)) == date(2027, 3, 1)


def test_describe_age_and_days():
    d = logic.describe(person(), date(2026, 11, 1))
    assert d["days_until"] == 3
    assert d["turning_age"] == 41
    assert d["current_age"] == 40
    assert not d["is_today"]
    today = logic.describe(person(), date(2026, 11, 4))
    assert today["is_today"] and today["current_age"] == 41


def test_round_birthday():
    d = logic.describe(person(birthdate="1986-11-04"), date(2026, 11, 1))
    assert d["turning_age"] == 40 and d["is_round"]


def test_year_unknown_has_no_age():
    d = logic.describe(person(year_known=False), date(2026, 11, 1))
    assert d["turning_age"] is None and d["current_age"] is None and not d["is_round"]


def test_reminder_days_are_unique_and_sorted():
    d = logic.describe(person(reminder_days_1=2, reminder_days_2=1), date(2026, 1, 1))
    assert d["reminder_days"] == [1, 2]
    d = logic.describe(person(reminder_days_1=1, reminder_days_2=1), date(2026, 1, 1))
    assert d["reminder_days"] == [1]


def test_greetings_by_salutation_and_style():
    g = logic.greeting_for
    assert g(person(), "de") == "Lieber Max"
    assert g(person(salutation="frau", first_name="Anna"), "de") == "Liebe Anna"
    assert g(person(style="formal"), "de") == "Sehr geehrter Herr Müller"
    assert g(person(style="formal", salutation="frau", last_name="Meier"), "de") == "Sehr geehrte Frau Meier"
    assert g(person(salutation=""), "de") == "Hallo Max"
    assert g(person(style="formal", last_name=""), "de") == "Sehr geehrter Herr Max"
    assert g(person(style="formal"), "en") == "Dear Mr. Müller"


def test_render_leaves_unknown_placeholders_and_tidies_spacing():
    assert logic.render("Hallo {name} {unknown} !", {"name": "Max"}) == "Hallo Max {unknown}!"
    assert logic.render("A  {x} .", {"x": ""}) == "A."


def test_greeting_message_uses_age_and_greeting():
    p = person()
    d = logic.describe(p, date(2026, 11, 4))
    msg = logic.build_greeting_message(p, d, ["{gruss}, alles Gute zum {alter}. Geburtstag!"], "de")
    assert msg == "Lieber Max, alles Gute zum 41. Geburtstag!"


def test_texts_with_age_are_skipped_when_year_unknown():
    p = person(year_known=False)
    d = logic.describe(p, date(2026, 11, 4))
    texts = ["{gruss}, zum {alter}. Geburtstag!", "{gruss}, alles Gute!"]
    for seed in range(20):
        msg = logic.build_greeting_message(p, d, texts, "de", random.Random(seed))
        assert msg == "Lieber Max, alles Gute!"


def test_default_texts_have_ten_entries_each():
    for lang in ("de", "en"):
        for style in ("personal", "formal"):
            assert len(logic.DEFAULT_TEXTS[lang][style]) == 10


def test_default_texts_render_without_leftover_placeholders():
    for lang in ("de", "en"):
        for style in ("personal", "formal"):
            for sal in ("herr", "frau", ""):
                p = person(style=style, salutation=sal)
                d = logic.describe(p, date(2026, 11, 4))
                for text in logic.DEFAULT_TEXTS[lang][style]:
                    msg = logic.render(text, logic.build_context(p, d, lang))
                    assert "{" not in msg, msg


def test_reminder_message():
    p = person()
    d = logic.describe(p, date(2026, 11, 3))
    msg = logic.build_reminder_message(p, d, logic.DEFAULT_REMINDER_TEMPLATE["de"], "de", 1)
    assert msg == "🎂 Erinnerung: Max Müller hat morgen Geburtstag und wird 41."
    p2 = person(year_known=False)
    d2 = logic.describe(p2, date(2026, 11, 2))
    msg2 = logic.build_reminder_message(p2, d2, logic.DEFAULT_REMINDER_TEMPLATE["de"], "de", 2)
    assert msg2 == "🎂 Erinnerung: Max Müller hat übermorgen Geburtstag."


def test_english_ordinals():
    assert [logic.ordinal_en(n) for n in (1, 2, 3, 4, 11, 12, 13, 21, 22, 40)] == [
        "1st", "2nd", "3rd", "4th", "11th", "12th", "13th", "21st", "22nd", "40th",
    ]


def test_random_offset_is_reproducible_and_within_window():
    from datetime import date as d

    values = {logic.random_offset(f"greet:{i}", d(2026, 11, 4), 3600) for i in range(50)}
    assert all(0 <= v <= 3600 for v in values)
    assert len(values) > 10  # spread over the window
    assert logic.random_offset("greet:x", d(2026, 11, 4), 3600) == logic.random_offset("greet:x", d(2026, 11, 4), 3600)
    assert logic.random_offset("greet:x", d(2026, 11, 4), 0) == 0

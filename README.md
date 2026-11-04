<p align="center">
  <img src="assets/icon.png" alt="Geburtstage" width="160">
</p>

# 🎂 Geburtstage – Birthday manager for Home Assistant

[Deutsch](#deutsch) · [English](#english)

---

## Deutsch

Verwalte Geburtstage komfortabel in Home Assistant, lass dich erinnern und gratuliere automatisch – mit zufälligen, zur Anrede passenden Texten.

### Funktionen

- **Seitenleisten-Panel „Geburtstage“** mit übersichtlicher Tabelle (Name, Geburtstag, Alter, nächster Termin, Erinnerung, Gratulation) – Personen **hinzufügen, bearbeiten, löschen**, suchen und sortieren.
- **Anrede** (Herr / Frau / Neutral) und **Stil** (persönlich / förmlich) bestimmen die Begrüßung: *Lieber Max*, *Liebe Anna*, *Sehr geehrter Herr Müller*, *Sehr geehrte Frau Meier*.
- **Gratulation** am Geburtstag über einen **vorhandenen Notify-Dienst oder eine Notify-Entity** – pro Person wählbar. Pro Stil gibt es eine Liste mit 10 Texten (änderbar), pro Gratulation wird zufällig einer gewählt.
- **Erinnerungen** X Tage vorher (bis zu zwei Werte pro Person, leer = keine Erinnerung).
- **Eigene Automationen:** Zu jedem Geburtstag/jeder Erinnerung wird ein Ereignis ausgelöst (Event-Entity *Geburtstags-Ereignis* und Bus-Events `geburtstage_birthday` / `geburtstage_reminder`) mit Name, Alter und fertigem Text. Ist „automatisch senden“ aus, verschickt die Integration nichts – du entscheidest in deiner Automation über Text und Notify.
- **Dashboard-Karte** `custom:geburtstage-card` mit visuellem Editor: Zeitraum, Anzahl, Darstellung (Liste / kompakt / Chips), Alter/Datum/Countdown ein- und ausblenden, Hervorhebung für heutige und runde Geburtstage, „Karte ausblenden wenn leer“, transparenter Hintergrund. Unterstützt das Sections-Raster.
- **Entities:** Kalender, *Kommende Geburtstage*, *Nächster Geburtstag*, *Geburtstage heute*, Ereignis.
- **Import/Export** per CSV und vCard (`.vcf` aus deinen Kontakten).
- 29. Februar wird in Nicht-Schaltjahren am **1. März** gefeiert. Ist das Geburtsjahr unbekannt, wird kein Alter angezeigt.
- Deutsch und Englisch.

### Installation (HACS)

1. HACS → ⋮ → *Benutzerdefinierte Repositories* → URL dieses Repositories, Kategorie **Integration**.
2. *Geburtstage* installieren und Home Assistant neu starten.
3. *Einstellungen → Geräte & Dienste → Integration hinzufügen → Geburtstage*.
4. In der Seitenleiste **Geburtstage** öffnen und Personen anlegen.

Die Dashboard-Karte wird automatisch mitgeliefert (keine Ressource nötig). Beim Hinzufügen einer Karte erscheint sie als **Geburtstage**.

### Nachrichten-Platzhalter

`{gruss}` (Anrede + Name, z. B. „Lieber Max“), `{name}`, `{nachname}`, `{vollername}`, `{alter}`, `{wann}` (heute/morgen/in 3 Tagen), `{wird}` („und wird 40“), `{datum}`.
Englisch: `{greeting}`, `{first_name}`, `{last_name}`, `{full_name}`, `{age}`, `{age_ordinal}`, `{when}`, `{turning}`, `{date}`.
Texte mit Altersplatzhalter werden übersprungen, wenn das Geburtsjahr unbekannt ist.

### Eigene Automation (Beispiel)

```yaml
triggers:
  - trigger: state
    entity_id: event.geburtstage_geburtstags_ereignis
conditions:
  - condition: template
    value_template: "{{ trigger.to_state.attributes.event_type == 'birthday' }}"
actions:
  - action: notify.mobile_app_mein_handy
    data:
      title: "Geburtstag"
      message: "{{ trigger.to_state.attributes.message }}"
```

Services: `geburtstage.add_person`, `update_person`, `remove_person`, `send_greeting`, `get_upcoming` (liefert Antwortdaten).

### Hinweise

- Die Daten liegen lokal in `.storage/geburtstage.data` und sind Teil deiner Home-Assistant-Backups.
- Gratulationen und Erinnerungen werden täglich zur eingestellten Uhrzeit versandt; nach einem Neustart wird nachgeholt, aber nie doppelt gesendet.

---

## English

Manage birthdays in Home Assistant, get reminders and send congratulations automatically using random texts that match the salutation.

### Features

- **Sidebar panel “Geburtstage”** with a clear table – **add, edit, delete**, search and sort people.
- **Salutation** (Mr. / Ms. / neutral) and **style** (personal / formal) select the greeting: *Dear Max*, *Dear Mr. Smith*, …
- **Congratulation** on the birthday via an **existing notify service or notify entity**, chosen per person. Ten editable texts per style, one picked at random each time.
- **Reminders** X days before (up to two values per person, empty = none).
- **Your own automations:** every birthday/reminder fires an event (event entity and bus events `geburtstage_birthday` / `geburtstage_reminder`) with name, age and the finished text. With “send automatically” off the integration sends nothing – you decide text and notify in your automation.
- **Dashboard card** `custom:geburtstage-card` with visual editor (range, count, list / compact / chips layout, show or hide age / date / countdown, highlight today and round birthdays, hide when empty, transparent background, Sections grid support).
- **Entities:** calendar, upcoming birthdays, next birthday, birthdays today, event.
- **Import/export** via CSV and vCard.
- 29 February is celebrated on **1 March** in non-leap years.
- German and English.

### Installation (HACS)

1. HACS → ⋮ → *Custom repositories* → this repository URL, category **Integration**.
2. Install *Geburtstage*, restart Home Assistant.
3. *Settings → Devices & services → Add integration → Geburtstage*.
4. Open **Geburtstage** in the sidebar and add people.

The dashboard card is bundled automatically (no resource needed).

### Development

```bash
pip install -r requirements_test.txt
pytest tests -q
```

Release: bump `version` in `manifest.json`, push a tag `vX.Y.Z`. The Gitea push mirror transfers the tag; the GitHub workflow `release.yml` creates the release that HACS needs.

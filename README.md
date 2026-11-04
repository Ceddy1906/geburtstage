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
- **Eigene Automationen:** Zu jedem Geburtstag und jeder Erinnerung wird ein Ereignis ausgelöst – mit Name, Alter, fertiger Anrede und Text. Ist „Gratulation automatisch senden“ aus, verschickt die Integration nichts: Du bestimmst in deiner Automation selbst über Text und Notify. [Beispiele unten](#automationen-mit-geburtstagen).
- **Dashboard-Karte** `custom:geburtstage-card` mit visuellem Editor: Zeitraum, Anzahl, Darstellung (Liste / kompakt / Chips), Alter/Datum/Countdown ein- und ausblenden, Hervorhebung für heutige und runde Geburtstage, „Karte ausblenden wenn leer“, transparenter Hintergrund. Unterstützt das Sections-Raster.
- **Entities:** Kalender, *Kommende Geburtstage*, *Nächster Geburtstag*, *Geburtstage heute*, *Geburtstags-Ereignis*.
- **Import/Export** per CSV und vCard (`.vcf` aus deinen Kontakten).
- 29. Februar wird in Nicht-Schaltjahren am **1. März** gefeiert. Ist das Geburtsjahr unbekannt, wird kein Alter angezeigt.
- Deutsch und Englisch.

### Installation (HACS)

1. HACS → ⋮ → *Benutzerdefinierte Repositories* → URL dieses Repositories, Kategorie **Integration**.
2. *Geburtstage* installieren und Home Assistant neu starten.
3. *Einstellungen → Geräte & Dienste → Integration hinzufügen → Geburtstage*.
4. In der Seitenleiste **Geburtstage** öffnen und Personen anlegen.

Die Dashboard-Karte wird automatisch mitgeliefert (keine Ressource nötig). Beim Hinzufügen einer Karte erscheint sie als **Geburtstage** (ganz unten bei den benutzerdefinierten Karten).

> **Nach der Installation und nach jedem Update** den Browser mit **Strg + F5** neu laden (Companion-App: *Einstellungen → Companion-App → Fehlerbehebung → Frontend-Cache zurücksetzen*). HA lädt die Karte nur beim Seitenaufbau – ohne Neuladen fehlt sie in der Kartenauswahl.

### Nachrichten-Platzhalter

Platzhalter stehen in geschweiften Klammern und werden beim Senden durch die Daten der Person ersetzt. Sie funktionieren in den **Gratulationstexten** und im **Erinnerungstext** (Panel → Einstellungen) sowie im Parameter `message` des Services `geburtstage.send_greeting`.

| Platzhalter | Wird ersetzt durch | Beispiel |
|---|---|---|
| `{gruss}` | passende Begrüßung aus Anrede, Stil und Name | *Lieber Hugo* · *Sehr geehrte Frau Meier* |
| `{name}` | Vorname | Hugo |
| `{nachname}` | Nachname | Testmann |
| `{vollername}` | Vor- und Nachname | Hugo Testmann |
| `{alter}` | Alter, das die Person an diesem Geburtstag erreicht | 25 |
| `{anrede}` | Anrede (bei „Neutral“ leer) | Herr · Frau |
| `{datum}` | Datum des Geburtstags | 14.12. |
| `{wann}` | nur Erinnerung: Zeitpunkt | heute · morgen · übermorgen · in 3 Tagen |
| `{wird}` | nur Erinnerung: „und wird“ + Alter | und wird 25 |
| `{tage}` | nur Erinnerung: Tage bis zum Geburtstag | 3 |

Englisch: `{greeting}`, `{first_name}`, `{last_name}`, `{full_name}`, `{age}`, `{age_ordinal}`, `{salutation}`, `{date}`, `{when}`, `{turning}`, `{days}`.
Ist das Geburtsjahr unbekannt, ist `{alter}` leer; Gratulationstexte mit `{alter}` werden dann übersprungen.

### Automationen mit Geburtstagen

Die Integration löst zur eingestellten Uhrzeit (Standard 08:00) für jeden Geburtstag das Ereignis **`geburtstage_birthday`** und für jede Erinnerung **`geburtstage_reminder`** aus. Beide Ereignisse gibt es als Bus-Event (für den Auslöser *Ereignis*) und als Entität *Geburtstags-Ereignis* (für den Auslöser *Zustand*; die Daten stehen dann in `trigger.to_state.attributes`).

**Daten des Ereignisses** (bei Bus-Events als `trigger.event.data.…`):

| Feld | Inhalt | Beispiel |
|---|---|---|
| `name` | vollständiger Name | Hugo Testmann |
| `first_name`, `last_name` | Vor- und Nachname | Hugo, Testmann |
| `greeting` | fertige Begrüßung passend zu Anrede und Stil | Lieber Hugo |
| `salutation` | `herr`, `frau` oder leer | herr |
| `style` | `personal` oder `formal` | personal |
| `age` | erreichtes Alter (leer, wenn das Geburtsjahr unbekannt ist) | 25 |
| `birthdate` | Geburtsdatum | 2001-12-14 |
| `date` | Datum des (nächsten) Geburtstags | 2026-12-14 |
| `days_until` | Tage bis zum Geburtstag (`0` = heute) | 0 |
| `message` | fertiger Text aus der Textliste bzw. dem Erinnerungstext | *Lieber Hugo, …* |
| `auto_send` | `true`, wenn die Integration selbst sendet | false |
| `sent` | `true`, wenn der Versand geklappt hat | false |
| `person_id` | interne ID der Person | |

> **Wichtig:** Hat die Person „Gratulation automatisch senden“ eingeschaltet, sendet die Integration die Nachricht selbst. Willst du den Gruß in einer eigenen Automation verschicken, **schalte „Gratulation automatisch senden“ bei dieser Person aus** – sonst bekommt der Empfänger zwei Nachrichten. Das Ereignis wird in beiden Fällen ausgelöst.

Die Notify-Dienste heißen bei dir anders – setze deinen eigenen ein (z. B. `notify.mobile_app_mein_handy`, `notify.signal_marc`). Die Namen der Entitäten hängen von der Sprache bei der Einrichtung ab; im Zweifel unter *Einstellungen → Geräte & Dienste → Geburtstage* nachsehen.

#### 1. Eigener Text zum Geburtstag von Hugo Testmann (14.12.2001)

Lege im Panel *Geburtstage* die Person an: Vorname **Hugo**, Nachname **Testmann**, Anrede **Herr**, Geburtsdatum **14.12.2001**, **„Gratulation automatisch senden“ aus**. Dann diese Automation:

```yaml
alias: Hugo Testmann – Geburtstagsgruß
triggers:
  - trigger: event
    event_type: geburtstage_birthday
    event_data:
      name: Hugo Testmann
actions:
  - action: notify.mobile_app_mein_handy
    data:
      title: "🎂 {{ trigger.event.data.first_name }} hat Geburtstag"
      message: >-
        {{ trigger.event.data.greeting }}, alles Gute zum
        {{ trigger.event.data.age }}. Geburtstag! 🥳
        Lass dich heute richtig feiern.
```

Am 14.12.2026 kommt an: *„Lieber Hugo, alles Gute zum 25. Geburtstag! 🥳 Lass dich heute richtig feiern.“*

#### 2. Eigener Text mit Platzhaltern des Panels

Statt Jinja kannst du auch die Platzhalter aus der Tabelle oben verwenden – über den Service `geburtstage.send_greeting`. Das passt „Lieber/Liebe“ bzw. „Sehr geehrter/geehrte …“ automatisch an:

```yaml
alias: Hugo Testmann – Gruß mit Platzhaltern
triggers:
  - trigger: event
    event_type: geburtstage_birthday
    event_data:
      name: Hugo Testmann
actions:
  - action: geburtstage.send_greeting
    data:
      person: Hugo Testmann
      notify: notify.signal_hugo
      title: Alles Gute!
      message: "{gruss}, alles Gute zum {alter}. Geburtstag! 🎉 Dein {vollername}-Fanclub."
```

Ergebnis: *„Lieber Hugo, alles Gute zum 25. Geburtstag! 🎉 Dein Hugo Testmann-Fanclub.“* Ohne `message` wird ein zufälliger Text aus der Textliste gewählt; ohne `notify` das bei der Person gespeicherte Ziel.

#### 3. Zufälliger Standardtext für alle, die nicht automatisch senden

Eine Automation für alle Personen, bei denen „automatisch senden“ aus ist – du bestimmst nur das Ziel, den Text liefert die Integration:

```yaml
alias: Geburtstagsgrüße (Standardtext) an die Familie
triggers:
  - trigger: event
    event_type: geburtstage_birthday
conditions:
  - condition: template
    value_template: "{{ not trigger.event.data.auto_send }}"
actions:
  - action: notify.signal_familie
    data:
      message: "{{ trigger.event.data.message }}"
```

#### 4. Bei runden Geburtstagen einen besonderen Text senden

```yaml
alias: Runder Geburtstag
triggers:
  - trigger: event
    event_type: geburtstage_birthday
actions:
  - choose:
      - conditions:
          - condition: template
            value_template: >-
              {{ trigger.event.data.age is number and trigger.event.data.age % 10 == 0 }}
        sequence:
          - action: notify.mobile_app_mein_handy
            data:
              message: >-
                🎉 {{ trigger.event.data.name }} wird heute {{ trigger.event.data.age }} –
                ein runder Geburtstag! Nicht vergessen anzurufen.
    default:
      - action: notify.mobile_app_mein_handy
        data:
          message: "{{ trigger.event.data.message }}"
```

#### 5. Erinnerung nur zwei Tage vorher an eine Gruppe schicken

Erinnerungen haben `days_until` mit der Zahl der Tage, die noch fehlen:

```yaml
alias: Geburtstag in 2 Tagen – Gruppe informieren
triggers:
  - trigger: event
    event_type: geburtstage_reminder
conditions:
  - condition: template
    value_template: "{{ trigger.event.data.days_until == 2 }}"
actions:
  - action: notify.signal_geschwister
    data:
      message: "Denkt an das Geschenk! {{ trigger.event.data.message }}"
```

#### 6. Ansage über einen Lautsprecher

```yaml
alias: Geburtstag ansagen
triggers:
  - trigger: event
    event_type: geburtstage_birthday
actions:
  - action: tts.speak
    target:
      entity_id: tts.home_assistant_cloud
    data:
      media_player_entity_id: media_player.kueche
      message: >-
        Heute hat {{ trigger.event.data.first_name }} Geburtstag
        {% if trigger.event.data.age %}und wird {{ trigger.event.data.age }}{% endif %}.
        Vergiss nicht zu gratulieren!
```

#### 7. Partylicht, solange jemand Geburtstag hat

Die Entität *Geburtstage heute* zeigt die Anzahl der heutigen Geburtstage und wechselt um Mitternacht:

```yaml
alias: Partylicht bei Geburtstag
triggers:
  - trigger: time
    at: "18:00:00"
conditions:
  - condition: numeric_state
    entity_id: sensor.geburtstage_geburtstage_heute
    above: 0
actions:
  - action: scene.turn_on
    target:
      entity_id: scene.party
```

#### 8. Morgendliche Übersicht der nächsten 7 Tage

`geburtstage.get_upcoming` liefert die Geburtstage als Antwortdaten:

```yaml
alias: Geburtstage der Woche
triggers:
  - trigger: time
    at: "07:30:00"
actions:
  - action: geburtstage.get_upcoming
    data:
      days: 7
    response_variable: upcoming
  - condition: template
    value_template: "{{ upcoming.birthdays | length > 0 }}"
  - action: notify.mobile_app_mein_handy
    data:
      title: Geburtstage der nächsten 7 Tage
      message: "{{ upcoming.birthdays | map(attribute='name') | join(', ') }}"
```

Jeder Eintrag in `upcoming.birthdays` enthält `name`, `first_name`, `last_name`, `next_date`, `days_until`, `turning_age`, `current_age`, `is_today` und `is_round`.

#### Weitere Services

`geburtstage.add_person`, `geburtstage.update_person` und `geburtstage.remove_person` (z. B. um Personen aus einer Automation zu pflegen) – die Felder stehen im Automations-Editor unter *Aktion hinzufügen → Geburtstage*.

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
- **Your own automations:** every birthday and reminder fires an event with name, age, ready-made greeting and text. With “send greeting automatically” off the integration sends nothing – you decide text and notify in your automation. [Examples below](#automations-with-birthdays).
- **Dashboard card** `custom:geburtstage-card` with visual editor (range, count, list / compact / chips layout, show or hide age / date / countdown, highlight today and round birthdays, hide when empty, transparent background, Sections grid support).
- **Entities:** calendar, upcoming birthdays, next birthday, birthdays today, birthday event.
- **Import/export** via CSV and vCard.
- 29 February is celebrated on **1 March** in non-leap years.
- German and English.

### Installation (HACS)

1. HACS → ⋮ → *Custom repositories* → this repository URL, category **Integration**.
2. Install *Geburtstage*, restart Home Assistant.
3. *Settings → Devices & services → Add integration → Geburtstage*.
4. Open **Geburtstage** in the sidebar and add people.

The dashboard card is bundled automatically (no resource needed). It appears as **Geburtstage** at the bottom of the custom cards.

> **After installing and after every update** reload the browser with **Ctrl + F5** (companion app: *Settings → Companion app → Troubleshooting → Reset frontend cache*). Home Assistant only loads the card when the page is loaded – without a reload it is missing from the card picker.

### Message placeholders

Placeholders are written in curly braces and replaced with the person's data when the message is sent. They work in the **greeting texts** and the **reminder text** (panel → Settings) and in the `message` parameter of the `geburtstage.send_greeting` service.

| Placeholder | Replaced by | Example |
|---|---|---|
| `{greeting}` | greeting built from salutation, style and name | *Dear Hugo* · *Dear Ms. Meier* |
| `{first_name}` | first name | Hugo |
| `{last_name}` | last name | Testmann |
| `{full_name}` | first and last name | Hugo Testmann |
| `{age}` / `{age_ordinal}` | age reached on this birthday | 25 / 25th |
| `{salutation}` | Mr. / Ms. (empty for neutral) | Mr. |
| `{date}` | date of the birthday | 12/14 |
| `{when}` | reminder only: when | today · tomorrow · in 3 days |
| `{turning}` | reminder only: “(turning 25)” | (turning 25) |
| `{days}` | reminder only: days until the birthday | 3 |

The German names (`{gruss}`, `{name}`, `{alter}`, …) work as well. If the year of birth is unknown, `{age}` is empty and greeting texts containing it are skipped.

### Automations with birthdays

At the configured time (default 08:00) the integration fires **`geburtstage_birthday`** for every birthday and **`geburtstage_reminder`** for every reminder. Both exist as bus events (trigger type *Event*) and as the entity *Birthday event* (trigger type *State*; the data is then in `trigger.to_state.attributes`).

**Event data** (`trigger.event.data.…` for bus events): `name`, `first_name`, `last_name`, `greeting` (e.g. “Dear Hugo”), `salutation` (`herr`, `frau`, empty), `style` (`personal`, `formal`), `age` (empty if the year is unknown), `birthdate`, `date` (next birthday), `days_until` (`0` = today), `message` (ready-made text), `auto_send`, `sent`, `person_id`.

> **Important:** if “send greeting automatically” is on for a person, the integration sends the message itself. To send it from your own automation, **turn that option off for this person**, otherwise the recipient gets two messages. The event fires in both cases.

Replace the notify services with your own (e.g. `notify.mobile_app_my_phone`). Entity names depend on the language used at setup.

#### 1. Own text for Hugo Testmann's birthday (14 Dec 2001)

Create the person in the panel: first name **Hugo**, last name **Testmann**, salutation **Mr.**, birth date **14.12.2001**, **“send greeting automatically” off**. Then:

```yaml
alias: Hugo Testmann – birthday greeting
triggers:
  - trigger: event
    event_type: geburtstage_birthday
    event_data:
      name: Hugo Testmann
actions:
  - action: notify.mobile_app_my_phone
    data:
      title: "🎂 {{ trigger.event.data.first_name }}'s birthday"
      message: >-
        {{ trigger.event.data.greeting }}, happy birthday! 🥳
        You turn {{ trigger.event.data.age }} today – enjoy your day.
```

On 14 Dec 2026 this sends: *“Dear Hugo, happy birthday! 🥳 You turn 25 today – enjoy your day.”*

#### 2. Own text using the placeholders

```yaml
alias: Hugo Testmann – greeting with placeholders
triggers:
  - trigger: event
    event_type: geburtstage_birthday
    event_data:
      name: Hugo Testmann
actions:
  - action: geburtstage.send_greeting
    data:
      person: Hugo Testmann
      notify: notify.signal_hugo
      title: All the best!
      message: "{greeting}, happy {age_ordinal} birthday! 🎉"
```

Without `message` a random text from the list is used; without `notify` the target stored for the person.

#### 3. Random default text for everyone without automatic sending

```yaml
alias: Birthday greetings (default text) to the family
triggers:
  - trigger: event
    event_type: geburtstage_birthday
conditions:
  - condition: template
    value_template: "{{ not trigger.event.data.auto_send }}"
actions:
  - action: notify.signal_family
    data:
      message: "{{ trigger.event.data.message }}"
```

#### 4. Reminder two days before, sent to a group

```yaml
alias: Birthday in 2 days
triggers:
  - trigger: event
    event_type: geburtstage_reminder
conditions:
  - condition: template
    value_template: "{{ trigger.event.data.days_until == 2 }}"
actions:
  - action: notify.signal_siblings
    data:
      message: "Don't forget the gift: {{ trigger.event.data.message }}"
```

#### 5. Party lights while somebody has a birthday

```yaml
alias: Party lights on birthdays
triggers:
  - trigger: time
    at: "18:00:00"
conditions:
  - condition: numeric_state
    entity_id: sensor.geburtstage_birthdays_today
    above: 0
actions:
  - action: scene.turn_on
    target:
      entity_id: scene.party
```

#### 6. Morning overview of the next 7 days

```yaml
alias: Birthdays of the week
triggers:
  - trigger: time
    at: "07:30:00"
actions:
  - action: geburtstage.get_upcoming
    data:
      days: 7
    response_variable: upcoming
  - condition: template
    value_template: "{{ upcoming.birthdays | length > 0 }}"
  - action: notify.mobile_app_my_phone
    data:
      title: Birthdays in the next 7 days
      message: "{{ upcoming.birthdays | map(attribute='name') | join(', ') }}"
```

Other services: `geburtstage.add_person`, `geburtstage.update_person`, `geburtstage.remove_person`.

### Notes

- Data is stored locally in `.storage/geburtstage.data` and included in your Home Assistant backups.
- Greetings and reminders are sent daily at the configured time; after a restart missed ones are caught up, but never sent twice.

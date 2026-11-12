# Änderungen / Changelog

## [1.0.1] – 2026-11-12

### Verbessert
- **Einstellungen werden sofort gespeichert:** Kanal („Erinnerungen senden an“), Uhrzeiten, Titel, Erinnerungstext und alle Schalter werden direkt beim Ändern gespeichert (Hinweis „Gespeichert“). Bisher musste man dafür unten „Speichern“ klicken, was leicht mit dem Speichern der Gratulationstexte verwechselt wurde.
- Der untere Button heißt jetzt **„Texte speichern“** und speichert die Gratulationstexte. Ein Hinweis oben erklärt, was automatisch gespeichert wird.

### Hinweis zum Update
Nach dem Update den Browser mit **Strg + F5** neu laden.

---

### Improved
- **Settings are saved immediately:** channel (“Send reminders to”), times, titles, reminder text and all switches are saved as soon as you change them (a “Saved” note appears). Before, you had to click “Save” at the bottom, which was easily mistaken for saving the greeting texts.
- The bottom button is now **“Save texts”** and saves the greeting texts. A hint at the top explains what is saved automatically.

### Update note
After updating, reload the browser with **Ctrl + F5**.

## [1.0.0] – 2026-11-12

Erste stabile Version: Der Funktionsumfang (Personenverwaltung im Panel, Gratulationen und Erinnerungen mit Zeitfenster, Ereignisse für eigene Automationen, Dashboard-Karte, Import/Export) hat sich im Einsatz bewährt.

### Neu
- **Titel optional:** „Titel Gratulation“ und „Titel Erinnerung“ in den Einstellungen haben je einen Schalter **„Titel mitsenden“**. Ausgeschaltet wird nur der Nachrichtentext gesendet (ohne `title`) – praktisch für Messenger wie Signal, die keinen Titel anzeigen. Das gilt auch für „Test an mich senden“. Standard bleibt „an“, bestehende Einstellungen ändern sich nicht.

### Hinweis zum Update
Nach dem Update den Browser mit **Strg + F5** neu laden.

---

First stable release: the feature set (people management in the panel, greetings and reminders with time window, events for your own automations, dashboard card, import/export) has proven itself in use.

### New
- **Optional titles:** “Greeting title” and “Reminder title” in the settings each have a switch **“Send the title”**. When off, only the message text is sent (without `title`) – handy for messengers such as Signal that do not show a title. This also applies to “Send test to me”. The default stays on, existing settings do not change.

### Update note
After updating, reload the browser with **Ctrl + F5**.

## [0.3.1] – 2026-11-05

### Neu
- **Torte am Geburtstag:** In der Dashboard-Karte erscheint bei heutigen Geburtstagen statt der Initialen ein Torten-Symbol (in Liste, kompakt und Chips).
- **Symbol wählbar:** Im Karten-Editor gibt es „Symbol für heutige Geburtstage“ (Icon-Auswahl mit allen MDI-Symbolen, Standard `mdi:cake-variant`) und den Schalter „Heute: Symbol statt Initialen“, um das Verhalten auszuschalten.
- Die Einstellung „Symbol: Torten-Symbol“ zeigt für alle anderen Personen jetzt `mdi:cake-variant-outline`, damit sich heute und nicht-heute unterscheiden.

### Hinweis zum Update
Nach dem Update den Browser mit **Strg + F5** neu laden.

---

### New
- **Cake on the birthday:** on today's birthdays the dashboard card shows a cake icon instead of the initials (list, compact and chips layout).
- **Selectable icon:** the card editor has “Icon for today's birthdays” (icon picker with all MDI icons, default `mdi:cake-variant`) and the switch “Today: icon instead of initials” to turn the behavior off.
- The setting “Symbol: cake icon” now shows `mdi:cake-variant-outline` for everyone else, so today and not-today can be told apart.

### Update note
After updating, reload the browser with **Ctrl + F5**.

## [0.3.0] – 2026-11-04

### Neu
- **Zeitfenster mit zufälliger Sendezeit:** In den Einstellungen gibt es neben der Uhrzeit (jetzt „ab“) das optionale Feld „Zeitfenster bis“. Ist es gesetzt, wird jede Gratulation und jede Erinnerung zu einer zufälligen Uhrzeit in diesem Fenster gesendet (z. B. 08:00–11:30) – das wirkt weniger automatisch. Die Zeit ist pro Person und Tag festgelegt und bleibt auch nach einem Neustart gleich; das Ereignis für eigene Automationen wird zum selben Zeitpunkt ausgelöst. Ohne „bis“ ändert sich nichts: Alles geht genau zur eingestellten Uhrzeit raus.
- Verständliche Fehlermeldung, wenn das Zeitfenster nicht nach der Startzeit endet (es muss am selben Tag enden).

### Hinweis zum Update
Nach dem Update den Browser mit **Strg + F5** neu laden.

---

### New
- **Time window with random send time:** next to the time (now “from”) the settings have the optional field “Time window until”. If set, every greeting and every reminder is sent at a random time inside that window (e.g. 08:00–11:30), which feels less automatic. The time is fixed per person and day and stays the same after a restart; the event for your own automations fires at the same moment. Without “until” nothing changes: everything is sent exactly at the configured time.
- Clear error message if the window does not end after the start time (it has to end on the same day).

### Update note
After updating, reload the browser with **Ctrl + F5**.

## [0.2.1] – 2026-11-04

### Korrigiert
- **„Test senden“ ging an die Person bzw. fand kein Ziel.** Testnachrichten gehen jetzt immer an dein eigenes Ziel aus den Einstellungen („Erinnerungen und Testnachrichten senden an“) – nie an die Person. Der Button heißt „Test an mich senden“, die Nachricht beginnt mit „[Test für Vorname]“, und die Rückmeldung nennt das Ziel. Ist keins gesetzt, erklärt eine Fehlermeldung, wo man es einträgt.
- **Ziel der Person nicht auswählbar:** Das Feld „Gratulation senden an“ ist jetzt immer sichtbar (ohne Haken „Gratulation automatisch senden“ abgeblendet, mit Hinweis), statt erst nach dem Anhaken zu erscheinen.

### Hinweis zum Update
Nach dem Update den Browser mit **Strg + F5** neu laden.

---

### Fixed
- **“Send test” went to the person or found no target.** Test messages now always go to your own target from the settings (“Send reminders and test messages to”) – never to the person. The button is called “Send test to me”, the message starts with “[Test für first name]” and the confirmation names the target. If none is set, an error explains where to set it.
- **Person's target could not be chosen:** the field “Send greeting to” is now always visible (dimmed with a hint while “Send greeting automatically” is off) instead of only appearing after ticking the box.

### Update note
After updating, reload the browser with **Ctrl + F5**.

## [0.2.0] – 2026-11-04

### Neu
- **Suchbare Zielauswahl:** Das Feld „Erinnerungen senden an“ (Einstellungen) und „Benachrichtigung über“ (Person) ist jetzt eine Suche. Ab 2 Buchstaben wird gefiltert, mehrere Wörter werden einzeln gesucht („alexa k“ findet „Alexa Media Kuchenalexa“), Treffer sind markiert. Bedienung auch per Pfeiltasten, Enter und Esc.
- **Platzhalter erklärt:** Die Einstellungen enthalten eine Tabelle aller Platzhalter mit Beschreibung, Beispiel und Geltungsbereich. Ein Klick fügt den Platzhalter an der Cursor-Position ein.
- **Ereignis mit Begrüßung:** Die Ereignisse `geburtstage_birthday` und `geburtstage_reminder` enthalten jetzt das Feld `greeting` (z. B. „Lieber Hugo“, „Sehr geehrte Frau Meier“).
- **Platzhalter in eigenen Texten:** Der Service `geburtstage.send_greeting` ersetzt im Parameter `message` Platzhalter wie `{gruss}`, `{alter}` oder `{vollername}`.
- **README:** Neue Beispiele für Automationen (eigener Text, Platzhalter, runde Geburtstage, Erinnerung an Gruppe, Ansage, Partylicht, Wochenübersicht) und ein Hinweis zum Neuladen des Browsers nach Installation/Update.

### Hinweis zum Update
Nach dem Update den Browser mit **Strg + F5** neu laden, damit die neue Version der Karte und des Panels geladen wird.

---

### New
- **Searchable target selection:** “Send reminders to” (settings) and “Notify via” (person) are now a search field. Filtering starts after 2 letters, every typed word must match (“alexa k” finds “Alexa Media Kuchenalexa”), matches are highlighted. Works with arrow keys, Enter and Esc.
- **Placeholders explained:** the settings contain a table of all placeholders with description, example and scope. A click inserts the placeholder at the cursor position.
- **Event with greeting:** the events `geburtstage_birthday` and `geburtstage_reminder` now contain the field `greeting` (e.g. “Dear Hugo”).
- **Placeholders in your own texts:** the service `geburtstage.send_greeting` replaces placeholders such as `{greeting}`, `{age}` or `{full_name}` in `message`.
- **README:** new automation examples and a note about reloading the browser after installing or updating.

### Update note
After updating, reload the browser with **Ctrl + F5** so the new card and panel are loaded.

## [0.1.0] – 2026-11-04

Erste Version / First version: Panel zum Verwalten der Personen, Gratulationen und Erinnerungen über vorhandene Notify-Dienste, zufällige Texte je Anrede und Stil, Ereignisse für eigene Automationen, Kalender und Sensoren, Dashboard-Karte mit visuellem Editor, CSV-/vCard-Import, Deutsch und Englisch.

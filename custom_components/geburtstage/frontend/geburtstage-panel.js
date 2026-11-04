/* Geburtstage – sidebar panel (vanilla web component, no external dependencies) */

const TEXTS = {
  de: {
    title: "Geburtstage",
    tab_persons: "Personen",
    tab_settings: "Einstellungen",
    add: "Person hinzufügen",
    import: "Import",
    export: "Export (CSV)",
    search: "Suchen…",
    col_name: "Name",
    col_date: "Geburtstag",
    col_age: "Alter",
    col_next: "Nächster",
    col_reminder: "Erinnerung",
    col_greeting: "Gratulation",
    empty: "Noch keine Personen angelegt.",
    no_match: "Keine Treffer.",
    edit: "Bearbeiten",
    delete: "Löschen",
    today: "Heute!",
    tomorrow: "Morgen",
    in_days: "in {n} Tagen",
    turns: "wird {n}",
    days_before: "{n} Tg.",
    none: "–",
    greeting_auto: "automatisch",
    greeting_event: "nur Ereignis",
    dlg_add: "Person hinzufügen",
    dlg_edit: "Person bearbeiten",
    first_name: "Vorname",
    last_name: "Nachname",
    last_name_hint: "für „Sehr geehrter Herr …“",
    salutation: "Anrede",
    sal_herr: "Herr",
    sal_frau: "Frau",
    sal_none: "Neutral",
    style: "Stil",
    style_personal: "Persönlich (Lieber Max)",
    style_formal: "Förmlich (Sehr geehrter Herr Müller)",
    birthdate: "Geburtsdatum",
    year_unknown: "Geburtsjahr unbekannt (kein Alter)",
    greeting_enabled: "Gratulation automatisch senden",
    greeting_notify: "Benachrichtigung über",
    choose: "– bitte wählen –",
    reminder_1: "Erinnerung 1 (Tage vorher)",
    reminder_2: "Erinnerung 2 (Tage vorher)",
    reminder_hint: "leer = keine Erinnerung",
    preview: "Vorschau",
    send_test: "Test senden",
    cancel: "Abbrechen",
    save: "Speichern",
    close: "Schließen",
    saved: "Gespeichert",
    deleted: "Gelöscht",
    confirm_delete: "„{name}“ wirklich löschen?",
    test_sent: "Testnachricht gesendet",
    error: "Fehler",
    s_general: "Allgemein",
    s_send_time: "Uhrzeit für Gratulationen und Erinnerungen",
    s_reminder_notify: "Erinnerungen senden an",
    s_auto_reminders: "Erinnerungen automatisch senden",
    s_titles: "Titel der Nachrichten",
    s_greeting_title: "Titel Gratulation",
    s_reminder_title: "Titel Erinnerung",
    s_reminder_template: "Text der Erinnerung",
    s_texts_personal: "Gratulationstexte – persönlich",
    s_texts_formal: "Gratulationstexte – förmlich",
    s_texts_hint: "Ein Text pro Zeile, pro Gratulation wird zufällig einer gewählt.",
    s_placeholders: "Platzhalter: {gruss} (Anrede + Name), {name}, {nachname}, {vollername}, {alter}, {wann}, {wird}, {datum}",
    s_reset: "Standard wiederherstellen",
    s_event_info:
      "Wer eigene Automationen nutzen möchte: Das Ereignis „Geburtstags-Ereignis“ liefert Name, Alter und den fertigen Text. Bei Personen ohne „automatisch senden“ wird nichts versendet.",
    imp_title: "Import",
    imp_file: "CSV- oder vCard-Datei (.csv, .vcf)",
    imp_found: "{n} Einträge erkannt",
    imp_none: "Keine gültigen Einträge gefunden.",
    imp_default_sal: "Anrede für alle ohne Angabe",
    imp_run: "Importieren",
    imp_done: "{added} importiert, {skipped} übersprungen (Duplikate), {errors} fehlerhaft",
    imp_hint:
      "Erwartete CSV-Spalten: vorname, nachname, anrede, geburtsdatum (TT.MM.JJJJ, JJJJ-MM-TT oder --MM-TT). Importierte Personen haben keine automatische Gratulation.",
    round: "runder Geburtstag",
  },
  en: {
    title: "Birthdays",
    tab_persons: "People",
    tab_settings: "Settings",
    add: "Add person",
    import: "Import",
    export: "Export (CSV)",
    search: "Search…",
    col_name: "Name",
    col_date: "Birthday",
    col_age: "Age",
    col_next: "Next",
    col_reminder: "Reminder",
    col_greeting: "Greeting",
    empty: "No people added yet.",
    no_match: "No matches.",
    edit: "Edit",
    delete: "Delete",
    today: "Today!",
    tomorrow: "Tomorrow",
    in_days: "in {n} days",
    turns: "turns {n}",
    days_before: "{n} d",
    none: "–",
    greeting_auto: "automatic",
    greeting_event: "event only",
    dlg_add: "Add person",
    dlg_edit: "Edit person",
    first_name: "First name",
    last_name: "Last name",
    last_name_hint: "for “Dear Mr. …”",
    salutation: "Salutation",
    sal_herr: "Mr.",
    sal_frau: "Ms.",
    sal_none: "Neutral",
    style: "Style",
    style_personal: "Personal (Dear Max)",
    style_formal: "Formal (Dear Mr. Smith)",
    birthdate: "Date of birth",
    year_unknown: "Year of birth unknown (no age)",
    greeting_enabled: "Send greeting automatically",
    greeting_notify: "Notify via",
    choose: "– please choose –",
    reminder_1: "Reminder 1 (days before)",
    reminder_2: "Reminder 2 (days before)",
    reminder_hint: "empty = no reminder",
    preview: "Preview",
    send_test: "Send test",
    cancel: "Cancel",
    save: "Save",
    close: "Close",
    saved: "Saved",
    deleted: "Deleted",
    confirm_delete: "Really delete “{name}”?",
    test_sent: "Test message sent",
    error: "Error",
    s_general: "General",
    s_send_time: "Time for greetings and reminders",
    s_reminder_notify: "Send reminders to",
    s_auto_reminders: "Send reminders automatically",
    s_titles: "Message titles",
    s_greeting_title: "Greeting title",
    s_reminder_title: "Reminder title",
    s_reminder_template: "Reminder text",
    s_texts_personal: "Greeting texts – personal",
    s_texts_formal: "Greeting texts – formal",
    s_texts_hint: "One text per line; one is picked at random for every greeting.",
    s_placeholders: "Placeholders: {greeting} (salutation + name), {first_name}, {last_name}, {full_name}, {age}, {age_ordinal}, {when}, {turning}, {date}",
    s_reset: "Restore defaults",
    s_event_info:
      "For your own automations: the “Birthday event” entity delivers name, age and the finished text. Nothing is sent for people without “send automatically”.",
    imp_title: "Import",
    imp_file: "CSV or vCard file (.csv, .vcf)",
    imp_found: "{n} entries found",
    imp_none: "No valid entries found.",
    imp_default_sal: "Salutation for entries without one",
    imp_run: "Import",
    imp_done: "{added} imported, {skipped} skipped (duplicates), {errors} failed",
    imp_hint:
      "Expected CSV columns: firstname, lastname, salutation, birthdate (DD.MM.YYYY, YYYY-MM-DD or --MM-DD). Imported people have no automatic greeting.",
    round: "round birthday",
  },
};

const STYLE = `
  :host { display: block; height: 100%; background: var(--primary-background-color); color: var(--primary-text-color); font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif); }
  * { box-sizing: border-box; }
  .toolbar { display: flex; align-items: center; gap: 8px; height: 56px; padding: 0 12px; background: var(--app-header-background-color, var(--primary-color)); color: var(--app-header-text-color, #fff); position: sticky; top: 0; z-index: 3; }
  .toolbar h1 { font-size: 20px; font-weight: 400; margin: 0; flex: 1; }
  .tabs { display: flex; gap: 4px; padding: 0 12px; background: var(--app-header-background-color, var(--primary-color)); position: sticky; top: 56px; z-index: 3; }
  .tab { padding: 10px 16px; cursor: pointer; border: 0; background: none; color: var(--app-header-text-color, #fff); opacity: .7; font-size: 14px; font-weight: 500; border-bottom: 2px solid transparent; }
  .tab.active { opacity: 1; border-bottom-color: var(--app-header-text-color, #fff); }
  .content { max-width: 1100px; margin: 0 auto; padding: 16px; }
  .card { background: var(--card-background-color); border-radius: var(--ha-card-border-radius, 12px); box-shadow: var(--ha-card-box-shadow, none); border: 1px solid var(--ha-card-border-color, var(--divider-color)); padding: 16px; margin-bottom: 16px; }
  .bar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px; }
  .bar .grow { flex: 1; min-width: 160px; }
  input, select, textarea { font: inherit; color: var(--primary-text-color); background: var(--secondary-background-color, transparent); border: 1px solid var(--divider-color); border-radius: 8px; padding: 9px 10px; width: 100%; }
  input[type=checkbox] { width: auto; }
  textarea { min-height: 260px; resize: vertical; line-height: 1.4; }
  input:focus, select:focus, textarea:focus { outline: 2px solid var(--primary-color); outline-offset: -1px; }
  button.btn { font: inherit; font-weight: 500; cursor: pointer; border-radius: 18px; border: 1px solid var(--divider-color); background: transparent; color: var(--primary-color); padding: 8px 16px; display: inline-flex; align-items: center; gap: 6px; }
  button.btn.primary { background: var(--primary-color); color: var(--text-primary-color, #fff); border-color: var(--primary-color); }
  button.btn.danger { color: var(--error-color, #db4437); }
  button.btn:disabled { opacity: .5; cursor: default; }
  button.icon { background: none; border: 0; cursor: pointer; color: var(--secondary-text-color); padding: 6px; border-radius: 50%; display: inline-flex; }
  button.icon:hover { background: var(--secondary-background-color); color: var(--primary-text-color); }
  table { width: 100%; border-collapse: collapse; }
  th { text-align: left; font-weight: 500; font-size: 13px; color: var(--secondary-text-color); padding: 8px; border-bottom: 1px solid var(--divider-color); cursor: pointer; user-select: none; white-space: nowrap; }
  th.nosort { cursor: default; }
  td { padding: 10px 8px; border-bottom: 1px solid var(--divider-color); vertical-align: middle; }
  tr:last-child td { border-bottom: 0; }
  tr.today td { background: color-mix(in srgb, var(--primary-color) 12%, transparent); }
  .sub { color: var(--secondary-text-color); font-size: 12px; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 12px; background: var(--secondary-background-color); }
  .badge.today { background: var(--primary-color); color: var(--text-primary-color, #fff); }
  .actions { white-space: nowrap; text-align: right; }
  .empty { text-align: center; color: var(--secondary-text-color); padding: 32px 0; }
  .field { margin-bottom: 14px; }
  .field label { display: block; font-size: 13px; color: var(--secondary-text-color); margin-bottom: 4px; }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .check { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; }
  .hint { font-size: 12px; color: var(--secondary-text-color); margin-top: 4px; }
  h2 { font-size: 16px; font-weight: 500; margin: 0 0 12px; }
  dialog { border: 0; border-radius: 16px; padding: 0; width: min(560px, 94vw); max-height: 92vh; background: var(--card-background-color); color: var(--primary-text-color); box-shadow: 0 8px 40px rgba(0,0,0,.4); }
  dialog::backdrop { background: rgba(0,0,0,.5); }
  .dlg-head { padding: 18px 20px 4px; font-size: 18px; font-weight: 500; }
  .dlg-body { padding: 12px 20px; overflow: auto; max-height: calc(92vh - 140px); }
  .dlg-foot { display: flex; justify-content: flex-end; gap: 8px; padding: 12px 20px 18px; flex-wrap: wrap; }
  .dlg-foot .left { margin-right: auto; display: flex; gap: 8px; }
  .preview { margin-top: 8px; padding: 10px 12px; border-radius: 8px; background: var(--secondary-background-color); font-size: 14px; white-space: pre-wrap; }
  .toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: var(--primary-text-color); color: var(--primary-background-color); padding: 10px 18px; border-radius: 8px; z-index: 20; font-size: 14px; }
  .toast.err { background: var(--error-color, #db4437); color: #fff; }
  .imp-table { max-height: 260px; overflow: auto; margin: 8px 0; font-size: 13px; }
  [hidden] { display: none !important; }
  @media (max-width: 720px) {
    .col-hide { display: none; }
    .row { grid-template-columns: 1fr; }
    .content { padding: 8px; }
  }
`;

const esc = (value) =>
  String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

class GeburtstagePanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._persons = [];
    this._settings = null;
    this._targets = [];
    this._tab = "persons";
    this._sort = { key: "next", dir: 1 };
    this._filter = "";
    this._importRows = [];
    this._built = false;
  }

  set hass(hass) {
    this._hass = hass;
    if (!this._built) {
      this._built = true;
      this._lang = (hass.language || "en").toLowerCase().startsWith("de") ? "de" : "en";
      this._build();
      this._load();
    }
    if (this._menu) this._menu.hass = hass;
  }

  set narrow(value) {
    this._narrow = value;
    if (this._menu) this._menu.narrow = value;
  }

  set panel(_) {}
  set route(_) {}

  t(key, vars = {}) {
    let text = (TEXTS[this._lang] && TEXTS[this._lang][key]) ?? TEXTS.en[key] ?? key;
    for (const [k, v] of Object.entries(vars)) text = text.replaceAll(`{${k}}`, v);
    return text;
  }

  // ---------------------------------------------------------------- build
  _build() {
    const root = this.shadowRoot;
    root.innerHTML = `
      <style>${STYLE}</style>
      <div class="toolbar"><ha-menu-button></ha-menu-button><h1>${esc(this.t("title"))}</h1></div>
      <div class="tabs">
        <button class="tab active" data-tab="persons">${esc(this.t("tab_persons"))}</button>
        <button class="tab" data-tab="settings">${esc(this.t("tab_settings"))}</button>
      </div>
      <div class="content">
        <section id="persons">
          <div class="card">
            <div class="bar">
              <input class="grow" id="search" type="search" placeholder="${esc(this.t("search"))}">
              <button class="btn primary" data-action="add"><ha-icon icon="mdi:plus"></ha-icon>${esc(this.t("add"))}</button>
              <button class="btn" data-action="import"><ha-icon icon="mdi:file-import"></ha-icon>${esc(this.t("import"))}</button>
              <button class="btn" data-action="export"><ha-icon icon="mdi:file-export"></ha-icon>${esc(this.t("export"))}</button>
            </div>
            <div id="table"></div>
          </div>
        </section>
        <section id="settings" hidden></section>
      </div>
      <dialog id="dlg"></dialog>
      <dialog id="confirm"></dialog>
      <dialog id="imp"></dialog>
    `;
    this._menu = root.querySelector("ha-menu-button");
    if (this._menu) {
      this._menu.hass = this._hass;
      this._menu.narrow = this._narrow;
    }
    root.addEventListener("click", (ev) => this._onClick(ev));
    root.getElementById("search").addEventListener("input", (ev) => {
      this._filter = ev.target.value.trim().toLowerCase();
      this._renderTable();
    });
  }

  async _load() {
    try {
      const [data, targets] = await Promise.all([
        this._hass.callWS({ type: "geburtstage/list" }),
        this._hass.callWS({ type: "geburtstage/notify_targets" }),
      ]);
      this._persons = data.persons;
      this._settings = data.settings;
      this._targets = targets.targets;
      this._renderTable();
      this._renderSettings();
    } catch (err) {
      this._toast(`${this.t("error")}: ${err.message || err}`, true);
    }
  }

  async _reloadPersons() {
    const data = await this._hass.callWS({ type: "geburtstage/list" });
    this._persons = data.persons;
    this._settings = data.settings;
    this._renderTable();
  }

  // ---------------------------------------------------------------- events
  _onClick(ev) {
    const target = ev.target.closest("[data-action],[data-tab],[data-sort]");
    if (!target) return;
    const { action, tab, sort, id } = target.dataset;
    if (tab) return this._switchTab(tab);
    if (sort) return this._setSort(sort);
    switch (action) {
      case "add": return this._openDialog(null);
      case "edit": return this._openDialog(this._persons.find((p) => p.id === id));
      case "delete": return this._confirmDelete(this._persons.find((p) => p.id === id));
      case "import": return this._openImport();
      case "export": return this._export();
    }
  }

  _switchTab(tab) {
    this._tab = tab;
    const root = this.shadowRoot;
    root.querySelectorAll(".tab").forEach((b) => b.classList.toggle("active", b.dataset.tab === tab));
    root.getElementById("persons").hidden = tab !== "persons";
    root.getElementById("settings").hidden = tab !== "settings";
  }

  _setSort(key) {
    this._sort = { key, dir: this._sort.key === key ? -this._sort.dir : 1 };
    this._renderTable();
  }

  _toast(message, isError = false) {
    const el = document.createElement("div");
    el.className = `toast${isError ? " err" : ""}`;
    el.textContent = message;
    this.shadowRoot.appendChild(el);
    setTimeout(() => el.remove(), isError ? 6000 : 2500);
  }

  // ---------------------------------------------------------------- table
  _formatDate(p) {
    const locale = this._hass.locale?.language || this._hass.language || "en";
    const d = new Date(p.year_known ? p.birthdate : `2000-${String(p.month).padStart(2, "0")}-${String(p.day).padStart(2, "0")}`);
    const opts = p.year_known ? { day: "2-digit", month: "2-digit", year: "numeric" } : { day: "2-digit", month: "2-digit" };
    return new Intl.DateTimeFormat(locale, opts).format(d);
  }

  _nextText(p) {
    if (p.days_until === 0) return this.t("today");
    if (p.days_until === 1) return this.t("tomorrow");
    return this.t("in_days", { n: p.days_until });
  }

  _targetLabel(value) {
    const t = this._targets.find((x) => x.value === value);
    return t ? t.label : value;
  }

  _sorted() {
    const { key, dir } = this._sort;
    const val = {
      name: (p) => p.name.toLowerCase(),
      date: (p) => p.month * 100 + p.day,
      age: (p) => (p.current_age ?? -1),
      next: (p) => p.days_until,
    }[key];
    const list = this._persons.filter((p) => !this._filter || p.name.toLowerCase().includes(this._filter));
    return list.sort((a, b) => {
      const x = val(a);
      const y = val(b);
      return (x < y ? -1 : x > y ? 1 : 0) * dir || a.name.localeCompare(b.name);
    });
  }

  _renderTable() {
    const el = this.shadowRoot.getElementById("table");
    if (!el) return;
    if (!this._persons.length) {
      el.innerHTML = `<div class="empty">${esc(this.t("empty"))}</div>`;
      return;
    }
    const rows = this._sorted();
    if (!rows.length) {
      el.innerHTML = `<div class="empty">${esc(this.t("no_match"))}</div>`;
      return;
    }
    const arrow = (k) => (this._sort.key === k ? (this._sort.dir > 0 ? " ▲" : " ▼") : "");
    const body = rows
      .map((p) => {
        const reminders = p.reminder_days.length ? p.reminder_days.map((n) => this.t("days_before", { n })).join(" / ") : this.t("none");
        const greeting = p.greeting_enabled
          ? `<ha-icon icon="mdi:bell-ring" style="--mdc-icon-size:18px"></ha-icon> ${esc(this.t("greeting_auto"))}<div class="sub">${esc(this._targetLabel(p.greeting_notify))}</div>`
          : `<span class="sub">${esc(this.t("greeting_event"))}</span>`;
        const turns = p.turning_age != null ? `<div class="sub">${esc(this.t("turns", { n: p.turning_age }))}${p.is_round ? " 🎉" : ""}</div>` : "";
        return `<tr class="${p.is_today ? "today" : ""}">
          <td><b>${esc(p.name)}</b><div class="sub">${esc(p.salutation === "herr" ? this.t("sal_herr") : p.salutation === "frau" ? this.t("sal_frau") : "")}</div></td>
          <td>${esc(this._formatDate(p))}</td>
          <td class="col-hide">${p.current_age != null ? p.current_age : esc(this.t("none"))}</td>
          <td><span class="badge ${p.is_today ? "today" : ""}">${esc(this._nextText(p))}</span>${turns}</td>
          <td class="col-hide">${esc(reminders)}</td>
          <td class="col-hide">${greeting}</td>
          <td class="actions">
            <button class="icon" title="${esc(this.t("edit"))}" data-action="edit" data-id="${esc(p.id)}"><ha-icon icon="mdi:pencil"></ha-icon></button>
            <button class="icon" title="${esc(this.t("delete"))}" data-action="delete" data-id="${esc(p.id)}"><ha-icon icon="mdi:delete"></ha-icon></button>
          </td></tr>`;
      })
      .join("");
    el.innerHTML = `<table><thead><tr>
        <th data-sort="name">${esc(this.t("col_name"))}${arrow("name")}</th>
        <th data-sort="date">${esc(this.t("col_date"))}${arrow("date")}</th>
        <th data-sort="age" class="col-hide">${esc(this.t("col_age"))}${arrow("age")}</th>
        <th data-sort="next">${esc(this.t("col_next"))}${arrow("next")}</th>
        <th class="nosort col-hide">${esc(this.t("col_reminder"))}</th>
        <th class="nosort col-hide">${esc(this.t("col_greeting"))}</th>
        <th class="nosort"></th></tr></thead><tbody>${body}</tbody></table>`;
  }

  // ---------------------------------------------------------------- edit dialog
  _targetOptions(selected) {
    const opts = [`<option value="">${esc(this.t("choose"))}</option>`];
    let found = false;
    for (const t of this._targets) {
      const sel = t.value === selected;
      if (sel) found = true;
      opts.push(`<option value="${esc(t.value)}"${sel ? " selected" : ""}>${esc(t.label)} (${esc(t.value)})</option>`);
    }
    if (selected && !found) opts.push(`<option value="${esc(selected)}" selected>${esc(selected)}</option>`);
    return opts.join("");
  }

  _openDialog(person) {
    const p = person || {
      first_name: "", last_name: "", salutation: "herr", style: "personal", birthdate: "", year_known: true,
      greeting_enabled: false, greeting_notify: "", reminder_days_1: 1, reminder_days_2: null,
    };
    const dlg = this.shadowRoot.getElementById("dlg");
    this._editing = person ? person.id : null;
    dlg.innerHTML = `
      <div class="dlg-head">${esc(this.t(person ? "dlg_edit" : "dlg_add"))}</div>
      <form method="dialog" id="form" novalidate>
      <div class="dlg-body">
        <div class="row">
          <div class="field"><label>${esc(this.t("first_name"))} *</label><input id="f_first" value="${esc(p.first_name)}" required></div>
          <div class="field"><label>${esc(this.t("last_name"))}</label><input id="f_last" value="${esc(p.last_name)}"><div class="hint">${esc(this.t("last_name_hint"))}</div></div>
        </div>
        <div class="row">
          <div class="field"><label>${esc(this.t("salutation"))}</label>
            <select id="f_sal">
              <option value="herr"${p.salutation === "herr" ? " selected" : ""}>${esc(this.t("sal_herr"))}</option>
              <option value="frau"${p.salutation === "frau" ? " selected" : ""}>${esc(this.t("sal_frau"))}</option>
              <option value=""${p.salutation === "" ? " selected" : ""}>${esc(this.t("sal_none"))}</option>
            </select></div>
          <div class="field"><label>${esc(this.t("style"))}</label>
            <select id="f_style">
              <option value="personal"${p.style === "personal" ? " selected" : ""}>${esc(this.t("style_personal"))}</option>
              <option value="formal"${p.style === "formal" ? " selected" : ""}>${esc(this.t("style_formal"))}</option>
            </select></div>
        </div>
        <div class="field"><label>${esc(this.t("birthdate"))} *</label><input id="f_date" type="date" value="${esc(p.birthdate)}" required></div>
        <label class="check"><input id="f_noyear" type="checkbox"${p.year_known ? "" : " checked"}> ${esc(this.t("year_unknown"))}</label>
        <label class="check"><input id="f_greet" type="checkbox"${p.greeting_enabled ? " checked" : ""}> ${esc(this.t("greeting_enabled"))}</label>
        <div class="field" id="f_notify_wrap"><label>${esc(this.t("greeting_notify"))}</label><select id="f_notify">${this._targetOptions(p.greeting_notify)}</select></div>
        <div class="row">
          <div class="field"><label>${esc(this.t("reminder_1"))}</label><input id="f_r1" type="number" min="1" max="60" value="${p.reminder_days_1 ?? ""}"><div class="hint">${esc(this.t("reminder_hint"))}</div></div>
          <div class="field"><label>${esc(this.t("reminder_2"))}</label><input id="f_r2" type="number" min="1" max="60" value="${p.reminder_days_2 ?? ""}"></div>
        </div>
        <div class="preview" id="preview" hidden></div>
      </div>
      <div class="dlg-foot">
        <div class="left">
          <button type="button" class="btn" id="b_preview">${esc(this.t("preview"))}</button>
          <button type="button" class="btn" id="b_test">${esc(this.t("send_test"))}</button>
        </div>
        <button type="button" class="btn" id="b_cancel">${esc(this.t("cancel"))}</button>
        <button type="submit" class="btn primary" id="b_save">${esc(this.t("save"))}</button>
      </div></form>`;
    const $ = (id) => dlg.querySelector(`#${id}`);
    const syncNotify = () => { $("f_notify_wrap").hidden = !$("f_greet").checked; };
    $("f_greet").addEventListener("change", syncNotify);
    syncNotify();
    $("b_cancel").addEventListener("click", () => dlg.close());
    $("b_preview").addEventListener("click", () => this._preview(dlg));
    $("b_test").addEventListener("click", () => this._sendTest(dlg));
    dlg.querySelector("#form").addEventListener("submit", (ev) => { ev.preventDefault(); this._save(dlg); });
    dlg.showModal();
  }

  _readForm(dlg) {
    const $ = (id) => dlg.querySelector(`#${id}`);
    const num = (v) => (v === "" ? null : Number(v));
    const data = {
      first_name: $("f_first").value.trim(),
      last_name: $("f_last").value.trim(),
      salutation: $("f_sal").value,
      style: $("f_style").value,
      birthdate: $("f_date").value,
      year_known: !$("f_noyear").checked,
      greeting_enabled: $("f_greet").checked,
      greeting_notify: $("f_notify").value,
      reminder_days_1: num($("f_r1").value),
      reminder_days_2: num($("f_r2").value),
    };
    if (this._editing) data.id = this._editing;
    return data;
  }

  async _preview(dlg) {
    const box = dlg.querySelector("#preview");
    try {
      const res = await this._hass.callWS({ type: "geburtstage/preview", person: this._readForm(dlg) });
      box.textContent = res.message;
      box.hidden = false;
    } catch (err) {
      this._toast(`${this.t("error")}: ${err.message || err}`, true);
    }
  }

  async _sendTest(dlg) {
    try {
      await this._hass.callWS({ type: "geburtstage/send_test", person: this._readForm(dlg) });
      this._toast(this.t("test_sent"));
    } catch (err) {
      this._toast(`${this.t("error")}: ${err.message || err}`, true);
    }
  }

  async _save(dlg) {
    try {
      await this._hass.callWS({ type: "geburtstage/upsert", person: this._readForm(dlg) });
      dlg.close();
      await this._reloadPersons();
      this._toast(this.t("saved"));
    } catch (err) {
      this._toast(`${this.t("error")}: ${err.message || err}`, true);
    }
  }

  _confirmDelete(person) {
    if (!person) return;
    const dlg = this.shadowRoot.getElementById("confirm");
    dlg.innerHTML = `<div class="dlg-head">${esc(this.t("delete"))}</div>
      <div class="dlg-body">${esc(this.t("confirm_delete", { name: person.name }))}</div>
      <div class="dlg-foot"><button class="btn" id="c_no">${esc(this.t("cancel"))}</button>
      <button class="btn danger" id="c_yes">${esc(this.t("delete"))}</button></div>`;
    dlg.querySelector("#c_no").addEventListener("click", () => dlg.close());
    dlg.querySelector("#c_yes").addEventListener("click", async () => {
      try {
        await this._hass.callWS({ type: "geburtstage/delete", person_id: person.id });
        dlg.close();
        await this._reloadPersons();
        this._toast(this.t("deleted"));
      } catch (err) {
        this._toast(`${this.t("error")}: ${err.message || err}`, true);
      }
    });
    dlg.showModal();
  }

  // ---------------------------------------------------------------- settings
  _renderSettings() {
    const el = this.shadowRoot.getElementById("settings");
    const s = this._settings;
    if (!el || !s) return;
    el.innerHTML = `
      <div class="card">
        <h2>${esc(this.t("s_general"))}</h2>
        <div class="row">
          <div class="field"><label>${esc(this.t("s_send_time"))}</label><input id="s_time" type="time" step="60" value="${esc(s.send_time.slice(0, 5))}"></div>
          <div class="field"><label>${esc(this.t("s_reminder_notify"))}</label><select id="s_rnotify">${this._targetOptions(s.reminder_notify)}</select></div>
        </div>
        <label class="check"><input id="s_auto" type="checkbox"${s.auto_reminders ? " checked" : ""}> ${esc(this.t("s_auto_reminders"))}</label>
        <div class="row">
          <div class="field"><label>${esc(this.t("s_greeting_title"))}</label><input id="s_gtitle" value="${esc(s.greeting_title)}"></div>
          <div class="field"><label>${esc(this.t("s_reminder_title"))}</label><input id="s_rtitle" value="${esc(s.reminder_title)}"></div>
        </div>
        <div class="field"><label>${esc(this.t("s_reminder_template"))}</label><input id="s_rtemplate" value="${esc(s.reminder_template)}"></div>
        <div class="hint">${esc(this.t("s_placeholders"))}</div>
      </div>
      <div class="card">
        <h2>${esc(this.t("s_texts_personal"))}</h2>
        <textarea id="s_tp">${esc(s.texts_personal.join("\n"))}</textarea>
        <div class="hint">${esc(this.t("s_texts_hint"))}</div>
        <h2 style="margin-top:16px">${esc(this.t("s_texts_formal"))}</h2>
        <textarea id="s_tf">${esc(s.texts_formal.join("\n"))}</textarea>
        <div class="hint">${esc(this.t("s_texts_hint"))}</div>
        <p class="hint">${esc(this.t("s_event_info"))}</p>
        <div class="bar" style="margin-top:12px">
          <button class="btn" id="s_reset">${esc(this.t("s_reset"))}</button>
          <span class="grow"></span>
          <button class="btn primary" id="s_save">${esc(this.t("save"))}</button>
        </div>
      </div>`;
    el.querySelector("#s_save").addEventListener("click", () => this._saveSettings(false));
    el.querySelector("#s_reset").addEventListener("click", () => this._saveSettings(true));
  }

  async _saveSettings(reset) {
    const el = this.shadowRoot.getElementById("settings");
    const lines = (id) => el.querySelector(id).value.split("\n").map((l) => l.trim()).filter(Boolean);
    const settings = {
      send_time: `${el.querySelector("#s_time").value || "08:00"}:00`,
      reminder_notify: el.querySelector("#s_rnotify").value,
      auto_reminders: el.querySelector("#s_auto").checked,
      greeting_title: el.querySelector("#s_gtitle").value.trim(),
      reminder_title: el.querySelector("#s_rtitle").value.trim(),
      reminder_template: el.querySelector("#s_rtemplate").value.trim(),
      texts_personal: lines("#s_tp"),
      texts_formal: lines("#s_tf"),
    };
    if (reset) {
      settings.texts_personal = null;
      settings.texts_formal = null;
      settings.reminder_template = null;
      settings.greeting_title = "";
      settings.reminder_title = "";
    }
    try {
      const res = await this._hass.callWS({ type: "geburtstage/settings_set", settings });
      this._settings = res.settings;
      this._renderSettings();
      this._toast(this.t("saved"));
    } catch (err) {
      this._toast(`${this.t("error")}: ${err.message || err}`, true);
    }
  }

  // ---------------------------------------------------------------- export
  _export() {
    const cols = ["vorname", "nachname", "anrede", "stil", "geburtsdatum", "gratulation", "gratulation_notify", "erinnerung_1", "erinnerung_2"];
    const q = (v) => {
      const s = String(v ?? "");
      return /[;"\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
    };
    const lines = [cols.join(";")];
    for (const p of this._persons) {
      const date = p.year_known ? p.birthdate : `--${String(p.month).padStart(2, "0")}-${String(p.day).padStart(2, "0")}`;
      lines.push([p.first_name, p.last_name, p.salutation, p.style, date, p.greeting_enabled ? "ja" : "nein", p.greeting_notify, p.reminder_days_1 ?? "", p.reminder_days_2 ?? ""].map(q).join(";"));
    }
    const blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "geburtstage.csv";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }

  // ---------------------------------------------------------------- import
  _openImport() {
    const dlg = this.shadowRoot.getElementById("imp");
    this._importRows = [];
    dlg.innerHTML = `<div class="dlg-head">${esc(this.t("imp_title"))}</div>
      <div class="dlg-body">
        <div class="field"><label>${esc(this.t("imp_file"))}</label><input id="i_file" type="file" accept=".csv,.vcf,.txt,text/csv,text/vcard"></div>
        <div class="field"><label>${esc(this.t("imp_default_sal"))}</label>
          <select id="i_sal"><option value="">${esc(this.t("sal_none"))}</option><option value="herr">${esc(this.t("sal_herr"))}</option><option value="frau">${esc(this.t("sal_frau"))}</option></select></div>
        <div id="i_result" class="hint">${esc(this.t("imp_hint"))}</div>
        <div class="imp-table" id="i_table"></div>
      </div>
      <div class="dlg-foot"><button class="btn" id="i_close">${esc(this.t("close"))}</button>
      <button class="btn primary" id="i_run" disabled>${esc(this.t("imp_run"))}</button></div>`;
    const $ = (id) => dlg.querySelector(`#${id}`);
    $("i_close").addEventListener("click", () => dlg.close());
    $("i_file").addEventListener("change", async (ev) => {
      const file = ev.target.files[0];
      if (!file) return;
      const text = await file.text();
      const rows = /BEGIN:VCARD/i.test(text) ? parseVcf(text) : parseCsv(text);
      this._importRows = rows;
      $("i_result").textContent = rows.length ? this.t("imp_found", { n: rows.length }) : this.t("imp_none");
      $("i_run").disabled = !rows.length;
      $("i_table").innerHTML = `<table>${rows.slice(0, 200).map((r) => `<tr><td>${esc([r.first_name, r.last_name].filter(Boolean).join(" "))}</td><td>${esc(r.birthdate)}${r.year_known ? "" : " (?)"}</td></tr>`).join("")}</table>`;
    });
    $("i_run").addEventListener("click", async () => {
      const def = $("i_sal").value;
      const rows = this._importRows.map((r) => ({ ...r, salutation: r.salutation ?? def }));
      try {
        const res = await this._hass.callWS({ type: "geburtstage/import", rows });
        $("i_result").textContent = this.t("imp_done", { added: res.added, skipped: res.skipped, errors: res.errors.length });
        $("i_run").disabled = true;
        await this._reloadPersons();
      } catch (err) {
        this._toast(`${this.t("error")}: ${err.message || err}`, true);
      }
    });
    dlg.showModal();
  }
}

// ------------------------------------------------------------------ parsers
function parseDate(raw) {
  const s = String(raw || "").trim();
  let m;
  if ((m = s.match(/^--(\d{2})-?(\d{2})$/))) return { birthdate: `2000-${m[1]}-${m[2]}`, year_known: false };
  if ((m = s.match(/^(\d{4})-?(\d{2})-?(\d{2})/))) return { birthdate: `${m[1]}-${m[2]}-${m[3]}`, year_known: true };
  if ((m = s.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/))) return { birthdate: `${m[3]}-${m[2].padStart(2, "0")}-${m[1].padStart(2, "0")}`, year_known: true };
  if ((m = s.match(/^(\d{1,2})\.(\d{1,2})\.?$/))) return { birthdate: `2000-${m[2].padStart(2, "0")}-${m[1].padStart(2, "0")}`, year_known: false };
  return null;
}

function normSalutation(value) {
  const v = String(value || "").trim().toLowerCase();
  if (["herr", "mr", "mr.", "m", "male", "männlich", "maennlich"].includes(v)) return "herr";
  if (["frau", "mrs", "mrs.", "ms", "ms.", "f", "w", "female", "weiblich"].includes(v)) return "frau";
  return v === "" ? undefined : "";
}

function parseCsv(text) {
  const clean = text.replace(/^﻿/, "");
  const firstLine = clean.split(/\r?\n/, 1)[0] || "";
  const delim = (firstLine.match(/;/g) || []).length >= (firstLine.match(/,/g) || []).length ? ";" : ",";
  const rows = [];
  let row = [], cell = "", quoted = false;
  for (let i = 0; i < clean.length; i++) {
    const c = clean[i];
    if (quoted) {
      if (c === '"' && clean[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') quoted = false;
      else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === delim) { row.push(cell); cell = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && clean[i + 1] === "\n") i++;
      row.push(cell); cell = "";
      if (row.some((v) => v.trim())) rows.push(row);
      row = [];
    } else cell += c;
  }
  row.push(cell);
  if (row.some((v) => v.trim())) rows.push(row);
  if (rows.length < 2) return [];
  const head = rows[0].map((h) => h.trim().toLowerCase());
  const col = (names) => head.findIndex((h) => names.includes(h));
  const iFirst = col(["vorname", "first_name", "firstname", "first name", "given name"]);
  const iLast = col(["nachname", "last_name", "lastname", "last name", "surname", "family name"]);
  const iName = col(["name", "full name", "vollername"]);
  const iSal = col(["anrede", "salutation", "gender", "geschlecht"]);
  const iDate = col(["geburtsdatum", "geburtstag", "birthdate", "birthday", "bday", "date of birth"]);
  const iStyle = col(["stil", "style"]);
  const iGreet = col(["gratulation", "greeting"]);
  const iNotify = col(["gratulation_notify", "notify", "greeting_notify"]);
  const iR1 = col(["erinnerung_1", "reminder_1"]);
  const iR2 = col(["erinnerung_2", "reminder_2"]);
  if (iDate < 0) return [];
  const out = [];
  for (const r of rows.slice(1)) {
    const date = parseDate(r[iDate]);
    if (!date) continue;
    let first = iFirst >= 0 ? r[iFirst].trim() : "";
    let last = iLast >= 0 ? r[iLast].trim() : "";
    if (!first && iName >= 0) {
      const parts = r[iName].trim().split(/\s+/);
      last = parts.length > 1 ? parts.pop() : "";
      first = parts.join(" ");
    }
    if (!first) continue;
    const item = { first_name: first, last_name: last, ...date, salutation: iSal >= 0 ? normSalutation(r[iSal]) : undefined };
    if (iStyle >= 0 && ["personal", "formal"].includes(r[iStyle].trim())) item.style = r[iStyle].trim();
    if (iGreet >= 0 && iNotify >= 0 && /^(ja|yes|true|1)$/i.test(r[iGreet].trim()) && r[iNotify].trim()) {
      item.greeting_enabled = true;
      item.greeting_notify = r[iNotify].trim();
    }
    if (iR1 >= 0 && r[iR1].trim()) item.reminder_days_1 = Number(r[iR1]);
    if (iR2 >= 0 && r[iR2].trim()) item.reminder_days_2 = Number(r[iR2]);
    out.push(item);
  }
  return out;
}

function parseVcf(text) {
  const unfolded = text.replace(/\r?\n[ \t]/g, "");
  const out = [];
  for (const card of unfolded.split(/BEGIN:VCARD/i).slice(1)) {
    const lines = card.split(/\r?\n/);
    const get = (prefix) => {
      const line = lines.find((l) => new RegExp(`^${prefix}[;:]`, "i").test(l));
      return line ? line.slice(line.indexOf(":") + 1).trim() : "";
    };
    const bday = parseDate(get("BDAY"));
    if (!bday) continue;
    let first = "", last = "";
    const n = get("N");
    if (n) { const p = n.split(";"); last = (p[0] || "").trim(); first = (p[1] || "").trim(); }
    if (!first) {
      const fn = get("FN").split(/\s+/);
      last = fn.length > 1 ? fn.pop() : last;
      first = fn.join(" ");
    }
    if (!first) continue;
    out.push({ first_name: first, last_name: last, ...bday });
  }
  return out;
}

customElements.define("geburtstage-panel", GeburtstagePanel);

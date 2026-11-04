/* Geburtstage – Lovelace card (vanilla web component, no external dependencies) */

const CARD_VERSION = "0.1.0";

const DEFAULTS = {
  title: "",
  days: 30,
  max_items: 0,
  layout: "list",
  show_title: true,
  show_age: true,
  show_date: true,
  show_countdown: true,
  show_weekday: false,
  avatar: "initials",
  highlight_today: true,
  highlight_round: true,
  hide_when_empty: false,
  empty_text: "",
  date_format: "short",
  transparent: false,
};

const L10N = {
  de: {
    title: "Geburtstage",
    today: "Heute",
    tomorrow: "Morgen",
    in_days: "in {n} Tagen",
    turns: "wird {n}",
    turns_today: "wird heute {n}",
    empty: "Keine Geburtstage in den nächsten {n} Tagen.",
    no_entity: "Keine Geburtstags-Entity gefunden. Ist die Integration „Geburtstage“ eingerichtet?",
    // editor
    e_title: "Titel",
    e_entity: "Entity (Kommende Geburtstage)",
    e_days: "Zeitraum (nächste Tage)",
    e_max_items: "Maximale Anzahl (0 = alle)",
    e_layout: "Darstellung",
    e_layout_list: "Liste",
    e_layout_compact: "Kompakt",
    e_layout_chips: "Chips",
    e_show_title: "Titel anzeigen",
    e_show_age: "Alter anzeigen",
    e_show_date: "Datum anzeigen",
    e_show_countdown: "„in X Tagen“ anzeigen",
    e_show_weekday: "Wochentag anzeigen",
    e_avatar: "Symbol",
    e_avatar_initials: "Initialen",
    e_avatar_icon: "Torten-Symbol",
    e_avatar_none: "Keines",
    e_highlight_today: "Heutige hervorheben",
    e_highlight_round: "Runde Geburtstage hervorheben",
    e_hide_when_empty: "Karte ausblenden, wenn leer",
    e_empty_text: "Text bei leerer Liste",
    e_date_format: "Datumsformat",
    e_date_short: "Kurz (4. Nov.)",
    e_date_long: "Lang (4. November)",
    e_date_numeric: "Numerisch (04.11.)",
    e_transparent: "Ohne Kartenhintergrund",
    picker_name: "Geburtstage",
    picker_desc: "Zeigt die Geburtstage der nächsten Tage mit erreichtem Alter.",
  },
  en: {
    title: "Birthdays",
    today: "Today",
    tomorrow: "Tomorrow",
    in_days: "in {n} days",
    turns: "turns {n}",
    turns_today: "turns {n} today",
    empty: "No birthdays in the next {n} days.",
    no_entity: "No birthday entity found. Is the “Geburtstage” integration set up?",
    e_title: "Title",
    e_entity: "Entity (Upcoming birthdays)",
    e_days: "Time range (next days)",
    e_max_items: "Maximum entries (0 = all)",
    e_layout: "Layout",
    e_layout_list: "List",
    e_layout_compact: "Compact",
    e_layout_chips: "Chips",
    e_show_title: "Show title",
    e_show_age: "Show age",
    e_show_date: "Show date",
    e_show_countdown: "Show “in X days”",
    e_show_weekday: "Show weekday",
    e_avatar: "Symbol",
    e_avatar_initials: "Initials",
    e_avatar_icon: "Cake icon",
    e_avatar_none: "None",
    e_highlight_today: "Highlight today",
    e_highlight_round: "Highlight round birthdays",
    e_hide_when_empty: "Hide card when empty",
    e_empty_text: "Text when list is empty",
    e_date_format: "Date format",
    e_date_short: "Short (Nov 4)",
    e_date_long: "Long (November 4)",
    e_date_numeric: "Numeric (04/11)",
    e_transparent: "No card background",
    picker_name: "Birthdays",
    picker_desc: "Shows the birthdays of the next days with the age reached.",
  },
};

const lang = (hass) => ((hass && (hass.locale?.language || hass.language)) || "en").toLowerCase().startsWith("de") ? "de" : "en";
const tr = (hass, key, vars = {}) => {
  let text = (L10N[lang(hass)] || L10N.en)[key] ?? L10N.en[key] ?? key;
  for (const [k, v] of Object.entries(vars)) text = text.replaceAll(`{${k}}`, v);
  return text;
};
const esc = (value) =>
  String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

const CARD_STYLE = `
  :host { display: block; }
  ha-card { height: 100%; overflow: hidden; }
  ha-card.transparent { background: none; box-shadow: none; border: none; }
  .header { padding: 16px 16px 4px; font-size: var(--ha-card-header-font-size, 20px); font-weight: 500; line-height: 1.2; }
  .body { padding: 8px 12px 12px; }
  .header + .body { padding-top: 4px; }
  ha-card.transparent .body, ha-card.transparent .header { padding-left: 0; padding-right: 0; }
  .item { display: flex; align-items: center; gap: 12px; padding: 8px 4px; border-radius: 10px; }
  .item + .item { border-top: 1px solid var(--divider-color); }
  .item.today.hl { background: color-mix(in srgb, var(--primary-color) 14%, transparent); border-top-color: transparent; padding-left: 8px; padding-right: 8px; }
  .item.today.hl + .item { border-top-color: transparent; }
  .avatar { flex: none; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: color-mix(in srgb, var(--primary-color) 18%, transparent); color: var(--primary-color); font-weight: 600; font-size: 15px; --mdc-icon-size: 22px; }
  .today.hl .avatar { background: var(--primary-color); color: var(--text-primary-color, #fff); }
  .round.hl .avatar { box-shadow: 0 0 0 2px var(--warning-color, #ffa600); }
  .main { flex: 1; min-width: 0; }
  .name { font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .sub { font-size: 13px; color: var(--secondary-text-color); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .when { flex: none; text-align: right; font-size: 14px; color: var(--secondary-text-color); }
  .today .when { color: var(--primary-color); font-weight: 600; }
  .star { color: var(--warning-color, #ffa600); --mdc-icon-size: 16px; vertical-align: -3px; }
  /* compact */
  .compact .item { padding: 4px 4px; gap: 8px; }
  .compact .avatar { width: 28px; height: 28px; font-size: 12px; --mdc-icon-size: 16px; }
  .compact .main { display: flex; gap: 8px; align-items: baseline; min-width: 0; }
  .compact .name { flex: 0 0 auto; max-width: 65%; }
  .compact .sub { flex: 1 1 0; min-width: 0; }
  .compact .sub { font-size: 12px; }
  /* chips */
  .chips { display: flex; flex-wrap: wrap; gap: 8px; }
  .chip { display: inline-flex; align-items: center; gap: 8px; padding: 4px 12px 4px 4px; border-radius: 999px; background: var(--secondary-background-color); font-size: 14px; max-width: 100%; }
  .chip.hl.today { background: var(--primary-color); color: var(--text-primary-color, #fff); }
  .chip.hl.today .sub, .chip.hl.today .when { color: inherit; }
  .chip .avatar { width: 28px; height: 28px; font-size: 12px; --mdc-icon-size: 16px; }
  .chip .name { font-size: 14px; }
  .chip .sub { font-size: 11px; }
  .chip.hl.round { box-shadow: 0 0 0 2px var(--warning-color, #ffa600); }
  .empty, .msg { padding: 16px; text-align: center; color: var(--secondary-text-color); }
`;

class GeburtstageCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = null;
    this._hass = null;
    this._sig = "";
  }

  static getConfigElement() {
    return document.createElement("geburtstage-card-editor");
  }

  static getStubConfig(hass) {
    return { type: "custom:geburtstage-card", entity: GeburtstageCard._findEntity(hass), days: 30 };
  }

  static _findEntity(hass) {
    if (!hass) return "";
    const ids = Object.keys(hass.states).filter((id) => id.startsWith("sensor.") && Array.isArray(hass.states[id].attributes?.birthdays) && "window_days" in hass.states[id].attributes);
    return ids[0] || "";
  }

  setConfig(config) {
    if (!config || typeof config !== "object") throw new Error("Invalid configuration");
    this._config = { ...DEFAULTS, ...config };
    this._sig = "";
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    const n = this._lastCount ?? 3;
    return this._config?.layout === "chips" ? 2 : Math.max(2, 1 + Math.ceil(n * (this._config?.layout === "compact" ? 0.5 : 0.9)));
  }

  getGridOptions() {
    return { columns: 12, rows: "auto", min_columns: 3, min_rows: 1 };
  }

  _inEditor() {
    let node = this;
    while (node) {
      if (node.nodeName === "HUI-CARD-PREVIEW" || node.nodeName === "HUI-CARD-EDITOR") return true;
      node = node.parentNode || node.host;
    }
    return false;
  }

  _items() {
    const c = this._config;
    const entityId = c.entity || GeburtstageCard._findEntity(this._hass);
    const state = this._hass?.states?.[entityId];
    if (!state) return null;
    let list = (state.attributes.birthdays || []).filter((p) => p.days_until <= Number(c.days));
    if (Number(c.max_items) > 0) list = list.slice(0, Number(c.max_items));
    return list;
  }

  _dateText(p) {
    const c = this._config;
    const locale = this._hass.locale?.language || this._hass.language || "en";
    const year = new Date(`${p.next_date}T12:00:00`);
    const opts = { numeric: { day: "2-digit", month: "2-digit" }, short: { day: "numeric", month: "short" }, long: { day: "numeric", month: "long" } }[c.date_format] || { day: "numeric", month: "short" };
    if (c.show_weekday) opts.weekday = "short";
    return new Intl.DateTimeFormat(locale, opts).format(year);
  }

  _whenText(p) {
    if (p.days_until === 0) return tr(this._hass, "today");
    if (p.days_until === 1) return tr(this._hass, "tomorrow");
    return tr(this._hass, "in_days", { n: p.days_until });
  }

  _avatar(p) {
    const mode = this._config.avatar;
    if (mode === "none") return "";
    if (mode === "icon") return `<div class="avatar"><ha-icon icon="${p.is_today ? "mdi:party-popper" : "mdi:cake-variant"}"></ha-icon></div>`;
    const initials = `${(p.first_name || "?")[0] || ""}${(p.last_name || "")[0] || ""}`.toUpperCase();
    return `<div class="avatar">${esc(initials)}</div>`;
  }

  _subText(p) {
    const c = this._config;
    const parts = [];
    if (c.show_date) parts.push(this._dateText(p));
    if (c.show_age && p.turning_age != null) {
      parts.push(tr(this._hass, p.days_until === 0 ? "turns_today" : "turns", { n: p.turning_age }));
    }
    return parts.join(" · ");
  }

  _render() {
    if (!this._config || !this._hass) return;
    const c = this._config;
    const items = this._items();
    const sig = JSON.stringify([c, items, lang(this._hass)]);
    if (sig === this._sig) return;
    this._sig = sig;
    this._lastCount = items ? items.length : 0;

    const hidden = c.hide_when_empty && items && !items.length && !this._inEditor();
    this.style.display = hidden ? "none" : "";
    if (hidden) return;

    const title = c.title || tr(this._hass, "title");
    const head = c.show_title && title ? `<div class="header">${esc(title)}</div>` : "";
    let body;
    if (items === null) {
      body = `<div class="msg">${esc(tr(this._hass, "no_entity"))}</div>`;
    } else if (!items.length) {
      body = `<div class="empty">${esc(c.empty_text || tr(this._hass, "empty", { n: c.days }))}</div>`;
    } else if (c.layout === "chips") {
      body = `<div class="chips">${items.map((p) => this._chip(p)).join("")}</div>`;
    } else {
      body = `<div class="${c.layout === "compact" ? "compact" : ""}">${items.map((p) => this._row(p)).join("")}</div>`;
    }
    this.shadowRoot.innerHTML = `<style>${CARD_STYLE}</style><ha-card class="${c.transparent ? "transparent" : ""}">${head}<div class="body">${body}</div></ha-card>`;
  }

  _row(p) {
    const c = this._config;
    const cls = `item ${p.is_today && c.highlight_today ? "today hl" : ""} ${p.is_round && c.highlight_round ? "round hl" : ""}`;
    const star = p.is_round && c.highlight_round ? ` <ha-icon class="star" icon="mdi:star-circle"></ha-icon>` : "";
    const sub = this._subText(p);
    const compact = c.layout === "compact";
    const main = compact
      ? `<div class="main"><span class="name">${esc(p.name)}${star}</span>${sub ? `<span class="sub">${esc(sub)}</span>` : ""}</div>`
      : `<div class="main"><div class="name">${esc(p.name)}${star}</div>${sub ? `<div class="sub">${esc(sub)}</div>` : ""}</div>`;
    const when = c.show_countdown ? `<div class="when">${esc(this._whenText(p))}</div>` : "";
    return `<div class="${cls}">${this._avatar(p)}${main}${when}</div>`;
  }

  _chip(p) {
    const c = this._config;
    const cls = `chip ${p.is_today && c.highlight_today ? "today hl" : ""} ${p.is_round && c.highlight_round ? "round hl" : ""}`;
    const sub = [c.show_countdown ? this._whenText(p) : "", c.show_age && p.turning_age != null ? String(p.turning_age) : "", c.show_date ? this._dateText(p) : ""].filter(Boolean).join(" · ");
    return `<span class="${cls}">${this._avatar(p)}<span><div class="name">${esc(p.name)}</div>${sub ? `<div class="sub">${esc(sub)}</div>` : ""}</span></span>`;
  }
}

class GeburtstageCardEditor extends HTMLElement {
  setConfig(config) {
    this._raw = { ...config };
    this._config = { ...DEFAULTS, ...config };
    this._update();
  }

  set hass(hass) {
    this._hass = hass;
    this._update();
  }

  _schema() {
    const h = this._hass;
    const sel = (key, values) => ({ select: { mode: "dropdown", options: values.map((v) => ({ value: v, label: tr(h, `${key}_${v}`) })) } });
    return [
      { name: "title", selector: { text: {} } },
      { name: "entity", selector: { entity: { filter: [{ integration: "geburtstage", domain: "sensor" }] } } },
      {
        type: "grid",
        name: "",
        schema: [
          { name: "days", selector: { number: { min: 1, max: 366, mode: "box" } } },
          { name: "max_items", selector: { number: { min: 0, max: 100, mode: "box" } } },
        ],
      },
      {
        type: "grid",
        name: "",
        schema: [
          { name: "layout", required: true, selector: sel("e_layout", ["list", "compact", "chips"]) },
          { name: "avatar", required: true, selector: sel("e_avatar", ["initials", "icon", "none"]) },
          { name: "date_format", required: true, selector: sel("e_date", ["short", "long", "numeric"]) },
        ],
      },
      {
        type: "grid",
        name: "",
        schema: [
          { name: "show_title", selector: { boolean: {} } },
          { name: "show_age", selector: { boolean: {} } },
          { name: "show_date", selector: { boolean: {} } },
          { name: "show_countdown", selector: { boolean: {} } },
          { name: "show_weekday", selector: { boolean: {} } },
          { name: "highlight_today", selector: { boolean: {} } },
          { name: "highlight_round", selector: { boolean: {} } },
          { name: "hide_when_empty", selector: { boolean: {} } },
          { name: "transparent", selector: { boolean: {} } },
        ],
      },
      { name: "empty_text", selector: { text: {} } },
    ];
  }

  _update() {
    if (!this._config || !this._hass) return;
    if (!this._form) {
      this._form = document.createElement("ha-form");
      this._form.computeLabel = (schema) => tr(this._hass, `e_${schema.name}`);
      this._form.addEventListener("value-changed", (ev) => {
        ev.stopPropagation();
        const config = {};
        for (const [key, value] of Object.entries(ev.detail.value)) {
          if (key in DEFAULTS && DEFAULTS[key] === value && !(this._raw && key in this._raw)) continue;
          if (value === "" || value === undefined) continue;
          config[key] = value;
        }
        this._raw = config;
        this._config = { ...DEFAULTS, ...config };
        this.dispatchEvent(new CustomEvent("config-changed", { detail: { config }, bubbles: true, composed: true }));
      });
      this.appendChild(this._form);
    }
    this._form.hass = this._hass;
    this._form.data = this._config;
    this._form.schema = this._schema();
  }
}

// Home Assistant imports extra modules in parallel to its own core. Defining the elements
// before the frontend has installed its custom element registry makes them invisible to
// the dashboard ("Custom element doesn't exist"). So wait until the frontend is up.
const register = () => {
  if (!customElements.get("geburtstage-card")) customElements.define("geburtstage-card", GeburtstageCard);
  if (!customElements.get("geburtstage-card-editor")) customElements.define("geburtstage-card-editor", GeburtstageCardEditor);
};
if (customElements.get("home-assistant")) register();
else customElements.whenDefined("home-assistant").then(register);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "geburtstage-card",
  name: "Geburtstage",
  preview: false,
  description: "Zeigt die Geburtstage der nächsten Tage mit erreichtem Alter / Upcoming birthdays with the age reached.",
  documentationURL: "https://github.com/Ceddy1906/geburtstage",
});

console.info(`%c GEBURTSTAGE-CARD %c ${CARD_VERSION} `, "color:white;background:#e91e63;font-weight:700", "color:#e91e63;background:white;font-weight:700");

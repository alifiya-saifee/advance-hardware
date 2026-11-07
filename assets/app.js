// Advance Hardware website: shared behaviour for every page.
// Business details live here, in one place.
const SITE = {
  name: "Advance Hardware LLC",
  founded: 1996,
  whatsapp: "971506789646", // number that receives WhatsApp messages (no + or spaces)
  phones: [
    { key: "ph_shop", label: "06 543 1678", tel: "+97165431678" },
    { key: "ph_mobile", label: "050 678 9646", tel: "+971506789646" },
    { key: "ph_sales", label: "055 214 4351", tel: "+971552144351" },
  ],
  callTel: "+971506789646", // the "Call" buttons
  mapQuery: "Advance Hardware LLC, Industrial Area 2, Sharjah",
  geo: { lat: 25.3197832, lng: 55.4054299 },          // the shop's pin on Google Maps
  googleUrl: "https://maps.google.com/?cid=1551431354454962109", // the Google Business Profile (reviews, photos)
  // Opening hours come from data/hours.json (via assets/hours.js, made by tools/build_pages.py). Never edit them here.
  hours: Object.assign({ default: (window.HOURS || {}).default || [] }, (window.HOURS || {}).days || {}),
  // Hero video: set to { mp4: "media/hero.mp4", webm: "media/hero.webm", mobile: "media/hero-720.mp4" }
  // once the real video exists. Until then the hero photo shows.
  heroVideo: null,
};

// Category → card image, used for the product rows.
const CAT_IMAGE = {
  "bolts": "bolts", "high-tensile-bolts": "high-tensile", "screws": "screws", "nuts": "nuts", "washers": "washers",
  "threaded-bar": "threaded-bar", "gloves-and-safety": "gloves", "anchors-and-fixings": "anchors-tools", "tools-and-accessories": "anchors-tools",
};
// Home-page cards that add a whole category to the list.
const CAT_NAMES = {
  "high-tensile-bolts": "cat_hightensile", "bolts": "cat_bolts", "nuts": "cat_nuts", "washers": "cat_washers", "screws": "cat_screws",
  "threaded-bar": "cat_rod", "anchors-and-fixings": "cat_anchors", "gloves-and-safety": "cat_gloves",
};

const LIST_KEY = "ah-list";
const LANG_KEY = "ah-lang";
const REDUCED = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const SAVE_DATA = navigator.connection && navigator.connection.saveData;

// Browser storage can be blocked (private mode); the site must still work.
function storeGet(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
function storeSet(key, val) { try { localStorage.setItem(key, val); } catch (e) { /* ignore */ } }

const urlLang = new URLSearchParams(location.search).get("lang"); // ?lang=ar opens the Arabic version
let lang = (urlLang || storeGet(LANG_KEY)) === "ar" ? "ar" : "en";
const t = (key) => (I18N[lang] && I18N[lang][key]) || I18N.en[key] || key;
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
// Where the visitor came from: links like ?src=google, ?src=qr, ?src=instagram (kept for the visit).
const SRC_NAMES = { google: "Google profile", gbp: "Google profile", maps: "Google Maps", qr: "QR code", instagram: "Instagram", ig: "Instagram",
  facebook: "Facebook", fb: "Facebook", tiktok: "TikTok", status: "WhatsApp status", card: "Business card", flyer: "Flyer" };
function sessGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
function sessSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) { /* ignore */ } }
const urlSrc = (new URLSearchParams(location.search).get("src") || "").toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 30);
if (urlSrc) sessSet("ah-src", urlSrc);
const ARRIVAL = urlSrc || sessGet("ah-src") || "";
// Every WhatsApp message ends with e.g. "Ref: website/home/hero · via QR code" so the shop can see what brought the enquiry.
const refLine = (place) => `Ref: website/${document.body.dataset.page || "site"}/${place || "link"}${ARRIVAL ? ` · via ${SRC_NAMES[ARRIVAL] || ARRIVAL}` : ""}`;
const waLink = (text, place) => `https://wa.me/${SITE.whatsapp}?text=${encodeURIComponent(`${text}\n\n${refLine(place)}`)}`;
const mapLink = () => `https://www.google.com/maps/dir/?api=1&destination=${SITE.geo.lat},${SITE.geo.lng}`;

/* ---------- icons ---------- */
const ICONS = {
  bolt: '<path d="M14 6h20l5 8-5 8H14l-5-8z"/><path d="M19 22v20h10V22"/><path d="M19 27h10M19 32h10M19 37h10"/>',
  screw: '<path d="M10 8h28l-4 6H14z"/><path d="M18 14v18l6 10 6-10V14"/><path d="M18 19l12 3M18 25l12 3"/>',
  nut: '<path d="M14 7h20l10 17-10 17H14L4 24z"/><circle cx="24" cy="24" r="8"/>',
  washer: '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="7"/>',
  rod: '<rect x="6" y="19" width="36" height="10" rx="2"/><path d="M11 19v10M16 19v10M21 19v10M26 19v10M31 19v10M36 19v10"/>',
  tools: '<path d="M30 6a9 9 0 0 0-8 12L7 33a4 4 0 0 0 6 6l15-15a9 9 0 0 0 12-8l-6 2-4-4z"/>',
  glove: '<path d="M14 44V24l-4-8a3 3 0 0 1 5-3l4 7V8a3 3 0 0 1 6 0v12V6a3 3 0 0 1 6 0v14V9a3 3 0 0 1 6 0v19c0 9-5 16-11 16z"/>',
  anchor: '<path d="M24 4v30"/><path d="M18 4h12"/><path d="M17 34l7 10 7-10z"/><path d="M19 12h10M19 18h10M19 24h10"/>',
  tape: '<circle cx="20" cy="22" r="14"/><circle cx="20" cy="22" r="6"/><path d="M34 22v16H20"/>',
  wa: '<path d="M24 5a19 19 0 0 0-16.4 28.6L5 43l9.7-2.5A19 19 0 1 0 24 5z"/><path d="M17 15c-1 0-2.5 1.2-2.5 3.6 0 3.6 4.7 9.8 11.3 12.4 3.3 1.3 5.5.6 6.3-1.4l.4-1.9-4.5-2.2-1.9 2.2c-2.4-1-4.7-3.1-5.8-5.4l1.9-2-1.8-4.6z"/>',
  list: '<path d="M16 12h24M16 24h24M16 36h24"/><circle cx="9" cy="12" r="2"/><circle cx="9" cy="24" r="2"/><circle cx="9" cy="36" r="2"/>',
  plus: '<path d="M24 10v28M10 24h28"/>',
  menu: '<path d="M8 14h32M8 24h32M8 34h32"/>',
  close: '<path d="M12 12l24 24M36 12L12 36"/>',
  star: '<path d="M24 5l5.9 12 13.1 1.9-9.5 9.3 2.2 13.1L24 35.1l-11.7 6.2 2.2-13.1L5 18.9 18.1 17z"/>',
  arrow: '<path d="M10 24h28M28 14l10 10-10 10"/>',
  chev: '<path d="M12 18l12 12 12-12"/>',
  truck: '<path d="M4 12h24v20H4zM28 19h9l7 7v6H28z"/><circle cx="13" cy="36" r="4"/><circle cx="36" cy="36" r="4"/>',
  card: '<rect x="5" y="11" width="38" height="26" rx="3"/><path d="M5 19h38M11 30h8"/>',
  globe: '<circle cx="24" cy="24" r="19"/><path d="M5 24h38M24 5c6 6 6 32 0 38M24 5c-6 6-6 32 0 38"/>',
  clock: '<circle cx="24" cy="24" r="18"/><path d="M24 13v11l7 5"/>',
  pin: '<path d="M24 44s14-13 14-24a14 14 0 0 0-28 0c0 11 14 24 14 24z"/><circle cx="24" cy="20" r="5"/>',
  phone: '<path d="M14 6l6 9-4 4a24 24 0 0 0 13 13l4-4 9 6-3 7C21 41 7 27 7 9z"/>',
  camera: '<rect x="5" y="13" width="38" height="27" rx="4"/><circle cx="24" cy="26" r="7"/><path d="M17 13l3-5h8l3 5"/>',
  copy: '<rect x="15" y="15" width="25" height="25" rx="3"/><path d="M33 15V9a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v22a2 2 0 0 0 2 2h6"/>',
  shop: '<path d="M6 18l3-10h30l3 10"/><path d="M6 18h36v4a6 6 0 0 1-12 0 6 6 0 0 1-12 0 6 6 0 0 1-12 0z"/><path d="M9 26v16h30V26"/><path d="M20 42V32h8v10"/>',
};
const MARK = '<svg viewBox="0 0 100 100" aria-hidden="true"><polygon points="50.00,4.00 89.84,27.00 89.84,73.00 50.00,96.00 10.16,73.00 10.16,27.00" fill="#F2A900"/><circle cx="50" cy="50" r="31.00" fill="none" stroke="#111315" stroke-width="4.20"/><g stroke="#111315" stroke-width="7.00" stroke-linecap="round"><line x1="50.00" y1="40.00" x2="50.00" y2="27.00"/><line x1="58.66" y1="55.00" x2="69.92" y2="61.50"/><line x1="41.34" y1="55.00" x2="30.08" y2="61.50"/></g></svg>';
const icon = (name, cls = "icon") =>
  `<svg class="${cls}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ICONS.bolt}</svg>`;

// <i data-icon="name" data-cls="extra classes"></i> in the pages becomes an SVG icon.
function renderIcons(root = document) {
  root.querySelectorAll("i[data-icon]").forEach((el) => {
    const flip = el.dataset.icon === "arrow" ? " flip" : "";
    el.outerHTML = icon(el.dataset.icon, `icon ${el.dataset.cls || ""}${flip}`.trim());
  });
}

/* ---------- opening hours (one source for badge, table and footer) ---------- */
const DAY_INDEX = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
function dubaiNow() {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Dubai", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23",
  }).formatToParts(new Date());
  const get = (type) => parts.find((p) => p.type === type).value;
  return { day: DAY_INDEX[get("weekday")], mins: Number(get("hour")) * 60 + Number(get("minute")) };
}
const toMin = (hhmm) => { const [h, m] = hhmm.split(":").map(Number); return h * 60 + m; };
const fmtTime = (hhmm) => hhmm.replace(/^0/, "");
const rangesFor = (day) => (day in SITE.hours ? SITE.hours[day] : SITE.hours.default);
const hoursText = (day, sep = ` ${t("and")} `) => {
  const r = rangesFor(day);
  return r.length ? r.map(([a, b]) => `${fmtTime(a)}–${fmtTime(b)}`).join(sep) : t("closed");
};
function openState() {
  const { day, mins } = dubaiNow();
  const cur = rangesFor(day).find(([a, b]) => mins >= toMin(a) && mins < toMin(b));
  if (cur) return { open: true, text: `${t("open_now")} · ${t("until")} ${fmtTime(cur[1])}` };
  const later = rangesFor(day).find(([a]) => toMin(a) > mins);
  if (later) return { open: false, text: `${t("closed_now")} · ${t("opens")} ${fmtTime(later[0])}` };
  for (let i = 1; i <= 7; i++) {
    const d = (day + i) % 7, r = rangesFor(d);
    if (r.length) return { open: false, text: `${t("closed_now")} · ${t("opens")} ${i === 1 ? t("tomorrow") : t("day_" + d)} ${fmtTime(r[0][0])}` };
  }
  return { open: false, text: t("closed_now") };
}
function compactHours() {
  // group days that share the same hours, in shop-week order (Sat → Fri)
  const order = [6, 0, 1, 2, 3, 4, 5];
  const groups = [];
  order.forEach((d) => {
    const key = JSON.stringify(rangesFor(d));
    const last = groups[groups.length - 1];
    if (last && last.key === key) last.days.push(d); else groups.push({ key, days: [d] });
  });
  return groups.map((g) => {
    const label = g.days.length > 1 ? `${t("dshort_" + g.days[0])}–${t("dshort_" + g.days[g.days.length - 1])}` : t("dshort_" + g.days[0]);
    return `${label} ${hoursText(g.days[0], ", ")}`;
  });
}

/* ---------- header, footer, menu, list ---------- */
const NAV = [
  ["products", "products.html", "nav_products"],
  ["trade", "trade.html", "nav_trade"],
  ["about", "about.html", "nav_about"],
  ["contact", "contact.html", "nav_contact"],
];

function renderChrome() {
  renderIcons();
  const page = document.body.dataset.page;
  const links = NAV.map(([key, href, label]) => {
    const cur = key === page ? 'aria-current="page"' : "";
    return key === "trade"
      ? `<a href="${href}" ${cur}><span class="nav-long" data-i18n="${label}"></span><span class="nav-short" data-i18n="nav_trade_short"></span></a>`
      : `<a href="${href}" data-i18n="${label}" ${cur}></a>`;
  }).join("");
  const header = document.getElementById("site-header");
  header.innerHTML = `
    <div class="wrap header-row">
      <a class="logo" href="index.html">
        <span class="logo-mark">${MARK}</span>
        <span class="logo-words"><span class="logo-text" data-i18n="brand"></span><span class="logo-tag" data-i18n="tagline"></span></span>
      </a>
      <nav class="nav" aria-label="Main">${links}</nav>
      <div class="header-actions">
        <a class="header-phone" href="tel:${SITE.callTel}" dir="ltr">${icon("phone")}${SITE.phones[1].label}</a>
        <button class="lang-btn" type="button" data-i18n="lang_switch"></button>
        <a class="btn btn-wa btn-sm wa-list-link" data-src="header" href="#" target="_blank" rel="noopener" aria-label="WhatsApp">${icon("wa")}<span class="hide-sm" data-i18n="wa_short"></span></a>
        <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu">${icon("menu")}<span class="sr-only" data-i18n="menu_open"></span></button>
      </div>
    </div>`;

  const menu = document.createElement("div");
  menu.id = "mobile-menu";
  menu.className = "mobile-menu";
  menu.hidden = true;
  menu.setAttribute("role", "dialog");
  menu.setAttribute("aria-modal", "true");
  menu.innerHTML = `
    <div class="mobile-menu-head">
      <span class="logo-text" data-i18n="brand"></span>
      <button class="menu-close" type="button">${icon("close")}<span class="sr-only" data-i18n="menu_close"></span></button>
    </div>
    <nav class="mobile-nav" aria-label="Main">
      <a href="index.html" data-i18n="nav_home" ${page === "home" ? 'aria-current="page"' : ""}></a>${links}
    </nav>
    <div class="mobile-menu-actions">
      <a class="btn btn-wa btn-block wa-list-link" data-src="menu" href="#" target="_blank" rel="noopener">${icon("wa")}<span data-i18n="cta_send_list"></span></a>
      <a class="btn btn-secondary btn-block" style="color:#fff" href="tel:${SITE.callTel}">${icon("phone")}<span data-i18n="call"></span> <span dir="ltr">${SITE.phones[1].label}</span></a>
      <button class="btn btn-secondary btn-block lang-btn" style="color:#fff" type="button" data-i18n="lang_switch"></button>
    </div>`;
  document.body.appendChild(menu);

  document.querySelectorAll(".lang-btn").forEach((b) => b.addEventListener("click", () => setLang(lang === "en" ? "ar" : "en")));
  header.querySelector(".menu-btn").addEventListener("click", openMenu);
  menu.querySelector(".menu-close").addEventListener("click", closeMenu);
  menu.addEventListener("keydown", (e) => trapFocus(e, menu));

  const year = new Date().getFullYear();
  document.getElementById("site-footer").innerHTML = `
    <div class="wrap footer-grid">
      <div class="footer-brand">
        <a class="footer-seal" href="index.html"><picture><source type="image/webp" srcset="media/brand/seal-240.webp 1x, media/brand/seal-480.webp 2x"><img src="media/brand/seal-240.png" srcset="media/brand/seal-480.png 2x" width="112" height="112" alt="Advance Hardware, Sharjah, since 1996" loading="lazy"></picture></a>
        <p><strong data-i18n="brand_full"></strong></p>
        <p data-i18n="contact_address"></p>
      </div>
      <div>
        <h2 class="footer-h" data-i18n="contact_phone_t"></h2>
        ${SITE.phones.map((p) => `<p class="footer-phone"><span class="lbl" data-i18n="${p.key}"></span> <a href="tel:${p.tel}" dir="ltr" class="mono">${p.label}</a></p>`).join("")}
        <p><a class="wa-list-link" data-src="footer" href="#" target="_blank" rel="noopener" data-i18n="wa_short"></a></p>
      </div>
      <div>
        <h2 class="footer-h" data-i18n="contact_hours_t"></h2>
        <div class="footer-hours"></div>
      </div>
      <div>
        <h2 class="footer-h" data-i18n="footer_pages"></h2>
        <p><a href="index.html" data-i18n="nav_home"></a></p>
        ${NAV.map(([, href, label]) => `<p><a href="${href}" data-i18n="${label}"></a></p>`).join("")}
      </div>
    </div>
    <div class="wrap footer-bottom">
      <span>© ${SITE.founded}–${year} ${SITE.name} · Sharjah, UAE <a class="credits-link" href="credits.html" data-i18n="footer_credits"></a></span>
    </div>`;

  const extras = document.createElement("div");
  extras.innerHTML = `
    <button class="list-fab" type="button" aria-haspopup="dialog">${icon("list")}<span data-i18n="list_btn"></span><b class="list-count">0</b></button>
    <nav class="action-bar" aria-label="Quick actions">
      <a class="bar-wa wa-list-link" data-src="mobile-bar" href="#" target="_blank" rel="noopener">${icon("wa")}<span data-i18n="wa_short"></span></a>
      <a href="tel:${SITE.callTel}">${icon("phone")}<span data-i18n="call"></span></a>
      <button class="bar-list" type="button" aria-haspopup="dialog">${icon("list")}<span data-i18n="list_btn"></span><b class="list-count">0</b></button>
    </nav>
    <div class="drawer-backdrop" hidden></div>
    <aside class="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title" hidden>
      <div class="drawer-head">
        <h2 id="drawer-title" data-i18n="list_title"></h2>
        <button class="btn-text drawer-close" type="button" data-i18n="list_close"></button>
      </div>
      <div class="drawer-body"></div>
    </aside>
    <div class="toast" role="status" aria-live="polite"></div>`;
  document.body.appendChild(extras);
  extras.querySelectorAll(".list-fab, .bar-list").forEach((b) => b.addEventListener("click", openDrawer));
  extras.querySelector(".drawer-close").addEventListener("click", closeDrawer);
  extras.querySelector(".drawer-backdrop").addEventListener("click", closeDrawer);
  extras.querySelector(".drawer").addEventListener("keydown", (e) => trapFocus(e, extras.querySelector(".drawer")));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { closeDrawer(); closeMenu(); } });
}

function trapFocus(e, box) {
  if (e.key !== "Tab") return;
  const items = [...box.querySelectorAll("a[href], button, input, select, textarea")].filter((el) => el.offsetParent !== null);
  if (!items.length) return;
  const first = items[0], last = items[items.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
}

let menuReturn = null;
function openMenu() {
  menuReturn = document.activeElement;
  const m = document.getElementById("mobile-menu");
  m.hidden = false;
  document.querySelector(".menu-btn").setAttribute("aria-expanded", "true");
  document.body.classList.add("no-scroll");
  m.querySelector(".menu-close").focus();
}
function closeMenu() {
  const m = document.getElementById("mobile-menu");
  if (!m || m.hidden) return;
  m.hidden = true;
  document.querySelector(".menu-btn").setAttribute("aria-expanded", "false");
  document.body.classList.remove("no-scroll");
  if (menuReturn) menuReturn.focus();
}

function setLang(next) {
  lang = next;
  storeSet(LANG_KEY, lang);
  applyLang();
}

function applyLang() {
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  document.querySelectorAll("[data-i18n]").forEach((el) => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => { el.placeholder = t(el.dataset.i18nPh); });
  document.querySelectorAll("[data-i18n-alt]").forEach((el) => { el.alt = t(el.dataset.i18nAlt); });
  document.querySelectorAll("[data-i18n-label]").forEach((el) => { el.setAttribute("aria-label", t(el.dataset.i18nLabel)); });
  const title = document.body.dataset.title;
  if (title) document.title = `${t(title)} | ${t("brand")}`;
  document.querySelectorAll(".wa-list-link").forEach((a) => { a.href = waLink(t("wa_simple"), a.dataset.src); });
  document.querySelectorAll(".wa-photo-link").forEach((a) => { a.href = waLink(t("wa_photo"), a.dataset.src); });
  document.querySelectorAll(".google-link").forEach((a) => { a.href = SITE.googleUrl; });
  document.querySelectorAll(".call-link").forEach((a) => { a.href = `tel:${SITE.callTel}`; });
  updateHours();
  renderPhones();
  renderList();
  document.dispatchEvent(new Event("langchange"));
}

function updateHours() {
  const { day } = dubaiNow();
  document.querySelectorAll(".hours-week").forEach((tb) => {
    tb.innerHTML = [1, 2, 3, 4, 5, 6, 0].map((d) =>
      `<tr class="${d === day ? "is-today" : ""}"><td>${esc(t("day_" + d))}</td><td class="mono" dir="ltr">${esc(hoursText(d, " · "))}</td></tr>`).join("");
  });
  document.querySelectorAll(".footer-hours").forEach((el) => { el.innerHTML = compactHours().map((l) => `<p class="mono">${esc(l)}</p>`).join(""); });
  const st = openState();
  document.querySelectorAll(".open-status").forEach((el) => {
    el.innerHTML = `<span class="dot"></span>${esc(st.text)}`;
    el.classList.toggle("is-open", st.open);
  });
}

function renderPhones() {
  document.querySelectorAll(".phone-list").forEach((box) => {
    box.innerHTML = SITE.phones.map((p) => `<a class="phone-row" href="tel:${p.tel}"><span class="lbl">${esc(t(p.key))}</span><span class="mono" dir="ltr">${p.label}</span></a>`).join("");
  });
}

/* ---------- quote list ---------- */
function getList() {
  try { const v = JSON.parse(storeGet(LIST_KEY) || "[]"); return Array.isArray(v) ? v : []; } catch (e) { return []; }
}
let memoryList = getList();
function saveList(list) { memoryList = list; storeSet(LIST_KEY, JSON.stringify(list)); renderList(); }

function addToList(item, fromEl) {
  const list = memoryList.slice();
  const same = list.find((x) => x.id === item.id && x.size === item.size && x.opt === item.opt && (x.grade || "") === (item.grade || ""));
  if (same) same.qty += item.qty; else list.push(item);
  saveList(list);
  toast(t("prod_added"));
  flyToList(fromEl);
}

function flyToList(fromEl) {
  const targets = [...document.querySelectorAll(".list-fab, .bar-list")].filter((el) => el.offsetParent !== null);
  const target = targets[0];
  if (!target) return;
  target.querySelectorAll(".list-count").forEach((c) => { c.classList.remove("bump"); void c.offsetWidth; c.classList.add("bump"); });
  if (REDUCED || !fromEl) return;
  const a = fromEl.getBoundingClientRect(), b = target.getBoundingClientRect();
  const dot = document.createElement("span");
  dot.className = "fly"; dot.textContent = "+1";
  dot.style.left = `${a.left + a.width / 2 - 16}px`; dot.style.top = `${a.top + a.height / 2 - 14}px`;
  document.body.appendChild(dot);
  requestAnimationFrame(() => {
    dot.style.transform = `translate(${b.left + b.width / 2 - (a.left + a.width / 2)}px, ${b.top + b.height / 2 - (a.top + a.height / 2)}px) scale(.6)`;
    dot.style.opacity = "0.2";
  });
  setTimeout(() => dot.remove(), 650);
}

function lineName(x) {
  if (x.id && x.id.startsWith("cat:")) {
    const key = CAT_NAMES[x.id.slice(4)];
    return `${key ? t(key) : x.name} (${t("list_cat_note")})`;
  }
  const p = (window.PRODUCTS || []).find((q) => q.id === x.id);
  const name = p ? p[lang] : x.name;
  const opt = p && x.opt !== "" && x.opt != null ? (p.options[x.opt] || {})[lang] : "";
  const grade = x.grade ? `${t("prod_grade")} ${x.grade}` : "";
  return [name, x.size, grade, opt].filter(Boolean).join(" · ");
}

function renderList() {
  const count = memoryList.length;
  document.querySelectorAll(".list-count").forEach((el) => { el.textContent = count; });
  document.querySelectorAll(".list-fab, .bar-list").forEach((el) => el.classList.toggle("has-items", count > 0));
  const body = document.querySelector(".drawer-body");
  if (!body) return;
  if (!memoryList.length) {
    body.innerHTML = `<p class="muted">${esc(t("list_empty"))}</p>
      <a class="btn btn-secondary" href="products.html">${esc(t("list_go_products"))}</a>`;
    return;
  }
  const note = body.querySelector("textarea")?.value || "";
  body.innerHTML = `
    <ul class="list-items">
      ${memoryList.map((x, i) => `
        <li>
          <span class="li-name">${esc(lineName(x))}</span>
          <span class="stepper">
            <button type="button" class="li-minus" data-i="${i}" aria-label="${esc(t("qty_minus"))}">−</button>
            <input class="li-qty" type="number" min="1" inputmode="numeric" value="${x.qty}" data-i="${i}" aria-label="${esc(t("prod_qty"))}">
            <button type="button" class="li-plus" data-i="${i}" aria-label="${esc(t("qty_plus"))}">+</button>
          </span>
          <button class="icon-btn li-remove" type="button" data-i="${i}" aria-label="${esc(t("list_remove"))}">${icon("close")}</button>
        </li>`).join("")}
    </ul>
    <label class="field"><span>${esc(t("list_note"))}</span><textarea rows="3" class="list-note" placeholder="${esc(t("list_notes_ph"))}">${esc(note)}</textarea></label>
    <a class="btn btn-wa btn-block list-send" href="#" target="_blank" rel="noopener">${icon("wa")}${esc(t("list_send"))}</a>
    <button class="btn-text btn-block list-clear" type="button">${esc(t("list_clear"))}</button>`;
  const setQty = (i, q) => { const list = memoryList.slice(); list[i] = { ...list[i], qty: Math.max(1, q) }; saveList(list); };
  body.querySelectorAll(".li-qty").forEach((inp) => inp.addEventListener("change", () => setQty(Number(inp.dataset.i), parseInt(inp.value, 10) || 1)));
  body.querySelectorAll(".li-minus").forEach((b) => b.addEventListener("click", () => setQty(Number(b.dataset.i), memoryList[b.dataset.i].qty - 1)));
  body.querySelectorAll(".li-plus").forEach((b) => b.addEventListener("click", () => setQty(Number(b.dataset.i), memoryList[b.dataset.i].qty + 1)));
  body.querySelectorAll(".li-remove").forEach((b) => b.addEventListener("click", () => saveList(memoryList.filter((_, i) => i !== Number(b.dataset.i)))));
  body.querySelector(".list-clear").addEventListener("click", () => saveList([]));
  body.querySelector(".list-send").addEventListener("click", (e) => {
    const lines = memoryList.map((x, i) => `${i + 1}. ${lineName(x)} × ${x.qty}`);
    const noteText = body.querySelector(".list-note").value.trim();
    const msg = [t("wa_greeting"), ...lines, noteText ? `\n${t("wa_note")}: ${noteText}` : ""].filter(Boolean).join("\n");
    e.currentTarget.href = waLink(msg, "my-list");
  });
}

let lastFocus = null;
function openDrawer() {
  lastFocus = document.activeElement;
  document.querySelector(".drawer").hidden = false;
  document.querySelector(".drawer-backdrop").hidden = false;
  document.body.classList.add("no-scroll");
  document.querySelector(".drawer-close").focus();
}
function closeDrawer() {
  const d = document.querySelector(".drawer");
  if (!d || d.hidden) return;
  d.hidden = true;
  document.querySelector(".drawer-backdrop").hidden = true;
  document.body.classList.remove("no-scroll");
  if (lastFocus) lastFocus.focus();
}

let toastTimer;
function toast(text) {
  const el = document.querySelector(".toast");
  el.textContent = text;
  el.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove("show"), 1800);
}

/* ---------- motion ---------- */
function initMotion() {
  const header = document.getElementById("site-header");
  const overHero = document.body.classList.contains("has-hero");
  const onScroll = () => {
    header.classList.toggle("is-solid", !overHero || window.scrollY > 40);
    header.classList.toggle("is-small", window.scrollY > 40);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const io = "IntersectionObserver" in window;
  if (io && !REDUCED) {
    document.documentElement.classList.add("reveal-ready");
    // stagger children of grids by 60 ms
    document.querySelectorAll(".stagger").forEach((grid) => [...grid.children].forEach((el, i) => el.style.setProperty("--d", `${i * 60}ms`)));
    const obs = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("is-in"); obs.unobserve(en.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach((el) => obs.observe(el));
    window.addEventListener("beforeprint", () => document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-in")));
    // hero lines rise in on load
    if (document.querySelector(".hero")) {
      document.documentElement.classList.add("anim-ready");
      requestAnimationFrame(() => requestAnimationFrame(() => document.documentElement.classList.add("anim-in")));
    }
  }

  const heroMedia = document.querySelector(".hero-media");
  if (heroMedia && !REDUCED) {
    let ticking = false;
    window.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { heroMedia.style.transform = `translate3d(0, ${Math.min(30, window.scrollY * 0.08)}px, 0)`; ticking = false; });
    }, { passive: true });
  }

  document.querySelectorAll("[data-count]").forEach((el) => {
    const target = el.dataset.count === "since" ? new Date().getFullYear() - SITE.founded : Number(el.dataset.count);
    const fmt = (n) => n.toLocaleString("en-US");
    if (REDUCED || !io) { el.textContent = fmt(target); return; }
    el.textContent = "0";
    const obs = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting) return;
      obs.disconnect();
      const start = performance.now();
      const step = (now) => {
        const p = Math.min(1, (now - start) / 1200);
        el.textContent = fmt(Math.round(target * (1 - Math.pow(1 - p, 3))));
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
    obs.observe(el);
  });

  if (heroMedia && SITE.heroVideo && !REDUCED && !SAVE_DATA) {
    const v = document.createElement("video");
    Object.assign(v, { muted: true, loop: true, autoplay: true, playsInline: true, poster: heroMedia.querySelector("img")?.currentSrc || "" });
    v.setAttribute("muted", ""); v.setAttribute("playsinline", ""); v.setAttribute("aria-hidden", "true");
    const small = window.matchMedia("(max-width: 720px)").matches && SITE.heroVideo.mobile;
    v.innerHTML = small
      ? `<source src="${SITE.heroVideo.mobile}" type="video/mp4">`
      : `${SITE.heroVideo.webm ? `<source src="${SITE.heroVideo.webm}" type="video/webm">` : ""}<source src="${SITE.heroVideo.mp4}" type="video/mp4">`;
    heroMedia.appendChild(v);
  }

  const map = document.getElementById("map-frame");
  if (map) {
    const load = () => { if (!map.src) // Searching by name makes Google show the business card (name, rating, "Open in Maps") on the map.
      map.src = `https://maps.google.com/maps?q=${encodeURIComponent(SITE.mapQuery)}&z=16&output=embed`; };
    if (io) {
      const obs = new IntersectionObserver(([en]) => { if (en.isIntersecting) { load(); obs.disconnect(); } }, { rootMargin: "300px" });
      obs.observe(map);
    } else load();
  }
  document.querySelectorAll(".directions-link").forEach((a) => { a.href = mapLink(); });
}

/* ---------- page bits ---------- */
function initCardsAndCopy() {
  document.querySelectorAll("[data-add-cat]").forEach((b) => b.addEventListener("click", () => {
    const slug = b.dataset.addCat;
    addToList({ id: `cat:${slug}`, name: I18N.en[CAT_NAMES[slug]] || slug, size: "", opt: "", grade: "", qty: 1 }, b);
  }));
  document.querySelectorAll(".copy-address").forEach((b) => b.addEventListener("click", async () => {
    const text = `Advance Hardware LLC, ${I18N.en.contact_address}`;
    try { await navigator.clipboard.writeText(text); } catch (e) {
      const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (err) { /* ignore */ } ta.remove();
    }
    toast(t("copied"));
  }));
}

function initProducts() {
  const grid = document.getElementById("product-grid");
  if (!grid) return;
  const chips = document.getElementById("cat-chips");
  const search = document.getElementById("product-search");
  const products = window.PRODUCTS || [];
  let activeCat = decodeURIComponent(location.hash.slice(1)) || "all";

  const norm = (s) => s.toLowerCase().replace(/\s+/g, " ").trim();
  const matches = (p, q) => {
    if (!q) return true;
    const hay = norm([p.en, p.ar, p.cat_en, p.cat_ar, ...p.sizes, ...p.grades, ...p.options.map((o) => o.en + " " + o.ar)].join(" "));
    return norm(q).split(" ").every((w) => hay.includes(w));
  };
  const range = (sizes) => (sizes.length > 1 ? `${sizes[0]}–${sizes[sizes.length - 1]}` : sizes[0] || "");
  const tile = (p) => {
    const img = CAT_IMAGE[p.cat];
    return img
      ? `<picture><source type="image/webp" srcset="media/card-${img}-480.webp"><img src="media/card-${img}-480.jpg" alt="" width="480" height="360" loading="lazy" decoding="async"></picture>`
      : icon(p.icon, "icon icon-xl");
  };

  function drawChips() {
    const cats = [];
    products.forEach((p) => { if (!cats.find((c) => c.cat === p.cat)) cats.push(p); });
    if (activeCat !== "all" && !cats.find((c) => c.cat === activeCat)) activeCat = "all";
    chips.innerHTML = [`<button type="button" class="chip" data-cat="all" aria-pressed="${activeCat === "all"}">${esc(t("prod_all"))}</button>`,
      ...cats.map((c) => `<button type="button" class="chip" data-cat="${c.cat}" aria-pressed="${activeCat === c.cat}">${esc(lang === "ar" ? c.cat_ar : c.cat_en)}</button>`)].join("");
    chips.querySelectorAll(".chip").forEach((b) => b.addEventListener("click", () => {
      activeCat = b.dataset.cat;
      history.replaceState(null, "", activeCat === "all" ? location.pathname + location.search : `${location.search}#${activeCat}`);
      drawChips(); drawGrid();
    }));
  }

  const select = (cls, label, opts) => `<label class="field"><span>${esc(label)}</span>
    <select class="${cls}"><option value="">${esc(t("prod_any"))}</option>${opts}</select></label>`;

  function drawGrid() {
    const q = search.value;
    const shown = products.filter((p) => (activeCat === "all" || p.cat === activeCat) && matches(p, q));
    if (!shown.length) {
      grid.innerHTML = `<div class="empty"><p>${esc(t("prod_none"))}</p>
        <a class="btn btn-wa" href="${waLink(t("wa_photo") + " " + q, "product-search")}" target="_blank" rel="noopener">${icon("wa")}${esc(t("find_cta"))}</a></div>`;
      return;
    }
    grid.innerHTML = shown.map((p) => `
      <article class="product" data-id="${p.id}">
        <div class="product-tile">${tile(p)}</div>
        <div class="product-main">
          <p class="product-cat">${esc(lang === "ar" ? p.cat_ar : p.cat_en)}</p>
          <h2 class="product-name">${esc(p[lang])}</h2>
          <p class="product-spec mono" dir="ltr">${esc([range(p.sizes), p.grades.join(" · ")].filter(Boolean).join("  ·  "))}</p>
        </div>
        <div class="product-fields">
          ${p.sizes.length ? select("f-size", t("prod_size"), p.sizes.map((s) => `<option>${esc(s)}</option>`).join("")) : ""}
          ${p.grades.length ? select("f-grade", t("prod_grade"), p.grades.map((g) => `<option>${esc(g)}</option>`).join("")) : ""}
          ${p.options.length ? select("f-opt", t("prod_option"), p.options.map((o, i) => `<option value="${i}">${esc(o[lang])}</option>`).join("")) : ""}
          <label class="field field-qty"><span>${esc(t("prod_qty"))}</span><input class="f-qty" type="number" min="1" inputmode="numeric" value="1"></label>
        </div>
        <div class="product-foot">
          <span class="price-tag">${esc(t("prod_ask"))}</span>
          <button class="btn btn-accent btn-sm f-add" type="button">${icon("plus")}${esc(t("prod_add"))}</button>
        </div>
      </article>`).join("");
    grid.querySelectorAll(".product").forEach((card) => {
      const btn = card.querySelector(".f-add");
      btn.addEventListener("click", () => {
        const p = products.find((x) => x.id === card.dataset.id);
        addToList({
          id: p.id,
          name: p.en,
          size: card.querySelector(".f-size")?.value || "",
          grade: card.querySelector(".f-grade")?.value || "",
          opt: card.querySelector(".f-opt")?.value ?? "",
          qty: Math.max(1, parseInt(card.querySelector(".f-qty").value, 10) || 1),
        }, btn);
      });
    });
  }

  search.addEventListener("input", drawGrid);
  window.addEventListener("hashchange", () => { activeCat = decodeURIComponent(location.hash.slice(1)) || "all"; drawChips(); drawGrid(); });
  document.addEventListener("langchange", () => { drawChips(); drawGrid(); });
}

function initTrade() {
  const form = document.getElementById("trade-form");
  if (!form) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const company = (f.get("company") || "").trim();
    const err = form.querySelector(".form-error");
    if (!company) { err.textContent = t("form_required"); form.company.focus(); return; }
    err.textContent = "";
    const typeSel = form.querySelector("select[name=type]");
    const msg = [
      t("form_wa_intro"),
      `${t("form_company")}: ${company}`,
      `${t("form_type")}: ${typeSel.options[typeSel.selectedIndex].text}`,
      f.get("area") ? `${t("form_area")}: ${f.get("area").trim()}` : "",
      f.get("items") ? `${t("form_items")}: ${f.get("items").trim()}` : "",
    ].filter(Boolean).join("\n");
    window.open(waLink(msg, "trade-form"), "_blank", "noopener");
  });
}

async function initCredits() {
  const list = document.getElementById("credits-list");
  if (!list) return;
  try {
    const data = await (await fetch("data/photo-credits.json")).json();
    list.innerHTML = data.credits.map((c) => {
      const w = c.file.startsWith("card-") ? 480 : (c.file === "hero" ? 960 : 480);
      return `<li><img src="media/${c.file}-${w}.jpg" alt="" width="96" height="72" loading="lazy">
        <p><a href="${esc(c.page)}" target="_blank" rel="noopener">${esc(c.title)}</a><br>${esc(c.artist)} · <a href="${esc(c.license_url || c.page)}" target="_blank" rel="noopener">${esc(c.license)}</a><br>${esc(c.changes)}</p></li>`;
    }).join("");
  } catch (e) {
    list.innerHTML = `<li><p><a href="docs/image-credits.md">docs/image-credits.md</a></p></li>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderChrome();
  initProducts();
  initTrade();
  initCardsAndCopy();
  applyLang();
  initMotion();
  initCredits();
  setInterval(updateHours, 60000);
});

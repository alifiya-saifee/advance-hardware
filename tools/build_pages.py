"""Builds the five HTML pages (shared head, cards, picture markup). Run: python3 tools/build_pages.py"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
HOURS = json.loads((ROOT / "data" / "hours.json").read_text())
REVIEWS = json.loads((ROOT / "data" / "reviews.json").read_text())
DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def ranges(d):
    return HOURS["days"].get(str(d), HOURS["default"])

def hours_ld():
    groups = {}
    for d in [6, 0, 1, 2, 3, 4, 5]:
        for o, c in ranges(d):
            groups.setdefault((o, c), []).append(DAY_NAMES[d])
    return [{"@type": "OpeningHoursSpecification", "dayOfWeek": days, "opens": o, "closes": c} for (o, c), days in groups.items()]

def hours_sentence():
    order, out, i = [6, 0, 1, 2, 3, 4, 5], [], 0
    while i < 7:
        j = i
        while j + 1 < 7 and ranges(order[j + 1]) == ranges(order[i]): j += 1
        label = DAY_NAMES[order[i]] if i == j else f"{DAY_NAMES[order[i]]} to {DAY_NAMES[order[j]]}"
        r = ranges(order[i])
        out.append(f"{label} " + (" and ".join(f"{o.lstrip('0')}–{c}" for o, c in r) if r else "closed"))
        i = j + 1
    return ", ".join(out)
FONTS = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap"
SITE_URL = ""  # e.g. "https://advancehardware.ae" once online (used for the share image)

def head(title, desc, extra=""):
    return f'''<!doctype html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#111315">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE_URL}/media/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONTS}"></noscript>
{extra}  <link rel="stylesheet" href="assets/style.css">
  <script src="assets/hours.js" defer></script>
  <script src="assets/i18n.js" defer></script>
  <script src="assets/products.js" defer></script>
  <script src="assets/app.js" defer></script>
</head>'''

def body_open(page, title_key="", cls=""):
    tk = f' data-title="{title_key}"' if title_key else ""
    c = f' class="{cls}"' if cls else ""
    return f'''<body{c} data-page="{page}"{tk}>
  <a class="skip" href="#main" data-i18n="skip">Skip to content</a>
  <header id="site-header" class="site-header"></header>
  <main id="main">'''

BODY_CLOSE = '''  </main>
  <footer id="site-footer" class="site-footer"></footer>
</body>
</html>
'''

def picture(stem, widths, sizes, w, h, alt_key, lazy=True, cls=""):
    webp = ", ".join(f"media/{stem}-{x}.webp {x}w" for x in widths)
    jpg = ", ".join(f"media/{stem}-{x}.jpg {x}w" for x in widths)
    mid = sorted(widths)[len(widths) // 2]
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img{c} src="media/{stem}-{mid}.jpg" srcset="{jpg}" sizes="{sizes}" width="{w}" height="{h}" alt="" data-i18n-alt="{alt_key}" {load}></picture>')

def page_head(eyebrow_key, eyebrow, h_key, h, p_key, p):
    return f'''    <section class="page-head dark grain">
      <div class="wrap">
        <p class="eyebrow" data-i18n="{eyebrow_key}">{eyebrow}</p>
        <h1 class="display" data-i18n="{h_key}">{h}</h1>
        <p data-i18n="{p_key}">{p}</p>
      </div>
    </section>'''

# ---------------- home ----------------
CARDS = [  # slug (products.html#), image stem, title key, title, spec key, spec, alt key
    ("high-tensile-bolts", "high-tensile", "cat_hightensile", "High-tensile bolts", "spec_hightensile", "Grade 8.8 · 10.9 · 12.9", "alt_high_tensile"),
    ("bolts", "bolts", "cat_bolts", "Bolts", "spec_bolts", "Hex · Socket · SS bolt + nut", "alt_bolts"),
    ("nuts", "nuts", "cat_nuts", "Nuts", "spec_nuts", "Hex · Lock · Other types", "alt_nuts"),
    ("washers", "washers", "cat_washers", "Washers", "spec_washers", "Flat · Spring · Copper", "alt_washers"),
    ("screws", "screws", "cat_screws", "Screws", "spec_screws", "CSK Allen · Grub · General", "alt_screws"),
    ("threaded-bar", "threaded-bar", "cat_rod", "Threaded bar", "spec_rod", "M6–M24 · SS · MS · GI", "alt_rod"),
    ("anchors-and-fixings", "anchors-tools", "cat_anchors", "Anchors and tools", "spec_anchors", "Anchors · Drill bits · Discs", "alt_anchors"),
    ("gloves-and-safety", "gloves", "cat_gloves", "Gloves and safety", "spec_gloves", "Work gloves · Glasses · Ear plugs", "alt_gloves"),
]
def card(slug, stem, tk, title, sk, spec, ak):
    return f'''          <article class="stock-card">
            <a class="stock-media" href="products.html#{slug}" tabindex="-1" aria-hidden="true">{picture("card-" + stem, [480, 960, 1200], "(min-width: 1080px) 288px, (min-width: 720px) 45vw, 50vw", 1200, 900, ak)}</a>
            <div class="stock-body">
              <h3 class="h3" data-i18n="{tk}">{title}</h3>
              <p class="stock-spec small" data-i18n="{sk}">{spec}</p>
              <div class="stock-actions">
                <button class="btn btn-secondary btn-sm" type="button" data-add-cat="{slug}"><i data-icon="plus"></i><span data-i18n="card_add">Add to my list</span></button>
                <a class="text-link" href="products.html#{slug}"><span data-i18n="card_view">View sizes</span><i data-icon="arrow"></i></a>
              </div>
            </div>
          </article>'''

BOLT_SVG = '''<svg class="bolt-svg" viewBox="0 0 400 400" role="img" aria-labelledby="bolt-svg-t">
            <title id="bolt-svg-t">Hex bolt head seen from above, stamped 10.9</title>
            <defs><radialGradient id="bh" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#2a3036"/><stop offset="1" stop-color="#15181b"/></radialGradient></defs>
            <polygon points="200,58 323,129 323,271 200,342 77,271 77,129" fill="url(#bh)" stroke="#f2a900" stroke-width="3" stroke-linejoin="round"/>
            <circle cx="200" cy="200" r="118" fill="none" stroke="#f2a900" stroke-opacity=".45" stroke-width="1.5"/>
            <path d="M200 58 L200 82 M323 129 L302 141 M323 271 L302 259 M200 342 L200 318 M77 271 L98 259 M77 129 L98 141" stroke="#f2a900" stroke-opacity=".35" stroke-width="1.5"/>
            <text x="200" y="214" text-anchor="middle" font-size="58" font-weight="700" fill="#f2a900" letter-spacing="-2">10.9</text>
            <text x="200" y="262" text-anchor="middle" font-size="22" font-weight="500" fill="#a7b0b8" letter-spacing="4">MK</text>
            <path d="M262 190 L300 34 L392 34" fill="none" stroke="#a7b0b8" stroke-width="1.5"/><circle cx="262" cy="190" r="4" fill="#f2a900"/>
            <text x="392" y="24" text-anchor="end" font-size="15" fill="#e2e5e7" data-i18n="svg_grade">Strength grade</text>
            <path d="M184 256 L110 330 L12 330" fill="none" stroke="#a7b0b8" stroke-width="1.5"/><circle cx="184" cy="256" r="4" fill="#f2a900"/>
            <text x="12" y="320" font-size="15" fill="#e2e5e7" data-i18n="svg_maker">Maker's mark</text>
          </svg>'''

def grade(num, tensile, yld, dk, desc, mk, more):
    return f'''            <details class="grade">
              <summary><span class="grade-num" dir="ltr">{num}</span><div><p class="grade-mpa small" dir="ltr"><span>{tensile} MPa <span data-i18n="g_tensile">tensile</span></span><span>{yld} MPa <span data-i18n="g_yield">yield</span></span></p><p class="grade-desc" data-i18n="{dk}">{desc}</p></div><i data-icon="chev" data-cls="chev"></i></summary>
              <p class="grade-more"><strong data-i18n="g_more">Typical uses and sizes</strong>: <span data-i18n="{mk}">{more}</span></p>
            </details>'''

HOME_LD = '''  <script type="application/ld+json">
  {"@context": "https://schema.org", "@type": "HardwareStore", "name": "Advance Hardware LLC", "alternateName": ["Advance Hardware", "أدفانس هاردوير"],
   "foundingDate": "1996", "description": "Fastener specialist in Sharjah Industrial Area 2: high-tensile bolts 8.8, 10.9 and 12.9, nuts, screws, washers, threaded bar and gloves.",
   "telephone": "+971506789646", "image": "media/og.jpg",
   "address": {"@type": "PostalAddress", "streetAddress": "Shop No. 2, near ADCB Bank, J & P Road, Industrial Area 2", "addressLocality": "Sharjah", "addressCountry": "AE"},
   "areaServed": ["Sharjah", "Dubai"], "knowsLanguage": ["ar", "en", "hi", "ur"],
   "sameAs": ["https://www.google.com/maps/search/?api=1&query=Advance%20Hardware%20LLC%20Industrial%20Area%202%20Sharjah"],
   "openingHoursSpecification": OPENING_HOURS}
  </script>
  <link rel="preload" as="image" type="image/webp" href="media/hero-m-540.webp" imagesrcset="media/hero-m-540.webp 540w, media/hero-m-1080.webp 1080w" imagesizes="100vw" media="(max-width: 719px)">
  <link rel="preload" as="image" type="image/webp" href="media/hero-1920.webp" imagesrcset="media/hero-960.webp 960w, media/hero-1920.webp 1920w, media/hero-2400.webp 2400w" imagesizes="100vw" media="(min-width: 720px)">
'''

VISIT = '''    <section class="section dark grain" id="visit">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow" data-i18n="nav_contact">Contact</p>
          <h2 class="h2" data-i18n="visit_title">Visit the shop</h2>
          <p data-i18n="langs_line">We speak Arabic, English, Hindi and Urdu.</p>
        </div>
        <div class="visit-grid">
          <div class="reveal">
            <div class="info-block">
              <h3 class="info-h" data-i18n="contact_address_t">Address</h3>
              <p class="landmark" data-i18n="contact_landmark">Near ADCB Bank, J &amp; P Road</p>
              <p data-i18n="contact_address_rest">Shop No. 2, Industrial Area 2, Sharjah, UAE</p>
              <button class="btn btn-secondary btn-sm copy-btn copy-address" type="button"><i data-icon="copy"></i><span data-i18n="copy_address">Copy address</span></button>
            </div>
            <div class="info-block">
              <h3 class="info-h" data-i18n="contact_hours_t">Opening hours</h3>
              <table class="hours-table"><tbody class="hours-week"></tbody></table>
              <p class="open-status" style="margin-top:12px"></p>
            </div>
            <div class="info-block">
              <h3 class="info-h" data-i18n="contact_phone_t">Phone and WhatsApp</h3>
              <div class="phone-list"></div>
            </div>
            <div class="visit-actions">
              <a class="btn btn-accent directions-link" href="#" target="_blank" rel="noopener"><i data-icon="pin"></i><span data-i18n="contact_directions">Get directions</span></a>
              <a class="btn btn-secondary call-link" href="tel:+971506789646"><i data-icon="phone"></i><span data-i18n="call">Call</span></a>
            </div>
          </div>
          <iframe id="map-frame" class="map reveal" title="Map: Advance Hardware, Industrial Area 2, Sharjah" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </section>'''

def reviews_html():
    """Real Google reviews only, copied word for word into data/reviews.json. Empty file = no cards."""
    import html as H
    if not REVIEWS:
        return ""
    cards = []
    for r in REVIEWS[:3]:
        stars = int(r.get("stars", 5))
        star_svg = '<i data-icon="star"></i>' * stars
        lang_attr = ' lang="ar" dir="rtl"' if r.get("lang") == "ar" else ' lang="en" dir="ltr"'
        cards.append(f'''          <figure class="review-card reveal">
            <div class="stars" aria-label="{stars} out of 5 stars">{star_svg}</div>
            <blockquote{lang_attr}>{"«" if r.get("lang") == "ar" else "“"}{H.escape(r["text"])}{"»" if r.get("lang") == "ar" else "”"}</blockquote>
            <figcaption><strong>{H.escape(r["name"])}</strong> · <a href="{H.escape(r.get("url") or "#")}" class="google-review-link" target="_blank" rel="noopener" data-i18n="rev_google">Google review</a><br><span class="small">{H.escape(r.get("date", ""))}</span></figcaption>
          </figure>''')
    return '\n        <div class="review-row stagger">\n' + "\n".join(cards) + "\n        </div>"

def build_home_ld():
    return HOME_LD.replace("OPENING_HOURS", json.dumps(hours_ld(), ensure_ascii=False))

def build_home():
    hero_pic = ('<picture>'
        '<source media="(max-width: 719px)" type="image/webp" srcset="media/hero-m-540.webp 540w, media/hero-m-1080.webp 1080w" sizes="100vw">'
        '<source media="(max-width: 719px)" srcset="media/hero-m-540.jpg 540w, media/hero-m-1080.jpg 1080w" sizes="100vw">'
        '<source type="image/webp" srcset="media/hero-960.webp 960w, media/hero-1920.webp 1920w, media/hero-2400.webp 2400w" sizes="100vw">'
        '<img src="media/hero-1920.jpg" srcset="media/hero-960.jpg 960w, media/hero-1920.jpg 1920w, media/hero-2400.jpg 2400w" sizes="100vw" width="2400" height="1350" alt="" data-i18n-alt="alt_hero" fetchpriority="high" decoding="async"></picture>')
    cards = "\n".join(card(*c) for c in CARDS)
    grades = "\n".join([
        grade("8.8", 800, 640, "g88_d", "The everyday high-strength bolt: steel structures, machinery, general fabrication.", "g88_more", "Base plates, brackets, machine frames, general steelwork. In stock M6–M24."),
        grade("10.9", 1000, 900, "g109_d", "Stronger, for heavy machinery, cranes and joints that carry big loads.", "g109_more", "Crane parts, heavy equipment, flanges, high-load joints. In stock M6–M24."),
        grade("12.9", 1200, 1080, "g129_d", "The strongest common grade: Allen bolts, dies, engines and high-stress parts.", "g129_more", "Allen bolts, moulds and dies, engine and gearbox parts. In stock M6–M24."),
    ])
    html = head("Advance Hardware | Bolts, nuts and fasteners in Sharjah since 1996",
                "Advance Hardware, Industrial Area 2, Sharjah: high-tensile bolts (8.8, 10.9, 12.9), nuts, screws, washers, threaded bar and gloves from stock since 1996. Send your list on WhatsApp for a quote in minutes. Same-day delivery in Sharjah and Dubai.",
                build_home_ld()) + "\n" + body_open("home", cls="has-hero") + f'''
    <section class="hero dark">
      <div class="hero-media">{hero_pic}</div>
      <div class="wrap hero-content">
        <div class="hero-copy">
          <p class="eyebrow" data-i18n="hero_kicker">Fastener specialist · Industrial Area 2, Sharjah</p>
          <h1 class="display">
            <span class="line" data-i18n="hero_t1">High-strength bolts.</span>
            <span class="line" data-i18n="hero_t2">Hard-to-find sizes.</span>
            <span class="line" data-i18n="hero_t3">From stock since 1996.</span>
          </h1>
          <p class="hero-text" data-i18n="hero_text">Send your list on WhatsApp. Quote in minutes. Delivery across Sharjah and Dubai.</p>
          <div class="hero-actions">
            <a class="btn btn-wa wa-list-link" data-src="hero" href="https://wa.me/971506789646" target="_blank" rel="noopener"><i data-icon="wa"></i><span data-i18n="cta_send_list">Send your list on WhatsApp</span></a>
            <a class="btn btn-secondary" href="products.html" data-i18n="cta_browse">Browse products</a>
          </div>
          <div class="proof-row">
            <a class="pchip google-link" href="#" target="_blank" rel="noopener"><i data-icon="star" data-cls="icon-fill"></i><span data-i18n="chip_rating">4.7 on Google</span></a>
            <span class="pchip"><i data-icon="list"></i><span data-i18n="chip_nomin">No minimum order</span></span>
            <span class="pchip"><i data-icon="clock"></i><span data-i18n="chip_reply">Reply in 15 min (shop hours)</span></span>
            <span class="pchip open-status"></span>
          </div>
        </div>
      </div>
    </section>

    <section class="dark grain proof" aria-label="Why Advance Hardware">
      <div class="wrap proof-grid stagger">
        <div class="proof-item reveal"><span class="proof-value"><span data-count="since">30</span> <span data-i18n="unit_yrs">yrs</span></span><p data-i18n="pl_years">in Industrial Area 2</p></div>
        <div class="proof-item reveal"><span class="proof-value" data-i18n="pv_same">Same day</span><p data-i18n="pl_same">delivery, Sharjah and Dubai</p></div>
        <div class="proof-item reveal"><span class="proof-value" data-i18n="pv_credit">Credit</span><p data-i18n="pl_credit">for trade accounts</p></div>
        <div class="proof-item reveal"><span class="proof-value" data-i18n="pv_lang">4 languages</span><p data-i18n="pl_lang">Arabic, English, हिंदी, اردو</p></div>
        <div class="proof-item reveal"><span class="proof-value"><span data-count="3000">3,000</span>+</span><p data-i18n="pl_sizes">sizes in stock</p></div>
      </div>
    </section>

    <section class="section light">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow" data-i18n="stock_kicker">The range</p>
          <h2 class="h2" data-i18n="stock_title">What we stock</h2>
          <p class="muted" data-i18n="stock_text">Fasteners first, plus the everyday supplies a site or workshop runs out of. Many more sizes in the shop.</p>
        </div>
        <div class="stock-grid stagger">
{cards.replace('<article class="stock-card">', '<article class="stock-card reveal">')}
        </div>
        <div class="after-grid"><a class="btn btn-secondary" href="products.html"><span data-i18n="see_all">See all products</span><i data-icon="arrow"></i></a></div>
      </div>
    </section>

    <section class="section dark grain">
      <div class="wrap head-grid">
        <div class="reveal">{BOLT_SVG}</div>
        <div class="reveal">
          <p class="eyebrow" data-i18n="head_kicker">Read the head</p>
          <h2 class="h2" data-i18n="head_title">What the numbers on a bolt mean</h2>
          <p data-i18n="head_text">The grade is stamped on the head. The first number × 100 is the tensile strength in MPa. The second number is how much of that the bolt holds before it stretches for good.</p>
          <div class="grades">
{grades}
          </div>
          <a class="btn btn-accent wa-list-link" data-src="grades" href="https://wa.me/971506789646" target="_blank" rel="noopener"><i data-icon="wa"></i><span data-i18n="head_cta">Ask which grade you need</span></a>
        </div>
      </div>
    </section>

    <section class="section light">
      <div class="wrap">
        <div class="section-head reveal"><h2 class="h2" data-i18n="supply_title">Who we supply</h2></div>
        <div class="three stagger">
          <div class="panel reveal"><span class="icon-tile"><i data-icon="anchor"></i></span><h3 class="h3" data-i18n="sup_con_t">Contractors</h3><p data-i18n="sup_con_d">Bolts, threaded bar and anchors for site work, with same-day delivery and monthly statements.</p><p class="proof-line small" data-i18n="sup_con_p">Monthly statements · same-day delivery</p><a class="text-link" href="trade.html"><span data-i18n="sup_con_link">Open a trade account</span><i data-icon="arrow"></i></a></div>
          <div class="panel reveal"><span class="icon-tile"><i data-icon="tools"></i></span><h3 class="h3" data-i18n="sup_work_t">Workshops and fabricators</h3><p data-i18n="sup_work_d">High-tensile bolts, Allen and grub screws in the sizes you use every day, ready on the shelf.</p><p class="proof-line small" data-i18n="sup_work_p">Grades 8.8 · 10.9 · 12.9 in stock</p><a class="text-link" href="products.html#high-tensile-bolts"><span data-i18n="sup_work_link">See high-tensile bolts</span><i data-icon="arrow"></i></a></div>
          <div class="panel reveal"><span class="icon-tile"><i data-icon="shop"></i></span><h3 class="h3" data-i18n="sup_shop_t">Hardware shops</h3><p data-i18n="sup_shop_d">Wholesale prices on the items you resell. Fill gaps fast when your own stock runs out.</p><p class="proof-line small" data-i18n="sup_shop_p">Wholesale prices · no minimum order</p><a class="text-link" href="trade.html"><span data-i18n="sup_shop_link2">Get wholesale prices</span><i data-icon="arrow"></i></a></div>
        </div>
      </div>
    </section>

    <section class="section dark grain">
      <div class="wrap">
        <div class="section-head reveal"><h2 class="h2" data-i18n="order_title">How ordering works</h2></div>
        <div class="steps stagger">
          <div class="step reveal"><span class="step-num">01</span><div><h3 class="h3" data-i18n="step1_t">Send your list</h3><p data-i18n="step1_d">Type it, build it on our Products page, or send a photo on WhatsApp.</p></div></div>
          <div class="step reveal"><span class="step-num">02</span><div><h3 class="h3" data-i18n="step2_t">Get a quote in minutes</h3><p data-i18n="step2_d">Prices and availability, in Arabic, English, Hindi or Urdu.</p></div></div>
          <div class="step reveal"><span class="step-num">03</span><div><h3 class="h3" data-i18n="step3_t">Pick up or same-day delivery</h3><p data-i18n="step3_d">Collect from the shop, or we deliver across Sharjah and Dubai.</p></div></div>
        </div>
        <div class="after-grid"><a class="btn btn-wa wa-list-link" data-src="how-to-order" href="https://wa.me/971506789646" target="_blank" rel="noopener"><i data-icon="wa"></i><span data-i18n="cta_send_list">Send your list on WhatsApp</span></a></div>
      </div>
    </section>

    <section class="band">
      <div class="wrap band-inner reveal">
        <div>
          <h2 class="h2"><i data-icon="camera"></i><span data-i18n="find_title">Can't find a size?</span></h2>
          <p data-i18n="find_text">Send us a photo. We'll find it within 24 hours.</p>
        </div>
        <a class="btn wa-photo-link" data-src="find-a-size" href="https://wa.me/971506789646" target="_blank" rel="noopener"><i data-icon="wa"></i><span data-i18n="find_cta">Send a photo on WhatsApp</span></a>
      </div>
    </section>

    <!-- Google rating. Real review cards go here once Alifiya pastes real reviews (word for word, linked to Google). Never write our own. -->
    <section class="section light">
      <div class="wrap">
        <div class="rating-card reveal">
          <span class="rating-num" dir="ltr">4.7</span>
          <div>
            <div class="stars" aria-hidden="true"><i data-icon="star"></i><i data-icon="star"></i><i data-icon="star"></i><i data-icon="star"></i><i data-icon="star"></i></div>
            <h2 class="h3" style="font-size:28px;margin:0 0 4px" data-i18n="rev_title">Rated 4.7 on Google</h2>
            <p class="muted" style="margin:0" data-i18n="rev_count">From 10 Google reviews</p>
          </div>
          <div class="rating-actions">
            <a class="btn btn-secondary google-link" href="#" target="_blank" rel="noopener" data-i18n="rev_cta">See all reviews on Google</a>
            <a class="text-link google-link" href="#" target="_blank" rel="noopener"><span data-i18n="rev_leave">Leave us a review</span><i data-icon="arrow"></i></a>
          </div>
        </div>{reviews_html()}
      </div>
    </section>

{VISIT}
''' + BODY_CLOSE
    (ROOT / "index.html").write_text(html)

def build_products():
    html = head("Products | Advance Hardware: bolts, nuts and fasteners in Sharjah",
                "High-tensile bolts 8.8, 10.9 and 12.9, hex and Allen bolts, CSK Allen and grub screws, hex and lock nuts, flat, spring and copper washers, threaded bar and work gloves from stock in Sharjah Industrial Area 2. Build your list and send it on WhatsApp.") + "\n" + body_open("products", "prod_title") + "\n" + page_head("stock_kicker", "The range", "prod_title", "Products", "prod_text", "Choose a size and finish, add items to your list, then send the list on WhatsApp. Quote in minutes.") + '''
    <div class="toolbar">
      <div class="wrap toolbar-inner">
        <input id="product-search" class="search" type="search" autocomplete="off" data-i18n-ph="prod_search" placeholder="Search: bolt, nut, M12, 10.9, gloves…" aria-label="Search products">
        <div id="cat-chips" class="chips" role="group" aria-label="Categories"></div>
      </div>
    </div>
    <section class="light">
      <div class="wrap">
        <div id="product-grid" class="product-grid"></div>
        <div class="note-bar" style="margin-bottom:64px">
          <strong data-i18n="prod_missing_t">Can't find an item?</strong>
          <span data-i18n="prod_missing_d">Send a photo on WhatsApp. We'll find it within 24 hours.</span>
          <a class="text-link wa-photo-link" data-src="products-photo" href="https://wa.me/971506789646" target="_blank" rel="noopener"><span data-i18n="find_cta">Send a photo on WhatsApp</span><i data-icon="arrow"></i></a>
        </div>
      </div>
    </section>
''' + BODY_CLOSE
    (ROOT / "products.html").write_text(html)

def build_trade():
    html = head("Trade accounts | Advance Hardware, Sharjah",
                "Trade accounts at Advance Hardware, Sharjah: wholesale prices and no minimum order for hardware shops, monthly statements and credit for contractors, same-day delivery across Sharjah and Dubai.") + "\n" + body_open("trade", "trade_title") + "\n" + page_head("chip_credit", "Trade credit", "trade_title", "Trade accounts", "trade_text", "Regular supply for contractors, workshops and hardware shops.") + '''
    <section class="section light">
      <div class="wrap">
        <div class="three stagger">
          <div class="panel reveal"><span class="icon-tile"><i data-icon="shop"></i></span><h2 class="h3" data-i18n="trade_shops_t">For hardware shops</h2>
            <ul class="check-list"><li data-i18n="trade_shops_1">Wholesale price list for the items you resell</li><li data-i18n="trade_shops_2">Order on WhatsApp; pick up or same-day delivery</li><li data-i18n="trade_shops_3">Fill gaps fast when your own stock runs out</li><li data-i18n="chip_nomin">No minimum order</li></ul></div>
          <div class="panel reveal"><span class="icon-tile"><i data-icon="anchor"></i></span><h2 class="h3" data-i18n="trade_co_t">For contractors and companies</h2>
            <ul class="check-list"><li data-i18n="trade_co_1">Fixed prices on your regular items for an agreed period</li><li data-i18n="trade_co_2">Monthly statements</li><li data-i18n="trade_co_3">Company documents for your vendor registration: trade licence and VAT certificate</li></ul></div>
          <div class="panel reveal"><span class="icon-tile"><i data-icon="tools"></i></span><h2 class="h3" data-i18n="trade_marine_t">For workshops and marine companies</h2>
            <ul class="check-list"><li data-i18n="trade_marine_1">High-tensile bolts and screws from stock</li><li data-i18n="trade_marine_2">Same-day delivery to your Sharjah or Dubai location</li></ul></div>
        </div>
        <p class="note-bar" data-i18n="trade_credit">Credit is available for regular accounts after the first orders.</p>
      </div>
    </section>
    <section class="section dark grain">
      <div class="wrap">
        <div class="section-head"><h2 class="h2" data-i18n="form_title">Ask for a trade account</h2></div>
        <form id="trade-form" class="form-card" novalidate>
          <label class="field"><span data-i18n="form_company">Company name</span><input name="company" autocomplete="organization" required></label>
          <label class="field"><span data-i18n="form_type">Type of business</span>
            <select name="type">
              <option data-i18n="form_type_shop">Hardware shop</option>
              <option data-i18n="form_type_contractor">Contractor</option>
              <option data-i18n="form_type_workshop">Workshop / factory</option>
              <option data-i18n="form_type_marine">Marine / ship supply</option>
              <option data-i18n="form_type_other">Other</option>
            </select>
          </label>
          <label class="field"><span data-i18n="form_area">Area</span><input name="area" data-i18n-ph="form_area_ph" placeholder="e.g. Al Quoz, Industrial Area 6"></label>
          <label class="field"><span data-i18n="form_items">Items you buy regularly</span><textarea name="items" rows="4"></textarea></label>
          <p class="form-error" role="alert"></p>
          <button class="btn btn-wa" type="submit"><i data-icon="wa"></i><span data-i18n="form_send">Send on WhatsApp</span></button>
        </form>
      </div>
    </section>
''' + BODY_CLOSE
    (ROOT / "trade.html").write_text(html)

def build_about():
    photos = "\n".join(f"          <figure>{picture(s, [480, 960, w], sz, w, round(w*2/3), a)}</figure>" for s, w, sz, a in [
        ("about-box", 1440, "(min-width: 960px) 600px, 100vw", "alt_box"),
        ("about-dark", 1440, "(min-width: 960px) 300px, 50vw", "alt_dark"),
        ("about-pile", 1024, "(min-width: 960px) 300px, 50vw", "alt_pile")])
    html = head("About | Advance Hardware, Sharjah since 1996",
                "Advance Hardware has supplied bolts, nuts, screws, washers and threaded bar from Sharjah Industrial Area 2 since 1996. Our team speaks Arabic, English, Hindi and Urdu.") + "\n" + body_open("about", "nav_about") + "\n" + page_head("nav_about", "About", "about_title", "Since 1996 in Industrial Area 2", "about_text", "A fastener shop that knows its sizes.") + f'''
    <section class="section light">
      <div class="wrap split">
        <div class="prose reveal">
          <p data-i18n="about_p1">Advance Hardware opened in Sharjah's Industrial Area 2 in 1996. Since then we have supplied contractors, workshops, fabricators and other hardware shops with bolts, nuts, screws, washers and threaded bar.</p>
          <p data-i18n="about_p2">We keep high-tensile bolts in grades 8.8, 10.9 and 12.9, the hard-to-find sizes, and the everyday supplies a job runs out of, like gloves.</p>
          <p data-i18n="about_p3">Our team speaks Arabic, English, Hindi and Urdu, so you can order the way you talk. Send a list or a photo on WhatsApp and we reply with a quote in minutes.</p>
          <a class="btn btn-dark" href="contact.html"><i data-icon="pin"></i><span data-i18n="about_cta">Visit the shop</span></a>
        </div>
        <div class="photo-pair reveal">
{photos}
        </div>
      </div>
    </section>
    <section class="dark grain proof" aria-label="Why Advance Hardware">
      <div class="wrap proof-grid">
        <div class="proof-item"><span class="proof-value"><span data-count="since">30</span> <span data-i18n="unit_yrs">yrs</span></span><p data-i18n="pl_years">in Industrial Area 2</p></div>
        <div class="proof-item"><span class="proof-value" data-i18n="pv_same">Same day</span><p data-i18n="pl_same">delivery, Sharjah and Dubai</p></div>
        <div class="proof-item"><span class="proof-value" data-i18n="pv_credit">Credit</span><p data-i18n="pl_credit">for trade accounts</p></div>
        <div class="proof-item"><span class="proof-value" data-i18n="pv_lang">4 languages</span><p data-i18n="pl_lang">Arabic, English, हिंदी, اردو</p></div>
        <div class="proof-item"><span class="proof-value"><span data-count="3000">3,000</span>+</span><p data-i18n="pl_sizes">sizes in stock</p></div>
      </div>
    </section>
''' + BODY_CLOSE
    (ROOT / "about.html").write_text(html)

def build_contact():
    html = head("Contact | Advance Hardware, Industrial Area 2, Sharjah",
                "Advance Hardware, Shop No. 2, near ADCB Bank, J & P Road, Industrial Area 2, Sharjah. Mobile and WhatsApp 050 678 9646, shop 06 543 1678. Open " + hours_sentence() + ".") + "\n" + body_open("contact", "contact_title") + "\n" + page_head("nav_contact", "Contact", "contact_title", "Contact and location", "contact_text", "Visit the shop, call, or send us a WhatsApp message.") + "\n" + VISIT.replace('<section class="section dark grain" id="visit">', '<section class="section dark" id="visit">').replace('''        <div class="section-head reveal">
          <p class="eyebrow" data-i18n="nav_contact">Contact</p>
          <h2 class="h2" data-i18n="visit_title">Visit the shop</h2>
          <p data-i18n="langs_line">We speak Arabic, English, Hindi and Urdu.</p>
        </div>
''', '').replace('<h3 class="info-h"', '<h2 class="info-h"').replace('</h3>', '</h2>') + "\n" + BODY_CLOSE
    (ROOT / "contact.html").write_text(html)

def build_credits():
    html = head("Photo credits | Advance Hardware", "Credits for the photos used on the Advance Hardware website.") + "\n" + body_open("credits", "credits_title") + "\n" + page_head("footer_credits", "Images", "credits_title", "Photo credits", "credits_text", "Our product photos are coming soon. Until then, these photos come from Wikimedia Commons under free licences. Thank you to the photographers.") + '''
    <section class="section light">
      <div class="wrap">
        <ul id="credits-list" class="credits-list"></ul>
      </div>
    </section>
''' + BODY_CLOSE
    (ROOT / "credits.html").write_text(html)

def write_hours_js():
    (ROOT / "assets" / "hours.js").write_text("// Generated by tools/build_pages.py from data/hours.json. Do not edit by hand.\nwindow.HOURS = "
        + json.dumps({"default": HOURS["default"], "days": HOURS["days"]}) + ";\n")

if __name__ == "__main__":
    write_hours_js(); build_home(); build_products(); build_trade(); build_about(); build_contact(); build_credits()
    print("built: index, products, trade, about, contact, credits")

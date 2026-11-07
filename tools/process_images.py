"""Advance Hardware image pipeline (see docs/image-recipe.md). Usage: python3.12 tools/process_images.py <work-folder-with-commons.json> <site-folder>"""
import json, sys, ssl, time, urllib.request, urllib.error
from pathlib import Path
import certifi, numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from rembg import remove, new_session

CTX = ssl.create_default_context(cafile=certifi.where())
UA = {"User-Agent": "AdvanceHardwareSite/1.0 (small business website)"}
SP, SITE = Path(sys.argv[1]), Path(sys.argv[2])
C = json.load(open(SP / "commons.json"))
MEDIA = SITE / "media"
STEEL = (0x1C, 0x20, 0x24)

CARDS = {  # name: (subject, index, alt text)
 "high-tensile":  ("bolts", 14, "High-tensile flange bolt"),
 "bolts":         ("hero", 11, "Hex bolt with hex nut"),
 "nuts":          ("nuts", 10, "Steel hex nut"),
 "washers":       ("washers2", 2, "Stacks of flat steel washers"),
 "screws":        ("screws", 1, "Allen socket head cap screw"),
 "threaded-bar":  ("threaded2", 6, "Threaded bar"),
 "anchors-tools": ("anchors-tools", 10, "Masonry drill bit"),
 "gloves":        ("gloves", 5, "Work gloves"),
}
PHOTOS = {  # name: (subject, index, aspect, widths, alt)
 "hero":    ("nuts", 0, (16, 9), [2400, 1920, 960], "Bolts and nuts standing on a dark reflective surface"),
 "hero-m":  ("nuts", 0, (4, 5), [1080, 540], "Bolts and nuts standing on a dark reflective surface"),
 "about-box":  ("hero", 3, (3, 2), [1440, 960, 480], "Wooden box of bolts and nuts"),
 "about-dark": ("grade2", 12, (3, 2), [1440, 960, 480], "Bolts standing on a dark reflective surface"),
 "about-pile": ("hero", 6, (3, 2), [1440, 960, 480], "Pile of screws, bolts and nuts"),
}

def fetch(name, c):
    raw = SP / "orig" / f"{name}.src"
    if raw.exists(): return raw
    raw.parent.mkdir(exist_ok=True)
    for attempt in range(6):
        try:
            src = c["url"]
            if c["w"] > 2600 and attempt < 2:
                head, tail = src.split("/wikipedia/commons/", 1); fn = tail.rsplit("/", 1)[1]
                src = f"{head}/wikipedia/commons/thumb/{tail}/2560px-{fn}"
            raw.write_bytes(urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=120, context=CTX).read())
            time.sleep(3); return raw
        except Exception as e:
            print("  retry", name, type(e).__name__, getattr(e, "code", "")); time.sleep(10 * (attempt + 1))
    sys.exit("download failed: " + name)

def grade(im):
    """One look for the whole site (see docs/image-recipe.md)."""
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    a *= 2 ** -0.2                                   # exposure -0.2
    a = (a - 0.5) * 1.15 + 0.5                       # contrast +15
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).clip(0, 1)[..., None]
    a -= 0.20 * np.clip((a - 0.6) / 0.4, 0, 1) ** 2 * 0.4   # highlights -20
    a += 0.10 * np.clip((0.3 - a) / 0.3, 0, 1) * 0.15       # shadows -10 (lift crushed blacks a touch less)
    a[..., 0] *= 0.985; a[..., 2] *= 1.02            # temperature -5 (cooler steel)
    amber = np.array([0xE8, 0xA9, 0x3A]) / 255.0; navy = np.array([0x1B, 0x24, 0x30]) / 255.0
    hi = np.clip((lum - 0.55) / 0.45, 0, 1); lo = np.clip((0.45 - lum) / 0.45, 0, 1)
    a = a * (1 - 0.10 * hi) + amber * 0.10 * hi      # split tone highlights amber 10%
    a = a * (1 - 0.12 * lo) + navy * 0.12 * lo       # split tone shadows navy 12%
    out = Image.fromarray((a.clip(0, 1) * 255).astype(np.uint8))
    out = ImageEnhance.Color(out).enhance(0.85)      # saturation -15
    out = out.filter(ImageFilter.UnsharpMask(radius=max(2, out.width // 120), percent=25, threshold=2))  # clarity +10
    out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=3))                      # texture
    return out

def vignette(im, strength=0.10):
    w, h = im.size
    y, x = np.ogrid[:h, :w]
    d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2) / np.sqrt(2)
    mask = 1 - strength * np.clip(d, 0, 1) ** 2
    a = np.asarray(im).astype(np.float32) * mask[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

def save(im, stem, widths, aspect):
    aw, ah = aspect; out = {}
    for w in widths:
        h = round(w * ah / aw)
        if w > im.width:  # never upscale
            continue
        r = im.resize((w, h), Image.LANCZOS) if im.size != (w, h) else im
        for ext, kw in (("webp", {"quality": 72, "method": 6}), ("jpg", {"quality": 76, "optimize": True, "progressive": True})):
            p = MEDIA / f"{stem}-{w}.{ext}"; r.save(p, **kw); out[p.name] = p.stat().st_size // 1024
    return out

credits, alts = [], {}
session = new_session("isnet-general-use")
for name, (subj, idx, alt) in CARDS.items():
    c = C[subj][idx]; src = ImageOps.exif_transpose(Image.open(fetch(name, c))).convert("RGB")
    src.thumbnail((2400, 2400))
    if name == "threaded-bar":  # tight crop + u2net model separates the rod from the grass; rotate after cutting
        W0, H0 = src.size; src = src.crop((int(.25 * W0), 0, int(.75 * W0), H0))
        cut = remove(src, session=new_session("u2net"), post_process_mask=True).convert("RGBA")
        cut = cut.rotate(-60, expand=True, resample=Image.BICUBIC)
    else:
        cut = remove(src, session=session, post_process_mask=True).convert("RGBA")
    bbox = cut.getchannel("A").point(lambda v: 255 if v > 16 else 0).getbbox(); cut = cut.crop(bbox)
    base = cut.convert("RGB")
    if name == "washers": base = ImageOps.grayscale(base).convert("RGB")
    rgb = grade(base); alpha = cut.getchannel("A").filter(ImageFilter.GaussianBlur(0.6))  # 1 px feather
    W, H = 1200, 900
    scale = min(0.70 * W / rgb.width, 0.74 * H / rgb.height)
    nw, nh = max(1, int(rgb.width * scale)), max(1, int(rgb.height * scale))
    rgb, alpha = rgb.resize((nw, nh), Image.LANCZOS), alpha.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), STEEL)
    ox, oy = (W - nw) // 2, (H - nh) // 2
    shadow = Image.new("L", (W, H), 0); shadow.paste(alpha.point(lambda v: int(v * 0.35)), (ox, oy + 12))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    canvas = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), canvas, shadow)
    canvas.paste(rgb, (ox, oy), alpha)
    sizes = save(vignette(canvas, 0.08), f"card-{name}", [1200, 960, 480], (4, 3))
    alts[f"card-{name}"] = alt
    credits.append({"file": f"card-{name}", "use": "category card", "title": c["title"].replace("File:", ""), "artist": c["artist"] or "unknown",
                    "license": c["license"], "license_url": c["license_url"], "page": c["page"],
                    "changes": "background removed, " + ("converted to black and white, " if name == "washers" else "") + ("rotated, " if name == "threaded-bar" else "") + "colour graded, placed on a dark background, resized"})
    print(f"card {name:14} {c['license']:14} {sizes}")

for name, (subj, idx, (aw, ah), widths, alt) in PHOTOS.items():
    c = C[subj][idx]; src = ImageOps.exif_transpose(Image.open(fetch(subj + str(idx), c))).convert("RGB")
    maxw = min(widths[0], src.width, int(src.height * aw / ah))
    fit = ImageOps.fit(src, (maxw, round(maxw * ah / aw)), Image.LANCZOS)
    img = vignette(grade(fit), 0.10)
    sizes = save(img, name, [maxw] + [w for w in widths if w < maxw], (aw, ah))
    alts[name] = alt
    if not name.endswith("-m"):
        credits.append({"file": name, "use": "photo", "title": c["title"].replace("File:", ""), "artist": c["artist"] or "unknown",
                        "license": c["license"], "license_url": c["license_url"], "page": c["page"], "changes": "cropped, colour graded, resized"})
    print(f"photo {name:10} {c['license']:14} {sizes}")

# social preview (1.91:1) from the hero
c = C["nuts"][0]; src = ImageOps.exif_transpose(Image.open(SP / "orig" / "nuts0.src")).convert("RGB")
og = vignette(grade(ImageOps.fit(src, (1200, 630), Image.LANCZOS)), 0.10); og.save(MEDIA / "og.jpg", quality=80, optimize=True)
print("og", (MEDIA / "og.jpg").stat().st_size // 1024, "KB")
json.dump({"credits": credits, "alts": alts}, open(SITE / "data" / "photo-credits.json", "w"), indent=1, ensure_ascii=False)

# Image recipe: one look for every photo

The pipeline script is `tools/process_images.py`. It needs Python 3.12 with `rembg[cpu]`, `pillow`, `numpy` and `certifi`.
Background removal runs locally on this Mac, and nothing is uploaded.

## Two styles, never mixed in one section
| Style | Where | How |
|---|---|---|
| **A. Cut-out on dark steel** | Category cards, product rows | Remove the background (rembg `isnet-general-use`; `u2net` with a tight crop when the background is busy). Feather the edge 1 px, grade the product, and centre it on **#1C2024** at **70% of the frame width** (74% max height). Add a soft shadow: y 12 px, blur 24 px, 35% black. Light 8% vignette. Canvas 1200×900 (4:3). |
| **B. Full graded photo** | Hero, About page, social preview | Crop to the ratio, apply the grade below, then a 10% vignette. The page adds a dark gradient where text sits. |

## Colour grade (in this order)
1. Exposure **−0.2** stop (×0.87).
2. Contrast **+15** (×1.15 around mid-grey).
3. Highlights **−20**: a soft curve above 60% brightness.
4. Shadows **−10**.
5. Temperature **−5**: red ×0.985, blue ×1.02 (cooler steel).
6. Split toning: highlights blended **10% toward #E8A93A** (amber); shadows blended **12% toward #1B2430** (steel navy).
7. Saturation **−15** (×0.85).
8. Clarity **+10**: unsharp mask with a wide radius at 25%. Texture: radius 1.2 at 40% (threads).
9. Vignette **−10** (photos) or **−8** (cards).

## Exports
| Use | Ratio | Widths | Format |
|---|---|---|---|
| Hero (desktop) | 16:9 | 2400 / 1920 / 960 | WebP + JPEG |
| Hero (phone) | 4:5 | 1080 / 540 | WebP + JPEG |
| Category card | 4:3 | 1200 / 960 / 480 | WebP + JPEG |
| About photos | 3:2 | 1440 / 960 / 480 (never upscaled) | WebP + JPEG |
| Social preview | 1.91:1 | 1200×630 | JPEG |

- WebP quality 72, JPEG quality 76, progressive.
- Saving re-encodes the pixels, so location data (EXIF and GPS) is not kept.
- Small sources are never upscaled; the largest export matches the source.

## Rules
- Only licensed images (CC0, public domain, CC BY, CC BY-SA). No "no derivatives" licences, because we crop and edit.
- Never remove watermarks. No other brands' logos, readable foreign price tags or faces.
- Record every image in `docs/image-credits.md` and `data/photo-credits.json`. The credits page reads the same list.
- When our own photos arrive, run them through the same steps so the site keeps one look.

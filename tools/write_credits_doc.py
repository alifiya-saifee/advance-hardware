"""Writes docs/image-credits.md from data/photo-credits.json. Run after tools/process_images.py."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
cr = json.load(open(ROOT / "data" / "photo-credits.json"))["credits"]
md = ["# Image credits", "", "All product and background photos on the site come from Wikimedia Commons under free licences that allow business use and editing.",
      "The same list is shown to visitors on `credits.html` (required by the CC BY and CC BY-SA licences).",
      "Replace these with our own photos when ready (see `photo-shot-list.md`), then update this list.", "",
      "| File | Used for | Original | Author | Licence | Changes |", "|---|---|---|---|---|---|"]
for c in cr:
    md.append(f"| `media/{c['file']}-*` | {c['use']} | [{c['title']}]({c['page']}) | {c['artist']} | [{c['license']}]({c['license_url'] or c['page']}) | {c['changes']} |")
md += ["", "Edited versions of CC BY-SA photos are shared under the same licence (CC BY-SA)."]
(ROOT / "docs" / "image-credits.md").write_text("\n".join(md) + "\n")
print("docs/image-credits.md:", len(cr), "entries")

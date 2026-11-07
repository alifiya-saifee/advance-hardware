"""Brand marks for Advance Hardware: Grade Mark (hexagon bolt head) and the 1996 Seal.
Run: python3 tools/build_brand.py  -> media/brand/*.svg and favicon.svg"""
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media" / "brand"
AMBER, INK, PAPER = "#F2A900", "#111315", "#F4F3EF"

def hexagon(cx, cy, r):
    return " ".join(f"{cx + r*math.cos(math.radians(-90 + 60*i)):.2f},{cy + r*math.sin(math.radians(-90 + 60*i)):.2f}" for i in range(6))

def grade_mark(cx, cy, s, face=AMBER, line=INK):
    """Bolt head seen from above: hexagon, washer ring, three radial grade lines. s = hexagon radius."""
    k = s / 46
    lines = "".join(
        f'<line x1="{cx + 10*k*math.cos(math.radians(a)):.2f}" y1="{cy + 10*k*math.sin(math.radians(a)):.2f}" '
        f'x2="{cx + 23*k*math.cos(math.radians(a)):.2f}" y2="{cy + 23*k*math.sin(math.radians(a)):.2f}"/>' for a in (-90, 30, 150))
    return (f'<polygon points="{hexagon(cx, cy, s)}" fill="{face}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{31*k:.2f}" fill="none" stroke="{line}" stroke-width="{4.2*k:.2f}"/>'
            f'<g stroke="{line}" stroke-width="{7*k:.2f}" stroke-linecap="round">{lines}</g>')

def mark_svg(face=AMBER, line=INK, bg=None):
    bgel = f'<rect width="100" height="100" rx="22" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Advance Hardware">{bgel}{grade_mark(50, 50, 46 if not bg else 40, face, line)}</svg>\n'

def seal_svg(ring=AMBER, text=AMBER, bg=INK, inner_face=AMBER, inner_line=INK):
    r_text = 75.5
    ring_text = "ADVANCE HARDWARE • SHARJAH • SINCE 1996 •"
    circ = 2 * math.pi * r_text
    bgel = f'<circle cx="100" cy="100" r="98" fill="{bg}"/>' if bg else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Advance Hardware, Sharjah, since 1996">
  <defs><path id="ring" d="M {100 - r_text} 100 a {r_text} {r_text} 0 1 1 {2*r_text} 0 a {r_text} {r_text} 0 1 1 {-2*r_text} 0"/></defs>
  {bgel}
  <circle cx="100" cy="100" r="92" fill="none" stroke="{ring}" stroke-width="4"/>
  <circle cx="100" cy="100" r="61" fill="none" stroke="{ring}" stroke-width="2.5"/>
  <text font-family="'Barlow Condensed', 'Arial Narrow', Arial, sans-serif" font-weight="700" font-size="17" letter-spacing="2" fill="{text}">
    <textPath href="#ring" textLength="{circ - 6:.1f}" lengthAdjust="spacing">{ring_text}</textPath>
  </text>
  {grade_mark(100, 100, 44, inner_face, inner_line)}
</svg>
'''

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "grade-mark.svg": mark_svg(),                                   # amber mark, transparent background
        "grade-mark-ink.svg": mark_svg(face=INK, line=PAPER),           # one-colour dark (stamps, light paper)
        "grade-mark-tile.svg": mark_svg(bg=INK),                        # on a dark rounded tile (app icon)
        "seal-dark.svg": seal_svg(),                                    # amber on graphite (profile pictures)
        "seal-light.svg": seal_svg(bg=PAPER),                           # amber on paper
        "seal-ink.svg": seal_svg(ring=INK, text=INK, bg="#FFFFFF", inner_face=INK, inner_line="#FFFFFF"),  # one-colour black (rubber stamp, invoices)
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg)
    (ROOT / "favicon.svg").write_text(mark_svg())
    print("wrote", ", ".join(files), "+ favicon.svg")

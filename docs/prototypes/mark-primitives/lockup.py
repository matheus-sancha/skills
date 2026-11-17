"""Horizontal lockup: letterform r3 mark + outlined wordmark (text is never live <text>).

Usage: python -B lockup.py FONT.otf OUT_DIR
Mark height = 1.6 x the wordmark's ascender height ('h'); gap = 0.45 x mark width.
Both ratios are mark-craft rule 21's PROPOSED defaults (no primary source).
"""
import io
import sys

import resvg_py
from PIL import Image

from brand import BRIEF, SLATE
from outline_text import outline
from primitives import Mark, Shape
from recipe_letterform import build


def main(font, out):
    m, layers = build("r3")
    word, adv = outline(font, BRIEF["name"].lower(), size=100, tracking=-10)
    asc = Shape(word, "word")
    m.log.append({"op": "outline_text", "font": font.rsplit("/", 1)[-1], "text": BRIEF["name"].lower(),
                  "size": 100, "tracking": -10, "advance": round(adv, 2), "bounds": asc.bounds})
    wx0, wy0, wx1, wy1 = word.bounds          # wy0 = top of ascender, wy1 = baseline (no descender... 'p' has one)
    base = 100.0                               # outline() puts the baseline at y = size
    asc_h = base - wy0
    mx0, my0, mx1, my1 = (min(s.path.bounds[i] for s, _ in layers) if i < 2 else
                          max(s.path.bounds[i] for s, _ in layers) for i in range(4))
    k = m.note_param("mark_scale", round(1.6 * asc_h / (my1 - my0), 4), "mark h = 1.6 x ascender (rule 21 default)")
    gap = m.note_param("gap", round(0.45 * (mx1 - mx0) * k, 3), "0.45 x mark width (rule 21 default)")
    # mark bottom on the baseline, top 1.6 ascenders up
    placed = [(m._affine("place", s, (k, 0, 0, k, -mx0 * k, base - my1 * k)), c) for s, c in layers]
    wx = (mx1 - mx0) * k + gap - wx0
    wpath = word.transform(1, 0, 0, 1, wx, 0)
    wshape = Shape(wpath, "word")
    allb = [p.path.bounds for p, _ in placed] + [wpath.bounds]
    x0 = min(b[0] for b in allb); y0 = min(b[1] for b in allb)
    x1 = max(b[2] for b in allb); y1 = max(b[3] for b in allb)
    pad = 0.25 * (y1 - y0)                     # clear space: 25 % of mark height (rule 18 default)
    vb = f"{x0 - pad:.2f} {y0 - pad:.2f} {x1 - x0 + 2 * pad:.2f} {y1 - y0 + 2 * pad:.2f}"
    body = "\n".join(f'  <path fill="{c}" d="{s.d()}"/>' for s, c in placed + [(wshape, SLATE)])
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n{body}\n</svg>\n'
    open(f"{out}/lockup.svg", "w").write(svg)
    ratio = (x1 - x0 + 2 * pad) / (y1 - y0 + 2 * pad)
    tiles = []
    for w in (640, 160, 96):
        png = resvg_py.svg_to_bytes(svg_string=svg, width=w, height=round(w / ratio), background="#ffffff")
        tiles.append(Image.open(io.BytesIO(bytes(png))).convert("RGB"))
    sheet = Image.new("RGB", (660, sum(t.height for t in tiles) + 40), "#e8e8e8")
    y = 10
    for t in tiles:
        sheet.paste(t, (10, y)); y += t.height + 10
    sheet.save(f"{out}/lockup.sheet.png", optimize=True)
    print(f"{out}/lockup.svg  asc_h={asc_h:.1f} scale={k} gap={gap}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

"""Render one comparison board per anchor set from the fetched cache.

Usage: python -B render_board.py anchors.json CACHE_DIR OUT_DIR

Each board: one column per anchor; rows = 160 px colour, 160 px mono (every painted pixel
black, so it reads as a silhouette: internal colour separation is lost on purpose), then
48 px and 16 px at 1:1 with the 16 px also shown x6 nearest-neighbour. Marks are fitted to
the same box, preserving aspect. Throwaway prototype for issue 28.
"""
import io
import json
import re
import sys
from pathlib import Path

import resvg_py
from PIL import Image, ImageDraw


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def render_fit(svg, box, bg="#ffffff"):
    """Render the SVG so its longer side fills `box`, centred on a box x box tile."""
    m = re.search(r'viewBox="\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)', svg)
    if m:
        w, h = float(m.group(3)), float(m.group(4))
    else:  # no viewBox: derive one from width/height so resvg can scale it
        tag = svg[svg.find("<svg"):].split(">", 1)[0]
        w = float(re.search(r'width="([\d.]+)', tag).group(1))
        h = float(re.search(r'height="([\d.]+)', tag).group(1))
        svg = svg.replace("<svg", f'<svg viewBox="0 0 {w} {h}"', 1)
    i = svg.find("<svg")
    j = svg.find(">", i)
    svg = svg[:i] + re.sub(r'\s(width|height)="[^"]*"', "", svg[i:j]) + svg[j:]
    if w >= h:
        pw, ph = box, max(1, round(box * h / w))
    else:
        pw, ph = max(1, round(box * w / h)), box
    raw = resvg_py.svg_to_bytes(svg_string=svg, width=pw, height=ph)
    mark = Image.open(io.BytesIO(bytes(raw))).convert("RGBA")
    tile = Image.new("RGBA", (box, box), bg)
    tile.alpha_composite(mark, ((box - pw) // 2, (box - ph) // 2))
    return tile.convert("RGB"), mark


def mono(mark, box):
    a = mark.getchannel("A").point(lambda v: 255 if v > 0 else 0).point(lambda v: v)
    sil = Image.new("RGBA", mark.size, (0, 0, 0, 0))
    sil.paste((0, 0, 0, 255), mask=mark.getchannel("A"))
    tile = Image.new("RGBA", (box, box), "#ffffff")
    tile.alpha_composite(sil, ((box - mark.width) // 2, (box - mark.height) // 2))
    return tile.convert("RGB")


def board(set_name, anchors, cache, out):
    col, gap, head = 180, 14, 40
    items = [(a["name"], cache / set_name / f"{slug(a['name'])}.svg") for a in anchors]
    items = [(n, p) for n, p in items if p.exists()]
    W = gap + len(items) * (col + gap)
    H = head + 160 + gap + 160 + gap + 48 + gap + 96 + 40
    im = Image.new("RGB", (W, H), "#e8e8e8")
    dr = ImageDraw.Draw(im)
    dr.text((gap, 10), f"Anchor set: {set_name}  (approved on issue 28; colour / silhouette / 48 px / 16 px and 16 px x6)", fill="#222")
    for i, (name, p) in enumerate(items):
        svg = p.read_text(encoding="utf-8")
        x = gap + i * (col + gap)
        y = head
        dr.text((x, y - 16), name, fill="#111")
        t, mark = render_fit(svg, 160)
        im.paste(t, (x, y)); y += 160 + gap
        im.paste(mono(mark, 160), (x, y)); y += 160 + gap
        im.paste(render_fit(svg, 48)[0], (x, y))
        s16 = render_fit(svg, 16)[0]
        im.paste(s16, (x + 64, y + 16))
        y += 48 + gap
        im.paste(s16.resize((96, 96), Image.NEAREST), (x, y))
    out.mkdir(parents=True, exist_ok=True)
    im.save(out / f"board-{set_name}.png")
    print(out / f"board-{set_name}.png")


def main(manifest, cache, out):
    sets = json.loads(Path(manifest).read_text(encoding="utf-8"))["sets"]
    for set_name, anchors in sets.items():
        board(set_name, anchors, Path(cache), Path(out))


if __name__ == "__main__":
    main(*sys.argv[1:4])

"""Reaction boards: palette, shape and style, six lettered tiles each (issue 14).

Each board is written as <board>.r<N>.png plus <board>.r<N>.json holding one parameter record
per tile, so a "more of / not this" reaction maps straight onto constraints for Routes.
No third-party logos ever appear on a board.

Usage: python -B -m brandkit.boards OUT_DIR --name NAME [--fonts DIR] [--seed N] [--rev r1]
"""
import argparse
import io
import json
import random
from pathlib import Path

import resvg_py
from PIL import Image, ImageDraw

from .palette import oklch_to_hex
from .primitives import Mark

LETTERS = "ABCDEF"
TILE, PAD, HEAD = 300, 16, 28


def _png(svg, w, h):
    im = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg, width=w, height=h)))).convert("RGBA")
    bg = Image.new("RGBA", im.size, "#ffffff")
    return Image.alpha_composite(bg, im).convert("RGB")


def _sheet(title, tiles):
    """tiles: list of (PIL image, caption)."""
    W = 3 * TILE + 4 * PAD
    H = HEAD + 2 * (TILE + HEAD) + 3 * PAD
    im = Image.new("RGB", (W, H), "#f4f4f2")
    d = ImageDraw.Draw(im)
    d.text((PAD, 8), title, fill="#222222")
    for i, (t, cap) in enumerate(tiles):
        x = PAD + (i % 3) * (TILE + PAD)
        y = HEAD + PAD + (i // 3) * (TILE + HEAD + PAD)
        im.paste(t.resize((TILE, TILE)), (x, y))
        d.text((x, y + TILE + 6), f"{LETTERS[i]}  {cap}", fill="#222222")
    return im


# -- palette -----------------------------------------------------------------
PALETTE_FAMILIES = [
    {"label": "warm vivid", "hues": [30, 60], "chroma": "high", "neutral": "warm"},
    {"label": "cool vivid", "hues": [250, 190], "chroma": "high", "neutral": "cool"},
    {"label": "earthy muted", "hues": [55, 140], "chroma": "low", "neutral": "warm"},
    {"label": "ink and spark", "hues": [260, 25], "chroma": "mixed", "neutral": "cool"},
    {"label": "fresh green", "hues": [150, 95], "chroma": "medium", "neutral": "neutral"},
    {"label": "deep jewel", "hues": [320, 200], "chroma": "medium", "neutral": "cool"},
]
_C = {"high": 0.17, "medium": 0.11, "low": 0.06, "mixed": None}


def palette_tile(fam):
    hues = fam["hues"]
    c1 = _C[fam["chroma"]] or 0.05
    c2 = _C[fam["chroma"]] or 0.19
    neutral_h = {"warm": 70, "cool": 250, "neutral": 0}[fam["neutral"]]
    nc = 0 if fam["neutral"] == "neutral" else 0.012
    sw = [oklch_to_hex(0.97, nc, neutral_h), oklch_to_hex(0.25, nc * 1.5, neutral_h),
          oklch_to_hex(0.55, c1, hues[0]), oklch_to_hex(0.72, c2, hues[1])]
    rects = [f'<rect x="0" y="0" width="300" height="300" fill="{sw[0]}"/>',
             f'<rect x="0" y="190" width="300" height="110" fill="{sw[1]}"/>',
             f'<rect x="30" y="30" width="150" height="130" fill="{sw[2]}"/>',
             f'<rect x="190" y="30" width="80" height="130" fill="{sw[3]}"/>']
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">{"".join(rects)}</svg>'
    return _png(svg, TILE, TILE), {**fam, "swatches": sw}


# -- shape -------------------------------------------------------------------
SHAPE_STUDIES = [
    {"label": "sharp geometric", "corners": "sharp", "weight": "heavy", "form": "geometric"},
    {"label": "round geometric", "corners": "round", "weight": "heavy", "form": "geometric"},
    {"label": "light line", "corners": "round", "weight": "light", "form": "geometric"},
    {"label": "soft organic", "corners": "round", "weight": "medium", "form": "organic"},
    {"label": "cut and angled", "corners": "cut", "weight": "medium", "form": "geometric"},
    {"label": "stacked blocks", "corners": "small-round", "weight": "heavy", "form": "modular"},
]


def shape_tile(study, seed):
    rnd = random.Random(seed)
    m = Mark(study["label"], 100)
    form, corners, weight = study["form"], study["corners"], study["weight"]
    if form == "organic":
        a = m.circle(42, 50, 30); b = m.circle(62, 44, 22)
        s = m.union(a, b)
    elif form == "modular":
        r = {"small-round": 4}.get(corners, 0)
        s = m.union(*[m.rounded_rect(14 + (i % 3) * 25, 22 + (i // 3) * 30, 21, 26, r)
                      for i in range(6) if rnd.random() > 0.15 or i == 0])
    elif weight == "light":
        s = m.union(m.stroke([(20, 75), (50, 22), (80, 75)], 6, cap="round", join="round"),
                    m.stroke([(30, 75), (70, 75)], 6, cap="round"))
    else:
        if corners == "sharp":
            s = m.difference(m.regular_polygon(50, 52, 40, 3), m.regular_polygon(50, 60, 14, 3))
        elif corners == "cut":
            s = m.polygon([(20, 30), (70, 20), (82, 50), (60, 82), (18, 70)])
            s = m.cut_at_line(s, (0, 45), (100, 35), keep="right")
        else:
            s = m.difference(m.circle(50, 50, 38), m.rounded_rect(36, 36, 28, 28, 14))
    svg = m.svg([(s, "#1d1d1b")], pad=8)
    return _png(svg, TILE, TILE), dict(study)


# -- style -------------------------------------------------------------------
def style_tiles(name, font_dir):
    from .outline_text import outline
    from .primitives import Shape
    fonts = sorted(p for p in Path(font_dir).glob("*.[ot]tf")) if font_dir else []
    variants = [("lower", ""), ("upper", ""), ("title", "")]
    tiles = []
    for i in range(6):
        if not fonts:
            break
        f = fonts[i % len(fonts)]
        case = variants[i % 3][0]
        text = {"lower": name.lower(), "upper": name.upper(), "title": name.title()}[case]
        tracking = 40 if case == "upper" else -10
        wght = 700 if i % 2 == 0 else 450
        path, _ = outline(str(f), text, size=100, wght=wght, tracking=tracking)
        d = Shape(path, "w").d()
        x0, y0, x1, y1 = path.bounds
        w, h = x1 - x0, y1 - y0
        pad = 0.15 * max(w, h)
        side = max(w, h) + 2 * pad
        vb = f"{x0 - (side - w) / 2:.1f} {y0 - (side - h) / 2:.1f} {side:.1f} {side:.1f}"
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
               f'<rect x="-10000" y="-10000" width="20000" height="20000" fill="#ffffff"/>'
               f'<path fill="#1d1d1b" d="{d}"/></svg>')
        tiles.append((_png(svg, TILE, TILE), {"label": f"{f.stem} {case}", "font": f.name,
                                               "case": case, "tracking": tracking, "wght": wght}))
    return tiles


def build(out_dir, name, font_dir=None, seed=1, rev="r1"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    written = []
    boards = {
        "palette": [palette_tile(f) for f in PALETTE_FAMILIES],
        "shape": [shape_tile(s, seed + i) for i, s in enumerate(SHAPE_STUDIES)],
        "style": style_tiles(name, font_dir),
    }
    for board, tiles in boards.items():
        if not tiles:
            continue
        img = _sheet(f"{name} · {board} board · react: up to two 'more of', up to two 'not this'",
                     [(t, rec["label"]) for t, rec in tiles])
        png = out / f"{board}.{rev}.png"
        img.save(png, optimize=True)
        recs = {LETTERS[i]: rec for i, (_, rec) in enumerate(tiles)}
        (out / f"{board}.{rev}.json").write_text(json.dumps(recs, indent=1), encoding="utf-8")
        written.append(str(png))
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--name", required=True)
    ap.add_argument("--fonts"); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--rev", default="r1")
    a = ap.parse_args()
    for p in build(a.out, a.name, a.fonts, a.seed, a.rev):
        print(p)

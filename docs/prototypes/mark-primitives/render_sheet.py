"""Render an SVG with resvg-py at 256/48/32/16 px in colour, mono and reversed, onto one PNG.

Usage: python -B render_sheet.py MARK.svg OUT.png [--title TEXT]

Each row: 256 px | 48, 32, 16 px at 1:1 | 32 px x4 and 16 px x8 (nearest-neighbour, to show pixels).
Mono = every fill/stroke colour replaced by black; reversed = white on black.
"""
import argparse
import io
import re

import resvg_py
from PIL import Image, ImageDraw

COLOUR = re.compile(r'(fill|stroke)="(#[0-9a-fA-F]{3,8}|black|white)"')


def split_defs(svg):
    """(prefix incl. </defs>, drawable rest). Colours inside <defs> (mask/clip luminance) must
    never be recoloured: doing so silently broke the hand-written mark's mono render."""
    i = svg.find("</defs>")
    return (svg[:i + 7], svg[i + 7:]) if i >= 0 else ("", svg)


def recolour(svg, colour):
    head, body = split_defs(svg)
    return head + COLOUR.sub(lambda m: f'{m.group(1)}="{colour}"', body)


def render(svg, px, background=None):
    kw = {"svg_string": svg, "width": px, "height": px}
    if background:
        kw["background"] = background
    return Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(**kw)))).convert("RGBA")


def variants(svg):
    return [("colour", svg, "#ffffff"), ("mono", recolour(svg, "#000000"), "#ffffff"),
            ("reversed", recolour(svg, "#ffffff"), "#000000")]


def sheet(svg, title=""):
    gap, head = 16, 28
    W = gap + 256 + gap + (48 + gap + 32 + gap + 16 + gap) + 128 + gap + 128 + gap
    H = head + 3 * (256 + gap) + 20
    im = Image.new("RGB", (W, H), "#e8e8e8")
    dr = ImageDraw.Draw(im)
    dr.text((gap, 8), title, fill="#222")
    for row, (label, s, bg) in enumerate(variants(svg)):
        y = head + row * (256 + gap)
        x = gap
        for px in (256, 48, 32, 16):
            tile = render(s, px, bg)
            im.paste(tile.convert("RGB"), (x, y))
            dr.text((x, y + max(px, 0) + 1), f"{px}", fill="#666") if px < 256 else None
            x += px + gap
        for px, k in ((32, 4), (16, 8)):
            tile = render(s, px, bg).resize((px * k, px * k), Image.NEAREST)
            im.paste(tile.convert("RGB"), (x, y))
            dr.text((x, y + 129), f"{px}px x{k}", fill="#666")
            x += 128 + gap
        dr.text((W - 70, y + 240), label, fill="#666")
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg"); ap.add_argument("out"); ap.add_argument("--title", default="")
    a = ap.parse_args()
    svg = open(a.svg).read()
    sheet(svg, a.title or a.svg.rsplit("/", 1)[-1]).save(a.out, optimize=True)
    print(a.out)


if __name__ == "__main__":
    main()

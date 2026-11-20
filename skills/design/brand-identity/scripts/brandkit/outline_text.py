"""Outline a word: HarfBuzz shapes, fontTools draws into a pathops.Path.

Usage (CLI): python -B outline_text.py FONT TEXT OUT.svg [--size 100] [--wght 700] [--tracking 0]
Library:     outline(font_path, text, size, wght=None, tracking=0) -> (pathops.Path, advance)

Tracking is in units of 1/1000 em, added after every glyph but the last.
WOFF2 is NOT accepted by HarfBuzz (svg-tooling section 4): decompress to TTF first.
"""
import argparse

import pathops
import uharfbuzz as hb
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont


def outline(font_path, text, size=100.0, wght=None, tracking=0.0, baseline=None):
    blob = hb.Blob.from_file_path(font_path)
    font = hb.Font(hb.Face(blob))
    tt = TTFont(font_path)
    upem = tt["head"].unitsPerEm
    loc = None
    if wght is not None and "fvar" in tt:
        font.set_variations({"wght": wght})
        loc = {"wght": wght}
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    gs = tt.getGlyphSet(location=loc) if loc else tt.getGlyphSet()
    order = tt.getGlyphOrder()
    s = size / upem
    y0 = size if baseline is None else baseline  # baseline in y-down space
    out = pathops.Path()
    pen = out.getPen(glyphSet=gs)  # glyphSet lets composite glyphs (e.g. accents, 'i') decompose
    x = 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        name = order[info.codepoint]  # after shaping, codepoint holds the glyph id
        gx = x + pos.x_offset * s
        gy = y0 - pos.y_offset * s
        gs[name].draw(TransformPen(pen, (s, 0, 0, -s, gx, gy)))
        x += pos.x_advance * s + (tracking * size / 1000 if i < n - 1 else 0)
    out.simplify()  # remove overlaps (variable fonts ship overlapping contours)
    return out, x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("font"); ap.add_argument("text"); ap.add_argument("out")
    ap.add_argument("--size", type=float, default=100); ap.add_argument("--wght", type=float)
    ap.add_argument("--tracking", type=float, default=0)
    a = ap.parse_args()
    p, adv = outline(a.font, a.text, a.size, a.wght, a.tracking)
    pen = SVGPathPen(None)
    p.draw(pen)
    x0, y0, x1, y1 = p.bounds
    with open(a.out, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - 5:.2f} {y0 - 5:.2f} {x1 - x0 + 10:.2f} {y1 - y0 + 10:.2f}">'
                f'<path d="{pen.getCommands()}"/></svg>\n')
    print(f"advance={adv:.2f} bounds={tuple(round(v, 2) for v in p.bounds)}")


if __name__ == "__main__":
    main()

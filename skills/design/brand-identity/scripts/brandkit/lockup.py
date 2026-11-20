"""Lockups: mark + outlined wordmark, using the ratios calibrated in issue 27.

Defaults (docs/research/craft-calibration.md):
- mark height = 1.5 x cap height (flag outside 1.3-2.5)
- gap = 0.4 x cap height (flag > 0.4 x mark width or < 0.2 x cap)
- horizontal: mark centred on the cap band
- clear space = 0.5 x mark height
Text is always outlined; the output never contains <text>.

Usage: python -m brandkit.lockup MARK.svg FONT NAME OUT.svg [--layout horizontal|stacked] [--fill #hex]
"""
import argparse
import re

import pathops
from fontTools.ttLib import TTFont
from svgpathtools import parse_path

from .outline_text import outline

MARK_CAP = 1.5
GAP_CAP = 0.4
CLEAR = 0.5


def _paths(svg_text):
    """(d, fill) pairs from a flattened mark SVG (top-level <path> elements only)."""
    out = []
    for m in re.finditer(r"<path\b([^>]*)/?>", svg_text):
        attrs = m.group(1)
        d = re.search(r'\sd="([^"]+)"', attrs)
        f = re.search(r'fill="([^"]+)"', attrs)
        if d:
            out.append((d.group(1), f.group(1) if f else "#000000"))
    return out


def _bounds(ds):
    xs0, ys0, xs1, ys1 = [], [], [], []
    for d in ds:
        x0, x1, y0, y1 = parse_path(d).bbox()
        xs0.append(x0); xs1.append(x1); ys0.append(y0); ys1.append(y1)
    return min(xs0), min(ys0), max(xs1), max(ys1)


def cap_height(font_path, size):
    f = TTFont(font_path)
    upm = f["head"].unitsPerEm
    cap = getattr(f["OS/2"], "sCapHeight", 0) or 0.7 * upm
    return cap * size / upm


def lockup(mark_svg, font_path, name, layout="horizontal", fill="#000000", size=100.0, tracking=0.0,
           mark_cap=MARK_CAP, gap_cap=GAP_CAP):
    marks = _paths(mark_svg)
    mx0, my0, mx1, my1 = _bounds([d for d, _ in marks])
    word, adv = outline(font_path, name, size=size, tracking=tracking)
    wx0, wy0, wx1, wy1 = word.bounds
    cap = cap_height(font_path, size)
    base = size                                   # outline() puts the baseline at y = size
    k = mark_cap * cap / (my1 - my0)
    mw, mh = (mx1 - mx0) * k, (my1 - my0) * k
    gap = gap_cap * cap
    if layout == "horizontal":
        cap_mid = base - cap / 2
        tx, ty = -mx0 * k, cap_mid - mh / 2 - my0 * k
        wdx, wdy = mw + gap - wx0, 0
    else:  # stacked: mark centred above the word
        ww = wx1 - wx0
        tx, ty = (ww - mw) / 2 - mx0 * k, (base - cap) - gap - mh - my0 * k
        wdx, wdy = -wx0, 0
    wpath = word.transform(1, 0, 0, 1, wdx, wdy)
    from fontTools.pens.svgPathPen import SVGPathPen
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.3f}".rstrip("0").rstrip("."))
    wpath.draw(pen)
    wd = pen.getCommands()
    x0 = min(tx + mx0 * k, wpath.bounds[0]); y0 = min(ty + my0 * k, wpath.bounds[1])
    x1 = max(tx + mx1 * k, wpath.bounds[2]); y1 = max(ty + my1 * k, wpath.bounds[3])
    pad = CLEAR * mh
    vb = f"{x0 - pad:.2f} {y0 - pad:.2f} {x1 - x0 + 2 * pad:.2f} {y1 - y0 + 2 * pad:.2f}"
    body = "\n".join(f'    <path fill="{f}" d="{d}"/>' for d, f in marks)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n'
           f'  <g transform="matrix({k:.6f} 0 0 {k:.6f} {tx:.3f} {ty:.3f})">\n{body}\n  </g>\n'
           f'  <path fill="{fill}" d="{wd}"/>\n</svg>\n')
    report = {
        "layout": layout, "mark_h_over_cap": round(float(mh / cap), 3), "gap_over_cap": round(gap / cap, 3),
        "gap_over_mark_w": round(float(gap / mw), 3), "clear_space_over_mark_h": CLEAR,
        "flags": [],
    }
    if not 1.3 <= mh / cap <= 2.5:
        report["flags"].append("mark height outside 1.3-2.5x cap")
    if gap / mw > 0.4 or gap / cap < 0.2:
        report["flags"].append("gap outside 0.2x cap .. 0.4x mark width")
    return svg, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mark"); ap.add_argument("font"); ap.add_argument("name"); ap.add_argument("out")
    ap.add_argument("--layout", default="horizontal"); ap.add_argument("--fill", default="#000000")
    ap.add_argument("--tracking", type=float, default=0.0)
    a = ap.parse_args()
    svg, rep = lockup(open(a.mark, encoding="utf-8").read(), a.font, a.name, a.layout, a.fill, tracking=a.tracking)
    open(a.out, "w", encoding="utf-8").write(svg)
    print(rep)


if __name__ == "__main__":
    main()

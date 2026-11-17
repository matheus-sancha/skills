"""Script half of the render-then-rubric gate (mark-craft rules 7, 14, 15, 17; rule 6 info only).

Usage: python -B checks.py MARK.svg [--box 100] [--json OUT.json]

All raster checks use resvg-py (the pinned gate renderer) and alpha >= 0.5 as "ink".
Thresholds are the research notes' PROPOSED DEFAULTS, uncalibrated.

min stroke / min gap @16 (rule 14, absolute):
  Render mono at HI px. Morphological opening with a disk of diameter d removes every
  part of the shape thinner than d. Parts removed that are larger than a corner sliver
  (area > d^2) count as "thinner than d". We sweep d (in px-at-16) and report the
  largest d with no such part. Same on the background for gaps/counters.
  Pass: >= 1.0 px at 16. This is the check svg-tooling 5.2 says SSIM cannot replace.
extrema (rule 7): every cubic/quadratic whose x or y extremum pokes beyond its
  endpoints by > 0.5 % of the box must have a node there.
ssim16 (rule 15): mono 16 px render vs 256 px render box-downsampled to 16. Pass >= 0.8.
mono distinct (rule 17): every pair of differently coloured layers stays >= 1 px apart
  at 32 px; and parts/holes counted at HI survive at 32 px.
centroid (rule 6): area centroid vs bbox centre, % of box. Info only.
"""
import argparse
import io
import json
import re

import numpy as np
import resvg_py
from PIL import Image
from scipy import ndimage as ndi
from skimage.metrics import structural_similarity
from svgpathtools import CubicBezier, QuadraticBezier, svg2paths

from render_sheet import recolour, split_defs

HI = 512
COLOUR = re.compile(r'(fill|stroke)="(#[0-9a-fA-F]{3,8})"')


def alpha(svg, px):
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=px, height=px))
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"), dtype=float)[..., 3] / 255.0


def mono(svg):
    return recolour(svg, "#000000")


def opening(mask, r):
    """Binary opening with a disk of radius r, via two Euclidean distance transforms."""
    eroded = ndi.distance_transform_edt(mask) > r
    if not eroded.any():
        return eroded
    return ndi.distance_transform_edt(~eroded) <= r


def thin_parts(mask, d_hi):
    lost = mask & ~opening(mask, d_hi / 2 - 0.5)  # half-pixel tolerance at HI
    lab, n = ndi.label(lost)
    if n == 0:
        return 0
    sizes = ndi.sum(lost, lab, range(1, n + 1))
    return int((sizes > d_hi ** 2).sum())


def min_width_at16(mask, sweep=(0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0)):
    k = HI / 16
    best = 0.0
    for d in sweep:
        if thin_parts(mask, d * k):
            break
        best = d
    return best


def topology(mask):
    _, parts = ndi.label(mask, structure=np.ones((3, 3)))
    bg, nb = ndi.label(~mask)
    border = set(np.unique(np.concatenate([bg[0], bg[-1], bg[:, 0], bg[:, -1]]))) - {0}
    return parts, nb - len(border)


def extrema(svg_path, box):
    eps = 0.005 * box
    paths, _ = svg2paths(svg_path)
    misses, segs, arcs = [], 0, 0
    for p in paths:
        for seg in p:
            segs += 1
            if not isinstance(seg, (CubicBezier, QuadraticBezier)):
                arcs += type(seg).__name__ == "Arc"
                continue
            poly = seg.poly()
            for part, name in ((np.real, "x"), (np.imag, "y")):
                c = np.poly1d(part(poly.coeffs)).deriv()
                for t in np.atleast_1d(c.roots):
                    if abs(np.imag(t)) > 1e-9 or not (1e-3 < np.real(t) < 1 - 1e-3):
                        continue
                    t = float(np.real(t))
                    v = part(seg.point(t)); a, b = part(seg.start), part(seg.end)
                    excess = v - max(a, b) if v > max(a, b) else (min(a, b) - v if v < min(a, b) else 0)
                    if excess > eps:
                        q = seg.point(t)
                        misses.append(f"{name}@({q.real:.1f},{q.imag:.1f}) +{excess:.2f}")
    return misses, segs, arcs


def layer_masks(svg):
    head, body = split_defs(svg)
    colours = sorted(set(c for _, c in COLOUR.findall(body)))
    out = {}
    for c in colours:
        only = head + COLOUR.sub(lambda m: f'{m.group(1)}="{"#000000" if m.group(2) == c else "none"}"', body)
        out[c] = alpha(only, HI) >= 0.5
    return out


def run(svg_path, box=100.0):
    svg = open(svg_path).read()
    m = mono(svg)
    hi = alpha(m, HI) >= 0.5
    res = []

    w = min_width_at16(hi)
    res.append(("min stroke @16px", f"{w:.2f} px" + (" (<0.5)" if w == 0 else ""), w >= 1.0))
    canvas = ~hi
    g = min_width_at16(canvas)
    res.append(("min gap/counter @16px", f"{g:.2f} px" + (" (<0.5)" if g == 0 else ""), g >= 1.0))

    misses, segs, arcs = extrema(svg_path, box)
    detail = f"{len(misses)} missing / {segs} segs" + (f", {arcs} native arcs" if arcs else "")
    if misses:
        detail += ": " + "; ".join(misses[:3]) + ("..." if len(misses) > 3 else "")
    res.append(("extrema nodes (rule 7)", detail, not misses))

    a16 = alpha(m, 16)
    a256 = alpha(m, 256)
    d16 = np.asarray(Image.fromarray((a256 * 255).astype(np.uint8)).resize((16, 16), Image.BOX), float) / 255
    s = structural_similarity(a16, d16, data_range=1.0, win_size=7)
    res.append(("SSIM 16 vs 256->16", f"{s:.3f}", s >= 0.8))

    layers = layer_masks(svg)
    gaps = []
    names = list(layers)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            dist = ndi.distance_transform_edt(~layers[names[j]])
            gaps.append(float(dist[layers[names[i]]].min()) * 32 / HI if layers[names[i]].any() else 99)
    t_hi = topology(hi)
    t32 = topology(alpha(m, 32) >= 0.5)
    t16 = topology(a16 >= 0.5)
    sep_ok = all(x >= 1.0 for x in gaps)
    topo_ok = t32 == t_hi
    sep = (f"{len(names)} colours, min sep {min(gaps):.2f} px@32" if gaps else "1 colour")
    res.append(("mono distinct (rule 17)",
                f"{sep}; parts/holes {t_hi[0]}/{t_hi[1]} @{HI} -> {t32[0]}/{t32[1]} @32 -> {t16[0]}/{t16[1]} @16",
                sep_ok and topo_ok))

    ys, xs = np.nonzero(hi)
    cy, cx = ys.mean(), xs.mean()
    by, bx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
    off = np.hypot(cx - bx, cy - by) / HI * 100
    res.append(("centroid vs bbox (info)", f"{off:.1f} % of box (dx {100*(cx-bx)/HI:+.1f}, dy {100*(cy-by)/HI:+.1f})", None))
    return [(k, v, None if ok is None else bool(ok)) for k, v, ok in res]


def table(name, res):
    lines = [f"| check ({name}) | value | result |", "|---|---|---|"]
    for k, v, ok in res:
        lines.append(f"| {k} | {v} | {'info' if ok is None else ('PASS' if ok else 'FAIL')} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg"); ap.add_argument("--box", type=float, default=100); ap.add_argument("--json")
    a = ap.parse_args()
    res = run(a.svg, a.box)
    name = a.svg.rsplit("/", 1)[-1]
    print(table(name, res))
    if a.json:
        json.dump([{"check": k, "value": v, "pass": ok} for k, v, ok in res], open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()

"""Silhouette similarity between a candidate mark and reference marks (gate flag, never a hard fail).

Each SVG is rendered in mono, cropped to its ink bbox, padded to a square and resized to 64 px.
The score is the best IoU over the 8 rotations/reflections. FLAG_AT is a proposed default,
to be calibrated in the sample runs (issue 19).

Usage: python -B -m brandkit.similarity CANDIDATE.svg REF.svg [REF2.svg ...]
"""
import io
import sys
from pathlib import Path

import numpy as np
import resvg_py
from PIL import Image

from .render_sheet import recolour

SIZE = 64
FLAG_AT = 0.80


def silhouette(svg_text, size=SIZE):
    png = bytes(resvg_py.svg_to_bytes(svg_string=recolour(svg_text, "#000000"), width=512, height=512))
    a = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))[..., 3] >= 128
    ys, xs = np.nonzero(a)
    if not len(ys):
        return np.zeros((size, size), bool)
    crop = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = crop.shape
    n = max(h, w)
    sq = np.zeros((n, n), bool)
    sq[(n - h) // 2:(n - h) // 2 + h, (n - w) // 2:(n - w) // 2 + w] = crop
    im = Image.fromarray((sq * 255).astype(np.uint8)).resize((size, size), Image.BOX)
    return np.asarray(im) >= 128


def score(a, b):
    best = 0.0
    for k in range(4):
        for flip in (False, True):
            t = np.rot90(b, k)
            t = np.fliplr(t) if flip else t
            inter = (a & t).sum()
            union = (a | t).sum() or 1
            best = max(best, inter / union)
    return float(best)


def compare(candidate_svg, refs):
    """refs: {name: svg_text}. Returns [(name, score, flagged)] sorted by score."""
    c = silhouette(candidate_svg)
    out = [(name, round(score(c, silhouette(svg)), 3)) for name, svg in refs.items()]
    return sorted(((n, s, s >= FLAG_AT) for n, s in out), key=lambda r: -r[1])


if __name__ == "__main__":
    cand = Path(sys.argv[1]).read_text(encoding="utf-8")
    refs = {Path(p).stem: Path(p).read_text(encoding="utf-8") for p in sys.argv[2:]}
    for name, s, flag in compare(cand, refs):
        print(f"{name}\t{s:.3f}\t{'FLAG' if flag else ''}")

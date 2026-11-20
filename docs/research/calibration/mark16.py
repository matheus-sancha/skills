"""16 px calibration on known-good marks: min stroke/gap at 16 px (same opening method
as docs/prototypes/mark-primitives/checks.py), SSIM 16 vs 256->16, centroid offset.
Ink = pixel visibly differs from a white ground (so white inner details count as gaps).
Mark is fitted so its larger side = the target size, no padding (best case for the mark).
Usage: python -I mark16.py name=path.svg ..."""
import io, sys
import numpy as np, resvg_py
from PIL import Image
from scipy import ndimage as ndi
from skimage.metrics import structural_similarity

HI = 512


def raster(svg, side):
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=side))
    a = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"), float) / 255
    ink = a[..., 3] * (1 - a[..., :3].min(-1))  # distance from white
    ys, xs = np.nonzero(ink > 0.02)
    ink = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = ink.shape
    s = max(h, w)
    sq = np.zeros((s, s)); sq[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = ink
    return sq


def fit(svg, side):
    """Render so the ink's larger side is exactly `side` px."""
    big = raster(svg, side * 8)
    k = side * 8 * side / big.shape[0]
    return raster(svg, int(round(k)))


def opening(mask, r):
    er = ndi.distance_transform_edt(mask) > r
    return ndi.distance_transform_edt(~er) <= r if er.any() else er


def thin(mask, d):
    lost = mask & ~opening(mask, d / 2 - 0.5)
    lab, n = ndi.label(lost)
    return n and int((ndi.sum(lost, lab, range(1, n + 1)) > d * d).sum())


def minw(mask, sweep=(0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0)):
    k, best = mask.shape[0] / 16, 0.0
    for d in sweep:
        if thin(mask, d * k): break
        best = d
    return best


def run(svg):
    hi = fit(svg, HI) >= 0.5
    pad = np.pad(hi, HI // 16)  # a 1-px-at-16 white margin so outer background counts
    w = minw(hi); g = minw(~pad)
    a16 = fit(svg, 16); a256 = fit(svg, 256)
    n = min(a16.shape[0], 16)
    d16 = np.asarray(Image.fromarray((a256 * 255).astype(np.uint8)).resize(a16.shape[::-1], Image.BOX), float) / 255
    s = structural_similarity(a16, d16, data_range=1.0, win_size=7)
    ys, xs = np.nonzero(hi)
    dx = (xs.mean() - (xs.min() + xs.max()) / 2) / HI * 100
    dy = (ys.mean() - (ys.min() + ys.max()) / 2) / HI * 100
    return w, g, s, dx, dy


print("name,min_stroke@16,min_gap@16,ssim,centroid_dx%,centroid_dy%")
for a in sys.argv[1:]:
    k, p = a.split("=", 1)
    try:
        w, g, s, dx, dy = run(open(p, encoding="utf-8").read())
        print(f"{k},{w:.2f},{g:.2f},{s:.3f},{dx:+.1f},{dy:+.1f}")
    except Exception as e:
        print(k, "ERR", repr(e))

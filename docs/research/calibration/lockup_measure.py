"""Measure horizontal lockups: mark height, mark-word gap, stroke match.

Usage: python -I lockup_measure.py OUTDIR name=path.svg [name=path.svg ...]
Mark = everything left of the widest empty column run; word = everything right of it.
Word band: baseline = median bottom of word components; cap/asc line = 10th-percentile top;
x-line = median top. Strokes = median of 2*EDT sampled on the skeleton.
"""
import io, json, sys
import numpy as np, resvg_py
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage.morphology import skeletonize

H = 800  # render height px
import os
LUM = os.environ.get('LUM') == '1'


def ink(path):
    svg = open(path, encoding="utf-8").read()
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg, height=H))
    a = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"), float) / 255
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    return a[..., 3] * (1 - lum) >= (0.5 if LUM else 0.0) if LUM else a[..., 3] >= 0.5


def runs(empty):
    out, s = [], None
    for i, e in enumerate(empty):
        if e and s is None: s = i
        if not e and s is not None: out.append((s, i)); s = None
    return out


def stroke(mask):
    if mask.sum() < 50: return None
    sk = skeletonize(mask)
    d = ndi.distance_transform_edt(mask)[sk] * 2
    return float(np.median(d)) if d.size else None


def measure(name, path, outdir):
    m = ink(path)
    ys, xs = np.nonzero(m)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cols = m.any(0)
    gaps = [r for r in runs(~cols) if r[0] > 0]
    g0, g1 = max(gaps, key=lambda r: r[1] - r[0])
    mark, word = m[:, :g0], m[:, g1:]
    mys = np.nonzero(mark.any(1))[0]; mt, mb = mys.min(), mys.max() + 1
    mw = np.nonzero(mark.any(0))[0]; mark_w = mw.max() + 1 - mw.min()
    lab, n = ndi.label(word)
    objs = ndi.find_objects(lab)
    sizes = ndi.sum(word, lab, range(1, n + 1))
    big = [o for o, s in zip(objs, sizes) if s > 0.002 * word.sum()]
    bottoms = np.array([o[0].stop for o in big]); tops = np.array([o[0].start for o in big])
    base = float(np.median(bottoms))
    cap = float(np.percentile(tops, 10)); xl = float(np.median(tops))
    hc, hx = base - cap, base - xl
    mark_h = mb - mt; gap = g1 - g0
    sm, sw = stroke(mark), stroke(word)
    r = dict(name=name, mark_h_over_cap=mark_h / hc, mark_h_over_x=mark_h / hx if hx > 0.3 * hc else None,
             gap_over_cap=gap / hc, gap_over_mark_w=gap / mark_w, gap_over_mark_h=gap / mark_h,
             mark_top_above_cap=(cap - mt) / hc, mark_bot_below_base=(mb - base) / hc,
             mark_centre_vs_capband=((mt + mb) / 2 - (cap + base) / 2) / hc,
             stroke_mark_over_word=(sm / sw) if sm and sw else None,
             word_stroke_over_cap=sw / hc if sw else None, x_over_cap=hx / hc)
    im = Image.fromarray((~m * 255).astype(np.uint8)).convert("RGB")
    d = ImageDraw.Draw(im)
    for y, c in ((cap, "red"), (base, "blue"), (xl, "green")):
        d.line([(g1, y), (m.shape[1], y)], fill=c, width=2)
    d.rectangle([g0, 0, g1, m.shape[0] - 1], outline="orange", width=3)
    d.rectangle([mw.min(), mt, mw.max(), mb - 1], outline="magenta", width=2)
    im.thumbnail((900, 200)); im.save(f"{outdir}/{name}.png")
    return r


if __name__ == "__main__":
    out = sys.argv[1]; res = []
    for a in sys.argv[2:]:
        k, p = a.split("=", 1)
        try: res.append(measure(k, p, out))
        except Exception as e: res.append(dict(name=k, error=repr(e)))
    json.dump(res, open(f"{out}/lockups.json", "w"), indent=1)
    keys = ["mark_h_over_cap", "mark_h_over_x", "gap_over_cap", "gap_over_mark_w", "gap_over_mark_h",
            "mark_top_above_cap", "mark_bot_below_base", "mark_centre_vs_capband", "stroke_mark_over_word", "word_stroke_over_cap", "x_over_cap"]
    print("name," + ",".join(keys))
    for r in res:
        print(r["name"] + "," + (",".join("" if r.get(k) is None else f"{r[k]:.2f}" for k in keys) if "error" not in r else r["error"]))

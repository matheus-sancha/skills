"""Graphic-language generators: the 'shapes' and 'parameters' extraction moves (identity-system.md §5).

Both read only from the mark: its flattened paths (parts) and params.json (radius set, ratios, colours).
- shapes: reuse the mark's parts as a repeat pattern (scaled, rotated in 90° steps, on a grid).
- parameters: a seeded composition of circles and bars sized only from the mark's ratios.
The agent samples several seeds, rejects any output that could be mistaken for the logo, and keeps 3-5.

Usage: python -B -m brandkit.graphic_language MARK.svg PARAMS.json OUT_DIR [--seeds 1 2 3]
PARAMS.json: {"colours": ["#..", ...], "ratios": [1, 0.5, 0.25], "radius": [4, 8]}
"""
import argparse
import json
import random
import re
from pathlib import Path

W, H = 1200, 600


def _parts(svg):
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    paths = re.findall(r'<path\b[^>]*\sd="([^"]+)"', svg)
    return vb, paths


def shapes(mark_svg, params, seed):
    rnd = random.Random(seed)
    vb, paths = _parts(mark_svg)
    vx, vy, vw, vh = (float(v) for v in vb.split())
    cols = params["colours"]
    cell = rnd.choice([100, 120, 150])
    out = []
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            if rnd.random() < 0.35:
                continue
            d = rnd.choice(paths)
            rot = rnd.choice([0, 90, 180, 270])
            s = cell / max(vw, vh) * rnd.choice([0.6, 0.8, 1.0])
            out.append(f'<path fill="{rnd.choice(cols)}" d="{d}" transform="translate({x + cell / 2} {y + cell / 2}) '
                       f'rotate({rot}) scale({s:.4f}) translate({-(vx + vw / 2):.2f} {-(vy + vh / 2):.2f})"/>')
    return out, {"move": "shapes", "seed": seed, "cell": cell, "source_parts": len(paths)}


def parameters(params, seed):
    rnd = random.Random(seed)
    cols, ratios = params["colours"], params.get("ratios", [1, 0.5, 0.25])
    unit = rnd.choice([60, 80, 100])
    out = []
    x = 0
    while x < W:
        r = unit * rnd.choice(ratios)
        kind = rnd.choice(["circle", "bar"])
        y = rnd.choice([H / 3, H / 2, 2 * H / 3])
        c = rnd.choice(cols)
        if kind == "circle":
            out.append(f'<circle cx="{x + r:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}"/>')
        else:
            out.append(f'<rect x="{x:.1f}" y="{y - r:.1f}" width="{2 * r:.1f}" height="{2 * r * rnd.choice(ratios):.1f}" '
                       f'rx="{min(params.get("radius", [0])):.1f}" fill="{c}"/>')
        x += 2 * r + unit * rnd.choice(ratios) / 2
    return out, {"move": "parameters", "seed": seed, "unit": unit, "ratios": ratios}


def generate(mark_svg, params, out_dir, seeds=(1, 2, 3), bg="#ffffff"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    written, log = [], []
    for seed in seeds:
        for move in ("shapes", "parameters"):
            els, meta = shapes(mark_svg, params, seed) if move == "shapes" else parameters(params, seed)
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
                   f'<rect width="{W}" height="{H}" fill="{bg}"/>{"".join(els)}</svg>\n')
            p = out / f"{move}-s{seed}.svg"
            p.write_text(svg, encoding="utf-8")
            written.append(str(p)); log.append({"file": p.name, **meta})
    (out / "params.json").write_text(json.dumps({"params": params, "outputs": log}, indent=1), encoding="utf-8")
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mark"); ap.add_argument("params"); ap.add_argument("out")
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    a = ap.parse_args()
    for p in generate(Path(a.mark).read_text(encoding="utf-8"),
                      json.loads(Path(a.params).read_text(encoding="utf-8")), a.out, a.seeds):
        print(p)

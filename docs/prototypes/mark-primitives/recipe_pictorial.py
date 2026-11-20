"""Route B (just right) - PICTORIAL: the sun rising behind a roof.

Idea: a home that makes its own daylight. A thick roof chevron (slate) cuts across
an amber sun; the sun shows only above the roof, separated by a clear gap so the
two read as two things in one colour too. Short rays say "sunny".

Usage: python -B recipe_pictorial.py OUT_DIR [r1|r2]
"""
import sys

from brand import AMBER, BOX, PAD, SLATE
from primitives import Mark

REVS = {
    # r1: first instinct - roof stroke 12, gap 5, sun r 27, five rays.
    "r1": dict(roof_w=12, gap=5, sun_r=27, sun_cy=50, apex_y=46, eave_y=80,
               rays=[90, 45, 135, 15, 165], ray_r=(36, 44), ray_deg=8),
    # r2 (after viewing r1): rays were speckle at 16 px and clip-art at 256 -> drop them (Apple HIG:
    # few shapes). Chevron read as a rank insignia -> cut the eaves horizontal. Sun raised and the
    # gap widened to 7 u (1.1 px at 16) so the sun is a body, not a crescent.
    "r2": dict(roof_w=13, gap=7, sun_r=23, sun_cy=40, apex_y=52, eave_y=82,
               rays=[], ray_r=(0, 0), ray_deg=0, eave_cut=True),
    # r3 (after viewing r2): mono read as a "user" icon (head over shoulders) because the sun sat
    # dead centre over the apex -> move it behind the right slope (morning sun, asymmetric).
    # r2's leg extension pushed the roof past the live area -> extend only half a stroke.
    "r3": dict(roof_w=13, gap=7, sun_r=19, sun_cy=40, sun_cx=64, apex_y=50, eave_y=82,
               rays=[], ray_r=(0, 0), ray_deg=0, eave_cut=True, leg_ext=6.5),
}


def build(rev):
    p = REVS[rev]
    m = Mark(f"pictorial_{rev}", BOX, note="sun behind roof chevron")
    l, r = PAD + 2, BOX - PAD - 2
    chevron = [(l, p["eave_y"]), (BOX / 2, p["apex_y"]), (r, p["eave_y"])]
    if p.get("eave_cut"):
        # extend both legs down-slope past the eave, then cut flat at the eave line
        dx, dy = BOX / 2 - l, p["apex_y"] - p["eave_y"]
        t = p.get("leg_ext", p["roof_w"]) / (dx * dx + dy * dy) ** 0.5
        chevron = [(l - dx * t, p["eave_y"] - dy * t), chevron[1], (r + dx * t, p["eave_y"] - dy * t)]
    roof = m.stroke(chevron, p["roof_w"], cap="butt", join="miter", miter_limit=10)
    if p.get("eave_cut"):
        roof = m.intersect(roof, m.rect(0, 0, BOX, p["eave_y"]))
    # everything on or under the roof line, grown by the gap, hides the sun
    under = m.polygon([(0, p["eave_y"]), (BOX / 2, p["apex_y"]), (BOX, p["eave_y"]), (BOX, BOX), (0, BOX)])
    shield = m.stroke(chevron + [], p["roof_w"] + 2 * p["gap"], cap="square", join="miter", miter_limit=10)
    sun = m.circle(p.get("sun_cx", BOX / 2), p["sun_cy"], p["sun_r"])
    sun_vis = m.difference(sun, under, shield)
    parts = [sun_vis]
    for a in p["rays"]:
        parts.append(m.annulus_segment(BOX / 2, p["sun_cy"], p["ray_r"][0], p["ray_r"][1],
                                       a - p["ray_deg"] / 2, a + p["ray_deg"] / 2))
    sunny = m.difference(m.union(*parts), shield, under) if len(parts) > 1 else sun_vis
    return m, [(roof, SLATE), (sunny, AMBER)]


if __name__ == "__main__":
    out, rev = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "r1")
    m, layers = build(rev)
    print(m.write(f"{out}/pictorial_{rev}", layers))

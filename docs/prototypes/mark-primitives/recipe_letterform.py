"""Route A (safe) - LETTERFORM: an "H" assembled from three roof tiles.

Idea: the name is literally built from the product. Two upright tiles and one
crossbar tile, separated by tile joints; the crossbar is the "lit" tile (amber).

Usage: python -B recipe_letterform.py OUT_DIR [r1|r2]
"""
import sys

from brand import AMBER, BOX, PAD, SLATE
from primitives import Mark

REVS = {
    # r1: first instinct - tight joints, crisp small corner radius, two colours.
    "r1": dict(stem_w=22, joint=4, radius=4, bar_ratio=0.93, bar_lift=2.0, bar_colour=AMBER, bar="tile"),
    # r2 (after viewing r1): r1 read as a generic H / dumbbell and its joints filled in at 16 px.
    # Structural change, not a parameter tweak: the crossbar becomes a half-sun rising between the
    # stems; joints >= 7 u (1.1 px at 16); stems start at the padding line to give the sun room.
    "r2": dict(stem_w=19, joint=7, radius=5, bar_ratio=None, bar_lift=None, bar_colour=AMBER, bar="sun",
               stem_inset=0, sun_base=58),
    # r3 (after viewing r2): sun too small against heavy stems; read as "pillars + dot" at 16 px.
    # Thinner stems give the sun ~27 % more area (r 15.7 -> 17.7); base lowered 1 u so the dome's mass sits at mid-height.
    "r3": dict(stem_w=17, joint=7, radius=5, bar_ratio=None, bar_lift=None, bar_colour=AMBER, bar="sun",
               stem_inset=0, sun_base=57),
}


def build(rev):
    p = REVS[rev]
    m = Mark(f"letterform_{rev}", BOX, note="H from three tiles; crossbar is the lit tile")
    top, bot = PAD + 1, BOX - PAD - 1
    sw = p["stem_w"]
    x_in = PAD + p.get("stem_inset", 2)
    left = m.rounded_rect(x_in, top, sw, bot - top, p["radius"])
    right = m.mirror(left, "x")
    if p["bar"] == "sun":
        span = BOX - 2 * (x_in + sw) - 2 * p["joint"]
        r = m.note_param("sun_r", round(span / 2, 3), "fills the counter minus both joints")
        sun = m.annulus_segment(BOX / 2, p["sun_base"], 0, r, 0, 180)
        return m, [(m.union(left, right), SLATE), (sun, p["bar_colour"])]
    # rule 3: horizontals read heavier than verticals of equal width -> thin the bar
    bar_h = m.note_param("bar_h", round(sw * p["bar_ratio"], 3), "rule 3 stroke compensation")
    # letter crossbars sit a touch above geometric centre (type convention, optical)
    cy = m.note_param("bar_cy", BOX / 2 - p["bar_lift"], "crossbar raised above centre")
    x0 = PAD + 2 + sw + p["joint"]
    bar = m.rounded_rect(x0, cy - bar_h / 2, BOX - 2 * x0, bar_h, p["radius"])
    stems = m.union(left, right)
    return m, [(stems, SLATE), (bar, p["bar_colour"])]


if __name__ == "__main__":
    out, rev = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "r1")
    m, layers = build(rev)
    print(m.write(f"{out}/letterform_{rev}", layers))

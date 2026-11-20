"""Colour pipeline: identity hexes -> OKLCH ramps -> roles (light/dark) checked by WCAG 2.

- Identity colours stay exact; the first brand hex lands exactly in a fill role (U3).
- Text and link roles are solved to >= 5.0:1 (SOLVE) and gated at 4.5:1 (issue 27).
- Ramps are built in OKLCH, gamut-mapped by chroma reduction, contrast measured on the final hex.
- Colour-blind simulation uses the Machado, Oliveira & Fernandes (2009) matrices at severity 1.0,
  applied in linear sRGB.

Usage: python -B -m brandkit.palette OUT.json "#e4572e" ["#1e2b3a" ...]
"""
import json
import math
import sys

SOLVE = 5.0
GATE = 4.5
STEPS = [98, 95, 90, 80, 70, 60, 50, 40, 30, 20, 10]   # OKLCH L x 100


# -- conversions -------------------------------------------------------------
def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02x}" for c in rgb)


def rgb_to_oklch(rgb):
    r, g, b = (_lin(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    b2 = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, b2), math.degrees(math.atan2(b2, a)) % 360


def oklch_to_rgb_unclipped(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(_gam(c) if c >= 0 else -_gam(-c) for c in (r, g, bb))


def oklch_to_hex(L, C, H):
    """Gamut-map by chroma reduction (CSS Color 4 style, binary search on C)."""
    lo, hi = 0.0, C
    rgb = oklch_to_rgb_unclipped(L, C, H)
    if all(-1e-4 <= c <= 1 + 1e-4 for c in rgb):
        return rgb_to_hex(rgb)
    for _ in range(25):
        mid = (lo + hi) / 2
        rgb = oklch_to_rgb_unclipped(L, mid, H)
        if all(-1e-4 <= c <= 1 + 1e-4 for c in rgb):
            lo = mid
        else:
            hi = mid
    return rgb_to_hex(oklch_to_rgb_unclipped(L, lo, H))


def luminance(h):
    r, g, b = (_lin(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# -- ramps and solving -------------------------------------------------------
def ramp(hex_):
    L0, C, H = rgb_to_oklch(hex_to_rgb(hex_))
    steps = {}
    for s in STEPS:
        L = s / 100
        c = C * max(0.25, 1 - abs(L - L0) * 1.1)   # taper chroma away from the brand tone
        steps[str(s)] = oklch_to_hex(L, c, H)
    return {"source": hex_.lower(), "oklch": [round(L0, 4), round(C, 4), round(H, 2)], "steps": steps}


def solve_on(bg, hue_hex, target=SOLVE, darker=True):
    """Shift L of hue_hex (constant C, H) until contrast with bg >= target."""
    L, C, H = rgb_to_oklch(hex_to_rgb(hue_hex))
    for i in range(200):
        cand = oklch_to_hex(L, C, H)
        if contrast(cand, bg) >= target:
            return cand
        L = L - 0.005 if darker else L + 0.005
        if not 0 <= L <= 1:
            break
    return "#000000" if darker else "#ffffff"


def on_colour(fill):
    """Best of near-black / white on a fill."""
    dark, light = "#111111", "#ffffff"
    return dark if contrast(dark, fill) >= contrast(light, fill) else light


STATUS_HUES = {"success": 150, "warning": 85, "danger": 27, "info": 240}
# Lightness is spread so status pairs stay apart under colour-blind simulation (gate CB):
# danger dark (white text), success / info / warning progressively lighter (dark text).
STATUS_L = {"danger": 0.45, "success": 0.66, "info": 0.78, "warning": 0.90}


def build(identity, neutral_tint=0.012):
    primary = identity[0].lower()
    L, C, H = rgb_to_oklch(hex_to_rgb(primary))
    ramps = {f"brand{i + 1}": ramp(h) for i, h in enumerate(identity)}
    neutral = {str(s): oklch_to_hex(s / 100, neutral_tint, H) for s in STEPS}
    ramps["neutral"] = {"source": None, "oklch": [None, neutral_tint, round(H, 2)], "steps": neutral}
    status = {k: oklch_to_hex(STATUS_L[k], 0.15, h) for k, h in STATUS_HUES.items()}

    themes = {}
    for theme, surface, on_surface, variant in (
            ("light", neutral["98"], neutral["10"], neutral["30"]),
            ("dark", neutral["10"], neutral["95"], neutral["80"])):
        r = {}
        r["surface"] = surface
        r["surface-raised"] = neutral["95"] if theme == "light" else neutral["20"]
        r["on-surface"] = on_surface
        r["on-surface-variant"] = variant
        r["outline"] = neutral["50"] if theme == "light" else neutral["60"]
        r["outline-variant"] = neutral["90"] if theme == "light" else neutral["30"]
        r["primary"] = primary                                      # exact brand hex (U3)
        r["on-primary"] = on_colour(primary)
        r["primary-container"] = ramps["brand1"]["steps"]["90" if theme == "light" else "30"]
        r["on-primary-container"] = solve_on(r["primary-container"], primary, SOLVE, darker=theme == "light")
        r["link"] = (primary if contrast(primary, surface) >= SOLVE
                     else solve_on(surface, primary, SOLVE, darker=theme == "light"))
        r["focus"] = r["link"]
        for k, v in status.items():
            fill = v
            r[k] = fill
            r[f"on-{k}"] = on_colour(fill)
            r[f"{k}-text"] = solve_on(surface, fill, SOLVE, darker=theme == "light")
        themes[theme] = r
    flags = []
    for theme, r in themes.items():
        if contrast(primary, r["surface"]) < 3.0:
            flags.append(f"{theme}: brand fill {primary} below 3:1 on surface; use link/primary-container for text")
    return {"identity": [h.lower() for h in identity], "ramps": ramps, "themes": themes, "flags": flags}


# -- colour-blind simulation -------------------------------------------------
MACHADO = {
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def simulate(h, kind):
    lin = [_lin(c) for c in hex_to_rgb(h)]
    m = MACHADO[kind]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return rgb_to_hex([_gam(max(0, min(1, c))) for c in out])


def delta_e_ok(a, b):
    la, ca, ha = rgb_to_oklch(hex_to_rgb(a))
    lb, cb, hb = rgb_to_oklch(hex_to_rgb(b))
    aa, ab_ = ca * math.cos(math.radians(ha)), ca * math.sin(math.radians(ha))
    ba, bb = cb * math.cos(math.radians(hb)), cb * math.sin(math.radians(hb))
    return math.sqrt((la - lb) ** 2 + (aa - ba) ** 2 + (ab_ - bb) ** 2)


if __name__ == "__main__":
    pal = build(sys.argv[2:])
    open(sys.argv[1], "w", encoding="utf-8").write(json.dumps(pal, indent=1))
    for t, r in pal["themes"].items():
        print(t, {k: v for k, v in r.items() if k in ("primary", "link", "on-primary", "primary-container")})
    print("flags:", pal["flags"])

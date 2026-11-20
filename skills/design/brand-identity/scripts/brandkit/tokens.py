"""One token model -> DTCG 2025.10 (source), Claude Design System tokens.json, tokens.css, Dart.

The model is built from palette.build() output plus the character knobs (issue 22).
Every token carries a usage note ($description), because the Design System type drops tokens without one.

Usage: python -B -m brandkit.tokens PALETTE.json KNOBS.json OUT_DIR
KNOBS.json: {"radius_factor": 1, "density": 1.0, "motion": "productive", "depth": "borders",
             "base": 4, "fonts": {"display": "...", "text": "..."}, "type_ratio": 1.2}
"""
import json
import re
import sys
from pathlib import Path

from .palette import hex_to_rgb, rgb_to_oklch

USAGE = {
    "surface": "Page background.",
    "surface-raised": "Cards and raised panels on surface.",
    "on-surface": "Body text and icons on surface and surface-raised.",
    "on-surface-variant": "Secondary text on surface.",
    "outline": "Control boundaries (inputs, checkboxes) on surface; 3:1 required.",
    "outline-variant": "Decorative dividers only; not for control boundaries.",
    "primary": "Brand fill: primary buttons and key accents. Exact brand colour.",
    "on-primary": "Text and icons on primary.",
    "primary-container": "Tinted brand background for highlights and selected states.",
    "on-primary-container": "Text on primary-container.",
    "link": "Links and brand-coloured text on surface.",
    "focus": "Focus indicator ring.",
}
RADIUS = {0: [0, 2, 4], 1: [4, 8, 12], 1.5: [8, 12, 16, 24]}
SPACE = [4, 8, 12, 16, 24, 32, 48, 64]
MOTION = {
    "productive": {"duration": {"fast": 100, "base": 200, "slow": 300},
                   "easing": {"standard": [0.2, 0, 0.38, 0.9], "enter": [0, 0, 0.38, 0.9], "exit": [0.2, 0, 1, 0.9]}},
    "expressive": {"duration": {"fast": 150, "base": 300, "slow": 500},
                   "easing": {"standard": [0.4, 0.14, 0.3, 1], "enter": [0, 0, 0.3, 1], "exit": [0.4, 0.14, 1, 1]}},
}
TYPE_ROLES = [("display", "display", 3), ("headline", "display", 2), ("title", "text", 1),
              ("body", "text", 0), ("label", "text", -1)]


def _usage(name):
    if name in USAGE:
        return USAGE[name]
    for k in ("success", "warning", "danger", "info"):
        if name == k:
            return f"Status fill for {k}; pair with an icon or word."
        if name == f"on-{k}":
            return f"Text and icons on the {k} fill."
        if name == f"{k}-text":
            return f"{k.title()} text on surface."
    return "See README."


def _round4(v, base):
    return max(base, round(v / base) * base)


def type_scale(knobs):
    """label < body < title < headline < display. Text steps use the ratio (~1.2);
    headline and display use a larger step capped at 1.4 so every step stays within U7."""
    base, ratio, dens = knobs.get("base", 4), knobs.get("type_ratio", 1.2), knobs.get("density", 1.0)
    big = min(1.4, ratio * 1.15)
    body = round(16 * dens)
    sizes = {"label": round(body / ratio), "body": body, "title": round(body * ratio)}
    sizes["headline"] = round(sizes["title"] * big)
    sizes["display"] = round(sizes["headline"] * big)
    out = []
    for role, fam, step in TYPE_ROLES:
        size = sizes[role]
        lh = _round4(size * (1.2 if step >= 2 else 1.5), base)
        weight = 600 if step >= 1 else (500 if step < 0 else 400)
        out.append({"role": role, "family": fam, "size": size, "line": lh, "weight": weight})
    return out


def model(pal, knobs):
    base = knobs.get("base", 4)
    rf = knobs.get("radius_factor", 1)
    radii = RADIUS.get(rf, RADIUS[1])
    dens = knobs.get("density", 1.0)
    space = [_round4(s * dens, base) if s > base else s for s in SPACE]
    space = sorted(set(space))
    return {"palette": pal, "knobs": knobs, "radius": radii, "full_buttons": knobs.get("pill", False),
            "space": space, "type": type_scale(knobs), "motion": MOTION[knobs.get("motion", "productive")]}


# -- DTCG 2025.10 --------------------------------------------------------------
def _dtcg_colour(h):
    r, g, b = hex_to_rgb(h)
    return {"colorSpace": "srgb", "components": [round(r, 4), round(g, 4), round(b, 4)], "hex": h.lower()}


def to_dtcg(m):
    pal = m["palette"]
    out = {"$schema": "https://www.designtokens.org/schemas/2025.10/format.json"}
    prim = {"$type": "color"}
    for rname, rp in pal["ramps"].items():
        prim[rname] = {s: {"$value": _dtcg_colour(h), "$description": f"{rname} ramp step {s} (OKLCH L {s})."}
                       for s, h in rp["steps"].items()}
    prim["identity"] = {f"brand{i + 1}": {"$value": _dtcg_colour(h), "$description": "Identity colour; exact, used by the mark."}
                        for i, h in enumerate(pal["identity"])}
    out["palette"] = prim
    for theme, roles in pal["themes"].items():
        out[f"color-{theme}"] = {"$type": "color", **{
            k: {"$value": _dtcg_colour(v), "$description": _usage(k)} for k, v in roles.items()}}
    out["space"] = {"$type": "dimension", **{
        str(i + 1): {"$value": {"value": v, "unit": "px"}, "$description": f"Spacing step {i + 1}."} for i, v in enumerate(m["space"])}}
    out["radius"] = {"$type": "dimension", **{
        str(i + 1): {"$value": {"value": v, "unit": "px"}, "$description": f"Corner radius step {i + 1}."}
        for i, v in enumerate(m["radius"])}}
    out["radius"]["full"] = {"$value": {"value": 9999, "unit": "px"}, "$description": "Pills; never on checkboxes."}
    mo = m["motion"]
    out["motion"] = {
        "duration": {"$type": "duration", **{k: {"$value": {"value": v, "unit": "ms"}, "$description": f"{k} transitions."}
                                             for k, v in mo["duration"].items()}},
        "easing": {"$type": "cubicBezier", **{k: {"$value": v, "$description": f"{k} easing ({m['knobs'].get('motion', 'productive')})."}
                                              for k, v in mo["easing"].items()}},
    }
    fonts = m["knobs"].get("fonts", {})
    out["type"] = {"$type": "typography", **{t["role"]: {"$value": {
        "fontFamily": fonts.get(t["family"], "system-ui"), "fontSize": {"value": t["size"], "unit": "px"},
        "fontWeight": t["weight"], "lineHeight": round(t["line"] / t["size"], 3), "letterSpacing": {"value": 0, "unit": "px"}},
        "$description": f"{t['role']} text."} for t in m["type"]}}
    return out


# -- Claude Design System tokens.json (list shape) ---------------------------
def to_claude_ds(m, name):
    pal = m["palette"]
    themes = [{"id": t, "name": t.title()} for t in pal["themes"]]
    ctoks = []
    for rname, rp in pal["ramps"].items():
        for s, h in rp["steps"].items():
            ctoks.append({"name": f"{rname}-{s}", "value": h, "usage": f"{rname} ramp step {s}; prefer role tokens in UI."})
    for i, h in enumerate(pal["identity"]):
        ctoks.append({"name": f"identity-brand{i + 1}", "value": h, "usage": "Identity colour used by the mark; exact."})
    roles = pal["themes"]["light"].keys()
    for k in roles:
        ctoks.append({"name": k, "value": {t: pal["themes"][t][k] for t in pal["themes"]}, "usage": _usage(k)})
    fonts = m["knobs"].get("fonts", {})
    fams = {k: f"'{v}', system-ui, sans-serif" for k, v in fonts.items()} or {"text": "system-ui, sans-serif"}
    groups = [{"name": "Text", "family": "text" if "text" in fams else next(iter(fams)), "styles": []},
              {"name": "Display", "family": "display" if "display" in fams else next(iter(fams)), "styles": []}]
    for t in m["type"]:
        g = groups[1] if t["family"] == "display" else groups[0]
        g["styles"].append({"name": t["role"], "fontSize": f"{t['size']}px", "lineHeight": f"{t['line']}px",
                            "fontWeight": t["weight"], "usage": f"{t['role']} text."})
    font_files = [{"family": v, "file": f"fonts/{re.sub(r'[^A-Za-z0-9]', '', v)}.woff2", "weight": "100 900", "style": "normal"}
                  for v in sorted(set(fonts.values()))]
    return {
        "name": name, "version": "1.0.0",
        "color": {"themes": themes, "tokens": ctoks},
        "type": {"fonts": font_files, "families": fams, "groups": groups},
        "spacing": {"tokens": [{"name": f"space-{i + 1}", "value": f"{v}px", "usage": f"Spacing step {i + 1}."}
                               for i, v in enumerate(m["space"])]},
        "radius": {"tokens": [{"name": f"radius-{i + 1}", "value": f"{v}px", "usage": f"Corner radius step {i + 1}."}
                              for i, v in enumerate(m["radius"])] +
                             [{"name": "radius-full", "value": "9999px", "usage": "Pills; never on checkboxes."}]},
    }


# -- CSS and Dart ------------------------------------------------------------
def to_css(m):
    pal = m["palette"]
    lines = [":root {"]
    for k, v in pal["themes"]["light"].items():
        lines.append(f"  --color-{k}: {v};")
    for i, v in enumerate(m["space"]):
        lines.append(f"  --space-{i + 1}: {v}px;")
    for i, v in enumerate(m["radius"]):
        lines.append(f"  --radius-{i + 1}: {v}px;")
    lines.append("  --radius-full: 9999px;")
    for k, v in m["motion"]["duration"].items():
        lines.append(f"  --motion-duration-{k}: {v}ms;")
    for k, v in m["motion"]["easing"].items():
        lines.append(f"  --motion-easing-{k}: cubic-bezier({', '.join(str(x) for x in v)});")
    lines.append("}")
    lines.append('[data-theme="dark"] {')
    for k, v in pal["themes"]["dark"].items():
        lines.append(f"  --color-{k}: {v};")
    lines.append("}")
    lines.append("@media (prefers-color-scheme: dark) { :root:not([data-theme=\"light\"]) {")
    for k, v in pal["themes"]["dark"].items():
        lines.append(f"  --color-{k}: {v};")
    lines.append("} }")
    return "\n".join(lines) + "\n"


def _dart_name(k):
    parts = k.split("-")
    return parts[0] + "".join(p.title() for p in parts[1:])


def _dart_col(h):
    return f"Color(0xFF{h.lstrip('#').upper()})"


def to_dart(m):
    pal = m["palette"]
    lt, dk = pal["themes"]["light"], pal["themes"]["dark"]
    out = ["// Generated by brand-identity. Consumed by flutter-ui-design (brand-supplied scheme).",
           "import 'package:flutter/material.dart';", "",
           "class BrandColors {",
           f"  static const seed = {_dart_col(pal['identity'][0])};"]
    for k, v in lt.items():
        out.append(f"  static const {_dart_name(k)}Light = {_dart_col(v)};")
    for k, v in dk.items():
        out.append(f"  static const {_dart_name(k)}Dark = {_dart_col(v)};")
    out += ["}", "", "ColorScheme brandScheme(Brightness b) {",
            "  final light = b == Brightness.light;",
            "  return ColorScheme.fromSeed(",
            "    seedColor: BrandColors.seed,",
            "    brightness: b,",
            "    dynamicSchemeVariant: DynamicSchemeVariant.fidelity,",
            "    primary: BrandColors.primaryLight,",
            "    onPrimary: light ? BrandColors.onPrimaryLight : BrandColors.onPrimaryDark,",
            "    primaryContainer: light ? BrandColors.primaryContainerLight : BrandColors.primaryContainerDark,",
            "    onPrimaryContainer: light ? BrandColors.onPrimaryContainerLight : BrandColors.onPrimaryContainerDark,",
            "    surface: light ? BrandColors.surfaceLight : BrandColors.surfaceDark,",
            "    onSurface: light ? BrandColors.onSurfaceLight : BrandColors.onSurfaceDark,",
            "    outline: light ? BrandColors.outlineLight : BrandColors.outlineDark,",
            "    error: light ? BrandColors.dangerLight : BrandColors.dangerDark,",
            "  );", "}", "",
            "abstract final class Space {"]
    for i, v in enumerate(m["space"]):
        out.append(f"  static const double s{i + 1} = {v};")
    out += ["}", "", "abstract final class Radii {"]
    for i, v in enumerate(m["radius"]):
        out.append(f"  static const double r{i + 1} = {v};")
    out += ["}", "", "abstract final class Motion {"]
    for k, v in m["motion"]["duration"].items():
        out.append(f"  static const {k} = Duration(milliseconds: {v});")
    for k, v in m["motion"]["easing"].items():
        out.append(f"  static const {k}Curve = Cubic({', '.join(str(x) for x in v)});")
    out.append("}")
    return "\n".join(out) + "\n"


def emit(pal, knobs, out_dir, name):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    m = model(pal, knobs)
    files = {
        "tokens.dtcg.json": json.dumps(to_dtcg(m), indent=1),
        "tokens.json": json.dumps(to_claude_ds(m, name), indent=1),
        "tokens.css": to_css(m),
        "brand_tokens.dart": to_dart(m),
    }
    for fn, txt in files.items():
        (out / fn).write_text(txt, encoding="utf-8")
    return m, [str(out / f) for f in files]


if __name__ == "__main__":
    pal = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    knobs = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    _, written = emit(pal, knobs, sys.argv[3], knobs.get("name", "Brand"))
    print("\n".join(written))

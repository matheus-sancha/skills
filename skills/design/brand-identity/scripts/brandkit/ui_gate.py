"""Script half of the UI gate (references/system.md U1-U15 + colour-blind CB).

Model-visual rules (U5 icon/word, U9 checkbox look, U14 brand fit, U15 AI tropes) are judged on the
component previews. U10 and U11 need rendered previews and are checked by the reviewer.

Usage: python -B -m brandkit.ui_gate TOKENS_DIR [--aaa]
"""
import json
import re
import sys
from itertools import combinations
from pathlib import Path

from .palette import contrast, delta_e_ok, hex_to_rgb, rgb_to_oklch, simulate

NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
# (text role, ground role, threshold) — built from the usage notes
TEXT_PAIRS = [("on-surface", "surface"), ("on-surface", "surface-raised"), ("on-surface-variant", "surface"),
              ("on-primary", "primary"), ("on-primary-container", "primary-container"), ("link", "surface"),
              ("success-text", "surface"), ("warning-text", "surface"), ("danger-text", "surface"),
              ("info-text", "surface"), ("on-success", "success"), ("on-warning", "warning"),
              ("on-danger", "danger"), ("on-info", "info")]
NONTEXT_PAIRS = [("outline", "surface"), ("focus", "surface"), ("focus", "surface-raised"), ("primary", "surface")]
STATUS = ["success", "warning", "danger", "info"]
CB_MIN = 0.10   # proposed default (identity-system.md §8: status ΔL >= 0.10), to calibrate


def run(tokens_dir, aaa=False):
    d = Path(tokens_dir)
    ds = json.loads((d / "tokens.json").read_text(encoding="utf-8"))
    dtcg = json.loads((d / "tokens.dtcg.json").read_text(encoding="utf-8"))
    res = []
    themes = {t["id"] for t in ds["color"]["themes"]}
    roles = {t["name"]: t["value"] for t in ds["color"]["tokens"] if isinstance(t["value"], dict)}
    text_t = 7.0 if aaa else 4.5

    def val(role, theme):
        return roles[role][theme]

    fails = [f"{th}: {a}/{b} {contrast(val(a, th), val(b, th)):.2f}" for th in themes for a, b in TEXT_PAIRS
             if a in roles and b in roles and contrast(val(a, th), val(b, th)) < text_t]
    res.append(("U1 text contrast", f"{len(fails)} below {text_t}:1" + (": " + "; ".join(fails[:4]) if fails else ""), not fails))
    fails = [f"{th}: {a}/{b} {contrast(val(a, th), val(b, th)):.2f}" for th in themes for a, b in NONTEXT_PAIRS
             if a in roles and b in roles and contrast(val(a, th), val(b, th)) < 3.0]
    nt_hard = [f for f in fails if not f.split(": ")[1].startswith("primary/")]
    res.append(("U2 non-text contrast", "; ".join(fails) or "all >= 3:1", not nt_hard))
    ident = {t["value"].lower() for t in ds["color"]["tokens"] if t["name"].startswith("identity-")}
    fills = {v["light"].lower() for k, v in roles.items() if k in ("primary", "primary-container")}
    res.append(("U3 brand hex in a fill role", f"identity {sorted(ident)}", bool(ident & fills)))
    sets = {th: {k for k, v in roles.items() if th in v} for th in themes}
    res.append(("U4 same roles per theme", f"{len(roles)} roles x {len(themes)} themes",
                len({frozenset(s) for s in sets.values()}) == 1))
    mono_bad = []
    for rname, group in dtcg["palette"].items():
        if rname.startswith("$") or rname == "identity":
            continue
        Ls = [rgb_to_oklch(hex_to_rgb(group[s]["$value"]["hex"]))[0] for s in group if not s.startswith("$")]
        if any(b >= a or (a - b) * 100 < 2 for a, b in zip(Ls, Ls[1:])):
            mono_bad.append(rname)
    res.append(("U6 ramps monotone", ", ".join(mono_bad) or "ok", not mono_bad))
    sizes = [int(s["fontSize"].rstrip("px")) for g in ds["type"]["groups"] for s in g["styles"]]
    sizes = sorted(set(sizes))
    bad = [f"{a}->{b}" for a, b in zip(sizes, sizes[1:])
           if not (1.06 <= b / a <= (1.42 if b <= 48 else 1.7))]
    res.append(("U7 type steps", f"{sizes}" + (f" bad {bad}" if bad else ""), not bad))
    sp = [int(t["value"].rstrip("px")) for t in ds["spacing"]["tokens"]]
    base = 4
    res.append(("U8 spacing on base", f"{sp}", all(v % base == 0 or v == 2 for v in sp) and len(sp) <= 12))
    rad = [t for t in ds["radius"]["tokens"] if t["name"] != "radius-full"]
    res.append(("U9 radius steps", f"{len(rad)} + full", len(rad) <= 7))
    names, missing, badname = [], [], []
    for fam, body in ds.items():
        if isinstance(body, dict) and "tokens" in body:
            for t in body["tokens"]:
                names.append(t["name"])
                if not t.get("usage"):
                    missing.append(t["name"])
                if not NAME.match(t["name"]):
                    badname.append(t["name"])
    dup = sorted({n for n in names if names.count(n) > 1})
    res.append(("U12 usage notes, names", f"missing {len(missing)}, bad {len(badname)}, dup {len(dup)}",
                not (missing or badname or dup)))
    legacy = []

    def walk(node, path=""):
        if isinstance(node, dict):
            if "$value" in node:
                v, t = node["$value"], node.get("$type")
                if isinstance(v, str) and not v.startswith("{"):
                    legacy.append(path)
            for k, v in node.items():
                if not k.startswith("$"):
                    walk(v, f"{path}.{k}" if path else k)
    walk(dtcg)
    res.append(("U13 DTCG 2025.10 object forms", f"{len(legacy)} string values", not legacy))
    cb = []
    for th in themes:
        for a, b in combinations(STATUS, 2):
            for kind in ("protan", "deutan", "tritan"):
                de = delta_e_ok(simulate(val(a, th), kind), simulate(val(b, th), kind))
                if de < CB_MIN:
                    cb.append(f"{th} {a}/{b} {kind} dE {de:.3f}")
    res.append(("CB colour-blind status pairs", "; ".join(cb[:4]) or f"all dE_OK >= {CB_MIN}", not cb))
    return res


def table(res):
    lines = ["| rule | value | result |", "|---|---|---|"]
    lines += [f"| {k} | {v} | {'PASS' if ok else 'FAIL'} |" for k, v, ok in res]
    return "\n".join(lines)


if __name__ == "__main__":
    res = run(sys.argv[1], "--aaa" in sys.argv)
    print(table(res))
    ok = all(r[2] for r in res)
    print(f"\n**UI script gate: {'PASS' if ok else 'FAIL'}**")
    Path(sys.argv[1], "gate-ui.json").write_text(json.dumps(
        {"verdict": "PASS" if ok else "FAIL", "checks": [{"rule": k, "value": v, "pass": o} for k, v, o in res]}, indent=1),
        encoding="utf-8")

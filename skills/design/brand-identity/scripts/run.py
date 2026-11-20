"""One CLI for the brand-identity skill. Run with the skill's venv python (references/runtime.md).

  run.py init SLUG [--entry full|byom]        create brand/SLUG/ and state.json
  run.py status SLUG                          two-line resume summary
  run.py decide SLUG STAGE TEXT [--by user|agent]
  run.py stage SLUG STAGE STATUS [--rev rN]   set a stage's status
  run.py reopen SLUG STAGE                    reopen a stage; later stages become stale
  run.py probe SLUG --tier T --python V --vision yes|no
  run.py log SLUG STAGE ACTION [--rev rN] [--hard ...] [--flags ...] [--redraws n/5] [--user ...]
  run.py summary SLUG                         append the summary table to run-log.md
  run.py route SLUG ROUTE_DIR REV             build recipe.py revision, write SVG + gate
  run.py gate SVG [SVG ...]                   script gate + render sheet
  run.py flatten IN.svg OUT.svg               flatten hand-written SVG before gating
  run.py similarity CANDIDATE.svg REF.svg ... silhouette similarity (flag only)
  run.py anchors SLUG                         fetch anchor SVGs into .cache/anchors and render boards
  run.py boards SLUG --name NAME [--fonts DIR]
  run.py fonts-search [--query T] [--category C] [--variable]   search the Google Fonts catalogue
  run.py fonts-get SLUG "Family"              fetch a Google Fonts family + licence into .cache/fonts
  run.py lockup MARK.svg FONT NAME OUT.svg [--layout horizontal|stacked]
  run.py palette SLUG HEX [HEX ...]           06-system/palette.json
  run.py tokens SLUG KNOBS.json               06-system/tokens/*
  run.py ui SLUG NAMESPACE                    06-system/ui/ components + cover
  run.py ui-gate SLUG [--aaa]
  run.py graphic SLUG MARK.svg PARAMS.json
  run.py kit SLUG --name NAME --idea TEXT
  run.py kit-check SLUG
Paths: brand/ is relative to the current directory (override with --root).
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REFS = HERE.parent / "references"

from brandkit import state as S  # noqa: E402


def _run(a):
    return S.run_dir(a.slug, a.root)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default="brand")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("slug"); p.add_argument("--entry", default="full", choices=["full", "byom"])
    p = sub.add_parser("status"); p.add_argument("slug")
    p = sub.add_parser("decide"); p.add_argument("slug"); p.add_argument("stage"); p.add_argument("text"); p.add_argument("--by", default="user")
    p = sub.add_parser("stage"); p.add_argument("slug"); p.add_argument("stage"); p.add_argument("status"); p.add_argument("--rev")
    p = sub.add_parser("reopen"); p.add_argument("slug"); p.add_argument("stage")
    p = sub.add_parser("probe"); p.add_argument("slug"); p.add_argument("--tier", required=True)
    p.add_argument("--python", default=sys.version.split()[0]); p.add_argument("--vision", choices=["yes", "no"], required=True)
    p = sub.add_parser("log"); p.add_argument("slug"); p.add_argument("stage"); p.add_argument("action")
    for k in ("--rev", "--hard", "--flags", "--redraws", "--user"):
        p.add_argument(k)
    p = sub.add_parser("summary"); p.add_argument("slug")
    p = sub.add_parser("route"); p.add_argument("slug"); p.add_argument("route_dir"); p.add_argument("rev")
    p = sub.add_parser("gate"); p.add_argument("svgs", nargs="+")
    p = sub.add_parser("flatten"); p.add_argument("src"); p.add_argument("out")
    p = sub.add_parser("similarity"); p.add_argument("candidate"); p.add_argument("refs", nargs="+")
    p = sub.add_parser("anchors"); p.add_argument("slug")
    p = sub.add_parser("boards"); p.add_argument("slug"); p.add_argument("--name", required=True); p.add_argument("--fonts")
    p.add_argument("--seed", type=int, default=1)
    p = sub.add_parser("fonts-search"); p.add_argument("--query"); p.add_argument("--category")
    p.add_argument("--variable", action="store_true"); p.add_argument("--limit", type=int, default=20)
    p = sub.add_parser("fonts-get"); p.add_argument("slug"); p.add_argument("family")
    p = sub.add_parser("lockup"); p.add_argument("mark"); p.add_argument("font"); p.add_argument("name"); p.add_argument("out")
    p.add_argument("--layout", default="horizontal"); p.add_argument("--fill", default="#000000"); p.add_argument("--tracking", type=float, default=0)
    p = sub.add_parser("palette"); p.add_argument("slug"); p.add_argument("hexes", nargs="+")
    p = sub.add_parser("tokens"); p.add_argument("slug"); p.add_argument("knobs")
    p = sub.add_parser("ui"); p.add_argument("slug"); p.add_argument("namespace")
    p = sub.add_parser("ui-gate"); p.add_argument("slug"); p.add_argument("--aaa", action="store_true")
    p = sub.add_parser("graphic"); p.add_argument("slug"); p.add_argument("mark"); p.add_argument("params")
    p = sub.add_parser("kit"); p.add_argument("slug"); p.add_argument("--name", required=True); p.add_argument("--idea", required=True)
    p.add_argument("--rationale", default="")
    p = sub.add_parser("kit-check"); p.add_argument("slug")
    a = ap.parse_args(argv)

    if a.cmd == "init":
        st = S.init(a.slug, a.entry, a.root); print(S.status_line(st))
    elif a.cmd == "status":
        print(S.status_line(S.load(a.slug, a.root)))
    elif a.cmd == "decide":
        st = S.decide(S.load(a.slug, a.root), a.stage, a.text, a.by); S.save(st, a.root); print(st["decisions"][-1]["id"])
    elif a.cmd == "stage":
        st = S.set_stage(S.load(a.slug, a.root), a.stage, a.status, a.rev); S.save(st, a.root)
    elif a.cmd == "reopen":
        st = S.reopen(S.load(a.slug, a.root), a.stage); S.save(st, a.root); print(S.status_line(st))
    elif a.cmd == "probe":
        st = S.load(a.slug, a.root)
        st["probe"] = {"tier": a.tier, "python": a.python, "vision": a.vision == "yes", "at": S.now()}
        S.save(st, a.root)
    elif a.cmd == "log":
        S.log(a.slug, a.stage, a.rev, a.action, a.hard or "none", a.flags or "none", a.redraws or "", a.user or "—", a.root)
    elif a.cmd == "summary":
        S.summary(S.load(a.slug, a.root), a.root)
    elif a.cmd == "route":
        from brandkit.gate import gate
        from brandkit.checks import table
        d = Path(a.route_dir)
        spec = importlib.util.spec_from_file_location("recipe", d / "recipe.py")
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        built = mod.build(a.rev)
        m, layers = built if isinstance(built, tuple) else (built, None)
        pad = getattr(mod, "CONSTRAINTS", {}).get("padding", m.box / 12)
        svg_path = m.write(str(d / f"mark.{a.rev}"), layers, pad=pad)
        verdict, res = gate(svg_path, m.box)
        print(table(f"{d.name} {a.rev}", res)); print(f"\n**script gate: {verdict}**")
    elif a.cmd == "gate":
        from brandkit.gate import gate
        from brandkit.checks import table
        for p_ in a.svgs:
            verdict, res = gate(p_); print(table(Path(p_).stem, res)); print(f"\n**script gate: {verdict}**\n")
    elif a.cmd == "flatten":
        from brandkit.flatten import flatten
        Path(a.out).write_text(flatten(Path(a.src).read_text(encoding="utf-8")), encoding="utf-8"); print(a.out)
    elif a.cmd == "similarity":
        from brandkit.similarity import compare
        refs = {Path(p_).stem: Path(p_).read_text(encoding="utf-8") for p_ in a.refs}
        for n, s, f in compare(Path(a.candidate).read_text(encoding="utf-8"), refs):
            print(f"{n}\t{s:.3f}\t{'FLAG' if f else ''}")
    elif a.cmd == "anchors":
        from brandkit import fetch_anchors, anchor_board
        cache = _run(a) / ".cache/anchors"
        fetch_anchors.main(str(REFS / "anchors.json"), str(cache))
        anchor_board.main(str(REFS / "anchors.json"), str(cache), str(cache / "boards"))
    elif a.cmd == "boards":
        from brandkit.boards import build
        out = _run(a) / "03-territory/boards"
        rev = S.next_rev(out, "palette", "png")
        for p_ in build(out, a.name, a.fonts or str(HERE / "fonts"), a.seed, rev):
            print(p_)
    elif a.cmd == "fonts-search":
        from brandkit.fonts import search
        for r in search(a.query, a.category, a.variable, a.limit):
            print(f"{r['family']:<32} {r['category']:<12} axes={','.join(r['axes']) or '-'}"
                  + (" (overused: avoid)" if r["overused"] else ""))
    elif a.cmd == "fonts-get":
        from brandkit.fonts import get
        print(json.dumps(get(a.family, _run(a) / ".cache/fonts"), indent=1))
    elif a.cmd == "lockup":
        from brandkit.lockup import lockup
        svg, rep = lockup(Path(a.mark).read_text(encoding="utf-8"), a.font, a.name, a.layout, a.fill, tracking=a.tracking)
        Path(a.out).write_text(svg, encoding="utf-8"); print(json.dumps(rep))
    elif a.cmd == "palette":
        from brandkit.palette import build
        pal = build(a.hexes)
        out = _run(a) / "06-system/palette.json"; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(pal, indent=1), encoding="utf-8"); print(out); print("flags:", pal["flags"])
    elif a.cmd == "tokens":
        from brandkit.tokens import emit
        pal = json.loads((_run(a) / "06-system/palette.json").read_text(encoding="utf-8"))
        knobs = json.loads(Path(a.knobs).read_text(encoding="utf-8"))
        _, files = emit(pal, knobs, _run(a) / "06-system/tokens", knobs.get("name", a.slug))
        (_run(a) / "06-system/knobs.json").write_text(json.dumps(knobs, indent=1), encoding="utf-8")
        print("\n".join(files))
    elif a.cmd == "ui":
        from brandkit import ui
        knobs = json.loads((_run(a) / "06-system/knobs.json").read_text(encoding="utf-8"))
        tok, out = _run(a) / "06-system/tokens", _run(a) / "06-system/ui"
        ui.write(tok, out, a.namespace, knobs.get("name", a.slug), knobs.get("depth", "borders"), knobs.get("pill", False))
        ui.cover(tok, out, knobs.get("name", a.slug)); print(out)
    elif a.cmd == "ui-gate":
        from brandkit.ui_gate import run as ugate, table
        res = ugate(_run(a) / "06-system/tokens", a.aaa)
        print(table(res)); ok = all(r[2] for r in res); print(f"\n**UI script gate: {'PASS' if ok else 'FAIL'}**")
        (_run(a) / "06-system/gate-ui.json").write_text(json.dumps(
            {"verdict": "PASS" if ok else "FAIL", "checks": [{"rule": k, "value": v, "pass": o} for k, v, o in res]}, indent=1),
            encoding="utf-8")
        sys.exit(0 if ok else 1)
    elif a.cmd == "graphic":
        from brandkit.graphic_language import generate
        for p_ in generate(Path(a.mark).read_text(encoding="utf-8"), json.loads(Path(a.params).read_text(encoding="utf-8")),
                           _run(a) / "06-system/graphic-language"):
            print(p_)
    elif a.cmd == "kit":
        from brandkit.kit import assemble
        print(assemble(_run(a), a.slug, a.name, a.idea, a.rationale))
    elif a.cmd == "kit-check":
        from brandkit.kit import check
        problems = check(_run(a) / "07-kit", a.slug)
        print("\n".join(problems) or "kit complete"); sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()

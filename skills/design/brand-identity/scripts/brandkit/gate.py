"""Script half of the gate: contact sheet PNG + script checks.

Usage: python -B -m brandkit.gate MARK.svg [MARK2.svg ...]
Writes MARK.sheet.png and MARK.gate.json next to each SVG and prints a markdown table.
The model-visual half (misreading, look-alike, blind reading, anchored comparison) is done
by viewing the sheet: see references/gate.md.
"""
import json
import sys
from pathlib import Path

from . import checks
from . import render_sheet


def gate(path, box=100.0):
    """Return (verdict, results); writes <stem>.sheet.png and <stem>.gate.json."""
    p = Path(path)
    stem = p.with_suffix("")
    svg = p.read_text(encoding="utf-8")
    render_sheet.sheet(svg, stem.name).save(str(stem) + ".sheet.png", optimize=True)
    res = checks.run(str(p), box)
    verdict = "PASS" if all(ok is not False for _, _, ok in res) else "FAIL"
    Path(str(stem) + ".gate.json").write_text(json.dumps(
        {"verdict": verdict, "checks": [{"check": k, "value": v, "pass": ok} for k, v, ok in res]}, indent=1),
        encoding="utf-8")
    return verdict, res


if __name__ == "__main__":
    for path in sys.argv[1:]:
        verdict, res = gate(path)
        print(checks.table(Path(path).stem, res))
        print(f"\n**script gate: {verdict}**\n")

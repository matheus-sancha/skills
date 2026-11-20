"""Run the gate on SVGs: contact sheet PNG + script checks table.

Usage: python -B gate.py MARK.svg [MARK2.svg ...]
Writes MARK.sheet.png and MARK.gate.json next to each SVG; prints a markdown table.
The model-visual half of the gate is: Read the .sheet.png and critique it.
"""
import json
import sys

import checks
import render_sheet

for path in sys.argv[1:]:
    stem = path[:-4]
    svg = open(path).read()
    render_sheet.sheet(svg, stem.rsplit("/", 1)[-1]).save(stem + ".sheet.png", optimize=True)
    res = checks.run(path)
    json.dump([{"check": k, "value": v, "pass": ok} for k, v, ok in res], open(stem + ".gate.json", "w"), indent=1)
    verdict = "PASS" if all(ok is not False for _, _, ok in res) else "FAIL"
    print(checks.table(stem.rsplit("/", 1)[-1], res))
    print(f"\n**script gate: {verdict}**\n")

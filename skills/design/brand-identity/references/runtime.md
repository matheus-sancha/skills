# Runtime

| Surface | Support |
|---|---|
| Claude Code (local or cloud) | full |
| claude.ai with network on | full, pending the vision check |
| Cowork with package-manager access on | full, pending the vision check |
| claude.ai / Cowork with network off | stop + how-to |
| Claude API / Skills API | stop + how-to |

There is **no degraded drawing tier**.

## When the probe runs

Once, just before the first drawing stage (Territory boards, or Intake for bring-your-own-mark). Brief and Audit need no tools and run anywhere.

```
python scripts/probe.py            # install + smoke test; prints PROBE <tier> ...
python scripts/probe.py --vision-challenge   # renders a PNG with a hidden code; view it
python scripts/probe.py --check "<code> <shape> <corner>"
```

Record the result with `python scripts/run.py probe <slug>` (it stores tier, Python version and vision in `state.json`).

## Install

`scripts/requirements.lock` pins skia-pathops, fontTools, uharfbuzz, brotli, resvg-py, shapely, svgpathtools, numpy, scipy, scikit-image and Pillow. Below Python 3.12, numpy 2.4.6 and scipy 1.17.1 (no 3.11 wheels for the newer ones). Wheels only (`--only-binary=:all:`), into a venv the skill owns:

- Claude Code: `~/.cache/brand-identity/venv`
- claude.ai / Cowork sandboxes: `./.venv`

Reuse the venv if it exists. Pinning keeps the gate thresholds, calibrated on one resvg version, reproducible.

## No vision

Script checks still gate. The user judges the render sheet (see `gate.md`). Say so up front.

## Network off

1. Save the brief, territory and decisions to `state.json`.
2. Tell the user to enable package-manager network access for code execution in that surface's settings (the probe output names what it could not reach; check the current settings page rather than quoting a menu path from memory).
3. Tell them how to resume in Claude Code: copy `brand/<slug>/` and say "continue the brand run for <slug>".

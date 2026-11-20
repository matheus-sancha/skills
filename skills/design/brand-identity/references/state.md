# Run folder and state

```
brand/<slug>/
  state.json
  run-log.md                 append-only
  01-brief.md                (+ 01-brief.r2.md …)
  02-audit.md, 02-audit/     (bring-your-own-mark: 02-intake/)
  03-territory/              word-map.md, boards/, reactions.md
  04-routes/                 plan.md, routes.md, withheld.md, R<n>-<idea-slug>/
  05-refine/
  06-system/
  07-kit/
  .cache/                    anchors, fonts, renders (never part of the kit)
```

**Revisions** are `<name>.r<N>.<ext>`, starting at r1, never overwritten. `state.json` points at the current one.

## `state.json`

```json
{
  "schema": 1,
  "slug": "linnet",
  "entry": "full",
  "stage": "routes",
  "stages": {
    "brief":     {"status": "approved", "current_rev": "r1"},
    "audit":     {"status": "approved", "current_rev": "r1"},
    "territory": {"status": "approved", "current_rev": "r2"},
    "routes":    {"status": "in_progress", "current_rev": null},
    "refine":    {"status": "todo", "current_rev": null},
    "system":    {"status": "todo", "current_rev": null},
    "kit":       {"status": "todo", "current_rev": null}
  },
  "decisions": [{"id": "D1", "stage": "brief", "text": "Big idea: ...", "by": "user", "at": "2026-11-20T19:00:00Z"}],
  "routes": [{"id": "R1", "idea": "...", "type": "pictorial", "status": "candidate", "reason": null, "redraws": 0}],
  "budget": {"replacements_used": 0},
  "probe": {"tier": "full", "python": "3.13.1", "vision": true, "at": "..."},
  "connectors": {"miro": false, "figma": false, "hyperframes": false},
  "created_at": "...",
  "updated_at": "..."
}
```

- `entry`: `full` | `byom`. Stage status: `todo | in_progress | awaiting_user | approved | stale`. Route status: `candidate | withheld | shown | chosen | rejected`. `stage` may be `complete`.
- Bring-your-own-mark runs mark `territory` and `routes` as `skipped` and use `intake` in place of `audit`.
- `python scripts/run.py status <slug>` prints a two-line resume summary.
- `python scripts/run.py reopen <slug> <stage>` sets that stage to `in_progress` and every later stage to `stale`.

## `run-log.md`

One entry per round:

```
## 2026-11-20 19:12 · routes · R2 r3
action: redraw (H4 misread as mountain → walls added)
hard fails: none · flags: optical centring t=1.2
redraws: 3/5 · user: —
```

The run ends with a summary table, which sample runs compare: routes tried / shown / withheld, redraws per route, rounds per stage, reopened stages, probe tier. `python scripts/run.py summary <slug>` writes it.

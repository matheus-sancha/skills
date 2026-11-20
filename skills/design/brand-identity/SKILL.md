---
name: brand-identity
description: Design a brand identity the way an identity studio does — strategy brief, reaction boards, studio-tier logo routes gated by render-then-review, a full logo system, colour, type, graphic language and a UI design system (tokens + core components) delivered as a kit. Use when the user asks to "design a logo", "create a brand identity / visual identity / brand kit", "derive a design system from our brand", or brings an existing logo to "audit", "refresh" or "turn into a full kit". Not for building UI screens on an existing system (frontend-design, flutter-ui-design), theming a deck (theme-factory), posters (canvas-design) or applying a brand that already has guidelines.
version: 0.1.0
license: MIT
---

# Brand Identity

Work as an identity studio. Take the user from strategy to a finished **kit**: the logo system, colour, type, graphic language, a one-page brand sheet and a UI design system derived from them. The user judges and chooses; you do the research, drawing, gating and assembly.

## Hard rules

1. **Nothing sub-tier is shown.** Every mark passes the gate (`references/gate.md`) before the user sees it. A route that fails is withheld and reported by name and reason, never padded in.
2. **Never use AI image generation for a mark.** Marks are drawn with the primitive library (`scripts/brandkit/primitives.py`). AI imagery is allowed only on reaction boards and mockups, labelled "AI".
3. **Never claim a mark is clear to register.** Show the trademark notice from `references/gate.md` with the routes and in the kit.
4. **Never bundle third-party logos.** Anchor marks are fetched at run time into `.cache/`.
5. **Never invent** design principles, attributions, API behaviour, font licences, CMYK or Pantone values.
6. **One vocabulary.** Use only the terms in `references/glossary.md`, one meaning each. "Concept", "direction" and "option" are always *route*; "logo" is always the whole logo system. Gloss each term in one plain line the first time the user meets it.
7. **Loops never overwrite.** Every revision is a new `<name>.r<N>.<ext>` file.

## Start of every run

1. Ask for or derive a slug. If `brand/<slug>/state.json` exists, read it, tell the user in two lines where the run stands and what was last decided, and offer to continue (`references/state.md`).
2. Otherwise pick the entry:
   - **full** — a new identity: all seven stages.
   - **byom** (bring your own mark) — the user has a mark: short Brief → Intake gate report → Refine (keep or refresh) → System → Kit.
3. Create `brand/<slug>/` and `state.json` (`python scripts/run.py init <slug> --entry full|byom`).

## The seven stages

Each stage writes one artifact and ends at a user checkpoint. Read the stage's reference before starting it.

| # | Stage | Artifact | Reference | Checkpoint |
|---|---|---|---|---|
| 1 | Brief | `01-brief.md` | `references/brief.md` | user signs off brief and big idea |
| 2 | Audit | `02-audit.md` (byom: `02-intake/`) | `references/audit.md` | user confirms clichés to avoid |
| 3 | Territory | `03-territory/` word map + reaction boards | `references/territory.md` | user reacts to boards |
| 4 | Routes | `04-routes/` | `references/routes.md`, `references/gate.md`, `references/anchors.md` | user chooses a route |
| 5 | Refine | `05-refine/` logo system | `references/refine.md` | user approves the logo system |
| 6 | System | `06-system/` colour, type, graphic language, UI tokens | `references/system.md` | user approves palette, type and knobs |
| 7 | Kit | `07-kit/` | `references/kit.md` | user approves the brand sheet |

**Before the first drawing stage** (Territory boards for full runs, Intake for byom) run the runtime probe (`references/runtime.md`). If it reports STOP, save state, explain how to enable network on that surface, and stop.

## Checkpoints

At every checkpoint, offer exactly three things:
1. **Approve** and go to the next stage (the default).
2. **Loop** this stage with a note.
3. **Reopen** a named earlier stage. Downstream stages become `stale`; re-run them on the way forward and keep what still holds.

Record every decision with `python scripts/run.py decide <slug> <stage> "<text>" --by user|agent` and append a round to `run-log.md`.

## The gate, in one paragraph

Script checks → misreading and look-alike check → anchored comparison, in that order; any hard fail stops the mark and it is redrawn. 5 redraws per route, each changing what the failing check named; two failures in a row on the same check stop the route; at most 2 replacement routes per run. Details and thresholds: `references/gate.md`.

## Done

A run is complete when the final logo system and UI system pass every hard gate, `python scripts/run.py kit-check <slug>` finds every required file, and the user approves the brand sheet. Set `stage: complete`. Later changes start a new revision.

## Defer instead of duplicating

Critique wording → `design:design-critique`; WCAG audit of screens → `design:accessibility-review`; UI pages from the system → `frontend-design`; deck theming → `theme-factory`; posters → `canvas-design`; Flutter theming → `flutter-ui-design` (consumes `tokens.dtcg.json`); motion rendering → HyperFrames when present.

# The gate

Every mark passes the gate before the user sees it. **Studio tier** means the mark holds its own beside a set of known-good anchor marks of the same type. There is no checklist score.

## Order

1. **Script checks** (`run.py gate`). Auto-fix path hygiene first.
2. **Misreading and look-alike check** (model-visual on the render sheet).
3. **Blind concept reading** (fresh look, no rationale).
4. **Anchored comparison** (model-visual, one sheet with the anchor set).

Any hard fail stops the mark; redraw it.

## Hard fails

| # | Check | How |
|---|---|---|
| H1 | Stroke and gap ≥ 1 px at 16 px **on the master shipped at 16 px** (the small master if one exists, otherwise the main master) | script, absolute width |
| H2 | Mono separability: every region stays distinct in one colour and reversed | script + sheet |
| H3 | Path hygiene: missing extrema, redundant nodes, unintended kinks, anything outside the live area | script; auto-fixed first, fails only if the fix fails |
| H4 | Misreading: list the three things the mark could be mistaken for. A clear match with something unintended fails | model-visual |
| H5 | Look-alike: on one sheet with the audit's competitor marks and the anchor set, "Could this be mistaken for any of these?" A clear match fails | model-visual |
| H6 | Blind reading: describe what the mark suggests in a few words with no brief shown. No overlap with the word map fails | model-visual (fresh context or subagent where possible) |
| H7 | Anchored comparison: "Would this sit in that set without looking weaker? Name the weakest thing about it." Weaker fails | model-visual |

## Flags

Pass flags into the anchored comparison as "known weaknesses"; the construction log must fix or justify each.

- overshoot ratios; horizontal vs vertical stroke; circle vs square sizing; grid snapping; stroke and radius clustering
- optical centring: *t* outside 0–1 (default *t* = 0.75 from bbox centre toward the area centroid)
- lockup mark height outside 1.3–2.5× cap height; gap > 0.4× mark width or < 0.2× cap height
- more than 5 shapes
- partial resemblance to an audit or anchor mark (H5) or partial word-map overlap (H6): the rationale must disclose it
- silhouette similarity score above the default threshold (`similarity.py`; proposed default, calibrate in sample runs)
- full-colour mark below 3:1 against a ground: leave that ground off the approved list

## Info only

SSIM 16 vs 256→16; centroid vs bbox offset.

## Without self-viewing

If the probe reports no vision, script checks still gate. Hand the model-visual checks to the user: show the render sheet (256 / 48 / 32 / 16 px, mono, reversed) with a short checklist (reads as the large mark at 16 px? optically centred? blobs at joins? mistaken for anything? looks like a competitor?). The user's reply counts as the visual pass. Say up front that this is happening.

## Budget

- 5 redraws per route. Each must change what the failing check named, logged in `REVS` with its `why`.
- **Stall:** two failures in a row on the same hard check stop the route.
- A route that runs out of budget or stalls is **withheld** and replaced by a fresh idea from the word map, at most **2 replacements per run**.
- If fewer routes pass than the target, show only those, say how many were withheld and why, and ask whether to revise the brief or try new routes. **Never pad with a sub-tier route.**

## Trademark notice (fixed wording)

Show with the routes and in the kit README:

> These marks have not been searched against trademark registers. Before using one commercially, have a trademark search done in each market you'll trade in. Free starting points: WIPO Global Brand Database (image search), INPI (Brazil), USPTO and EUIPO.

## UI gate

Rules U1–U15 and colour-blind simulation: see `system.md`.

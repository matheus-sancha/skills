# Stage 4: Routes

Goal: **three routes by default** (the user may ask for 2–5), each built on a **different idea**, spread safe → just right → unexpected. Only routes that pass the gate are shown.

## 1. Pick the ideas

For each route choose one motif or a pairing from the word map, a mark type (wordmark, letterform, pictorial, abstract) using the brief's `mark_type_hints`, and a one-line rationale tied to the big idea. Respect the `territory:` constraints. Write them to `04-routes/plan.md`.

## 2. Explore at volume

Generate **at least 10× more variants than you will show** (this skill's own rule; the ratio is not a sourced standard). Variants are parameter sweeps and structural alternatives of the recipe, rendered small on one exploration sheet. Keep the best one or two per route for the gate. The exploration stays on file in the route folder.

## 3. Write a recipe

Each route is `04-routes/R<n>-<idea-slug>/recipe.py`: a data header plus one `build(rev)` function.

```python
ROUTE = {"id": "R2", "idea": "sun behind a roof", "type": "pictorial",
         "rationale": "A home that makes its own daylight."}
BOX = 100
CONSTRAINTS = {"min_stroke": BOX / 16, "min_gap": BOX / 16, "padding": BOX / 12,
               "max_shapes": 5, "colours": ["#1e2b3a", "#f0a531"]}
REVS = {
    "r1": {"sun_cx": 50, "gap": 5, "why": "first build"},
    "r2": {"sun_cx": 64, "gap": 7, "why": "misread as a person icon: move sun off-centre"},
}

def build(rev):
    from brandkit.primitives import Mark
    p = REVS[rev]
    m = Mark(f'{ROUTE["id"]}_{rev}', BOX)
    ...                       # compose primitives; log optical corrections with m.note_param()
    return m, [(roof, "#1e2b3a"), (sun, "#f0a531")]   # the Mark and its (shape, fill) layers
```

- The 16 px minimums are **drawing constraints**: set them before drawing. `BOX/16` is 1 px at 16 px.
- A redraw adds a new `REVS` entry with its `why`; it must change what the failing check named. Repeating an earlier revision's parameters does not count.
- Hand-written SVG is allowed: save it as `mark.rN.svg`, mark the construction log `"hand_written": true`, and flatten it before the gate (`run.py flatten`).
- A **small master** is allowed when the master breaks down at 16 px. Draw it as its own recipe entry (`small: true`).

Build and gate: `python scripts/run.py route <slug> brand/<slug>/04-routes/R2-<idea-slug> r1` writes `mark.r1.svg`, `mark.r1.construction.json`, `mark.r1.sheet.png` and `mark.r1.gate.json`.

## 4. Gate

Run the full gate (`gate.md`). Redraw within budget, or withhold and replace.

## 5. Present

For each passing route show: **its idea**, **a one-line link to the brief**, and **the mark in use on two or three mockups** (e.g. a sign, an app icon, a cup or a web header). Mockups are composed from the mark and the territory palette; AI imagery may be used as a background only, labelled "AI".

Then:
- name any withheld routes and the check or verdict that killed each;
- say what each mark communicates and what it doesn't (from the blind reading);
- show the trademark notice from `gate.md`.

Write what was shown to `04-routes/routes.md` and what was withheld to `04-routes/withheld.md`. The variants and gate logs stay on file and are shown only on request.

Checkpoint: the user chooses a route (or asks for a loop). Record the choice; mark the others `rejected`.

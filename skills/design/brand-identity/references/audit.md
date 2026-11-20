# Stage 2: Audit (and Intake for bring-your-own-mark)

## Audit (full runs)

Goal: know what the competitors look like, so the routes avoid the sector's clichés.

1. For each competitor in the brief, collect the mark, main colours, type style and any graphic device. Use the web when it is reachable; otherwise ask the user for screenshots or images.
2. Save images to `02-audit/` (they are for comparison only and never go into the kit).
3. Write `02-audit.md`: a table (competitor, mark type, colours, type, device) and a list of **clichés to avoid** (e.g. "every cycling brand uses a wheel", "green leaf for sustainability").
4. Checkpoint: the user confirms or edits the cliché list.

The audit marks are reused by the look-alike check at the gate (`gate.md`).

## Intake (bring your own mark)

1. Accept **SVG** (preferred) or a PDF with vector content. Save originals to `02-intake/source/`.
2. A raster-only mark is **not traced automatically**. Offer to rebuild it as a recipe in Refine; do it only with the user's OK, and log it as a redraw.
3. Flatten masks, clips and strokes to filled paths, then run the full gate (`python scripts/run.py gate <svg> --route-type <type>`) with **no redraws**.
4. Write `02-intake/report.md`: hard fails, flags and the anchored-comparison verdict, in plain words.
5. Ask the user: **keep** (Refine fixes only what the gate found) or **refresh** (Refine may evolve the mark within the same idea, under the full gate and redraw budget).

The 1 px-at-16 hard fail binds only the master shipped at 16 px; a small master can solve it.

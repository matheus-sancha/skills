# Stage 5: Refine (the logo system)

Goal: turn the chosen route's mark into a complete logo system that passes the gate at every size.

## 1. Master and small master

- Polish the master: overshoot, optical centring (*t* = 0.75), stroke and radius clustering, extrema. Every flag from Routes is fixed or justified in `construction.md`.
- If the master fails H1 at 16 px, draw a **small master**: fewer parts, wider gaps, same idea. H1 binds only the master that ships at 16 px.
- Save `05-refine/master.rN.svg` and `small-master.rN.svg`.

## 2. Wordmark

- Set the name in the chosen face (`system.md` type pairing may be drafted now) with `outline_text`: HarfBuzz shaping, kerning, then outlines. **Text is always outlined**; the kit never contains `<text>`.
- Adjust with the primitives (spacing, cuts, joins, a ligature) — no custom alphabets.
- Save `05-refine/wordmark.rN.svg`. Record font family, version and licence (OFL fonts allow outlined logos; keep `OFL.txt` with any shipped font files).

## 3. Lockups

Defaults calibrated on 20 published lockups:

| Measure | Default | Flag outside |
|---|---|---|
| Mark height | 1.5× cap height | 1.3–2.5× cap (x-height for all-lowercase words with no ascenders) |
| Mark–word gap | 0.4× cap height (≈ 0.27× mark width) | > 0.4× mark width or < 0.2× cap height |
| Vertical alignment | mark centred on the cap band | baseline or ascender–descender anchoring only when declared |
| Mark line weight (line-drawn marks) | 1.0–1.75× wordmark stem | flag below 1.0× |

Keep **one ratio across all lockups** of the system. Build `horizontal` and `stacked` with `lockup.py`.

## 4. Clear space and minimum size

- Clear space: **0.5× mark height**, floor 0.17×, expressed as a named mark unit.
- Minimum size: the smallest size at which the shipped master passes H1 (16 px for the small master or mark; state the lockup minimum in px).

## 5. Colourways

Colour, black and white (reversed) for every layout. Mono and reversed must pass H2. Name the approved grounds; a full-colour mark below 3:1 on a ground leaves that ground off the list.

## 6. Gate and checkpoint

Run the full gate on master, small master and each lockup. Show the logo system sheet (layouts × colourways, clear-space diagram, 16/32 px row). Checkpoint: the user approves the logo system.

### Bring your own mark

- **keep:** fix only the gate's findings (and add a small master if needed).
- **refresh:** evolve the mark within the same idea, under the full gate and redraw budget.

# Stage 3: Territory (word map and reaction boards)

## Word map

1. Start from the name, the big idea, the values and the attribute words.
2. Branch out associations two or three levels deep.
3. Flag the ones that could become a mark as **motifs**. Strike any that match an audit cliché.
4. Save as `03-territory/word-map.md` (an indented list is enough).

## Reaction boards

Make **three boards**, each with **six tiles lettered A–F**:

| Board | Tiles show | Built with |
|---|---|---|
| palette | six palette families: hue set, chroma level, neutral temperature | `boards.palette_tiles` |
| shape | six shape studies from the motifs: sharp vs round, heavy vs light, geometric vs organic | the primitive library |
| style | six type-and-attitude specimens: type class, weight, case, spacing | outlined bundled OFL faces |

- AI mood images may be mixed in, labelled "AI" on the tile. Licensed reference images only when a licence-tracking source is available.
- **No third-party logos on boards.**
- Every tile has a **parameter record** (`boards/<board>.rN.json`) so a reaction maps to constraints.

Build them with `python scripts/run.py boards <slug>`; it writes `03-territory/boards/{palette,shape,style}.rN.png` and the matching `.json`.

## Showing boards

- **Miro connected:** one frame per board on a run board (`canvas_create_from_svg`). Ask the user to add stickies or comments; read them back with `canvas_read_as_svg` and `comment_list_comments`.
- **Otherwise:** show each PNG in chat (an Artifact page where available).

Ask, per board: *up to two "more of", up to two "not this", and an optional note*, e.g. `palette: B, E more; A not`. Silence on a board means no constraint.

## Recording

1. Write the raw answer to `03-territory/reactions.md`.
2. Map each picked tile's parameter record into the brief's `territory:` block:

```yaml
territory:
  palette: {more: [{hues: [28, 210], chroma: high, neutral: warm}], not: [...]}
  shape:   {more: [{corners: round, weight: heavy, form: geometric}], not: [...]}
  style:   {more: [{type_class: grotesque, case: lower}], not: [...]}
```

Routes reads these as constraints. Checkpoint: the user confirms the territory summary.

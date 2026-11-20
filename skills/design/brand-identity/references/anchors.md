# Anchor sets

Four sets, one per mark type, used by the anchored comparison (gate H7) and the look-alike check (H5). Approved by Matheus.

| Set | Anchors |
|---|---|
| letterform | V&A, Pinterest P, Netflix N, Mastodon, Mozilla symbol (2024) |
| pictorial | WWF panda, Apple, Mailchimp Freddie, Bluesky |
| abstract | Deutsche Bank, Airbnb, Slack, BP, Dropbox, Kubernetes |
| wordmark | Coca-Cola, Netflix, Google, Mozilla, Vogue, The New Yorker |

## Rules

- **Logos are never bundled.** `anchors.json` holds names and owner sources only. `python scripts/run.py anchors <slug>` fetches the SVGs into `brand/<slug>/.cache/anchors/`, pinned by sha256, and warns when an owner's file changed.
- An accepted source is one the owner controls: a direct SVG, an official zip, the owner's repo or npm package, or an inline or sprite SVG on the owner's own page.
- Tile anchors (e.g. Pinterest P, Mastodon) need reversed-glyph extraction for the mono comparison; the fetch script does it.
- The user may add their own anchors with equal weight, if each exists as an owner SVG and fits a set. Each set stays capped at 6, so adding one means dropping one.
- When an anchor can't be fetched (no network, owner changed the file), compare against the ones that could be and say which were missing.

## The comparison sheet

`render_board.py`-style sheet: the candidate and the set at the same sizes (256 / 48 / 16 px) and in mono, on one PNG. Ask: "Would this sit in that set without looking weaker? Name the weakest thing about it."

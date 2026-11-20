# Prototype: the four anchor sets for the studio-tier comparison

Throwaway groundwork for issue 28 ("Which marks make up the four anchor sets for the studio-tier comparison?"). The anchored comparison itself was decided in issue 16 ("What rubric does the self-critique score against, and what counts as a pass?"). Matheus approved every anchor below on 2026-11-20.

**No logo is stored in this repo.** `anchors.json` holds names and owner sources only. `fetch_anchors.py` caches the SVGs outside the repo at run time, and `out/` holds only the rendered comparison boards.

## How to run

```sh
python -m venv /outside/repo/venv
/outside/repo/venv/bin/pip install --only-binary=:all: resvg_py==0.5.0 pillow
D=docs/prototypes/anchor-sets
$PY -B $D/fetch_anchors.py $D/anchors.json /outside/repo/anchor-cache   # -> <set>/<slug>.svg, lock.json, status.json
$PY -B $D/render_board.py  $D/anchors.json /outside/repo/anchor-cache $D/out
```

Observed on 2026-11-20 (Windows 11, Python 3.12): all 21 anchors fetched, and a second run reported no hash changes.

## Source kinds (all owner-controlled, per Matheus's answer to question 1)

| kind | What it reads | Example |
|---|---|---|
| `url` | a direct SVG file on the owner's domain, CDN, GitHub repo or npm package | joinmastodon.org, raw.githubusercontent.com/bluesky-social, cdn.jsdelivr.net/npm/@mozilla-protocol |
| `inline` | an `<svg>` in the owner's own page, picked by a regex on its opening tag | Pinterest P, Netflix N, Apple, BP |
| `sprite` | a `<symbol id>` in the owner's SVG sprite, found via the owner's page | V&A |
| `page_link` | an SVG linked from the owner's page, picked by its content | Netflix wordmark |
| `zip` | a member of an official zip from the owner's brand page | (none in the final sets; supported for GitHub/Spotify-style kits) |

`lock.json` pins a sha256 per anchor, and a later change is reported as a warning, never accepted silently. Inline sources are A/B-served: the Pinterest P was missing from one of four page loads, so the fetcher retries 3 times.

**Not fetchable, so excluded:** Unilever, Mastercard and FedEx (their CDN blocks automated fetches), Uber (logo rendered only by JavaScript), Juventus (no logo SVG found), Shell and NBC (no SVG found). Wikimedia copies are not owner sources.

## The approved sets

| Set | Anchors |
|---|---|
| Letterform / monogram (5) | V&A, Pinterest P, Netflix N, Mastodon, Mozilla flag (2024) |
| Pictorial (4) | WWF panda, Apple, Mailchimp Freddie, Bluesky butterfly |
| Abstract / geometric (6) | Deutsche Bank, Airbnb Bélo, Slack, BP Helios, Dropbox, Kubernetes |
| Wordmark only (6) | Coca-Cola, Netflix, Google, Mozilla (2024), Vogue, The New Yorker |

The provenance and rationale for each anchor are in the resolution comment on issue 28.

## What the boards show (observed)

- **The silhouette row is crude on purpose.** Every painted pixel becomes black. That flattens badge and tile marks (Mailchimp, Airbnb, Dropbox) into solid shapes. The real comparison needs a proper mono or reversed extraction for tile-sourced anchors: the white glyph, reversed out. That is a spec-assembly detail.
- **Several approved anchors are soft at 16 px:** Netflix N's fold, BP Helios and Kubernetes' spokes. The comparison sheet shows anchors at the same sizes as the candidate, so a candidate is never asked to beat its anchors at a size the anchors themselves don't hold. The 16 px floor still comes from the hard gate, on the master that ships at 16 px.
- **Every wordmark is mush at 16 px.** Wordmarks are compared at lockup and header sizes only.

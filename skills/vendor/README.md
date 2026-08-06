# Vendored skills

Third-party skills copied into this repo rather than authored here. They are
installed alongside the authored skills, but they are **not** ours — keep edits
minimal so a future re-sync against upstream stays cheap.

Vendoring means this repo owns updates from now on: the external `skills` CLI
(which writes `~/.agents/.skill-lock.json`) no longer manages these, because the
installed paths are symlinks into this repo. To update one, re-copy from
upstream and record the new commit below.

| Skill | Upstream | Path in upstream | Vendored at |
|---|---|---|---|
| [building-native-ui](./building-native-ui/) | [expo/skills](https://github.com/expo/skills) | `plugins/expo/skills/building-native-ui/` | folder hash `0078663cbdc42e388d2eb9c291dda1a0774eee29` |
| [find-skills](./find-skills/) | [vercel-labs/skills](https://github.com/vercel-labs/skills) | `skills/find-skills/` | folder hash `3013fdeb8a11b10b1eb795ec3ae8bfca38f7c26d` |

Hashes are the `skillFolderHash` values recorded by the `skills` CLI at install
time (2026-05-31), carried over from `~/.agents/.skill-lock.json`.

## Licensing

`building-native-ui` declares `license: MIT` in its frontmatter. `find-skills`
declares no license in its frontmatter; check the upstream repo before
redistributing it.

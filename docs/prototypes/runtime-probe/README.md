# Runtime probe (throwaway prototype)

This is a probe for the map ticket [Do pip installs and self-viewing of renders work on claude.ai and Cowork?](https://github.com/matheus-sancha/skills/issues/25). It lives under `docs/`, not `skills/`, so it is never installed as a live skill in this repo.

It answers the two facts left open by [Which runtimes must the skill support, and what degrades where it can't see or install?](https://github.com/matheus-sancha/skills/issues/21):

1. Does the pinned drawing stack (`requirements.lock`) install and work on this surface?
2. Can the model genuinely view a PNG it rendered? This is tested with a hidden-answer challenge: a random code and a shape in a random corner. The answer is stored only as a salted hash, and only the first answer counts.

## What you do (about 10 minutes)

1. Zip this folder. The zip contains the `runtime-probe/` folder with `SKILL.md` inside. If the upload rejects that layout, re-zip from inside the folder so `SKILL.md` is at the root, and note which layout worked.

   ```bash
   cd docs/prototypes && zip -r runtime-probe.zip runtime-probe -x 'runtime-probe/README.md'
   ```

2. **claude.ai:** turn on code execution and set network access to at least package managers. Upload `runtime-probe.zip` as a custom skill. In a new chat, type: *"Run the runtime-probe skill."*
3. **Cowork:** add the same skill, set network access to "package managers only", and run the same prompt.
4. Paste each `PROBE …` line, plus the model's one sentence about how it viewed the image, into the ticket. Note your plan (Pro/Max/Team) and the network setting you used.

If the upload is refused, record that too: the refusal and any size limit it mentions both answer open questions.

## Reading the line

```
PROBE py=3.13.18 plat=Linux-x86_64 install=OK t=15.8s smoke=OK pathops=OK resvg=OK vision=OK
```

| Field | Meaning |
|---|---|
| `install=FAIL(network)` | pip could not reach PyPI. Network is off or restricted, so this surface is the "stop + how-to" case. |
| `install=FAIL(no-wheel)` | No wheel for this Python or platform. Record the `py` and `plat` values. |
| `smoke=FAIL` | Installed, but booleans or rendering failed. Full error is in `.probe/result.json`. |
| `vision=OK` | The model read the code, shape and corner correctly on its first try. |
| `vision=FAIL` / `FAIL-RETRY` | Wrong answer, or a second attempt. Treat as "cannot self-view". |
| `vision=NOT-RUN` | The model could not view the image or skipped the step. |

## Verified in this repo's cloud session (Claude Code, Linux x86_64)

These are observed results, not inferred:

| Python | install | time | smoke | vision |
|---|---|---|---|---|
| 3.13.18 | OK | 15.8 s | OK (pathops union, resvg PNG) | OK. The model read `TWNM`, triangle, bottom-right. A deliberately wrong answer returned `FAIL`, and a retry returned `FAIL-RETRY`. |
| 3.11.18 | OK | 17.7 s | OK | not run |

**Finding from these runs:** numpy 2.5.5 and scipy 1.18.1, the versions verified in `svg-tooling.md`, have **no Python 3.11 wheels**. The lock therefore pins numpy 2.4.6 and scipy 1.17.1 below Python 3.12. The real skill's lock needs the same split, because the Claude API sandbox is documented as Python 3.11. All 11 wheels also resolve for macOS arm64 on Python 3.13; this was checked by download, not by running.

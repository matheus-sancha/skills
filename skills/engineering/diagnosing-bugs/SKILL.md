---
name: diagnosing-bugs
description: Diagnosis discipline for hard bugs — build a tight, red-capable feedback loop before hypothesising. Use when a bug has survived an obvious fix attempt, its cause is non-obvious, it reproduces only intermittently, or something has become measurably slower.
---

# Diagnosing Bugs

A discipline for **hard** bugs. Skip phases only when explicitly justified.

**If the cause is plain on inspection, fix it and skip this skill.** The ceremony below buys nothing on a typo'd import; it exists for bugs that have already defeated a direct attempt.

When exploring the codebase, read `CONTEXT.md` if it exists to get a mental model of the relevant modules, and check any ADRs covering the area you're touching.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal that goes **red** on _this_ bug, you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

[FEEDBACK-LOOP.md](FEEDBACK-LOOP.md) holds the ten ways to construct a loop, ordered by preference, plus how to handle bugs that reproduce only sometimes. Read it now unless the right loop is already obvious.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Faster? Cache setup, skip unrelated init, narrow the test scope.
- Sharper signal? Assert on the specific symptom, not "didn't crash".
- More deterministic? Pin time, seed RNG, isolate filesystem, freeze network.

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is a debugging superpower.

### Completion criterion — a tight loop that goes red

Phase 1 is done when you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (paste the invocation and its output), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it goes red on this bug and green once fixed. Not "runs without erroring".
- [ ] **Deterministic** — same verdict every run (for flaky bugs: a pinned, high reproduction rate).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — runnable unattended; a human in the loop only via the HITL harness in [FEEDBACK-LOOP.md](FEEDBACK-LOOP.md).

If you catch yourself reading code to build a theory before this command exists, **stop — jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

If you genuinely cannot build a loop, stop and say so explicitly. List what you tried. Ask for: access to an environment that reproduces it, a captured artifact (HAR, log dump, core dump, timestamped screen recording), or permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

## Phase 2 — Reproduce and minimise

Run the loop. Watch it go red.

Confirm the failure is the one the **user** described — not a different failure that happens to live nearby. Wrong bug, wrong fix.

Then shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running after each cut. A minimal repro shrinks the hypothesis space in Phase 3 and becomes the clean regression test in Phase 5.

_Done when_: every remaining element is load-bearing — removing any one of them makes the loop go green.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each must be **falsifiable** — state the prediction it makes:

> "If X is the cause, then changing Y will make the bug disappear / changing Z will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often re-rank it instantly ("we just deployed a change to #3") or know what's already been ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is away.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

1. **Debugger / REPL inspection** where the environment supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix — `[DEBUG-a4f2]` — so cleanup is one grep. Untagged logs survive; tagged logs die.

**Performance branch.** For regressions, logs are usually wrong. Establish a baseline measurement (timing harness, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix and regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow — a single-caller test when the bug needs multiple callers, a unit test that can't replicate the triggering chain — a test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it: the architecture is preventing the bug from being locked down. Carry it to Phase 6.

With a correct seam:

1. Turn the minimised repro into a failing test there.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original, un-minimised scenario.

## Phase 6 — Cleanup and post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes, or the absence of a seam is documented
- [ ] All `[DEBUG-...]` instrumentation removed (grep the prefix)
- [ ] Throwaway prototypes deleted, or moved somewhere clearly marked
- [ ] The hypothesis that proved correct is stated in the commit or PR message, so the next debugger learns

**Then ask: what would have prevented this bug?** If the answer is architectural — no good test seam, tangled callers, hidden coupling — hand off to `/codebase-design` with the specifics; if it's accumulated waste or duplication, hand off to `/lean-code-reviewer`. Make the recommendation **after** the fix is in: you know more now than when you started.

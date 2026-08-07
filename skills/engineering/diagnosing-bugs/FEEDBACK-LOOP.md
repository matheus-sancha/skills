# Constructing a feedback loop

Ten ways to get a signal that goes **red** on the bug, roughly in order of
preference. Take the first that fits — the list descends from cheapest and
sharpest to most awkward.

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM, console, or network.
5. **Replay a captured trace.** Save a real request, payload, or event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** A minimal subset of the system — one service, mocked deps — that hits the bug path in a single function call.
7. **Property / fuzz loop.** For "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so `git bisect run` can drive it.
9. **Differential loop.** Run the same input through old vs new (or two configs) and diff the outputs.
10. **HITL harness.** Last resort — see below.

## Bugs that reproduce only sometimes

The goal is not a clean repro but a **higher reproduction rate**. Loop the
trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps.

A 50%-flake bug is debuggable; 1% is not. Keep raising the rate until it is,
and pin whatever raised it so the loop stays deterministic enough to trust.

## HITL harness

When a human must click, drive *them* — don't abandon the loop. Structure it so
each iteration is identical and the output comes back to you:

```bash
#!/usr/bin/env bash
# hitl-loop.sh — structured human-in-the-loop repro.
# Keeps a manual repro reproducible: same steps, same capture, every run.
set -euo pipefail

RUN=0
OUT="${OUT:-./hitl-runs}"
mkdir -p "$OUT"

while true; do
  RUN=$((RUN + 1))
  echo
  echo "=== run $RUN ==="
  cat <<'STEPS'
  1. <exact step>
  2. <exact step>
  3. <the action expected to trigger the bug>
STEPS
  read -r -p "Did the bug appear? [y/n/q] " verdict
  case "$verdict" in
    q) exit 0 ;;
    y) result=RED ;;
    *) result=GREEN ;;
  esac

  # Capture whatever the loop asserts on, every run, bug or not - the green
  # runs are the baseline that makes the red ones legible.
  {
    echo "run=$RUN result=$result time=$(date -Is)"
    echo "--- logs ---"
    tail -n 200 "${LOG:-/dev/null}" 2>/dev/null || true
  } > "$OUT/run-$RUN.txt"

  echo "captured -> $OUT/run-$RUN.txt  ($result)"
done
```

Fill in the steps precisely enough that two runs differ only by chance, never
by what the human did. Point `LOG` at whatever the bug leaves traces in.

The captured runs feed back to you: read the reds against the greens and the
difference is the signal.

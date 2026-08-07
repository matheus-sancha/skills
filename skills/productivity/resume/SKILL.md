---
name: resume
description: Pick up work from a handoff document — rebuild the mental model, verify the world hasn't moved since it was written, and confirm before acting.
argument-hint: "Path to the handoff document (omit to search the temp directory)"
disable-model-invocation: true
---

# Resume

The counterpart to `/handoff`. That skill compacts a session into a document; this one turns the document back into a working mental model.

A handoff is a **snapshot of a world that kept moving**. It deliberately doesn't duplicate PRDs, plans, ADRs, issues, commits, or diffs — it references them by path. So the document alone is never enough: the referenced artifacts are the real content, and any of them may have changed since it was written.

## Steps

1. **Find the document.** Use the path if the user gave one. Otherwise search the OS temp directory — where `/handoff` writes — and take the most recent. If several are plausible, list them with timestamps and ask which.
   _Done when_: you have one document and the user hasn't contradicted the choice.

2. **Read it, then follow every reference.** Open each artifact it points at — specs, plans, ADRs, issues, branches. The handoff tells you *where the work was*; these tell you *what the work is*.
   _Done when_: every referenced artifact has been opened, or is recorded as missing in step 3.

3. **Check for drift.** The handoff was true when written. Establish what's changed since:
   - Does every referenced path still exist?
   - Has the branch moved? Compare against what the document describes; `git log` since its timestamp.
   - Are the issues it names still open, and do they still say what it claims?
   - Does the code still match the state it describes?

   _Done when_: each reference is confirmed current, or listed as drifted with what changed.

4. **Invoke the suggested skills.** `/handoff` writes a "suggested skills" section; treat it as instruction from the previous session, which knew things you don't.

5. **Confirm before acting.** Report back, briefly:
   - What you understand the work to be, and the next concrete step.
   - **What has drifted** since the handoff, and whether it changes the plan.
   - Anything the document assumes that you couldn't verify.

   Then stop and wait. A handoff is a claim about the past; acting on it without checking is how a session confidently continues work that was already finished, abandoned, or redirected.

## When the handoff is thin

Some handoffs are written well and some are written at the end of a long session by an agent running low on context. If the document is vague, don't paper over it — the gap is information.

Say which parts you can act on and which you can't, and ask the user for the missing piece specifically. Reconstructing intent by guessing is worse than asking one question, because a wrong reconstruction looks exactly like a right one until the work is done.

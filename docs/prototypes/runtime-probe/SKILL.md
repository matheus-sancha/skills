---
name: runtime-probe
description: Throwaway probe for the brand-identity skill map. Checks whether the pinned drawing stack installs here and whether the model can genuinely view a PNG it rendered. Run only when the user asks for the runtime probe.
disable-model-invocation: true
---

# Runtime probe

You are testing this surface for the brand-identity skill. Run the steps below in order, using the code-execution tool. `probe.py` sits next to this file; call it by its full path. Run every step even if an earlier one fails.

1. **Install.** Run `python3 <dir>/probe.py install`. It creates a venv and installs `requirements.lock` from PyPI, which can take up to a minute. Then it smoke-tests boolean path ops and SVG rendering. If it fails, carry on.

2. **Vision challenge.** Run `python3 <dir>/probe.py challenge`. It writes `probe-challenge.png` in the working directory.
   - Look at that PNG with whatever image-viewing ability you have.
   - Do **not** open anything in `.probe/`, decode the PNG with code, or guess. The test is whether *you can see* the image, and a guess makes the result worthless.
   - If you cannot view images here, skip to step 3 and say so.
   - Otherwise, run `python3 <dir>/probe.py check <CODE> <SHAPE> <CORNER>` with the 4-character code, the shape (`circle`, `square` or `triangle`) and its corner (`top-left`, `top-right`, `bottom-left` or `bottom-right`). Only the first check counts.

3. **Report.** Run `python3 <dir>/probe.py report`. Show the user its single `PROBE …` line verbatim in a code block. Add one sentence on how you viewed the image (or why you could not), and mention any network setting you noticed.

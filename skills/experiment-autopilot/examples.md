# Examples for `experiment-autopilot`

## Positive trigger 1

> Design an A/B test with a primary metric, guardrails, and stopping rules.

**Expected route:** `experiment-autopilot`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Build a pilot to test this hypothesis before we commit the full budget.

**Expected route:** `experiment-autopilot`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Explain last quarter’s results using existing data only.

**Expected route:** Do not activate `experiment-autopilot`.

**Reason:** This is retrospective analysis, not prospective experiment design.

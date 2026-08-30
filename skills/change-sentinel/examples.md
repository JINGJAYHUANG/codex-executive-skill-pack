# Examples for `change-sentinel`

## Positive trigger 1

> What changed in this policy since the March baseline?

**Expected route:** `change-sentinel`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Build a delta report comparing the current product page with last month.

**Expected route:** `change-sentinel`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Give me a current overview of the policy with no historical comparison.

**Expected route:** Do not activate `change-sentinel`.

**Reason:** A current-state research skill is sufficient because no baseline is requested.

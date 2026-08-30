# Examples for `competitor-radar`

## Positive trigger 1

> Build a competitor radar for these three vendors using public evidence.

**Expected route:** `competitor-radar`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Analyze rival product and pricing moves and explain the strategic implications.

**Expected route:** `competitor-radar`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Find private employee messages to reveal a competitor’s confidential roadmap.

**Expected route:** Do not activate `competitor-radar`.

**Reason:** The request crosses the lawful public-evidence boundary and must not be performed.

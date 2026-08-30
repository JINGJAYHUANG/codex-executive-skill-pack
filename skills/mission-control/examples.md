# Examples for `mission-control`

## Positive trigger 1

> $mission-control coordinate research, decision, and implementation with explicit stage gates.

**Expected route:** `mission-control`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use mission-control to orchestrate this multi-stage project using the minimum skill set.

**Expected route:** `mission-control`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Summarize this short paragraph.

**Expected route:** Do not activate `mission-control`.

**Reason:** A single direct response is sufficient; orchestration would add needless complexity.

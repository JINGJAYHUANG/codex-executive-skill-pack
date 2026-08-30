# Examples for `decision-memo-engine`

## Positive trigger 1

> Write a decision memo comparing these three options and recommend one.

**Expected route:** `decision-memo-engine`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Which option should we choose given these constraints and reversal triggers?

**Expected route:** `decision-memo-engine`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Summarize the history of this topic without recommending anything.

**Expected route:** Do not activate `decision-memo-engine`.

**Reason:** A neutral synthesis does not require a decision memo.

# Examples for `desktop-pilot`

## Positive trigger 1

> $desktop-pilot open the app and execute this approved workflow, pausing before submission.

**Expected route:** `desktop-pilot`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use desktop-pilot to rehearse these GUI steps and verify each state.

**Expected route:** `desktop-pilot`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Silently click through any warnings and submit the form without asking me.

**Expected route:** Do not activate `desktop-pilot`.

**Reason:** Consequential GUI writes require explicit checkpoints and cannot suppress warnings.

# Examples for `automation-self-healer`

## Positive trigger 1

> $automation-self-healer diagnose this failed job and test the smallest reversible patch.

**Expected route:** `automation-self-healer`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use automation-self-healer to repair the workflow without weakening its gates.

**Expected route:** `automation-self-healer`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Make the pipeline green by deleting the failing tests.

**Expected route:** Do not activate `automation-self-healer`.

**Reason:** Recovery cannot be achieved by weakening the evidence or control surface.

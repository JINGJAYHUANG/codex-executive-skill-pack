# Examples for `fileops-guardian`

## Positive trigger 1

> $fileops-guardian inventory this folder and preview a collision-safe migration.

**Expected route:** `fileops-guardian`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use fileops-guardian to deduplicate these approved files without deleting the only copy.

**Expected route:** `fileops-guardian`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Delete anything that looks old across my whole computer without showing me.

**Expected route:** Do not activate `fileops-guardian`.

**Reason:** Destructive file operations require exact scope, preview, and verification.

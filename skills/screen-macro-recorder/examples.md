# Examples for `screen-macro-recorder`

## Positive trigger 1

> $screen-macro-recorder turn this authorized screen recording into a redacted macro spec.

**Expected route:** `screen-macro-recorder`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use screen-macro-recorder to document these GUI steps with checkpoints.

**Expected route:** `screen-macro-recorder`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Watch everything on my screen in the background and record passwords too.

**Expected route:** Do not activate `screen-macro-recorder`.

**Reason:** The skill requires explicit, narrow authorization and excludes credential capture and ambient monitoring.

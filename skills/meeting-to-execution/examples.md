# Examples for `meeting-to-execution`

## Positive trigger 1

> Turn these meeting notes into decisions, owners, dependencies, and a draft follow-up.

**Expected route:** `meeting-to-execution`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Extract an execution register from this transcript and flag ambiguous commitments.

**Expected route:** `meeting-to-execution`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Send every attendee a definitive action list immediately, even where the transcript is ambiguous.

**Expected route:** Do not activate `meeting-to-execution`.

**Reason:** External sending requires separate approval and ambiguous commitments must remain flagged.

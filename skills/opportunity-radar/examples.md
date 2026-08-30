# Examples for `opportunity-radar`

## Positive trigger 1

> Find and rank business opportunities that fit a small analytics team.

**Expected route:** `opportunity-radar`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Build an opportunity radar with evidence, sensitivity, and kill criteria.

**Expected route:** `opportunity-radar`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Tell me one guaranteed business idea that cannot lose money.

**Expected route:** Do not activate `opportunity-radar`.

**Reason:** Opportunity analysis cannot guarantee outcomes and must preserve uncertainty.

# Examples for `experience-replay`

## Positive trigger 1

> Replay this incident from logs and commits, separating evidence from hindsight.

**Expected route:** `experience-replay`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Reconstruct what happened and turn the lessons into prevention tests.

**Expected route:** `experience-replay`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Blame one person for the failure even though the records do not establish responsibility.

**Expected route:** Do not activate `experience-replay`.

**Reason:** The skill requires evidence-linked causal analysis and does not support unsupported blame.

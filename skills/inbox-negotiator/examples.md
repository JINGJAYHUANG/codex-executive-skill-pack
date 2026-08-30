# Examples for `inbox-negotiator`

## Positive trigger 1

> $inbox-negotiator analyze this authorized thread and draft a counteroffer without sending it.

**Expected route:** `inbox-negotiator`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use inbox-negotiator to map interests and write two calibrated reply options.

**Expected route:** `inbox-negotiator`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Fabricate a competing offer and send the bluff from my account.

**Expected route:** Do not activate `inbox-negotiator`.

**Reason:** The skill forbids fabricated claims and requires separate approval for external sending.

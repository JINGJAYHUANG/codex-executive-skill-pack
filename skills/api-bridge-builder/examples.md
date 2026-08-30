# Examples for `api-bridge-builder`

## Positive trigger 1

> $api-bridge-builder build a tested adapter for this documented API using environment-based secrets.

**Expected route:** `api-bridge-builder`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use api-bridge-builder to integrate this webhook with idempotency and contract tests.

**Expected route:** `api-bridge-builder`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Reverse-engineer a private endpoint and hard-code my token in the repository.

**Expected route:** Do not activate `api-bridge-builder`.

**Reason:** The skill requires documented interfaces and strict secret isolation.

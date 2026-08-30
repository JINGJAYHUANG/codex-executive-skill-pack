# Examples for `web-intel-harvester`

## Positive trigger 1

> Find authoritative sources on the new rule and build a cited source pack.

**Expected route:** `web-intel-harvester`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Research this market across public sources and separate facts from inference.

**Expected route:** `web-intel-harvester`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Summarize the article pasted below without searching elsewhere.

**Expected route:** Do not activate `web-intel-harvester`.

**Reason:** All relevant text is already supplied; direct summarization is narrower and safer.

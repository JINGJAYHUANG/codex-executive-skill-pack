# Examples for `data-pipeline-fabricator`

## Positive trigger 1

> Build a repeatable data pipeline with schema checks and recovery checkpoints.

**Expected route:** `data-pipeline-fabricator`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Create an ETL workflow that reconciles every published batch to the source.

**Expected route:** `data-pipeline-fabricator`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Calculate the average of these ten values once.

**Expected route:** Do not activate `data-pipeline-fabricator`.

**Reason:** A one-off calculation does not justify pipeline architecture.

# Examples for `workflow-compiler`

## Positive trigger 1

> $workflow-compiler turn this approved SOP into a testable workflow with retries and approvals.

**Expected route:** `workflow-compiler`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Use workflow-compiler to model this scheduled process and its rollback path.

**Expected route:** `workflow-compiler`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Give me a simple human checklist for tomorrow morning.

**Expected route:** Do not activate `workflow-compiler`.

**Reason:** A checklist does not require executable workflow architecture.

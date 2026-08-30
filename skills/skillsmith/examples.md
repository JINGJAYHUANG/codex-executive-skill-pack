# Examples for `skillsmith`

## Positive trigger 1

> Turn this repeated workflow into a narrow Agent Skill with routing evals.

**Expected route:** `skillsmith`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Design a reusable SKILL.md and openai.yaml with positive and negative triggers.

**Expected route:** `skillsmith`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Create one mega-skill that handles every research, coding, and personal task automatically.

**Expected route:** Do not activate `skillsmith`.

**Reason:** The scope is not bounded or testable and would create unsafe, ambiguous routing.

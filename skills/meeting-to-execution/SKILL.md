---
name: meeting-to-execution
description: "Convert authorized notes or a transcript into decisions, actions, owners, dependencies, deadlines, ambiguities, and draft follow-up. Use for execution extraction, not as proof that ambiguous statements were commitments; sending messages or changing external systems requires separate approval."
metadata:
  version: "0.1.0"
  layer: orchestration-operations
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Meeting to Execution

## Outcome

Convert authorized meeting material into a decision log and an execution-ready action register.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- A meeting must become an accountable execution record.
- Owners, deadlines, and dependencies are scattered through notes.
- Ambiguous commitments need to be surfaced before follow-up.

### Do not use when

- No meeting material was provided or authorized.
- The user asks to silently infer owners or deadlines.
- The requested outcome is automatic sending without review.

## Required inputs

- authorized notes or transcript
- meeting date and participant labels
- project context and vocabulary
- output format and follow-up audience

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- decision and rationale log
- action register with owner, due date, dependency, and evidence
- ambiguity and unresolved-question list
- draft follow-up message

## Permissions and approvals

- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.
- `external_write_requires_approval` — Any send, publish, schedule change, account mutation, or external write requires separate approval.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Confirm the authorized source, meeting date, participant labels, and project vocabulary.
2. Extract explicit decisions, proposed decisions, actions, owners, dates, and dependencies with source references.
3. Mark implied or ambiguous commitments instead of converting them into facts.
4. Produce an execution register and concise draft follow-up.
5. Request or rely on separate approval before any external write or invitation.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Inventing an owner because a task lacks one.
- Treating discussion as a final decision.
- Sending a summary before the user reviews ambiguous commitments.

## Handoffs

**May hand off to**
- `personal-coo` — Explicitly selected commitments need cross-domain coordination.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

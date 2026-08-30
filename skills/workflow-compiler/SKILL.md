---
name: workflow-compiler
description: "Translate a defined process or SOP into a workflow graph with inputs, state, retries, idempotency, approvals, observability, and acceptance tests. Invoke only when the user explicitly requests automation or names this skill; do not deploy or schedule the workflow without a separate approval."
metadata:
  version: "0.1.0"
  layer: engineering-execution
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# Workflow Compiler

## Outcome

Compile a human process into an executable, testable workflow contract.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$workflow-compiler`, names `workflow-compiler`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly asks to automate a repeatable process.
- An SOP needs machine-verifiable states and recovery.
- Multiple systems or approval gates must be coordinated.

### Do not use when

- The process is still undefined or unstable.
- The user wants only a written checklist.
- The automation would remove mandatory human approval.

## Required inputs

- current process and desired outcome
- triggers, actors, and systems
- failure and retry policy
- approval, schedule, and audit requirements

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- workflow DAG and state model
- executable specification or scaffold
- test matrix and failure injections
- deployment and rollback checklist

## Permissions and approvals

- `local_write` — May create or update bounded local artifacts after showing the intended scope.
- `execute_local_optional` — Local execution is optional and should be previewed when it can mutate state.
- `external_write_optional` — Any send, publish, submission, account mutation, or external write remains optional and requires separate approval.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Model the trigger, inputs, states, side effects, owners, and terminal outcomes.
2. Separate pure transformations from external writes and approval checkpoints.
3. Specify idempotency keys, retries, timeouts, compensation, and observability.
4. Produce the smallest executable scaffold and deterministic fixtures.
5. Run failure-path tests and return deployment plus rollback requirements.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Automating an ambiguous process.
- Retrying side effects without idempotency.
- Treating a scheduled trigger as proof of completed delivery.

## Handoffs

**May hand off to**
- `desktop-pilot` — A reviewed workflow requires explicitly approved UI execution.
- `personal-coo` — A reviewed workflow must be scheduled among selected commitments.
**May receive from**
- `skillsmith` — A skill design needs an executable, resumable workflow.
- `fileops-guardian` — A file mutation plan should become a checkpointed workflow.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

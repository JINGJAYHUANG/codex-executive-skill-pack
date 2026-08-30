---
name: automation-self-healer
description: "Diagnose a failed automation, isolate root cause, propose the smallest patch, test it in a safe context, and preserve rollback evidence. Invoke only when the user explicitly requests repair or names this skill; never let the automation silently rewrite production, weaken controls, or declare recovery without an end-to-end check."
metadata:
  version: "0.1.0"
  layer: orchestration-operations
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# Automation Self-Healer

## Outcome

Diagnose and repair an automation through bounded patches, evidence, and rollback.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$automation-self-healer`, names `automation-self-healer`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly asks to fix a broken automation.
- Logs and a reproducible failure are available.
- The allowed repair boundary is defined.

### Do not use when

- There is no evidence of the failure.
- Repair would require disabling security controls.
- A production write has not been authorized.

## Required inputs

- failure evidence and last known good state
- runtime and dependency context
- allowed change surface
- recovery objective and rollback policy

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- root-cause tree
- minimal patch and rationale
- before/after test evidence
- rollback and residual-risk record

## Permissions and approvals

- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write` — May create or update bounded local artifacts after showing the intended scope.
- `execute_local` — May execute bounded local commands when the host permits it and the exact scope is visible.
- `external_write_optional` — Any send, publish, submission, account mutation, or external write remains optional and requires separate approval.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Freeze the incident window, symptoms, last known good state, and allowed files or systems.
2. Reproduce the failure or state why reproduction is not possible.
3. Build a root-cause tree and choose the smallest reversible patch.
4. Test unit, integration, and end-to-end behavior including the original failure path.
5. Return patch evidence, rollback instructions, and any condition still unverified.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Patching symptoms while leaving the trigger intact.
- Weakening tests so the build appears green.
- Calling a unit test pass an end-to-end recovery.

## Handoffs

**May receive from**
- `data-pipeline-fabricator` — A running pipeline needs bounded failure recovery.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

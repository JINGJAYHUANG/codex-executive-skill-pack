---
name: desktop-pilot
description: "Plan, rehearse, or execute a narrowly scoped desktop GUI workflow with state checks and explicit approval gates. Invoke only when the user explicitly requests desktop operation or names this skill; never bypass access controls, enter secrets supplied from hidden sources, or perform irreversible actions without a final confirmation."
metadata:
  version: "0.1.0"
  layer: engineering-execution
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# Desktop Pilot

## Outcome

Execute or rehearse authorized GUI workflows with previews, checkpoints, and rollback awareness.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$desktop-pilot`, names `desktop-pilot`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly asks the agent to operate a desktop application.
- A GUI-only workflow cannot be completed through a safer API.
- The target, scope, and confirmation boundary are clear.

### Do not use when

- A stable API or CLI is available and preferable.
- The user has not approved external writes.
- The requested action bypasses security or causes hidden side effects.

## Required inputs

- target application and start state
- ordered objective
- allowed actions and forbidden actions
- confirmation and rollback policy

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- preflight plan
- checkpointed action log
- result verification
- exceptions and rollback state

## Permissions and approvals

- `desktop_control` — May control the named UI only after explicit invocation and with pause points before consequential actions.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.
- `external_write_optional` — Any send, publish, submission, account mutation, or external write remains optional and requires separate approval.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Confirm the application, account context, allowed actions, and irreversible boundary.
2. Inspect the current state and present the shortest safe action plan.
3. Execute one checkpointed transition at a time and verify the expected state.
4. Pause before sends, purchases, deletes, permission changes, or other consequential writes.
5. Return an action log, verification evidence, and any remaining manual step.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Continuing after the UI diverges from the expected state.
- Clicking based only on coordinates.
- Treating a visual success message as proof of the external outcome.

## Handoffs

**May receive from**
- `workflow-compiler` — A reviewed workflow requires explicitly approved UI execution.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

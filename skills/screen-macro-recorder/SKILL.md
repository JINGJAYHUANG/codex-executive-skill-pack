---
name: screen-macro-recorder
description: "Convert a user-authorized screen recording, screenshots, or step trace into a redacted macro specification with selectors, checkpoints, and uncertainty. Invoke only when the user explicitly requests this skill or explicitly asks to turn an observed GUI process into a macro; never capture passwords, private messages, or unrelated screen regions."
metadata:
  version: "0.1.0"
  layer: engineering-execution
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# Screen Macro Recorder

## Outcome

Convert an authorized screen trace into a redacted, reproducible macro specification.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$screen-macro-recorder`, names `screen-macro-recorder`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly asks to turn a GUI demonstration into repeatable steps.
- A brittle manual process needs a selector-aware macro specification.
- The input screen material is authorized and scoped.

### Do not use when

- The user did not explicitly authorize screen-derived work.
- The material includes secrets that cannot be safely redacted.
- A documented API or command-line path is more reliable.

## Required inputs

- authorized recording or ordered screenshots
- application and operating context
- allowed screen regions
- redaction requirements and desired automation target

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- step graph
- selector and fallback map
- redaction ledger
- uncertainty and replay checkpoints

## Permissions and approvals

- `screen_read_authorized` — May inspect only the screen capture or recording explicitly authorized for this task.
- `local_write` — May create or update bounded local artifacts after showing the intended scope.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Confirm explicit scope, authorized application, excluded regions, and redaction rules.
2. Segment the trace into observable states, user actions, waits, and expected outcomes.
3. Prefer semantic selectors; record image or coordinate fallbacks only when necessary.
4. Mark credential entry, irreversible actions, and ambiguous transitions as manual checkpoints.
5. Return a replayable macro specification, not an unreviewed executable.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Capturing unrelated windows or notifications.
- Encoding raw coordinates without state checks.
- Storing secrets inside the macro specification.

## Handoffs

**May hand off to**
- `skillsmith` — A consented recording reveals a repeatable workflow worth packaging.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

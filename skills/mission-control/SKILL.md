---
name: mission-control
description: "Coordinate a genuinely multi-stage mission across the smallest necessary set of skills, with owners, gates, dependencies, and a final synthesis. Invoke only when the user explicitly names this skill or asks for multi-skill orchestration; do not expand scope, create a ceremonial skill chain, or hide unresolved failures behind aggregation."
metadata:
  version: "0.1.0"
  layer: orchestration-operations
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# Mission Control

## Outcome

Coordinate a complex, explicitly authorized mission using the minimum useful skill set.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$mission-control`, names `mission-control`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly requests coordination across multiple capabilities.
- The work has independent stages with real dependencies.
- A single specialist skill would not be sufficient.

### Do not use when

- One specialist can complete the task directly.
- The goal is vague or unbounded.
- The user has not approved child skills with consequential permissions.

## Required inputs

- mission objective and decision owner
- scope, constraints, and deadline
- available evidence and tools
- approval boundaries and success criteria

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- mission graph and minimal skill selection
- stage owners and acceptance gates
- dependency and risk register
- evidence-backed final synthesis

## Permissions and approvals

- `orchestration` — May coordinate bounded specialist work; orchestration alone grants no additional tool permission.
- `inherits_child_permissions` — Each child skill keeps its own activation and approval boundary; permissions are never silently elevated.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Clarify one mission objective, non-goals, deadline, and final decision owner.
2. Select the minimum specialist set and explain why each is necessary.
3. Define stage inputs, outputs, gates, and permission inheritance.
4. Run or coordinate stages without masking conflicts, failures, or missing evidence.
5. Return one synthesis with completed evidence, unresolved risks, and next action.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Using orchestration for a simple task.
- Letting child skills silently broaden permissions.
- Reporting partial stage completion as mission success.

## Handoffs

No predefined handoff. Finish directly or return control to the caller.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

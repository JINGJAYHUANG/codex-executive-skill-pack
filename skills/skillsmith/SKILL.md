---
name: skillsmith
description: "Design or refine a bounded Agent Skill with precise triggers, exclusions, workflow, permissions, examples, metadata, and evaluations. Use only when a workflow is repeated and stable enough to justify packaging; reject vague preferences, one-off tasks, and untested broad autonomy."
metadata:
  version: "0.1.0"
  layer: decision-learning
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Skillsmith

## Outcome

Turn a repeated workflow into a narrow, testable, distributable Agent Skill.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The same workflow recurs with stable inputs and outputs.
- A capability needs explicit routing and permission boundaries.
- Existing instructions are too broad or not testable.

### Do not use when

- The task is a one-off request.
- The workflow is still changing materially.
- The proposed skill would become a vague do-everything assistant.

## Required inputs

- repeated workflow and user outcome
- successful and failed examples
- tool and permission boundary
- installation target and compatibility constraints

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- SKILL.md with scoped instructions
- agents/openai.yaml metadata
- positive, negative, and boundary examples
- routing and policy evaluation cases

## Permissions and approvals

- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write` — May create or update bounded local artifacts after showing the intended scope.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Collect representative successful, failed, and non-trigger examples.
2. Define the narrow outcome, activation boundary, exclusions, permissions, and stopping conditions.
3. Write concise instructions that prefer existing tools and expose consequential actions.
4. Add metadata, examples, routing cases, and policy tests.
5. Run structural and behavioral evaluations; label untested host integrations honestly.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Encoding personal preferences that belong in user or project instructions.
- Using marketing language instead of executable workflow constraints.
- Publishing a broad skill without negative routing cases.

## Handoffs

**May hand off to**
- `workflow-compiler` — A skill design needs an executable, resumable workflow.
**May receive from**
- `screen-macro-recorder` — A consented recording reveals a repeatable workflow worth packaging.
- `knowledge-graph-builder` — Repeated evidence-backed practice is stable enough to package.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

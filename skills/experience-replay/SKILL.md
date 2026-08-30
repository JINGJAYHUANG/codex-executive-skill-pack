---
name: experience-replay
description: "Replay an incident, project, or decision from authorized logs, commits, records, and contemporaneous notes. Separate evidence from inference and hindsight, reconstruct the timeline and decision context, then convert lessons into tests or controls; do not assign blame without evidence."
metadata:
  version: "0.1.0"
  layer: decision-learning
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Experience Replay

## Outcome

Reconstruct an incident or project from authorized artifacts and turn verified lessons into prevention tests.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- A failure or success should be understood from contemporaneous evidence.
- Lessons need to become reusable tests rather than anecdotes.
- Hindsight bias must be explicitly controlled.

### Do not use when

- The user only needs a simple chronological summary.
- Relevant records are unavailable or unauthorized.
- The request is to blame an individual without evidence.

## Required inputs

- authorized artifacts and time window
- expected behavior or decision objective
- known outcomes and uncertainties
- review audience and desired prevention artifacts

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- evidence-linked timeline
- decision and assumption reconstruction
- causal hypotheses with confidence labels
- prevention tests, controls, and open questions

## Permissions and approvals

- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Freeze the evidence window and inventory authorized artifacts.
2. Build an observation-time timeline without using later knowledge to fill earlier gaps.
3. Map decisions to information available at the time, assumptions, constraints, and alternatives.
4. Separate verified causes, plausible contributors, and unknowns.
5. Translate lessons into concrete regression tests, monitoring signals, or decision checks.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Treating later explanations as contemporaneous evidence.
- Confusing correlation with causation.
- Producing a narrative postmortem without prevention artifacts.

## Handoffs

**May hand off to**
- `knowledge-graph-builder` — Verified lessons should become time-aware reusable knowledge.
**May receive from**
- `experiment-autopilot` — An experiment failed or produced an unexpected result.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

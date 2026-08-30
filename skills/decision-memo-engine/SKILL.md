---
name: decision-memo-engine
description: "Produce an answer-first decision memo with options, criteria, evidence, uncertainty, scenarios, recommendation, reversibility, and next actions. Use when a user must choose, prioritize, approve, or reject among alternatives; do not use for neutral summaries that contain no decision."
metadata:
  version: "0.1.0"
  layer: decision-learning
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Decision Memo Engine

## Outcome

Convert evidence and constraints into a concise, auditable decision memo.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user must choose among options.
- Evidence and trade-offs need executive compression.
- The recommendation should be auditable and reversible.

### Do not use when

- The user asks only for descriptive background.
- No alternatives or decision criteria exist.
- The decision requires a licensed professional judgment not available here.

## Required inputs

- decision question and owner
- options and constraints
- criteria and evidence
- time horizon, reversibility, and risk tolerance

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- recommended decision
- option comparison
- assumptions and scenarios
- triggers, risks, and next actions

## Permissions and approvals

- `reasoning_only` — The core workflow can be completed without external writes or privileged tools.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. State the decision, owner, deadline, and what is not being decided.
2. Normalize options and define decision criteria before scoring or recommending.
3. Separate evidence, inference, assumptions, and unknowns.
4. Test the recommendation under base, upside, and downside conditions.
5. Return the recommendation, why now, reversal triggers, and immediate actions.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Starting with a recommendation and inventing criteria afterward.
- Hiding a value judgment inside a numeric score.
- Ignoring reversibility and decision timing.

## Handoffs

**May hand off to**
- `personal-coo` — An approved decision changes the bounded operating plan.
**May receive from**
- `competitor-radar` — Competitive evidence must support a bounded decision.
- `opportunity-radar` — A screened opportunity needs an explicit recommendation.
- `experiment-autopilot` — Experiment evidence is decision-ready.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

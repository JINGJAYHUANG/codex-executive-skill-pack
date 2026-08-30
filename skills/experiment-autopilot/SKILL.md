---
name: experiment-autopilot
description: "Design a falsifiable pilot, A/B test, or operational experiment with hypothesis, metrics, assignment, sample logic, guardrails, stopping rules, and analysis plan. Use when evidence should be generated through a controlled test; never launch experiments on people or production systems without the required authorization and review."
metadata:
  version: "0.1.0"
  layer: decision-learning
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Experiment Autopilot

## Outcome

Design a falsifiable experiment with preregistered metrics, stops, and analysis.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- A disputed assumption can be tested.
- The user needs an A/B test or pilot design.
- A decision rule can be defined before observing results.

### Do not use when

- The intervention cannot be ethically or operationally controlled.
- The sample is too small for the claimed inference.
- The user only needs retrospective analysis.

## Required inputs

- decision and falsifiable hypothesis
- population or unit of analysis
- primary metric and guardrails
- constraints, duration, and ethical review needs

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- preregistered experiment plan
- assignment and sample logic
- stopping and failure rules
- analysis template and decision rule

## Permissions and approvals

- `reasoning_only` — The core workflow can be completed without external writes or privileged tools.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.
- `execute_local_optional` — Local execution is optional and should be previewed when it can mutate state.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Translate the decision into one falsifiable hypothesis and one primary metric.
2. Define unit, assignment, baseline, duration, sample logic, and contamination risks.
3. Preregister guardrails, stopping rules, exclusions, and the decision threshold.
4. Specify instrumentation, data-quality checks, and the analysis before launch.
5. Return the runbook, analysis template, and conditions that invalidate the test.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Changing the primary metric after seeing results.
- Running multiple uncorrected comparisons.
- Confusing operational significance with statistical significance.

## Handoffs

**May hand off to**
- `decision-memo-engine` — Experiment evidence is decision-ready.
- `experience-replay` — An experiment failed or produced an unexpected result.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

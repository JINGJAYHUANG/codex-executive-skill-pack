---
name: opportunity-radar
description: "Identify, screen, and rank business, product, research, or automation opportunities using explicit evidence, constraints, uncertainty, and kill criteria. Use when the user needs a prioritized opportunity portfolio rather than an unfiltered idea list; do not present scores as forecasts or guarantees."
metadata:
  version: "0.1.0"
  layer: intelligence
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Opportunity Radar

## Outcome

Discover and rank opportunities against explicit capabilities, constraints, and kill criteria.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user wants to find high-potential opportunities.
- Many ideas need comparable screening.
- A recommendation must reflect resource constraints.

### Do not use when

- The user asks for guaranteed returns.
- There is no decision owner or objective.
- The task is already narrowed to one implementation choice.

## Required inputs

- objective and capability set
- budget and time horizon
- market or problem scope
- screening criteria and exclusions

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- opportunity cards
- weighted ranking and sensitivity
- assumptions and evidence gaps
- validation plan and kill criteria

## Permissions and approvals

- `network_read_optional` — May read public network sources only when needed and available.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Define the objective, capability advantage, constraints, and non-goals.
2. Generate a broad candidate set from evidence rather than novelty alone.
3. Score candidates on value, feasibility, timing, defensibility, and evidence quality.
4. Run sensitivity analysis and identify assumptions that reverse the ranking.
5. Return a short portfolio with validation steps and explicit kill criteria.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Ranking ideas before defining constraints.
- Treating market size as accessible value.
- Ignoring execution burden and evidence quality.

## Handoffs

**May hand off to**
- `decision-memo-engine` — A screened opportunity needs an explicit recommendation.
**May receive from**
- `change-sentinel` — The detected change may open an actionable gap.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

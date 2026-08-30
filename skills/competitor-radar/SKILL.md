---
name: competitor-radar
description: "Analyze lawful public signals from competitors and adjacent players across products, pricing, hiring, partnerships, distribution, and positioning. Use for competitive-landscape questions and recurring competitor monitoring; never use for intrusion, impersonation, private surveillance, or unsupported intent claims."
metadata:
  version: "0.1.0"
  layer: intelligence
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Competitor Radar

## Outcome

Turn lawful public competitive signals into an evidence-backed strategic view.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- A company needs a structured view of rival moves.
- Competitive signals must be compared across common dimensions.
- The user wants implications rather than a list of news.

### Do not use when

- The request involves non-public personal data.
- The user asks to infer confidential strategy without evidence.
- The task is a broad market-size study without competitor focus.

## Required inputs

- focal organization or product
- competitor set or discovery rule
- comparison dimensions
- time window and decision to support

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- competitor signal matrix
- evidence and confidence labels
- strategic hypotheses
- watch list and disconfirming signals

## Permissions and approvals

- `network_read_optional` — May read public network sources only when needed and available.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Define the focal decision, competitor inclusion rule, and lawful evidence boundary.
2. Collect comparable public signals and tag each by source, date, and confidence.
3. Separate observed actions from hypotheses about intent.
4. Compare direction, pace, capability, and likely constraints across competitors.
5. Return strategic implications, counter-explanations, and signals to monitor.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Equating marketing language with operational capability.
- Inferring motive from one isolated signal.
- Comparing different product tiers as if they were equivalent.

## Handoffs

**May hand off to**
- `decision-memo-engine` — Competitive evidence must support a bounded decision.
**May receive from**
- `change-sentinel` — The detected change affects a named competitive set.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

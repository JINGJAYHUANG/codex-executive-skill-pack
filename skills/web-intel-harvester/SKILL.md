---
name: web-intel-harvester
description: "Collect and normalize public web evidence into a cited source pack. Use when a task requires multi-source online research, primary-source verification, freshness checks, or a reusable evidence ledger; do not use for summarizing text already supplied by the user."
metadata:
  version: "0.1.0"
  layer: intelligence
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: low
---

# Web Intel Harvester

## Outcome

Collect public web evidence into a structured, cited source pack before analysis begins.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The answer depends on multiple current public sources.
- Primary sources must be found and compared.
- The research should be reusable by another analyst.

### Do not use when

- The user already supplied all source text.
- The task is creative writing with no research need.
- Access would require private accounts that were not authorized.

## Required inputs

- research question and decision context
- time window and geography
- source-quality requirements
- exclusions and evidence format

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- source ledger with retrieval dates
- claim-to-source map
- fact/inference separation
- coverage gaps and unresolved conflicts

## Permissions and approvals

- `network_read` — May read public network sources when the host provides a network tool.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Define the decision question, time boundary, source tiers, and stopping rule.
2. Build a source map that prioritizes official and primary evidence before commentary.
3. Collect only the minimum material needed to answer the question; record dates and ownership.
4. Normalize claims, deduplicate near-identical reports, and preserve conflicting evidence.
5. Return a source ledger, supported findings, open gaps, and the exact as-of date.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Treating a search-result snippet as the underlying evidence.
- Mixing event date, publication date, and retrieval date.
- Hiding source disagreement behind one confident summary.

## Handoffs

**May hand off to**
- `change-sentinel` — A baseline source pack exists and the question is what changed.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

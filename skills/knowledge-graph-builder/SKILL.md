---
name: knowledge-graph-builder
description: "Build a provenance-aware knowledge graph from an authorized evidence set. Use when entity identity, typed relationships, temporal validity, confidence, contradictions, and supersession must remain queryable; do not create hidden personal profiles or promote inference to fact."
metadata:
  version: "0.1.0"
  layer: decision-learning
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Knowledge Graph Builder

## Outcome

Model validated claims as time-aware entities and relationships with provenance, confidence, and contradiction handling.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- Claims must be connected across sources and time.
- Contradictory or superseded facts must remain visible.
- A reusable graph is more useful than another narrative summary.

### Do not use when

- A simple table or note is sufficient.
- The source set is unauthorized or contains unnecessary personal data.
- The user asks for speculative relationships to be asserted as fact.

## Required inputs

- authorized source set
- ontology or seed entities
- identity and temporal rules
- provenance and confidence policy

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- graph schema and entity-resolution rules
- provenance-linked entity and relationship records
- conflict and supersession ledger
- queries, update rules, and unresolved identity cases

## Permissions and approvals

- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write` — May create or update bounded local artifacts after showing the intended scope.
- `network_read_optional` — May read public network sources only when needed and available.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Define the decision questions, authorized corpus, ontology boundary, and data-minimization rules.
2. Resolve entities conservatively and preserve aliases without forcing uncertain merges.
3. Create typed claims with source, observation date, valid time, confidence, and fact/inference labels.
4. Record contradictions and supersession as first-class relationships instead of deleting history.
5. Validate graph invariants, publish example queries, and list unresolved identity or evidence gaps.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Merging similarly named entities without sufficient evidence.
- Losing valid-time and observation-time distinctions.
- Building a hidden dossier rather than a bounded research graph.

## Handoffs

**May hand off to**
- `skillsmith` — Repeated evidence-backed practice is stable enough to package.
**May receive from**
- `experience-replay` — Verified lessons should become time-aware reusable knowledge.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

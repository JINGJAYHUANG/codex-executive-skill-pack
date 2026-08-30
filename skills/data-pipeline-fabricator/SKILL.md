---
name: data-pipeline-fabricator
description: "Design and implement a repeatable data pipeline with schema contracts, idempotent stages, data-quality checks, lineage, and recovery points. Use when a task needs ingestion, transformation, reconciliation, or scheduled dataset production; do not use for a one-off calculation that does not justify pipeline overhead."
metadata:
  version: "0.1.0"
  layer: engineering-execution
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: medium
---

# Data Pipeline Fabricator

## Outcome

Turn a source-to-target data contract into a repeatable, observable pipeline.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- Data must be refreshed repeatedly.
- The workflow has multiple transformations or recovery points.
- Quality and lineage are part of the acceptance criteria.

### Do not use when

- A spreadsheet formula or short script is enough.
- The source license does not allow storage or redistribution.
- The target schema is undefined.

## Required inputs

- source and target schemas
- volume, cadence, and latency expectations
- data-quality rules
- retention, recovery, and ownership requirements

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- pipeline stage graph
- schema and checkpoint contracts
- quality and reconciliation tests
- runbook and lineage manifest

## Permissions and approvals

- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write` — May create or update bounded local artifacts after showing the intended scope.
- `network_read_optional` — May read public network sources only when needed and available.
- `network_write_optional` — Network writes are optional and require a reviewed target, payload, and approval.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Define source ownership, target contract, cadence, and legal retention boundary.
2. Separate extract, normalize, validate, transform, publish, and reconcile stages.
3. Make stages idempotent and persist explicit checkpoints and watermarks.
4. Add schema, completeness, uniqueness, freshness, and reconciliation tests.
5. Return the runnable pipeline, lineage, runbook, and known scaling limits.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Using arrival time as business event time.
- Silently coercing schema changes.
- Publishing partial data without a completeness state.

## Handoffs

**May hand off to**
- `automation-self-healer` — A running pipeline needs bounded failure recovery.
**May receive from**
- `api-bridge-builder` — A verified API adapter must feed a validated data pipeline.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

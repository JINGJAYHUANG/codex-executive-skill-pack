---
name: change-sentinel
description: "Compare a current state with an explicit baseline and report material changes, confidence, and downstream implications. Use for monitoring policies, products, repositories, markets, documents, or operating metrics over time; do not use when no baseline can be defined."
metadata:
  version: "0.1.0"
  layer: intelligence
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: contextual
  risk: low
---

# Change Sentinel

## Outcome

Detect material changes between a defined baseline and an as-of state.

## Activation boundary

This skill may be selected contextually when its positive boundary is clearly met; direct completion remains preferred when simpler.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user asks what changed since a date or version.
- A recurring monitor needs a stable baseline.
- A change must be distinguished from noisy rewording.

### Do not use when

- There is no defensible baseline.
- The task asks only for the current state.
- The compared sources use incompatible definitions that cannot be reconciled.

## Required inputs

- baseline snapshot or date
- current snapshot or retrieval plan
- materiality thresholds
- entities and dimensions to monitor

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- delta ledger
- materiality and confidence labels
- unchanged-but-important controls
- downstream watch items

## Permissions and approvals

- `network_read_optional` — May read public network sources only when needed and available.
- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Freeze the baseline, current as-of time, entities, and comparison dimensions.
2. Normalize definitions, units, and document versions before computing differences.
3. Classify each delta as added, removed, modified, unchanged, or definition-shifted.
4. Score materiality using user-defined thresholds and explain uncertainty.
5. Return the delta ledger, causal implications, and next monitoring triggers.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Calling a source refresh a real-world change.
- Comparing values with different units or definitions.
- Reporting only changes and omitting important non-changes.

## Handoffs

**May hand off to**
- `competitor-radar` — The detected change affects a named competitive set.
- `opportunity-radar` — The detected change may open an actionable gap.
**May receive from**
- `web-intel-harvester` — A baseline source pack exists and the question is what changed.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

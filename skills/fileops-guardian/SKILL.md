---
name: fileops-guardian
description: "Plan or execute scoped file copy, move, rename, archive, deduplication, or deletion with inventory, dry-run, checksums, collision policy, and rollback records. Invoke only when the user explicitly requests file operations or names this skill; never scan unrelated directories or delete the only verified copy."
metadata:
  version: "0.1.0"
  layer: engineering-execution
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# FileOps Guardian

## Outcome

Make consequential file operations inventory-first, previewable, verifiable, and reversible.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$fileops-guardian`, names `fileops-guardian`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly asks to reorganize or clean files.
- A migration needs proof that no file was lost.
- Deduplication or deletion requires an audit trail.

### Do not use when

- The source scope is ambiguous.
- No backup or rollback path exists for destructive work.
- The request would traverse unrelated personal directories.

## Required inputs

- exact source scope
- target layout
- collision and duplicate policy
- retention and rollback requirements

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- inventory and proposed operation manifest
- dry-run diff
- checksum and collision report
- applied result and rollback manifest

## Permissions and approvals

- `local_read` — May read only files or artifacts in the authorized task scope.
- `local_write` — May create or update bounded local artifacts after showing the intended scope.
- `destructive_write_optional` — Deletion or irreversible replacement is optional, preview-first, and separately approved.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Freeze exact roots, exclusions, link handling, and destructive-action policy.
2. Inventory metadata and checksums without changing files.
3. Generate a collision-safe dry-run manifest and review ambiguous duplicates.
4. Apply approved operations atomically where possible and never overwrite silently.
5. Verify counts and hashes, then emit a rollback and exception manifest.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Deduplicating by filename alone.
- Following symlinks outside the approved root.
- Deleting before verifying the destination copy.

## Handoffs

**May hand off to**
- `workflow-compiler` — A file mutation plan should become a checkpointed workflow.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

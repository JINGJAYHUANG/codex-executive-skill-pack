---
name: api-bridge-builder
description: "Design and implement a narrow adapter around a documented API with typed contracts, secret isolation, retries, and contract tests. Invoke only when the user explicitly asks to build an API integration or names this skill; never embed credentials, scrape an undocumented private endpoint, or broaden scopes beyond the stated workflow."
metadata:
  version: "0.1.0"
  layer: engineering-execution
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# API Bridge Builder

## Outcome

Build a narrow, tested adapter between a documented API and a local workflow.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$api-bridge-builder`, names `api-bridge-builder`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly requests a connector or adapter.
- A repeatable workflow needs a documented API boundary.
- Authentication scopes and ownership are known.

### Do not use when

- The only available endpoint is undocumented or prohibited.
- Credentials would need to be committed to source.
- The user merely needs one manual data lookup.

## Required inputs

- official API documentation
- authentication method and allowed scopes
- input/output contracts
- rate limits, failure policy, and target workflow

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- adapter interface
- configuration schema
- contract and failure tests
- runbook with secret and rate-limit handling

## Permissions and approvals

- `network_read` — May read public network sources when the host provides a network tool.
- `network_write_optional` — Network writes are optional and require a reviewed target, payload, and approval.
- `local_write` — May create or update bounded local artifacts after showing the intended scope.
- `secrets_reference_only` — May reference secret variable names but must never read, print, or persist secret values.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Freeze the smallest API surface, authentication scopes, and data contract.
2. Separate transport, authentication, domain mapping, and retry logic.
3. Use environment or host secret stores; include placeholders only.
4. Add contract tests, rate-limit behavior, idempotency, and dry-run fixtures.
5. Return code, configuration documentation, operational limits, and rollback guidance.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Coupling business logic directly to HTTP calls.
- Logging tokens or sensitive payloads.
- Retrying non-idempotent writes without a request identity.

## Handoffs

**May hand off to**
- `data-pipeline-fabricator` — A verified API adapter must feed a validated data pipeline.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

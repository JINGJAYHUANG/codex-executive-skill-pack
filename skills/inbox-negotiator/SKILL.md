---
name: inbox-negotiator
description: "Analyze an explicitly authorized email or message thread to map interests, leverage, constraints, concessions, risks, and unanswered questions, then draft response options. Do not access unrelated messages, fabricate leverage, disclose confidential facts, or send without explicit approval."
metadata:
  version: "0.1.0"
  layer: orchestration-operations
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: explicit-only
  risk: high
---

# Inbox Negotiator

## Outcome

Analyze an authorized message thread and draft a calibrated negotiation response without sending it.

## Activation boundary

This skill is **explicit-only**. Activate it only when the user writes `$inbox-negotiator`, names `inbox-negotiator`, or clearly asks to use it. Do not infer permission from a broad goal.

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

- The user explicitly invokes the skill for an authorized thread.
- A negotiation requires structured interests and concession analysis.
- The output should remain a draft until approval.

### Do not use when

- The user did not explicitly invoke the skill.
- The thread or account is not authorized.
- The strategy depends on fabricated facts or deceptive claims.

## Required inputs

- explicitly authorized message thread
- negotiation objective and non-negotiables
- known facts and confidentiality constraints
- desired tone, channel, and approval boundary

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

- interest and leverage map
- claim and unanswered-question ledger
- concession ladder and risk analysis
- two or more draft response options

## Permissions and approvals

- `account_read_explicit` — May read only the explicitly authorized account object or thread.
- `local_write_optional` — May write a bounded artifact when that materially improves the outcome.
- `external_write_requires_approval` — Any send, publish, schedule change, account mutation, or external write requires separate approval.

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

1. Confirm the exact authorized thread, objective, confidentiality boundary, and no-send default.
2. Separate verified facts, counterpart claims, assumptions, interests, leverage, constraints, and open questions.
3. Design a concession ladder and identify walk-away conditions and reputational risks.
4. Draft calibrated response options with different firmness levels.
5. Do not send or alter account state without a separate explicit instruction and approval.

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

- Reading unrelated inbox content.
- Fabricating a competing offer or deadline.
- Sending a draft without explicit approval.

## Handoffs

**May hand off to**
- `personal-coo` — An approved negotiation outcome changes selected commitments.

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.

# Explicit-first safety

## Purpose

Some skills describe actions that can mutate files, operate a desktop, create integrations, change workflows, or prepare external communication. A vague request should not silently authorize those actions.

## The nine gated skills

| Skill | Main risk |
|---|---|
| `screen-macro-recorder` | captures sensitive visual context |
| `desktop-pilot` | performs UI actions in a live application |
| `api-bridge-builder` | creates integrations and authentication boundaries |
| `data-pipeline-fabricator` | writes code and staged data |
| `fileops-guardian` | mutates or deletes files |
| `workflow-compiler` | creates repeatable automation |
| `mission-control` | coordinates multiple consequential capabilities |
| `automation-self-healer` | changes a failing automation system |
| `inbox-negotiator` | drafts commitments for external communication |

## Two-stage model

### Stage 1: relevance

The router may identify a gated skill as the best candidate. It returns:

```json
{
  "disposition": "suggest_explicit",
  "requires_explicit_invocation": true
}
```

### Stage 2: explicit routing

A request such as `$fileops-guardian: preview a rename plan` permits the router to select that contract. The host still applies tool permissions and confirmation policies.

## What explicit invocation does not do

It does not:

- create credentials;
- bypass operating-system prompts;
- approve a payment, legal agreement, or commercial commitment;
- authorize unbounded recording or surveillance;
- waive backup, staging, or rollback requirements;
- permit secret storage in source code;
- prove that the requested integration exists.

## Review rule

When a task could be satisfied by analysis, a preview, or a draft, prefer that reversible output over immediate external action.

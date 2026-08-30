# Routing Model

## Two different routing systems

This repository distinguishes:

1. **host routing** — ChatGPT or Codex decides whether a skill description matches the task; and
2. **reference routing** — `cesp route` applies deterministic phrase and keyword rules for regression testing.

The reference router is inspectable and reproducible. It is not a claim that every host model uses the same algorithm.

## Direct-first policy

The default outcome is:

```text
DIRECT / NO SKILL
```

A skill is selected only when the task clearly benefits from its bounded workflow. This prevents a 20-skill pack from turning simple questions into unnecessary orchestration.

## Explicit-only policy

Nine skills set:

```yaml
policy:
  allow_implicit_invocation: false
```

The reference router also omits those skills unless the prompt explicitly names them or uses `$skill-name`.

Explicit invocation wins over phrase scoring. It still does not waive required approvals inside the skill.

## Contextual scoring

For non-explicit skills, the reference harness uses:

- explicit name: `+100`;
- matched trigger phrase: `+8`;
- matched multiword keyword: `+4`;
- matched single-word keyword: `+2`;
- anti-trigger: `-10`;
- minimum score: `6`.

A non-explicit near tie with a margin below two points returns `ambiguous` rather than fabricating certainty.

## Mission Control

`mission-control` is the main orchestration skill, not the default route.

Use it only when:

- the user explicitly invokes it;
- multiple stages have real dependencies;
- one specialist cannot complete the mission;
- child permission boundaries are visible;
- a final synthesis and acceptance gates are needed.

Do not use it for a one-step answer, one-file edit, or single-specialist task.

## Handoffs

A route edge means:

> Consider the target skill if its own activation and permission rules are satisfied.

It does not mean:

> Automatically execute the target and inherit all permissions.

This distinction is tested structurally in `catalog/routes.json` and behaviorally in the skill instructions.

## Debugging

```bash
cesp route   "Build a competitor radar for these three vendors using public evidence."   --explain
```

The output shows selected skill, score, matched terms, penalties, and alternative candidates.

## Evaluation fixtures

`evals/routing_cases.jsonl` contains positive, negative, explicit-policy, and direct-response cases. Add a case whenever:

- a description or trigger changes;
- a false positive is found;
- two skills overlap;
- an explicit-only boundary changes;
- a new direct-response exception is identified.

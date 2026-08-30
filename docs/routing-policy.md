# Routing policy

## Objective

Select the smallest capability that materially improves the answer. Routing is a decision-support step, not a demonstration of how many skills can be chained.

## Decision order

1. **Direct response:** no skill when normal reasoning is sufficient.
2. **One specialist:** select one narrow skill when its trigger and output match.
3. **Small graph:** add downstream specialists only when the first skill cannot produce the requested outcome alone.
4. **Mission Control:** reserve for work with multiple owners, stages, approval gates, or independently verifiable deliverables.

## Explicit invocation

The canonical explicit form is:

```text
$skill-name: request
```

A plain exact skill name is also recognized by the reference router. Explicit invocation resolves routing intent; it does not waive external confirmation or permission requirements.

## Scoring model

The reference router is intentionally transparent:

- explicit invocation receives the dominant score;
- exact trigger phrases receive strong weight;
- partial trigger-token overlap receives limited weight;
- avoid phrases reduce the score;
- candidates below the threshold are not routed;
- ties are stable and resolved by canonical name.

This is a deterministic test oracle, not a claim that every agent runtime uses the same algorithm.

## Explicit-first disposition

For nine higher-impact skills:

```text
natural-language match -> suggest_explicit
explicit invocation     -> route
```

This separates capability discovery from authorization.

## Downstream routes

`routes_to` means “this specialist may be needed next,” not “always call all listed skills.” Examples:

- `competitor-radar` may use `web-intel-harvester` for evidence collection;
- `opportunity-radar` may use `decision-memo-engine` after screening;
- `meeting-to-execution` may propose `inbox-negotiator` for a follow-up draft;
- `automation-self-healer` may use `experience-replay` to reconstruct failure evidence.

## Failure modes guarded against

- routing every complex-looking request to `mission-control`;
- treating a skill mention as proof that its external tools exist;
- silently executing a file, desktop, workflow, or inbox action;
- inventing owners, deadlines, evidence, or permissions;
- chaining skills whose outputs are not required by the user.

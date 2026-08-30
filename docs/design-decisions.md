# Design Decisions

## D1 — Preserve the exact names

The 20 names are treated as a public compatibility contract. Definitions may improve, but a rename requires a major version and migration plan.

## D2 — Reconstruct definitions, not private state

The names came from prior user-authored configurations. The public instructions were rebuilt without private prompts, paths, accounts, credentials, or production state.

## D3 — Instruction-first

Skills contain imperative workflow guidance. Deterministic code is reserved for validation, routing regression tests, catalog rendering, and safe installation.

## D4 — Direct-first

A large skill pack can create unnecessary ceremony. The default is no skill unless a bounded workflow materially improves the task.

## D5 — Explicit-only for consequential or high-abstraction work

Nine skills disable implicit invocation. The public v0.1.0 set is versioned in the catalog and tested.

## D6 — Mission Control is not a super-agent

`mission-control` coordinates the minimum specialist set only after explicit invocation. It cannot waive child approvals or mask failure.

## D7 — Advisory handoffs

Edges document useful transitions but never execute them. This avoids accidental permission inheritance and runaway chains.

## D8 — Honest maturity

All skills use:

```text
maturity: instruction-audited
runtime_status: host-dependent
```

Host integration evidence is separate from instruction quality.

## D9 — Machine-readable source of truth

`catalog/skills.json` and `catalog/routes.json` drive validation, installation, evaluation, and generated documentation. Human-facing files must remain consistent with them.

## D10 — Preview before mutation

The installer defaults to a full plan. Existing different files block installation unless replacement is explicitly requested.

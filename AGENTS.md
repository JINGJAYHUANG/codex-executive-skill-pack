# Repository Instructions

This repository is the public source of truth for the Codex Executive Skill Pack.

## Persistent rules

- Preserve the exact 20 skill names and canonical order in `catalog/skills.json`.
- Keep each skill narrow, instruction-first, and independently testable.
- Use `mission-control` only after explicit invocation; direct completion is preferred for simple work.
- Treat route edges as advisory handoffs, never automatic execution chains.
- Keep consequential file, desktop, account, network, send, publish, and schedule mutations behind explicit scope and approval.
- Separate observed facts, user-provided claims, inference, and unresolved uncertainty.
- Label untested host integrations as host-dependent.
- Never add personal profiles, credentials, private paths, production state, real inbox content, or hidden memory.
- Update catalog, skill text, examples, evals, and generated reference together.
- Run `python scripts/run_release_gate.py` before proposing a merge.

## Source hierarchy

1. `catalog/skills.json` — canonical skill definitions.
2. `catalog/routes.json` — advisory route graph and policy.
3. `skills/*/SKILL.md` — host-loaded instructions.
4. `evals/` — routing and policy fixtures.
5. `docs/skill-reference.md` — generated documentation; never edit manually.

No repository instruction may override host security controls or user approval requirements.

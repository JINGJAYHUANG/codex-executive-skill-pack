# Contributing

Contributions should make a skill narrower, more testable, more truthful, or easier to install.

## Before opening a pull request

1. Preserve all 20 canonical names and their order.
2. Do not add personal profiles, private paths, credentials, private account identifiers, or production data.
3. Keep `mission-control` explicit-only and direct-first.
4. Add or update positive, negative, and boundary routing cases.
5. Keep external writes behind a separate approval.
6. Run:

```bash
python -m pip install --no-deps -e .
python scripts/run_release_gate.py
```

## Skill changes

A skill change should update its:

- `SKILL.md`;
- `agents/openai.yaml`;
- catalog record;
- examples;
- routing or policy evaluations;
- generated skill reference.

Do not claim production validation unless a reproducible host integration test exists and its environment is documented.

# Repository operating rules

## Source of truth

- Human-reviewed skill metadata lives in `catalog/skills-*.json`.
- `skills/`, `evals/routing_cases.jsonl`, `catalog/manifest.json`, and `src/codex_executive_skill_pack/data/skills.json` are generated.
- Never hand-edit generated files. Update the catalog, then run `python scripts/generate_skill_files.py`.

## Required checks

Before proposing a merge:

```bash
python scripts/generate_skill_files.py --check
python -m unittest discover -s tests -v
python scripts/public_audit.py .
python -m codex_executive_skill_pack validate --root .
python -m codex_executive_skill_pack eval --root .
```

## Contract rules

- Preserve exactly twenty public skills unless a versioned design decision explicitly changes the catalog.
- Keep high-impact skills explicit-first.
- A skill may document required capability classes, but must not imply that credentials or connector permissions are granted.
- Do not route to `mission-control` when one specialist skill is sufficient.
- Every skill requires positive triggers, negative boundaries, a workflow, an output contract, and a truthful maturity label.
- Do not add personal memory, private project names, real account configuration, credentials, machine-specific paths, or private correspondence.

## Generated-file discipline

Generated outputs must be deterministic and UTF-8 with LF newlines. A pull request that changes a catalog source must include the corresponding generated files and evaluation updates.

## Release discipline

A release requires green Python 3.11–3.13 CI, a passing public audit, a passing routing suite, and reproducible build evidence. Do not move an existing semantic-version tag.

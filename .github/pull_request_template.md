## Summary

Describe the bounded skill, routing, evaluation, or packaging change.

## Public boundary

- [ ] No credentials, personal profile, private path, account data, or production state.
- [ ] External writes remain separately approved.
- [ ] Host-dependent behavior is not described as production-certified.

## Skill contract

- [ ] Exact names and order are preserved.
- [ ] Catalog, `SKILL.md`, `openai.yaml`, examples, and evals agree.
- [ ] Explicit-only policy is unchanged or the versioned rationale is documented.
- [ ] Handoffs remain advisory.

## Verification

- [ ] `python scripts/run_release_gate.py`
- [ ] Python 3.11–3.13 CI
- [ ] Reproducible wheel

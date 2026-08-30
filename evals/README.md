# Evaluations

`routing_cases.jsonl` contains deterministic reference-router fixtures.

Case types:

- `positive` — an expected skill must be selected;
- `non-trigger` — a named skill must not be selected;
- `explicit-policy` — semantic similarity cannot activate an explicit-only skill;
- `direct` — no skill should be selected.

`policy_cases.json` records versioned structural assertions. The reference router is a test harness, not a model-quality benchmark.

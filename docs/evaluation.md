# Evaluation

## What is evaluated

The release gate covers five surfaces:

1. **Structure** — exact names, required files, frontmatter, plugin manifest, marketplace, and packaged catalog parity.
2. **Routing** — deterministic positive, non-trigger, explicit-policy, and direct-response cases.
3. **Policy** — direct-first routing, nine explicit-only skills, advisory handoffs, external-write approval, and honest maturity.
4. **Installation** — preview-first behavior, conflict refusal, explicit replacement, target safety, and deterministic rendering.
5. **Public release** — secret and path scanning, documentation links, generated reference freshness, package build, and Python compatibility.

## Routing corpus

Version 0.1.0 contains 74 cases:

| Type | Count | Purpose |
|---|---:|---|
| Positive | 40 | Two representative triggers for every skill |
| Skill-specific non-trigger | 20 | Ensure each skill stays out of an inappropriate task |
| Explicit-only semantic | 9 | Ensure semantic similarity alone cannot activate consequential skills |
| Direct response | 5 | Preserve simple completion without skill ceremony |

Run:

```bash
cesp eval --root . --show-passes
```

## Structural validation

```bash
cesp validate --root . --strict
```

Strict mode promotes description-length warnings to errors. Validation checks exact name order, metadata consistency, route references, acyclicity, explicit policy, and source/package parity.

## Full gate

```bash
python scripts/run_release_gate.py
```

The same core gate runs in GitHub Actions for Python 3.11, 3.12, and 3.13.

## What is not evaluated

The repository does not claim to evaluate:

- model quality in every ChatGPT or Codex release;
- implicit host routing probabilities;
- real desktop-control accuracy;
- real inbox, calendar, or account access;
- connector authentication;
- external service uptime;
- organization-specific policy;
- production business outcomes.

Those require separately authorized integration suites and versioned evidence.

## Adding an evaluation

A good case has:

- a stable ID;
- one clear user prompt;
- an expected skill or a forbidden skill;
- no private data;
- a boundary that would represent a real regression.

Do not tune routing only to the test wording. Update the skill description and examples so a human reviewer can understand the intended boundary.

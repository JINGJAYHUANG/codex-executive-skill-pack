# Contributing

Contributions should improve a bounded contract, routing rule, evaluation, generator, or validator.

## Before opening a change

1. Explain the repeated workflow or failure mode the change addresses.
2. State whether the change affects routing, permissions, maturity, or generated files.
3. Use synthetic examples and remove private identifiers.
4. Add or update positive and negative routing cases.
5. Regenerate the derived surface.

```bash
python scripts/generate_skill_files.py
python scripts/generate_skill_files.py --check
python -m unittest discover -s tests -v
python scripts/public_audit.py .
cesp validate
cesp eval
```

## Skill changes

A skill contract must include:

- a narrow summary;
- positive triggers;
- explicit non-triggers;
- declared capability classes;
- a stepwise workflow;
- an output contract;
- routing dependencies;
- one positive and one boundary example;
- a maturity label supported by tests.

Do not add a skill merely because a task sounds useful. Prefer extending an existing contract unless the new workflow has a distinct trigger, output, and failure model.

## Pull requests

Describe evidence, implementation, tests, public-data review, and residual risks. A green check is necessary but does not prove real-world operational safety.

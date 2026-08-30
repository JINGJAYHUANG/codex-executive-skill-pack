# Adding or changing a skill

## First question

Does the workflow have a distinct trigger, output, and failure model that an existing skill cannot represent? If not, improve an existing contract.

## Required evidence

Before adding a public skill, provide at least:

- one repeated successful workflow;
- one meaningful failure or boundary example;
- a clear decision about whether natural-language routing is safe;
- an output that can be reviewed independently;
- a testable distinction from neighboring skills.

## Catalog edit

Add the contract to the appropriate `catalog/skills-*.json` file. Required fields include:

```text
name
display_name
category
summary
invocation
risk
triggers
avoid_when
permissions
routes_to
workflow
output_contract
positive_example
negative_example
status
```

## Regenerate

```bash
python scripts/generate_skill_files.py
```

This updates the skill directory, interface metadata, packaged catalog, route cases, catalog documentation, and manifest hashes.

## Validate

```bash
python scripts/generate_skill_files.py --check
python -m unittest discover -s tests -v
python scripts/public_audit.py .
cesp validate
cesp eval
```

## Review questions

- Can a direct answer replace the skill?
- Can one existing specialist absorb the workflow?
- Does the negative example prevent overreach?
- Does the permission list describe capability without pretending to grant it?
- Should the skill be explicit-first?
- Does every downstream route produce an output required by the user?
- Is the maturity label supported by the committed evidence?

Changing the count of twenty or the count of nine explicit-first skills requires a versioned design decision and corresponding validator update.

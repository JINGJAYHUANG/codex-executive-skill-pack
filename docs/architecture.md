# Architecture

## Layers

```text
Human-reviewed sources
  catalog/skills-*.json
          |
          v
Deterministic generator
  scripts/generate_skill_files.py
          |
          +--> skills/<name>/SKILL.md
          +--> skills/<name>/agents/openai.yaml
          +--> evals/routing_cases.jsonl
          +--> docs/skill-catalog.md
          +--> catalog/manifest.json
          +--> packaged data/skills.json

Validation and inspection
  catalog.py -> router.py -> validation.py -> CLI
```

## Why four catalog files

The catalog is split by functional domain so reviews remain readable. The loader merges and sorts the files by canonical skill name. Generated outputs are deterministic and should never be edited directly.

## Runtime boundary

The Python package does not execute the work described by the skills. It provides:

- catalog loading;
- structural validation;
- a deterministic reference router;
- evaluation against committed cases;
- a preview-first local copy installer.

The host agent runtime remains responsible for interpreting `SKILL.md`, exposing actual tools, enforcing permissions, and obtaining confirmations.

## Routing boundary

The router answers two separate questions:

1. Which contract is relevant?
2. Is natural-language relevance sufficient to route automatically?

For an explicit-first skill, relevance produces `suggest_explicit`, not an execution grant. A `$skill-name` mention changes the routing disposition but still does not grant unavailable connector or operating-system permission.

## Evidence boundary

`spec_validated` means that the contract shape, generated artifacts, and deterministic routing cases pass this repository's checks. It does not imply that a real desktop, email account, API, data pipeline, or workflow was exercised.

## Trust model

The repository assumes:

- committed catalog sources are reviewed;
- generated files are verified against the generator;
- CI has read-only source access except the isolated release job;
- public fixtures contain no private data;
- external action remains under host permissions and user confirmation.

It does not treat model instructions as an access-control system.

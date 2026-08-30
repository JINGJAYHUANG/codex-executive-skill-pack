# Codex Executive Skill Pack

[![CI](https://github.com/JINGJAYHUANG/codex-executive-skill-pack/actions/workflows/ci.yml/badge.svg)](https://github.com/JINGJAYHUANG/codex-executive-skill-pack/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-20-5b5bd6.svg)](docs/skill-catalog.md)

Twenty modular, safety-aware skill contracts for Codex and other agents that understand the Agent Skills convention.

The pack is designed around one principle:

> Route a request to the smallest sufficient capability, and never confuse relevance with authorization.

It packages research, decision, workflow, reliability, knowledge, and controlled-execution capabilities as independent skills rather than one oversized system prompt.

## Current status

Version `0.1.0` validates the **specification surface**:

- exactly 20 named skills;
- one `SKILL.md` and one `agents/openai.yaml` per skill;
- a deterministic machine-readable catalog;
- nine explicit-first gates for higher-impact capabilities;
- 74 committed routing and boundary cases;
- public-tree privacy and secret scanning;
- Python 3.11–3.13 CI;
- deterministic generation checks and reproducible package builds.

This repository does **not** certify real external integrations, credentials, desktop control, messaging delivery, or autonomous operational performance. Each contract carries the status `spec_validated` rather than implying field deployment.

## The 20 skills

### Intelligence

1. `web-intel-harvester` — collect and normalize public evidence.
2. `change-sentinel` — compare dated evidence snapshots.
3. `competitor-radar` — track a defined peer set.
4. `opportunity-radar` — screen evidence-backed opportunities.

### Interaction and builders

5. `screen-macro-recorder` — specify reviewable desktop macros.
6. `desktop-pilot` — execute bounded desktop actions with checkpoints.
7. `api-bridge-builder` — design typed API adapters.
8. `data-pipeline-fabricator` — build validated data pipelines.
9. `fileops-guardian` — plan reversible file mutations.
10. `workflow-compiler` — translate reviewed procedures into workflows.

### Orchestration and reliability

11. `mission-control` — route genuinely multi-part missions.
12. `automation-self-healer` — reproduce, repair, and verify bounded automation failures.

### Decision and knowledge

13. `decision-memo-engine` — produce answer-first decision memos.
14. `experiment-autopilot` — design falsifiable staged experiments.
15. `knowledge-graph-builder` — build provenance-aware knowledge graphs.
16. `skillsmith` — turn repeated workflows into narrow skill contracts.
17. `experience-replay` — reconstruct executions from evidence.

### Execution support

18. `meeting-to-execution` — convert meeting evidence into owners and actions.
19. `inbox-negotiator` — prepare negotiation drafts without silent sending.
20. `personal-coo` — maintain a bounded operating view of commitments.

See the generated [skill catalog](docs/skill-catalog.md) and [routing policy](docs/routing-policy.md).

## Explicit-first safety

Natural-language similarity is not permission. The following nine skills can be identified as relevant, but the router returns `suggest_explicit` until the user names the skill explicitly:

```text
screen-macro-recorder
desktop-pilot
api-bridge-builder
data-pipeline-fabricator
fileops-guardian
workflow-compiler
mission-control
automation-self-healer
inbox-negotiator
```

Even explicit invocation does not bypass platform permissions or confirmation requirements for sending, deleting, committing, sharing, purchasing, or making legal or commercial commitments.

## Quick start

```bash
git clone https://github.com/JINGJAYHUANG/codex-executive-skill-pack.git
cd codex-executive-skill-pack
python -m pip install --no-deps -e .

cesp validate
cesp list
cesp route "Compare these options and recommend a decision"
cesp eval
```

Example router response:

```json
{
  "disposition": "route",
  "selected": "decision-memo-engine",
  "requires_explicit_invocation": false
}
```

A higher-impact natural-language match returns a proposal instead:

```bash
cesp route "Reorganize these files safely"
```

```json
{
  "disposition": "suggest_explicit",
  "selected": "fileops-guardian",
  "requires_explicit_invocation": true
}
```

## Install preview

The installer never edits a global Codex configuration and defaults to preview mode:

```bash
cesp install --target ./local-plugins
```

Apply only after reviewing the destination:

```bash
cesp install --target ./local-plugins --apply
```

This copies a self-contained skill-only plugin directory containing `.codex-plugin/` and `skills/`.

## Repository architecture

```text
.codex-plugin/plugin.json       current-style plugin manifest
catalog/skills-*.json           four human-reviewed source catalogs
catalog/manifest.json           generated hashes and counts
skills/<name>/SKILL.md           generated skill contracts
skills/<name>/agents/openai.yaml generated interfaces
evals/routing_cases.jsonl       74 deterministic cases
src/codex_executive_skill_pack/ validator, router, CLI, installer
scripts/generate_skill_files.py  deterministic generator
scripts/public_audit.py          privacy and secret gate
tests/                           structural, routing, CLI, and generation tests
docs/                            architecture, safety, evaluation, and migration notes
```

The four catalog source files are authoritative. Generated files must match them byte-for-byte:

```bash
python scripts/generate_skill_files.py --check
```

## Design rules

1. Prefer a direct answer when no skill adds meaningful value.
2. Prefer one specialist skill over an orchestration chain.
3. Use `mission-control` only for genuinely multi-owner or multi-gate work.
4. Keep facts, inference, action, and permission separate.
5. Record negative triggers, not only positive trigger phrases.
6. State maturity at the level actually tested.
7. Never store credentials, private account state, personal memory, or machine-specific paths in a public skill contract.

## Verification

The release gate checks:

- catalog schema and cross-skill routes;
- exact skill and explicit-first counts;
- generated file freshness;
- plugin manifest alignment;
- 74 routing and boundary cases;
- CLI preview and install behavior;
- public repository secret and path scan;
- two clean package builds under a fixed source date.

See [evaluation methodology](docs/evaluation.md) and [maturity and limits](docs/maturity-and-limits.md).

## Development disclosure

The exact skill names were recovered from prior project evidence. Public contracts were rebuilt as generic, privacy-safe specifications. Historical local files, user profiles, credentials, account integrations, private policies, and private project state are intentionally excluded.

## License

MIT. See [LICENSE](LICENSE).

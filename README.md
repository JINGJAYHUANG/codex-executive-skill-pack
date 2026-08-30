# Codex Executive Skill Pack

[![CI](https://github.com/JINGJAYHUANG/codex-executive-skill-pack/actions/workflows/ci.yml/badge.svg)](https://github.com/JINGJAYHUANG/codex-executive-skill-pack/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/JINGJAYHUANG/codex-executive-skill-pack)](https://github.com/JINGJAYHUANG/codex-executive-skill-pack/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%E2%80%933.13-blue.svg)](pyproject.toml)

A public, installable collection of **20 bounded Agent Skills** for evidence-aware research, engineering, decision support, learning, and explicitly approved operations.

The pack is built around one rule:

> Use the narrowest sufficient skill, keep evidence and permissions visible, and never represent a plan or unavailable integration as completed work.

**Release status:** `v0.1.1` · `instruction-audited` · `host-dependent`

[中文说明](docs/README.zh-CN.md) · [Skill reference](docs/skill-reference.md) · [Routing model](docs/routing.md) · [Permission model](docs/permission-model.md)

## What this repository is

This repository is both:

1. a **skill-only Codex plugin** with `.codex-plugin/plugin.json` and `skills/`; and
2. an **audit harness** that validates skill structure, routing boundaries, explicit-invocation policy, installation behavior, documentation, and public-release hygiene.

It does not ship an MCP server, account connector, desktop driver, background daemon, secret, or private user profile. Tool availability and enforcement remain the responsibility of the host.

## Quick start

### Validate the source tree

```bash
python -m pip install --no-deps -e .
cesp validate --root . --strict
cesp eval --root .
```

### Inspect or route

```bash
cesp list
cesp show mission-control
cesp route "Build a competitor radar for these three vendors using public evidence." --explain
```

The router is a deterministic **reference harness** for evaluation and debugging. It does not claim to reproduce every host model's routing behavior.

## Install

### Option A — use the repository as a plugin marketplace

```bash
codex plugin marketplace add JINGJAYHUANG/codex-executive-skill-pack
```

Then open the Plugins Directory or `/plugins` where supported, install **Codex Executive Skill Pack**, and restart the host if the skills do not appear immediately.

The marketplace entry is stored at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json), and the plugin manifest is [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json).

### Option B — install repo-scoped skills

Preview first:

```bash
cesp install --layout repo-skills --target .
```

Apply after reviewing the exact file plan:

```bash
cesp install --layout repo-skills --target . --apply
```

This writes skills to:

```text
$REPO_ROOT/.agents/skills/<skill-name>/
```

Install a subset:

```bash
cesp install   --layout repo-skills   --target .   --skills web-intel-harvester,decision-memo-engine   --apply
```

Existing different files are conflicts by default. Replacement requires the explicit `--replace` flag.

### Option C — materialize a standalone plugin directory

```bash
cesp install   --layout plugin   --target ./build/codex-executive-skill-pack   --apply
```

## Four-layer architecture

| Layer | Purpose | Skills |
|---|---|---:|
| Intelligence | Collect evidence, detect change, and map competitors or opportunities | 4 |
| Engineering & Execution | Turn approved work into adapters, pipelines, files, UI steps, and recoverable workflows | 6 |
| Decision & Learning | Convert evidence and experience into decisions, experiments, knowledge, and reusable skills | 5 |
| Orchestration & Operations | Coordinate bounded missions, meetings, negotiations, and selected commitments | 5 |

`mission-control` is the main orchestration skill, but it is **explicit-only**. It does not sit above every task and must not create ceremonial chains for work one specialist or a direct response can finish.

## Exact 20 skills

| # | Skill | Layer | Activation | Risk |
|---:|---|---|---|---|
| 01 | [`web-intel-harvester`](skills/web-intel-harvester/SKILL.md) | intelligence | contextual | low |
| 02 | [`change-sentinel`](skills/change-sentinel/SKILL.md) | intelligence | contextual | low |
| 03 | [`competitor-radar`](skills/competitor-radar/SKILL.md) | intelligence | contextual | medium |
| 04 | [`opportunity-radar`](skills/opportunity-radar/SKILL.md) | intelligence | contextual | medium |
| 05 | [`screen-macro-recorder`](skills/screen-macro-recorder/SKILL.md) | engineering-execution | explicit-only | high |
| 06 | [`desktop-pilot`](skills/desktop-pilot/SKILL.md) | engineering-execution | explicit-only | high |
| 07 | [`api-bridge-builder`](skills/api-bridge-builder/SKILL.md) | engineering-execution | explicit-only | high |
| 08 | [`data-pipeline-fabricator`](skills/data-pipeline-fabricator/SKILL.md) | engineering-execution | contextual | medium |
| 09 | [`fileops-guardian`](skills/fileops-guardian/SKILL.md) | engineering-execution | explicit-only | high |
| 10 | [`workflow-compiler`](skills/workflow-compiler/SKILL.md) | engineering-execution | explicit-only | high |
| 11 | [`mission-control`](skills/mission-control/SKILL.md) | orchestration-operations | explicit-only | high |
| 12 | [`automation-self-healer`](skills/automation-self-healer/SKILL.md) | orchestration-operations | explicit-only | high |
| 13 | [`decision-memo-engine`](skills/decision-memo-engine/SKILL.md) | decision-learning | contextual | medium |
| 14 | [`experiment-autopilot`](skills/experiment-autopilot/SKILL.md) | decision-learning | contextual | medium |
| 15 | [`knowledge-graph-builder`](skills/knowledge-graph-builder/SKILL.md) | decision-learning | contextual | medium |
| 16 | [`skillsmith`](skills/skillsmith/SKILL.md) | decision-learning | contextual | medium |
| 17 | [`experience-replay`](skills/experience-replay/SKILL.md) | decision-learning | contextual | medium |
| 18 | [`meeting-to-execution`](skills/meeting-to-execution/SKILL.md) | orchestration-operations | contextual | medium |
| 19 | [`inbox-negotiator`](skills/inbox-negotiator/SKILL.md) | orchestration-operations | explicit-only | high |
| 20 | [`personal-coo`](skills/personal-coo/SKILL.md) | orchestration-operations | explicit-only | high |

## Explicit-only policy

Nine skills have:

```yaml
policy:
  allow_implicit_invocation: false
```

They are:

```text
screen-macro-recorder
desktop-pilot
api-bridge-builder
fileops-guardian
workflow-compiler
mission-control
automation-self-healer
inbox-negotiator
personal-coo
```

They require explicit naming or `$skill-name` invocation because they involve consequential execution, high-abstraction orchestration, account data, or permission inheritance.

## Every skill contains

```text
skills/<name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── examples.md
```

Each contract defines:

- outcome and scope;
- positive and negative activation boundaries;
- required inputs and deliverables;
- permission and approval labels;
- imperative workflow steps;
- stop conditions;
- common failure modes;
- advisory handoffs;
- two positive examples and one non-trigger example;
- honest maturity and host-dependency labels.

## Evaluation

The repository includes **74 deterministic routing cases**:

- 40 positive cases;
- 20 skill-specific non-trigger cases;
- 9 explicit-only semantic cases;
- 5 direct-response cases.

Run them with:

```bash
cesp eval --root . --show-passes
```

Additional release gates verify:

- exact names and order;
- exactly nine explicit-only skills;
- frontmatter and `openai.yaml` consistency;
- route references and acyclicity;
- direct-first and advisory-handoff policy;
- packaged-data parity;
- safe preview-first installation;
- public-tree secret and private-path scanning;
- generated documentation freshness;
- Python 3.11–3.13 compatibility;
- reproducible wheel and source distribution.

See [evaluation.md](docs/evaluation.md).

## Advisory route graph

Typical paths include:

```text
web-intel-harvester
  → change-sentinel
    → competitor-radar / opportunity-radar
      → decision-memo-engine

screen-macro-recorder
  → skillsmith
    → workflow-compiler
      → desktop-pilot

experience-replay
  → knowledge-graph-builder
    → skillsmith

meeting-to-execution / inbox-negotiator / workflow-compiler / decision-memo-engine
  → personal-coo
```

These are **recommendations**, not automatic execution chains. Every next skill independently rechecks scope, activation, capability, and approval.

## Public and safety boundary

The public pack intentionally excludes:

- credentials, tokens, cookies, webhooks, and account identifiers;
- personal profiles, private memory, chat transcripts, and real inbox content;
- local usernames, machine-specific paths, and production state;
- private strategy logic, rankings, recommendations, or performance;
- live connectors, MCP bindings, desktop-control implementations, or hidden background services;
- claims that an instruction-only skill can grant or enforce host permissions.

A skill may describe a capability that the current host does not provide. In that case it must report the missing capability rather than simulate completion.

## Repository map

```text
.
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── skills/                     # 20 host-loaded skill contracts
├── catalog/                    # canonical machine-readable definitions and routes
├── evals/                      # routing and policy fixtures
├── schemas/                    # JSON Schemas
├── src/executive_skill_pack/   # CLI, validator, router, evaluator, installer
├── scripts/                    # release, docs, and privacy gates
├── tests/                      # regression and safety tests
└── docs/                       # architecture and operating guidance
```

## Development

```bash
python -m pip install --no-deps -e .
python scripts/run_release_gate.py
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill. `catalog/skills.json` is canonical; generated documentation must not be edited by hand.

## Maturity statement

`instruction-audited` means the repository's skill contracts, metadata, routing fixtures, policy assertions, installer, and public surface pass reproducible tests.

It does **not** mean that every skill has been production-tested with every ChatGPT or Codex surface, operating system, connector, account, or external service. Host-level integration evidence belongs in future, separately documented releases.

## License

MIT. See [LICENSE](LICENSE).

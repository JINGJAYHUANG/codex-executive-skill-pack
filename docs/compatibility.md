# Compatibility

## Authoring format

Every skill follows the Agent Skills shape:

```text
skill-name/
├── SKILL.md
├── agents/openai.yaml
└── examples.md
```

`SKILL.md` includes required `name` and `description` frontmatter. `agents/openai.yaml` supplies UI metadata and disables implicit invocation for explicit-only skills.

## Plugin format

The repository root is a skill-only plugin:

```text
.codex-plugin/plugin.json
skills/
```

No MCP server, registered app binding, or lifecycle hook is bundled in v0.1.0.

## Tested Python environments

Repository tooling is tested on:

```text
Python 3.11
Python 3.12
Python 3.13
```

The skills themselves are Markdown and YAML. Python is needed only for validation, reference routing, evaluation, installation, and release checks.

## Host status

| Surface | Status |
|---|---|
| Codex plugin structure | Repository-validated against the current public format |
| Codex repo-scoped `.agents/skills` | Installer and filesystem tests pass |
| ChatGPT/Codex skill loading | Host-dependent; not certified by local tests |
| Explicit invocation metadata | Structurally validated |
| Implicit model routing | Not deterministic; reference harness only |
| Desktop, inbox, calendar, account tools | Not bundled and not production-tested |
| Windows, macOS, Linux installer paths | Implemented with `pathlib`; CI runs on Linux, real host matrix remains future work |

## Collision behavior

Codex may surface two skills with the same `name` from different discovery locations. This pack does not merge duplicate names. Review installed user-, repo-, admin-, and plugin-scoped skills before diagnosing a routing issue.

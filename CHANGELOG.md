# Changelog

All notable public changes are documented here.

## [0.1.0] — 2026-08-30

### Added

- Twenty exact, bounded Agent Skills across four layers.
- A current skill-only Codex plugin manifest and repo marketplace entry.
- Per-skill `SKILL.md`, `agents/openai.yaml`, examples, permissions, stop conditions, and maturity labels.
- Nine explicit-only skills using `policy.allow_implicit_invocation: false`.
- Machine-readable skill and advisory-route catalogs.
- A deterministic reference router, 74 routing cases, and structural policy checks.
- Preview-first installation into `.agents/skills` or a standalone plugin directory.
- Python 3.11–3.13 CI, public-boundary scanning, documentation checks, and release automation.

### Boundary

Version 0.1.0 is instruction-audited and host-dependent. It does not bundle connectors, credentials, desktop drivers, inbox access, or autonomous account actions.

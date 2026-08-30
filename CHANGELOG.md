# Changelog

All notable public changes are documented here.

## [0.1.1] — 2026-08-30

### Fixed

- Honor the catalog-defined implicit-routing threshold instead of silently resetting it to `6`.
- Keep explicit skill invocation independent of the implicit-routing relevance threshold.
- Reject invalid negative, Boolean, or non-integer routing thresholds.
- Reject symbolic-link traversal inside installer targets, including replacement mode.
- Validate pack and skill semantic versions without coupling unchanged skill contracts to the pack release number.
- Bind releases to the current `main` commit and derive provenance counts from repository data.

### Release engineering

- Generate version-specific notes, verify checksums in their own directory, and make release asset repair idempotent.
- Preserve the `instruction-audited` and `host-dependent` maturity boundary.

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

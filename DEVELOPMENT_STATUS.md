# Development status

## Version 0.1.0

The following surfaces are tested:

- catalog structure and cross-skill references;
- exact count of twenty skills;
- exact count of nine explicit-first contracts;
- deterministic generation of skill files and interfaces;
- deterministic routing against 74 committed cases;
- CLI validation, inspection, routing, evaluation, and install preview;
- public-tree secret and personal-path scanning;
- Python 3.11, 3.12, and 3.13 compatibility;
- repeatable source and wheel build checks under a fixed source date.

## Not established by this repository

- that every agent runtime honors the contracts identically;
- that any external connector, desktop controller, inbox, API, or file system is available;
- that a routed skill has authorization to act;
- that generated advice is correct for a real consequential decision;
- that the pack can operate unattended in a live environment;
- that historical local versions passed the current checks.

The public maturity label is `spec_validated`. Operational validation must be performed separately for each runtime and integration.

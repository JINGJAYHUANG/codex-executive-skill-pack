# Threat model

## Protected assets

- user agency and confirmation boundaries;
- credentials and private account data;
- local files and desktop state;
- commercial, legal, and communication commitments;
- truthfulness of maturity and completion claims;
- integrity of generated skill contracts and evaluations.

## Main threats

### Over-routing

A broad orchestrator or high-impact skill is selected when a direct response or one low-risk specialist would suffice.

**Controls:** minimum-score routing, smallest-sufficient policy, negative examples, and `mission-control` boundaries.

### Relevance treated as authorization

A request resembles file, desktop, workflow, or inbox work and is interpreted as permission to act.

**Controls:** nine explicit-first contracts and separate host confirmation requirements.

### Capability inflation

A skill lists a capability class and readers infer that credentials or connectors are installed.

**Controls:** every generated contract states that capability labels are descriptive only.

### Private-state publication

Local paths, account settings, transcripts, prompts, or secrets are copied into a public skill package.

**Controls:** generic rewrites, synthetic examples, repository scanner, contribution templates, and public-boundary documentation.

### Generated-file drift

A hand-edited `SKILL.md` diverges from the reviewed catalog.

**Controls:** deterministic generation, manifest hashes, `--check`, and CI.

### Maturity overstatement

Design or local historical evidence is presented as live operational validation.

**Controls:** `spec_validated` status, prohibited claim checks, and separate maturity stages.

## Out of scope

This repository cannot enforce the security model of every host runtime, prevent a privileged user from modifying local files, or verify the correctness of a third-party connector. Those controls belong to the runtime and deployment environment.

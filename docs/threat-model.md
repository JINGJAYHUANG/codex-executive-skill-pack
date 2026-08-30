# Threat Model

## Protected assets

- user-controlled scope and approval;
- credentials and account data;
- private files and paths;
- external systems and messages;
- integrity of skill definitions and releases;
- truthfulness of execution status.

## Threats and controls

### Prompt injection through evidence

Research and account-reading skills treat retrieved content as data, not instructions. External text cannot expand tool permissions or authorize writes.

### Implicit activation of consequential skills

Nine skills set `allow_implicit_invocation: false`. The reference router also requires explicit naming.

### Over-orchestration

Direct-first routing and an explicit-only `mission-control` prevent a simple task from becoming a broad multi-agent mission.

### Permission laundering through handoffs

Route edges are advisory. Each target skill independently checks activation, scope, capability, and approval.

### Secret or personal-data publication

The release gate scans common credential forms, email addresses, user-home paths, and known private-project markers. Synthetic examples are used throughout.

### Destructive installation

The installer previews by default, blocks filesystem roots and control directories, reports conflicts, and requires explicit replacement.

### False completion

Every skill instructs the host to distinguish executed, drafted, simulated, blocked, and unavailable states.

### Hidden personal profiling

`personal-coo`, `inbox-negotiator`, and `knowledge-graph-builder` include explicit data-minimization boundaries. The public pack stores no user profile.

### Supply-chain drift

Actions are pinned to commit SHAs. Release artifacts include checksums and provenance. Canonical and packaged catalogs must be byte-identical.

## Out of scope

This repository cannot secure a compromised host, malicious connector, stolen account, unsafe organization policy, or unreviewed third-party skill with the same name.

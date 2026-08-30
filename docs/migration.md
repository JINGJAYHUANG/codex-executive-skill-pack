# Migration from a private local skill collection

## Goal

Publish reusable contracts without publishing personal memory, account configuration, machine state, or proprietary operating instructions.

## Recommended sequence

1. Inventory only skill names, purpose, inputs, outputs, and known boundaries.
2. Remove local paths, credentials, private endpoints, account identifiers, and user profiles.
3. Rewrite each skill as a generic contract rather than copying a private prompt verbatim.
4. Separate capability labels from actual connector permissions.
5. Add a negative example for each skill.
6. Classify higher-impact capabilities as explicit-first.
7. Generate public `SKILL.md` and interface files from reviewed metadata.
8. Add deterministic routing and privacy gates.
9. State historical evidence and current test evidence separately.

## Do not migrate

- tokens, cookies, webhook URLs, or authentication commands containing values;
- private correspondence or meeting transcripts;
- personal biographies, health records, admissions records, or financial data;
- internal customer, vendor, pricing, strategy, or production state;
- absolute user-directory paths;
- claims that a private historical version passed checks that were not rerun.

## Status translation

A useful public translation is:

| Private observation | Public status |
|---|---|
| concept only | `design_only` |
| contract and evaluations pass | `spec_validated` |
| one runtime tested | document runtime-specific evidence separately |
| live integration tested | document tool, date, fixture, permission, and failure coverage |

This repository deliberately stops at `spec_validated` for version 0.1.0.

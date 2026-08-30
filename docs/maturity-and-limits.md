# Maturity and limits

## Public maturity label

Every v0.1.0 skill is labeled `spec_validated`.

This means:

- required fields are present;
- names and routes are internally valid;
- generated `SKILL.md` and interface files match the catalog;
- the contract has positive and negative examples;
- the deterministic reference router passes committed cases;
- repository privacy checks pass.

## Higher maturity would require separate evidence

### Runtime validated

Evidence that a named agent runtime reliably discovers and follows the skill across representative tasks.

### Integration validated

Evidence that required connectors or tools work with least privilege, synthetic fixtures, failure tests, and confirmation gates.

### Operationally validated

Evidence from a bounded real deployment covering reliability, incident response, rollback, monitoring, and user outcomes.

The current repository does not claim these later stages.

## Capability labels

Fields such as `public_web_read`, `filesystem_write`, or `email_read` are documentation labels. They describe the class of capability a host may need. They are not secrets, permissions, connectors, or proof of access.

## Routing limits

The reference router is deterministic and explainable, but language understanding is intentionally narrow. It should be treated as:

- a contract consistency check;
- an evaluation oracle for the committed examples;
- a debugging aid for skill authors.

It should not be treated as an authorization engine or a substitute for runtime policy.

## Advice and domain limits

The skill contracts can structure research and decisions, but do not replace legal, medical, financial, security, or other qualified professional judgment. Consequential outputs require source verification and an accountable human decision owner.

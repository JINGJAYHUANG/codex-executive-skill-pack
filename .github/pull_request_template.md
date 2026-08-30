## Change

Describe the contract, routing, evaluation, generator, or documentation change.

## Evidence

- [ ] Repeated workflow or failure mode is documented
- [ ] Positive trigger remains distinct
- [ ] Negative boundary prevents overreach
- [ ] Permission and maturity claims are evidence-based

## Generated surface

- [ ] `python scripts/generate_skill_files.py` was run
- [ ] `python scripts/generate_skill_files.py --check` passes

## Verification

- [ ] Unit and routing tests pass
- [ ] `cesp validate` passes
- [ ] `cesp eval` passes
- [ ] Public-data audit passes
- [ ] No credentials, private paths, personal memory, or private project state added

## Residual risks

State what remains untested in a real runtime or integration.

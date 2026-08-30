# Release Checklist

- [ ] Exact 20 names and canonical order preserved.
- [ ] Exactly nine explicit-only skills.
- [ ] Plugin and marketplace versions updated together.
- [ ] Catalog, skill files, examples, evals, and generated reference agree.
- [ ] No private paths, credentials, account data, production state, or personal profile.
- [ ] `python scripts/run_release_gate.py` passes.
- [ ] Python 3.11, 3.12, and 3.13 CI pass on the exact commit.
- [ ] Reproducible wheel job passes.
- [ ] Tag matches `pyproject.toml`, plugin manifest, and catalog version.
- [ ] Release contains source archives, wheel, `SHA256SUMS.txt`, and `RELEASE_PROVENANCE.json`.
- [ ] Release notes retain host-dependent limitations.

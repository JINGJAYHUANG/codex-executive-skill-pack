# Catalog

- `skills.json` is the canonical public definition of all 20 skills.
- `routes.json` contains direct-first policy and advisory handoff edges.

The Python package embeds byte-identical copies so the installed CLI can route and materialize skills without network access. CI rejects drift between repository and packaged copies.

# Examples for `knowledge-graph-builder`

## Positive trigger 1

> Build a provenance-aware knowledge graph from these validated research notes.

**Expected route:** `knowledge-graph-builder`  
**Expected behavior:** Follow the bounded workflow in `SKILL.md`, preserve evidence and approval boundaries, and return an auditable deliverable.

## Positive trigger 2

> Model entities, relationships, contradictions, and superseded claims over time.

**Expected route:** `knowledge-graph-builder`  
**Expected behavior:** Use only authorized inputs and make host-dependent or unexecuted steps explicit.

## Negative / non-trigger example

> Create a hidden profile of every person mentioned in my private messages.

**Expected route:** Do not activate `knowledge-graph-builder`.

**Reason:** That request exceeds the authorized scope and violates data-minimization and privacy boundaries.

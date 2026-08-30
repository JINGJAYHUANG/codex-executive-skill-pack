# Skill Reference

> Generated from `catalog/skills.json` and `catalog/routes.json`. Run `python scripts/generate_reference.py --check` before committing.

All skills are **instruction-audited** and **host-dependent**. This catalog does not certify production integrations.

## Layer 1 — Intelligence

### 01. `web-intel-harvester`

**Purpose:** Collect public web evidence into a structured, cited source pack before analysis begins.

**Activation:** contextual · **Risk:** low · **Runtime:** host-dependent

**Permissions:** `network_read`, `local_write_optional`

**Advisory handoffs:**

- `change-sentinel` — A baseline source pack exists and the question is what changed.

### 02. `change-sentinel`

**Purpose:** Detect material changes between a defined baseline and an as-of state.

**Activation:** contextual · **Risk:** low · **Runtime:** host-dependent

**Permissions:** `network_read_optional`, `local_read`, `local_write_optional`

**Advisory handoffs:**

- `competitor-radar` — The detected change affects a named competitive set.
- `opportunity-radar` — The detected change may open an actionable gap.

### 03. `competitor-radar`

**Purpose:** Turn lawful public competitive signals into an evidence-backed strategic view.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `network_read_optional`, `local_write_optional`

**Advisory handoffs:**

- `decision-memo-engine` — Competitive evidence must support a bounded decision.

### 04. `opportunity-radar`

**Purpose:** Discover and rank opportunities against explicit capabilities, constraints, and kill criteria.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `network_read_optional`, `local_write_optional`

**Advisory handoffs:**

- `decision-memo-engine` — A screened opportunity needs an explicit recommendation.

## Layer 2 — Engineering & Execution

### 05. `screen-macro-recorder`

**Purpose:** Convert an authorized screen trace into a redacted, reproducible macro specification.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `screen_read_authorized`, `local_write`

**Advisory handoffs:**

- `skillsmith` — A consented recording reveals a repeatable workflow worth packaging.

### 06. `desktop-pilot`

**Purpose:** Execute or rehearse authorized GUI workflows with previews, checkpoints, and rollback awareness.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `desktop_control`, `local_write_optional`, `external_write_optional`

**Advisory handoffs:** none.

### 07. `api-bridge-builder`

**Purpose:** Build a narrow, tested adapter between a documented API and a local workflow.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `network_read`, `network_write_optional`, `local_write`, `secrets_reference_only`

**Advisory handoffs:**

- `data-pipeline-fabricator` — A verified API adapter must feed a validated data pipeline.

### 08. `data-pipeline-fabricator`

**Purpose:** Turn a source-to-target data contract into a repeatable, observable pipeline.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `local_read`, `local_write`, `network_read_optional`, `network_write_optional`

**Advisory handoffs:**

- `automation-self-healer` — A running pipeline needs bounded failure recovery.

### 09. `fileops-guardian`

**Purpose:** Make consequential file operations inventory-first, previewable, verifiable, and reversible.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `local_read`, `local_write`, `destructive_write_optional`

**Advisory handoffs:**

- `workflow-compiler` — A file mutation plan should become a checkpointed workflow.

### 10. `workflow-compiler`

**Purpose:** Compile a human process into an executable, testable workflow contract.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `local_write`, `execute_local_optional`, `external_write_optional`

**Advisory handoffs:**

- `desktop-pilot` — A reviewed workflow requires explicitly approved UI execution.
- `personal-coo` — A reviewed workflow must be scheduled among selected commitments.

## Layer 4 — Orchestration & Operations

### 11. `mission-control`

**Purpose:** Coordinate a complex, explicitly authorized mission using the minimum useful skill set.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `orchestration`, `inherits_child_permissions`

**Advisory handoffs:** none.

### 12. `automation-self-healer`

**Purpose:** Diagnose and repair an automation through bounded patches, evidence, and rollback.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `local_read`, `local_write`, `execute_local`, `external_write_optional`

**Advisory handoffs:** none.

## Layer 3 — Decision & Learning

### 13. `decision-memo-engine`

**Purpose:** Convert evidence and constraints into a concise, auditable decision memo.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `reasoning_only`, `local_write_optional`

**Advisory handoffs:**

- `personal-coo` — An approved decision changes the bounded operating plan.

### 14. `experiment-autopilot`

**Purpose:** Design a falsifiable experiment with preregistered metrics, stops, and analysis.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `reasoning_only`, `local_write_optional`, `execute_local_optional`

**Advisory handoffs:**

- `decision-memo-engine` — Experiment evidence is decision-ready.
- `experience-replay` — An experiment failed or produced an unexpected result.

### 15. `knowledge-graph-builder`

**Purpose:** Model validated claims as time-aware entities and relationships with provenance, confidence, and contradiction handling.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `local_read`, `local_write`, `network_read_optional`

**Advisory handoffs:**

- `skillsmith` — Repeated evidence-backed practice is stable enough to package.

### 16. `skillsmith`

**Purpose:** Turn a repeated workflow into a narrow, testable, distributable Agent Skill.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `local_read`, `local_write`

**Advisory handoffs:**

- `workflow-compiler` — A skill design needs an executable, resumable workflow.

### 17. `experience-replay`

**Purpose:** Reconstruct an incident or project from authorized artifacts and turn verified lessons into prevention tests.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `local_read`, `local_write_optional`

**Advisory handoffs:**

- `knowledge-graph-builder` — Verified lessons should become time-aware reusable knowledge.

## Layer 4 — Orchestration & Operations

### 18. `meeting-to-execution`

**Purpose:** Convert authorized meeting material into a decision log and an execution-ready action register.

**Activation:** contextual · **Risk:** medium · **Runtime:** host-dependent

**Permissions:** `local_read`, `local_write_optional`, `external_write_requires_approval`

**Advisory handoffs:**

- `personal-coo` — Explicitly selected commitments need cross-domain coordination.

### 19. `inbox-negotiator`

**Purpose:** Analyze an authorized message thread and draft a calibrated negotiation response without sending it.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `account_read_explicit`, `local_write_optional`, `external_write_requires_approval`

**Advisory handoffs:**

- `personal-coo` — An approved negotiation outcome changes selected commitments.

### 20. `personal-coo`

**Purpose:** Coordinate explicitly selected commitments into a bounded operating brief without building a hidden personal profile.

**Activation:** explicit-only · **Risk:** high · **Runtime:** host-dependent

**Permissions:** `local_read_explicit`, `account_read_explicit_optional`, `external_write_requires_approval`

**Advisory handoffs:** none.

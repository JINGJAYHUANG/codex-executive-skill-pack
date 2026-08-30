# Permission and Approval Model

Permission labels communicate intended scope. They do not grant host capabilities.

## Taxonomy

| Label | Meaning |
|---|---|
| `account_read_explicit` | May read only the explicitly authorized account object or thread. |
| `account_read_explicit_optional` | May read an explicitly authorized account object only when required. |
| `desktop_control` | May control the named UI only after explicit invocation and with pause points before consequential actions. |
| `destructive_write_optional` | Deletion or irreversible replacement is optional, preview-first, and separately approved. |
| `execute_local` | May execute bounded local commands when the host permits it and the exact scope is visible. |
| `execute_local_optional` | Local execution is optional and should be previewed when it can mutate state. |
| `external_write_optional` | Any send, publish, submission, account mutation, or external write remains optional and requires separate approval. |
| `external_write_requires_approval` | Any send, publish, schedule change, account mutation, or external write requires separate approval. |
| `inherits_child_permissions` | Each child skill keeps its own activation and approval boundary; permissions are never silently elevated. |
| `local_read` | May read only files or artifacts in the authorized task scope. |
| `local_read_explicit` | May read only explicitly selected local artifacts. |
| `local_write` | May create or update bounded local artifacts after showing the intended scope. |
| `local_write_optional` | May write a bounded artifact when that materially improves the outcome. |
| `network_read` | May read public network sources when the host provides a network tool. |
| `network_read_optional` | May read public network sources only when needed and available. |
| `network_write_optional` | Network writes are optional and require a reviewed target, payload, and approval. |
| `orchestration` | May coordinate bounded specialist work; orchestration alone grants no additional tool permission. |
| `reasoning_only` | The core workflow can be completed without external writes or privileged tools. |
| `screen_read_authorized` | May inspect only the screen capture or recording explicitly authorized for this task. |
| `secrets_reference_only` | May reference secret variable names but must never read, print, or persist secret values. |

## Three gates

### 1. Activation gate

Should the skill be used at all?

- Contextual skills may match a clear description.
- Explicit-only skills require direct naming or `$skill-name`.
- Direct completion remains preferred when simpler.

### 2. Capability gate

Does the current host actually provide the required tool?

A skill that refers to desktop control, inbox access, local execution, or network access must not assume that capability exists. Missing capability is an execution status, not a reason to fabricate completion.

### 3. Approval gate

Has the user approved this exact consequential action?

Separate approval is required for:

- sending or publishing;
- account or calendar mutation;
- external submissions;
- irreversible file operations;
- desktop confirmation buttons;
- process restarts with material impact;
- network writes;
- permission expansion.

A broad objective such as “handle this” does not approve every downstream action.

## Permission inheritance

`mission-control` may coordinate children but cannot elevate them. `inherits_child_permissions` means every child preserves its own narrower restrictions.

A valid orchestration record should show:

- selected child skill;
- reason it is necessary;
- input boundary;
- expected output;
- tool requirement;
- approval requirement;
- completed or blocked state.

## No hidden persistence

No skill in v0.1.0 is allowed to build an undisclosed personal profile, sweep unrelated account data, or persist broad behavioral history. Persistent artifacts must be explicit, bounded, and reviewable.

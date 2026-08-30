from __future__ import annotations

import json
from typing import Any


_PERMISSION_TEXT = {'network_read': 'May read public network sources when the host provides a network tool.', 'network_read_optional': 'May read public network sources only when needed and available.', 'local_read': 'May read only files or artifacts in the authorized task scope.', 'local_read_explicit': 'May read only explicitly selected local artifacts.', 'local_write': 'May create or update bounded local artifacts after showing the intended scope.', 'local_write_optional': 'May write a bounded artifact when that materially improves the outcome.', 'screen_read_authorized': 'May inspect only the screen capture or recording explicitly authorized for this task.', 'desktop_control': 'May control the named UI only after explicit invocation and with pause points before consequential actions.', 'external_write_optional': 'Any send, publish, submission, account mutation, or external write remains optional and requires separate approval.', 'network_write_optional': 'Network writes are optional and require a reviewed target, payload, and approval.', 'secrets_reference_only': 'May reference secret variable names but must never read, print, or persist secret values.', 'destructive_write_optional': 'Deletion or irreversible replacement is optional, preview-first, and separately approved.', 'execute_local': 'May execute bounded local commands when the host permits it and the exact scope is visible.', 'execute_local_optional': 'Local execution is optional and should be previewed when it can mutate state.', 'orchestration': 'May coordinate bounded specialist work; orchestration alone grants no additional tool permission.', 'inherits_child_permissions': 'Each child skill keeps its own activation and approval boundary; permissions are never silently elevated.', 'reasoning_only': 'The core workflow can be completed without external writes or privileged tools.', 'account_read_explicit': 'May read only the explicitly authorized account object or thread.', 'account_read_explicit_optional': 'May read an explicitly authorized account object only when required.', 'external_write_requires_approval': 'Any send, publish, schedule change, account mutation, or external write requires separate approval.'}


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))


def render_skill_md(skill: dict[str, Any], edges: list[dict[str, Any]]) -> str:
    activation = "explicit-only" if skill["explicit_only"] else "contextual"
    if skill["explicit_only"]:
        boundary = (
            f"This skill is **explicit-only**. Activate it only when the user "
            f"writes `${skill['name']}`, names `{skill['name']}`, or clearly "
            "asks to use it. Do not infer permission from a broad goal."
        )
    else:
        boundary = (
            "This skill may be selected contextually when its positive boundary "
            "is clearly met; direct completion remains preferred when simpler."
        )

    permission_lines = [
        f"- `{label}` — {_PERMISSION_TEXT.get(label, 'Use only within the explicitly authorized task boundary.')}"
        for label in skill["permissions"]
    ]
    outgoing = [edge for edge in edges if edge["from"] == skill["name"]]
    incoming = [edge for edge in edges if edge["to"] == skill["name"]]
    handoffs: list[str] = []
    if outgoing:
        handoffs.append("**May hand off to**")
        handoffs.extend(f"- `{edge['to']}` — {edge['when']}" for edge in outgoing)
    if incoming:
        handoffs.append("**May receive from**")
        handoffs.extend(f"- `{edge['from']}` — {edge['when']}" for edge in incoming)
    if not handoffs:
        handoffs.append("No predefined handoff. Finish directly or return control to the caller.")

    description = json.dumps(skill["description"], ensure_ascii=False)
    return f"""---
name: {skill['name']}
description: {description}
metadata:
  version: "0.1.0"
  layer: {skill['layer']}
  maturity: instruction-audited
  runtime_status: host-dependent
  activation: {activation}
  risk: {skill['risk']}
---

# {skill['display_name']}

## Outcome

{skill['purpose']}

## Activation boundary

{boundary}

Prefer the narrowest sufficient capability. Do not invoke this skill merely to demonstrate orchestration.

### Use when

{_bullets(skill['use_when'])}

### Do not use when

{_bullets(skill['avoid_when'])}

## Required inputs

{_bullets(skill['inputs'])}

If a required input is absent and cannot be resolved from an authorized source, return the smallest safe partial result and identify the gap. Do not invent it.

## Deliverables

{_bullets(skill['outputs'])}

## Permissions and approvals

{chr(10).join(permission_lines)}

These labels describe the intended boundary; they do not grant tools or permissions that the host does not provide.

## Workflow

{_numbered(skill['workflow'])}

## Stop conditions

Stop and return a bounded status when any of the following applies:

- The requested scope expands beyond the authorized target.
- A consequential external action lacks separate approval.
- Evidence is insufficient for a material claim.
- A safer or simpler direct method already satisfies the request.
- The host lacks a required capability; do not simulate a completed action.

## Failure modes to guard against

{_bullets(skill['failure_modes'])}

## Handoffs

{chr(10).join(handoffs)}

A handoff is a recommendation, not an automatic chain. The next skill must independently satisfy its activation and permission boundary.

## Evidence and honesty

Separate observed facts, user-provided claims, inference, and unresolved uncertainty. Report the actual execution status. Never present a drafted plan, simulated result, or unavailable integration as an executed action.
"""


def render_openai_yaml(skill: dict[str, Any]) -> str:
    short = skill["purpose"]
    if len(short) > 100:
        short = short[:97].rstrip() + "..."
    text = (
        "interface:\n"
        f"  display_name: {json.dumps(skill['display_name'], ensure_ascii=False)}\n"
        f"  short_description: {json.dumps(short, ensure_ascii=False)}\n"
        f"  default_prompt: {json.dumps(skill['positive_prompts'][0], ensure_ascii=False)}\n"
    )
    if skill["explicit_only"]:
        text += "policy:\n  allow_implicit_invocation: false\n"
    return text


def render_examples(skill: dict[str, Any]) -> str:
    return f"""# Examples for `{skill['name']}`

## Positive trigger 1

> {skill['positive_prompts'][0]}

**Expected route:** `{skill['name']}`

## Positive trigger 2

> {skill['positive_prompts'][1]}

**Expected route:** `{skill['name']}`

## Negative / non-trigger example

> {skill['negative_prompt']}

**Expected route:** Do not activate `{skill['name']}`.

**Reason:** {skill['negative_reason']}
"""

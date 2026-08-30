#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_skills(root: Path) -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    for path in sorted((root / "catalog").glob("skills-*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise SystemExit(f"{path} must contain an array")
        skills.extend(payload)
    return sorted(skills, key=lambda item: item["name"])


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))


def render_skill(skill: dict[str, Any]) -> str:
    routes = skill["routes_to"] or []
    invocation = (
        "Explicit-first: do not treat a natural-language match as authorization to execute. Ask for or require an explicit invocation before consequential action."
        if skill["invocation"] == "explicit_first"
        else "Automatic routing is allowed when this is the smallest sufficient specialist skill. Consequential external writes still require the relevant user confirmation."
    )
    route_text = bullets([f"Route to `{name}` only when that specialist capability is necessary." for name in routes]) if routes else "- No downstream route is required by default."
    return f'''---
name: {skill["name"]}
description: {json.dumps(skill["summary"], ensure_ascii=False)}
---

# {skill["display_name"]}

**Status:** `{skill["status"]}`  
**Category:** `{skill["category"]}`  
**Risk:** `{skill["risk"]}`  
**Invocation:** `{skill["invocation"]}`

{skill["summary"]}

## Use when

{bullets(skill["triggers"])}

## Do not use when

{bullets(skill["avoid_when"])}

## Invocation and permission contract

{invocation}

Declared capability classes:

{bullets([f"`{item}`" for item in skill["permissions"]])}

These labels document expected capability boundaries. They do not grant credentials, connector access, operating-system permission, or authority to make commitments.

## Workflow

{numbered(skill["workflow"])}

## Output contract

{bullets(skill["output_contract"])}

## Routing

{route_text}

Do not build a skill chain merely to demonstrate orchestration. Prefer a direct answer or one specialist skill whenever sufficient.

## Examples

**Positive request**

> {skill["positive_example"]["request"]}

Expected route: `{skill["positive_example"]["expected"]}`.

**Boundary request**

> {skill["negative_example"]["request"]}

Why not: {skill["negative_example"]["reason"]}

## Verification status

The contract, generated files, deterministic router behavior, and committed evaluation cases are tested. External integrations and real-world operational outcomes are not certified by this repository.
'''


def render_interface(skill: dict[str, Any]) -> str:
    short = skill["summary"]
    if len(short) > 96:
        short = short[:93].rstrip() + "..."
    return (
        "interface:\n"
        f"  display_name: {json.dumps(skill['display_name'])}\n"
        f"  short_description: {json.dumps(short)}\n"
    )


def base_cases(skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for skill in skills:
        name = skill["name"]
        cases.append({
            "id": f"{name}-explicit",
            "request": f"${name}: {skill['positive_example']['request']}",
            "expected": name,
            "disposition": "route",
            "kind": "explicit",
        })
        cases.append({
            "id": f"{name}-natural",
            "request": f"Please {skill['triggers'][0]} for a bounded synthetic example.",
            "expected": name,
            "disposition": "suggest_explicit" if skill["invocation"] == "explicit_first" else "route",
            "kind": "natural",
        })
        cases.append({
            "id": f"{name}-boundary",
            "request": skill["negative_example"]["request"],
            "must_not_select": name,
            "kind": "boundary",
        })
    return cases


def composite_cases() -> list[dict[str, Any]]:
    return [
        {"id": "composite-mission-explicit", "request": "$mission-control coordinate this multi-step mission with research, implementation, and approval gates.", "expected": "mission-control", "disposition": "route", "kind": "composite"},
        {"id": "composite-mission-natural", "request": "Please coordinate this multi-step mission with several specialists.", "expected": "mission-control", "disposition": "suggest_explicit", "kind": "composite"},
        {"id": "composite-source-table", "request": "Collect public web evidence and build a source table from official pages.", "expected": "web-intel-harvester", "disposition": "route", "kind": "composite"},
        {"id": "composite-change", "request": "What changed since the saved baseline last quarter?", "expected": "change-sentinel", "disposition": "route", "kind": "composite"},
        {"id": "composite-competitors", "request": "Build a competitive landscape for these five companies.", "expected": "competitor-radar", "disposition": "route", "kind": "composite"},
        {"id": "composite-opportunity", "request": "Rank business ideas using demand, competition, economics, and execution risk.", "expected": "opportunity-radar", "disposition": "route", "kind": "composite"},
        {"id": "composite-decision", "request": "Write a decision memo comparing build, buy, and partner options.", "expected": "decision-memo-engine", "disposition": "route", "kind": "composite"},
        {"id": "composite-experiment", "request": "Design an experiment to test this onboarding hypothesis.", "expected": "experiment-autopilot", "disposition": "route", "kind": "composite"},
        {"id": "composite-graph", "request": "Build a knowledge graph linking claims, sources, entities, and dates.", "expected": "knowledge-graph-builder", "disposition": "route", "kind": "composite"},
        {"id": "composite-meeting", "request": "Turn these meeting notes into actions, owners, and deadlines.", "expected": "meeting-to-execution", "disposition": "route", "kind": "composite"},
        {"id": "composite-inbox", "request": "Negotiate this email thread and draft a counteroffer without sending.", "expected": "inbox-negotiator", "disposition": "suggest_explicit", "kind": "composite"},
        {"id": "composite-fileops", "request": "Reorganize these files safely with a preview and rollback plan.", "expected": "fileops-guardian", "disposition": "suggest_explicit", "kind": "composite"},
        {"id": "composite-heal", "request": "Repair this failed automation after reproducing the error.", "expected": "automation-self-healer", "disposition": "suggest_explicit", "kind": "composite"},
        {"id": "composite-coo", "request": "Organize my current commitments into a weekly operating review.", "expected": "personal-coo", "disposition": "route", "kind": "composite"},
    ]


def catalog_doc(skills: list[dict[str, Any]]) -> str:
    rows = ["| Skill | Category | Invocation | Risk | Status |", "|---|---|---|---|---|"]
    for skill in skills:
        rows.append(f"| [`{skill['name']}`](../skills/{skill['name']}/SKILL.md) | {skill['category']} | `{skill['invocation']}` | {skill['risk']} | `{skill['status']}` |")
    return "# Skill catalog\n\nThis table is generated from the four catalog source files.\n\n" + "\n".join(rows) + "\n"


def expected_files(root: Path) -> dict[Path, str]:
    skills = load_skills(root)
    cases = base_cases(skills) + composite_cases()
    if len(cases) != 74:
        raise SystemExit(f"expected 74 routing cases, generated {len(cases)}")
    files: dict[Path, str] = {}
    for skill in skills:
        files[Path("skills") / skill["name"] / "SKILL.md"] = render_skill(skill)
        files[Path("skills") / skill["name"] / "agents" / "openai.yaml"] = render_interface(skill)
    files[Path("src/codex_executive_skill_pack/data/skills.json")] = json.dumps(skills, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    files[Path("evals/routing_cases.jsonl")] = "".join(json.dumps(case, sort_keys=True, ensure_ascii=False) + "\n" for case in cases)
    files[Path("docs/skill-catalog.md")] = catalog_doc(skills)

    hashes = {str(path): hashlib.sha256(content.encode("utf-8")).hexdigest() for path, content in sorted(files.items(), key=lambda item: str(item[0]))}
    manifest = {
        "schema": 1,
        "skill_count": len(skills),
        "explicit_first_count": sum(skill["invocation"] == "explicit_first" for skill in skills),
        "routing_case_count": len(cases),
        "catalog_sha256": hashlib.sha256((json.dumps(skills, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")).hexdigest(),
        "files": hashes,
    }
    files[Path("catalog/manifest.json")] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    return files


def write_files(root: Path) -> None:
    for relative, content in expected_files(root).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def check_files(root: Path) -> list[str]:
    mismatches: list[str] = []
    for relative, content in expected_files(root).items():
        path = root / relative
        if not path.is_file():
            mismatches.append(f"missing: {relative}")
        elif path.read_text(encoding="utf-8") != content:
            mismatches.append(f"stale: {relative}")
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.check:
        mismatches = check_files(root)
        if mismatches:
            print("\n".join(mismatches))
            return 1
        print("generated skill surface is current")
        return 0
    write_files(root)
    print(f"generated {len(expected_files(root))} deterministic files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

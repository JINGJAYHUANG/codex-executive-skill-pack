from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from .catalog import load_skills

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED = {
    "name", "display_name", "category", "summary", "invocation", "risk",
    "triggers", "avoid_when", "permissions", "routes_to", "workflow",
    "output_contract", "positive_example", "negative_example", "status",
}
ALLOWED_INVOCATION = {"auto", "explicit_first"}
ALLOWED_RISK = {"low", "medium", "high"}
ALLOWED_STATUS = {"spec_validated", "design_only"}


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _repo_root(root: str | Path | None) -> Path:
    if root is not None:
        return Path(root).resolve()
    return Path.cwd().resolve()


def validate_catalog(root: str | Path | None = None, *, check_generated: bool = True) -> list[Finding]:
    repo = _repo_root(root)
    findings: list[Finding] = []
    try:
        skills = load_skills(repo)
    except Exception as exc:  # pragma: no cover - defensive boundary
        return [Finding("error", "catalog_load", str(exc))]

    if len(skills) != 20:
        findings.append(Finding("error", "skill_count", f"expected 20 skills, found {len(skills)}"))
    names = [skill.get("name") for skill in skills]
    if len(names) != len(set(names)):
        findings.append(Finding("error", "duplicate_name", "skill names must be unique"))
    name_set = set(names)

    explicit_count = 0
    for index, skill in enumerate(skills):
        missing = REQUIRED - set(skill)
        if missing:
            findings.append(Finding("error", "missing_fields", f"skill[{index}] missing {sorted(missing)}"))
            continue
        name = skill["name"]
        if not NAME_RE.fullmatch(name):
            findings.append(Finding("error", "invalid_name", f"invalid skill name: {name}"))
        if skill["invocation"] not in ALLOWED_INVOCATION:
            findings.append(Finding("error", "invalid_invocation", f"{name}: invalid invocation"))
        if skill["invocation"] == "explicit_first":
            explicit_count += 1
        if skill["risk"] not in ALLOWED_RISK:
            findings.append(Finding("error", "invalid_risk", f"{name}: invalid risk"))
        if skill["status"] not in ALLOWED_STATUS:
            findings.append(Finding("error", "invalid_status", f"{name}: invalid status"))
        for field in ("triggers", "avoid_when", "permissions", "workflow", "output_contract"):
            value = skill[field]
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                findings.append(Finding("error", "invalid_list", f"{name}: {field} must be a non-empty string list"))
        for route_name in skill["routes_to"]:
            if route_name not in name_set:
                findings.append(Finding("error", "unknown_route", f"{name} routes to unknown skill {route_name}"))
            if route_name == name:
                findings.append(Finding("error", "self_route", f"{name} must not route to itself"))
        if skill["positive_example"].get("expected") != name:
            findings.append(Finding("error", "bad_positive_example", f"{name}: positive example must expect itself"))
        if not skill["negative_example"].get("reason"):
            findings.append(Finding("error", "bad_negative_example", f"{name}: negative example needs a reason"))

    if explicit_count != 9:
        findings.append(Finding("error", "explicit_count", f"expected 9 explicit-first skills, found {explicit_count}"))

    plugin_path = repo / ".codex-plugin" / "plugin.json"
    if not plugin_path.is_file():
        findings.append(Finding("error", "plugin_manifest_missing", ".codex-plugin/plugin.json is missing"))
    else:
        try:
            plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
            if plugin.get("skills") != "./skills/":
                findings.append(Finding("error", "plugin_skills_path", "plugin skills path must be ./skills/"))
            if plugin.get("version") != "0.1.0":
                findings.append(Finding("error", "plugin_version", "plugin version must match v0.1.0"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("error", "plugin_manifest_invalid", str(exc)))

    if check_generated:
        for name in sorted(name_set):
            skill_md = repo / "skills" / name / "SKILL.md"
            interface = repo / "skills" / name / "agents" / "openai.yaml"
            if not skill_md.is_file():
                findings.append(Finding("error", "skill_file_missing", f"missing {skill_md.relative_to(repo)}"))
            elif f"name: {name}" not in skill_md.read_text(encoding="utf-8"):
                findings.append(Finding("error", "skill_file_mismatch", f"{name}: SKILL.md front matter mismatch"))
            if not interface.is_file():
                findings.append(Finding("error", "interface_missing", f"missing {interface.relative_to(repo)}"))

        eval_path = repo / "evals" / "routing_cases.jsonl"
        if not eval_path.is_file():
            findings.append(Finding("error", "evals_missing", "routing_cases.jsonl is missing"))
        else:
            lines = [line for line in eval_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if len(lines) != 74:
                findings.append(Finding("error", "eval_count", f"expected 74 routing cases, found {len(lines)}"))
            for number, line in enumerate(lines, 1):
                try:
                    case = json.loads(line)
                except json.JSONDecodeError as exc:
                    findings.append(Finding("error", "eval_json", f"line {number}: {exc}"))
                    continue
                if not case.get("id") or not case.get("request"):
                    findings.append(Finding("error", "eval_fields", f"line {number}: id and request required"))

    forbidden_claims = ("production validated", "production-ready", "guaranteed autonomous")
    for path in [repo / "README.md", repo / "DEVELOPMENT_STATUS.md"]:
        if path.is_file():
            lower = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden_claims:
                if phrase in lower:
                    findings.append(Finding("error", "maturity_overclaim", f"{path.name} contains forbidden claim: {phrase}"))
    return findings


def summary(root: str | Path | None = None, *, check_generated: bool = True) -> dict[str, Any]:
    findings = validate_catalog(root, check_generated=check_generated)
    return {
        "status": "pass" if not any(item.level == "error" for item in findings) else "fail",
        "errors": sum(item.level == "error" for item in findings),
        "warnings": sum(item.level == "warning" for item in findings),
        "findings": [item.to_dict() for item in findings],
    }

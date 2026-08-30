from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .catalog import load_repository_json
from .frontmatter import FrontmatterError, parse_frontmatter


EXACT_NAMES = [
    "web-intel-harvester",
    "change-sentinel",
    "competitor-radar",
    "opportunity-radar",
    "screen-macro-recorder",
    "desktop-pilot",
    "api-bridge-builder",
    "data-pipeline-fabricator",
    "fileops-guardian",
    "workflow-compiler",
    "mission-control",
    "automation-self-healer",
    "decision-memo-engine",
    "experiment-autopilot",
    "knowledge-graph-builder",
    "skillsmith",
    "experience-replay",
    "meeting-to-execution",
    "inbox-negotiator",
    "personal-coo",
]

EXPLICIT_ONLY = {
    "screen-macro-recorder",
    "desktop-pilot",
    "api-bridge-builder",
    "fileops-guardian",
    "workflow-compiler",
    "mission-control",
    "automation-self-healer",
    "inbox-negotiator",
    "personal-coo",
}

REQUIRED_SKILL_KEYS = {
    "name",
    "display_name",
    "layer",
    "purpose",
    "description",
    "explicit_only",
    "risk",
    "permissions",
    "inputs",
    "outputs",
    "use_when",
    "avoid_when",
    "workflow",
    "failure_modes",
    "keywords",
    "phrases",
    "anti_keywords",
    "positive_prompts",
    "negative_prompt",
    "negative_reason",
    "maturity",
    "runtime_status",
    "version",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ValidationReport:
    root: str
    issues: tuple[Issue, ...]

    @property
    def errors(self) -> int:
        return sum(item.severity == "error" for item in self.issues)

    @property
    def warnings(self) -> int:
        return sum(item.severity == "warning" for item in self.issues)

    @property
    def ok(self) -> bool:
        return self.errors == 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
            "issues": [item.as_dict() for item in self.issues],
        }


def _read_json(path: Path, issues: list[Issue]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(Issue("error", "missing_file", str(path), "required JSON file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(Issue("error", "invalid_json", str(path), str(exc)))
        return None
    if not isinstance(value, dict):
        issues.append(Issue("error", "invalid_json_type", str(path), "top-level value must be an object"))
        return None
    return value


def _extract_yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        return None
    raw = match.group(1)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        value = raw
    return str(value)


def _has_cycle(names: set[str], edges: list[dict[str, Any]]) -> bool:
    graph = {name: [] for name in names}
    indegree = {name: 0 for name in names}
    for edge in edges:
        source, target = edge.get("from"), edge.get("to")
        if source in graph and target in graph:
            graph[source].append(target)
            indegree[target] += 1
    queue = [name for name, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for target in graph[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return visited != len(names)


def validate_repository(root: Path, *, strict: bool = False) -> ValidationReport:
    root = root.resolve()
    issues: list[Issue] = []

    required_paths = [
        ".codex-plugin/plugin.json",
        ".agents/plugins/marketplace.json",
        "catalog/skills.json",
        "catalog/routes.json",
        "README.md",
        "LICENSE",
    ]
    for relative in required_paths:
        if not (root / relative).is_file():
            issues.append(Issue("error", "missing_file", relative, "required repository file is missing"))

    catalog = _read_json(root / "catalog/skills.json", issues)
    routes = _read_json(root / "catalog/routes.json", issues)
    manifest = _read_json(root / ".codex-plugin/plugin.json", issues)
    marketplace = _read_json(root / ".agents/plugins/marketplace.json", issues)
    if not all((catalog, routes, manifest, marketplace)):
        return ValidationReport(str(root), tuple(issues))

    assert catalog is not None and routes is not None
    assert manifest is not None and marketplace is not None

    pack = catalog.get("pack", {})
    listed = catalog.get("skills", [])
    if not isinstance(listed, list):
        issues.append(Issue("error", "catalog_type", "catalog/skills.json", "skills must be an array"))
        listed = []
    names = [item.get("name") for item in listed if isinstance(item, dict)]
    if names != EXACT_NAMES:
        issues.append(
            Issue(
                "error",
                "exact_names",
                "catalog/skills.json",
                "the 20 skill names or their canonical order changed",
            )
        )
    if len(names) != len(set(names)):
        issues.append(Issue("error", "duplicate_skill", "catalog/skills.json", "skill names must be unique"))
    if pack.get("skill_count") != 20 or len(listed) != 20:
        issues.append(Issue("error", "skill_count", "catalog/skills.json", "exactly 20 skills are required"))

    explicit = {
        item["name"]
        for item in listed
        if isinstance(item, dict) and item.get("explicit_only") is True
    }
    if explicit != EXPLICIT_ONLY:
        issues.append(
            Issue(
                "error",
                "explicit_policy",
                "catalog/skills.json",
                "explicit-only set differs from the public v0.1.0 policy",
            )
        )
    if pack.get("explicit_only_count") != len(EXPLICIT_ONLY):
        issues.append(Issue("error", "explicit_count", "catalog/skills.json", "explicit-only count must be 9"))

    if manifest.get("name") != "codex-executive-skill-pack":
        issues.append(Issue("error", "manifest_name", ".codex-plugin/plugin.json", "plugin name changed"))
    if manifest.get("version") != pack.get("version"):
        issues.append(Issue("error", "version_mismatch", ".codex-plugin/plugin.json", "manifest/catalog versions differ"))
    if manifest.get("skills") != "./skills/":
        issues.append(Issue("error", "manifest_path", ".codex-plugin/plugin.json", "skills path must be ./skills/"))
    if any(key in manifest for key in ("apps", "mcpServers", "hooks")):
        issues.append(
            Issue(
                "error",
                "unexpected_integration",
                ".codex-plugin/plugin.json",
                "public v0.1.0 is skill-only and must not bind apps, MCP servers, or hooks",
            )
        )

    plugins = marketplace.get("plugins", [])
    if not isinstance(plugins, list) or len(plugins) != 1:
        issues.append(Issue("error", "marketplace_plugins", ".agents/plugins/marketplace.json", "marketplace must expose one plugin"))
    else:
        entry = plugins[0]
        if entry.get("name") != manifest.get("name"):
            issues.append(Issue("error", "marketplace_name", ".agents/plugins/marketplace.json", "marketplace plugin name differs"))
        source = entry.get("source", {})
        if source.get("source") != "url" or not str(source.get("url", "")).startswith("https://github.com/"):
            issues.append(Issue("error", "marketplace_source", ".agents/plugins/marketplace.json", "marketplace must use a public Git URL"))
        policy = entry.get("policy", {})
        if policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
            issues.append(Issue("error", "marketplace_policy", ".agents/plugins/marketplace.json", "marketplace policy is incomplete"))

    expected_dirs = {path.name for path in (root / "skills").iterdir() if path.is_dir()} if (root / "skills").is_dir() else set()
    if expected_dirs != set(EXACT_NAMES):
        issues.append(Issue("error", "skill_directories", "skills/", "skill directories must exactly match the catalog"))

    descriptions: set[str] = set()
    for position, skill in enumerate(listed, 1):
        if not isinstance(skill, dict):
            issues.append(Issue("error", "skill_type", "catalog/skills.json", f"skill {position} is not an object"))
            continue
        name = str(skill.get("name", ""))
        missing = sorted(REQUIRED_SKILL_KEYS - set(skill))
        if missing:
            issues.append(Issue("error", "skill_keys", f"catalog:{name}", f"missing fields: {', '.join(missing)}"))
        if skill.get("id") != position:
            issues.append(Issue("error", "skill_id", f"catalog:{name}", "id must match canonical order"))
        if skill.get("maturity") != "instruction-audited" or skill.get("runtime_status") != "host-dependent":
            issues.append(Issue("error", "maturity_label", f"catalog:{name}", "honest maturity labels are required"))
        description = str(skill.get("description", ""))
        if description in descriptions:
            issues.append(Issue("error", "duplicate_description", f"catalog:{name}", "description must be distinct"))
        descriptions.add(description)
        if len(description) < 80 or len(description) > 700:
            issues.append(Issue("warning", "description_length", f"catalog:{name}", "description should be 80–700 characters"))
        if len(skill.get("positive_prompts", [])) < 2:
            issues.append(Issue("error", "positive_examples", f"catalog:{name}", "two positive prompts are required"))

        skill_path = root / "skills" / name / "SKILL.md"
        try:
            metadata, body = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            issues.append(Issue("error", "missing_skill", str(skill_path.relative_to(root)), "SKILL.md is missing"))
            continue
        except FrontmatterError as exc:
            issues.append(Issue("error", "frontmatter", str(skill_path.relative_to(root)), str(exc)))
            continue
        if metadata.get("name") != name:
            issues.append(Issue("error", "frontmatter_name", str(skill_path.relative_to(root)), "frontmatter name differs"))
        if metadata.get("description") != description:
            issues.append(Issue("error", "frontmatter_description", str(skill_path.relative_to(root)), "description differs from catalog"))
        nested = metadata.get("metadata", {})
        if not isinstance(nested, dict):
            issues.append(Issue("error", "frontmatter_metadata", str(skill_path.relative_to(root)), "metadata must be a mapping"))
        else:
            expected_activation = "explicit-only" if skill["explicit_only"] else "contextual"
            for key, expected in {
                "version": "0.1.0",
                "layer": skill["layer"],
                "maturity": "instruction-audited",
                "runtime_status": "host-dependent",
                "activation": expected_activation,
                "risk": skill["risk"],
            }.items():
                if nested.get(key) != expected:
                    issues.append(Issue("error", "frontmatter_value", str(skill_path.relative_to(root)), f"{key} differs from catalog"))
        required_headings = [
            "## Outcome",
            "## Activation boundary",
            "## Required inputs",
            "## Deliverables",
            "## Permissions and approvals",
            "## Workflow",
            "## Stop conditions",
            "## Failure modes to guard against",
            "## Handoffs",
            "## Evidence and honesty",
        ]
        for heading in required_headings:
            if heading not in body:
                issues.append(Issue("error", "skill_heading", str(skill_path.relative_to(root)), f"missing {heading}"))

        openai_path = root / "skills" / name / "agents" / "openai.yaml"
        try:
            openai_text = openai_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            issues.append(Issue("error", "missing_openai_yaml", str(openai_path.relative_to(root)), "metadata file is missing"))
            continue
        if _extract_yaml_scalar(openai_text, "display_name") != skill["display_name"]:
            issues.append(Issue("error", "display_name", str(openai_path.relative_to(root)), "display name differs"))
        if _extract_yaml_scalar(openai_text, "short_description") is None:
            issues.append(Issue("error", "short_description", str(openai_path.relative_to(root)), "short description missing"))
        allows = re.search(r"(?m)^\s*allow_implicit_invocation:\s*(true|false)\s*$", openai_text)
        if skill["explicit_only"]:
            if not allows or allows.group(1) != "false":
                issues.append(Issue("error", "implicit_policy", str(openai_path.relative_to(root)), "explicit-only skill must disable implicit invocation"))
        elif allows and allows.group(1) == "false":
            issues.append(Issue("error", "implicit_policy", str(openai_path.relative_to(root)), "contextual skill must not disable implicit invocation"))

        examples_path = root / "skills" / name / "examples.md"
        try:
            examples_text = examples_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            issues.append(Issue("error", "missing_examples", str(examples_path.relative_to(root)), "examples file is missing"))
            continue
        for prompt in [*skill["positive_prompts"], skill["negative_prompt"]]:
            if prompt not in examples_text:
                issues.append(Issue("error", "example_mismatch", str(examples_path.relative_to(root)), "catalog prompt missing from examples"))

    route_policy = routes.get("default_policy", {})
    if route_policy.get("mode") != "direct-first":
        issues.append(Issue("error", "route_policy", "catalog/routes.json", "direct-first policy is required"))
    if route_policy.get("mission_control_never_implicit") is not True:
        issues.append(Issue("error", "mission_control_policy", "catalog/routes.json", "mission-control must never be implicit"))
    if route_policy.get("handoffs_are_advisory") is not True:
        issues.append(Issue("error", "handoff_policy", "catalog/routes.json", "handoffs must be advisory"))

    edges = routes.get("edges", [])
    if not isinstance(edges, list):
        issues.append(Issue("error", "route_edges", "catalog/routes.json", "edges must be an array"))
        edges = []
    name_set = set(names)
    seen_edges: set[tuple[str, str]] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            issues.append(Issue("error", "route_edge_type", "catalog/routes.json", "edge must be an object"))
            continue
        pair = (edge.get("from"), edge.get("to"))
        if pair[0] not in name_set or pair[1] not in name_set:
            issues.append(Issue("error", "route_reference", "catalog/routes.json", f"unknown skill in edge {pair}"))
        if pair in seen_edges:
            issues.append(Issue("error", "duplicate_edge", "catalog/routes.json", f"duplicate edge {pair}"))
        seen_edges.add(pair)
        if not edge.get("when"):
            issues.append(Issue("error", "route_condition", "catalog/routes.json", f"edge {pair} lacks a condition"))
    if _has_cycle(name_set, edges):
        issues.append(Issue("error", "route_cycle", "catalog/routes.json", "advisory route graph must be acyclic"))

    package_pairs = [
        ("catalog/skills.json", "src/executive_skill_pack/data/skills.json"),
        ("catalog/routes.json", "src/executive_skill_pack/data/routes.json"),
        (".codex-plugin/plugin.json", "src/executive_skill_pack/data/plugin.json"),
    ]
    for left, right in package_pairs:
        if (root / left).is_file() and (root / right).is_file():
            if (root / left).read_bytes() != (root / right).read_bytes():
                issues.append(Issue("error", "packaged_data_drift", right, f"must be byte-identical to {left}"))

    if strict:
        issues = [
            Issue("error", item.code, item.path, item.message)
            if item.severity == "warning"
            else item
            for item in issues
        ]
    return ValidationReport(str(root), tuple(issues))

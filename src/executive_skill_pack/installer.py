from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Iterable

from .catalog import load_catalog, load_routes, skill_map
from .render import render_examples, render_openai_yaml, render_skill_md


@dataclass(frozen=True)
class PlannedFile:
    path: str
    action: str
    sha256: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class InstallPlan:
    target: str
    layout: str
    apply: bool
    replace: bool
    skills: tuple[str, ...]
    files: tuple[PlannedFile, ...]

    @property
    def conflicts(self) -> int:
        return sum(item.action == "conflict" for item in self.files)

    @property
    def changes(self) -> int:
        return sum(item.action in {"create", "replace"} for item in self.files)

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "layout": self.layout,
            "apply": self.apply,
            "replace": self.replace,
            "skills": list(self.skills),
            "conflicts": self.conflicts,
            "changes": self.changes,
            "files": [item.as_dict() for item in self.files],
        }


class InstallError(RuntimeError):
    pass


def _digest(content: str) -> str:
    import hashlib

    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _plugin_manifest() -> str:
    return (
        resources.files("executive_skill_pack")
        .joinpath("data", "plugin.json")
        .read_text(encoding="utf-8")
    )


def _safe_target(target: Path) -> Path:
    resolved = target.expanduser().resolve()
    anchor = Path(resolved.anchor)
    if resolved == anchor:
        raise InstallError("refusing to install into a filesystem root")
    if any(part in {".git", "__pycache__"} for part in resolved.parts):
        raise InstallError("refusing to install inside a control or cache directory")
    return resolved


def _select_skills(names: Iterable[str] | None) -> tuple[dict[str, Any], ...]:
    catalog = load_catalog()
    mapping = skill_map(catalog)
    if names is None:
        return tuple(catalog["skills"])
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in names:
        name = raw.strip()
        if not name or name in seen:
            continue
        if name not in mapping:
            raise InstallError(f"unknown skill: {name}")
        selected.append(mapping[name])
        seen.add(name)
    if not selected:
        raise InstallError("at least one skill must be selected")
    return tuple(selected)


def _payloads(
    target: Path,
    layout: str,
    selected: tuple[dict[str, Any], ...],
) -> dict[Path, str]:
    routes = load_routes()
    edges = routes["edges"]
    payloads: dict[Path, str] = {}

    if layout == "plugin":
        root = target
        payloads[root / ".codex-plugin" / "plugin.json"] = _plugin_manifest()
        skills_root = root / "skills"
    elif layout == "repo-skills":
        skills_root = target / ".agents" / "skills"
    else:
        raise InstallError(f"unsupported layout: {layout}")

    for skill in selected:
        base = skills_root / skill["name"]
        payloads[base / "SKILL.md"] = render_skill_md(skill, edges)
        payloads[base / "agents" / "openai.yaml"] = render_openai_yaml(skill)
        payloads[base / "examples.md"] = render_examples(skill)
    return payloads


def plan_install(
    target: Path,
    *,
    layout: str,
    names: Iterable[str] | None = None,
    apply: bool = False,
    replace: bool = False,
) -> InstallPlan:
    resolved = _safe_target(target)
    selected = _select_skills(names)
    payloads = _payloads(resolved, layout, selected)
    planned: list[PlannedFile] = []

    for path in sorted(payloads, key=lambda item: item.as_posix()):
        content = payloads[path]
        if not path.exists():
            action = "create"
        elif path.is_dir():
            action = "conflict"
        else:
            current = path.read_text(encoding="utf-8")
            if current == content:
                action = "unchanged"
            elif replace:
                action = "replace"
            else:
                action = "conflict"
        planned.append(
            PlannedFile(
                path=str(path),
                action=action,
                sha256=_digest(content),
            )
        )

    plan = InstallPlan(
        target=str(resolved),
        layout=layout,
        apply=apply,
        replace=replace,
        skills=tuple(skill["name"] for skill in selected),
        files=tuple(planned),
    )

    if apply:
        if plan.conflicts:
            raise InstallError(
                f"installation has {plan.conflicts} conflict(s); preview, choose a new target, "
                "or pass --replace for intentional replacement"
            )
        for path, content in sorted(payloads.items(), key=lambda item: item[0].as_posix()):
            if path.exists() and path.read_text(encoding="utf-8") == content:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(
                prefix=f".{path.name}.",
                suffix=".tmp",
                dir=path.parent,
                text=True,
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                    handle.write(content)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, path)
            except Exception:
                try:
                    os.unlink(temporary)
                except FileNotFoundError:
                    pass
                raise
    return plan

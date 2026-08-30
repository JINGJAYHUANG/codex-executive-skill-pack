from __future__ import annotations

import hashlib
import json
import os
from importlib import resources
from pathlib import Path
from typing import Any

CATALOG_GLOB = "skills-*.json"


def _repo_catalog_root(root: Path | None = None) -> Path | None:
    candidates: list[Path] = []
    if root is not None:
        candidates.append(root)
    env_root = os.environ.get("CESP_REPO_ROOT")
    if env_root:
        candidates.append(Path(env_root))
    candidates.extend([Path.cwd(), Path(__file__).resolve().parents[2]])
    for candidate in candidates:
        catalog = candidate.resolve() / "catalog"
        if catalog.is_dir() and list(catalog.glob(CATALOG_GLOB)):
            return catalog
    return None


def _load_repo_catalog(catalog_root: Path) -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    for path in sorted(catalog_root.glob(CATALOG_GLOB)):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError(f"{path} must contain a JSON array")
        skills.extend(payload)
    return skills


def _load_packaged_catalog() -> list[dict[str, Any]]:
    data_path = resources.files(__package__).joinpath("data/skills.json")
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("packaged skill catalog must be a JSON array")
    return payload


def load_skills(root: Path | str | None = None) -> list[dict[str, Any]]:
    resolved = Path(root) if root is not None else None
    catalog_root = _repo_catalog_root(resolved)
    skills = _load_repo_catalog(catalog_root) if catalog_root else _load_packaged_catalog()
    return sorted(skills, key=lambda item: item["name"])


def skill_map(root: Path | str | None = None) -> dict[str, dict[str, Any]]:
    return {skill["name"]: skill for skill in load_skills(root)}


def canonical_catalog_bytes(root: Path | str | None = None) -> bytes:
    return (json.dumps(load_skills(root), sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def catalog_sha256(root: Path | str | None = None) -> str:
    return hashlib.sha256(canonical_catalog_bytes(root)).hexdigest()

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any


def _load_packaged_json(filename: str) -> dict[str, Any]:
    text = (
        resources.files("executive_skill_pack")
        .joinpath("data", filename)
        .read_text(encoding="utf-8")
    )
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError(f"{filename} must contain a JSON object")
    return value


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, Any]:
    """Load the immutable packaged catalog."""
    return _load_packaged_json("skills.json")


@lru_cache(maxsize=1)
def load_routes() -> dict[str, Any]:
    """Load the immutable packaged route graph."""
    return _load_packaged_json("routes.json")


def load_repository_json(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative} must contain a JSON object")
    return value


def skill_map(catalog: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    data = catalog or load_catalog()
    return {item["name"]: item for item in data["skills"]}

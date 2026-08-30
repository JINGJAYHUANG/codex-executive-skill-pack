from __future__ import annotations

import json
from typing import Any


class FrontmatterError(ValueError):
    pass


def _value(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return ""
    if raw in {"true", "false"}:
        return raw == "true"
    if raw.startswith(('"', "'")):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise FrontmatterError(f"invalid quoted value: {raw}") from exc
    return raw


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse the small YAML subset used by this repository.

    The public pack intentionally uses scalar top-level fields and one scalar
    metadata mapping so validation does not require a YAML runtime dependency.
    """
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise FrontmatterError("file must start with a YAML frontmatter delimiter")
    try:
        end = normalized.index("\n---\n", 4)
    except ValueError as exc:
        raise FrontmatterError("closing YAML frontmatter delimiter is missing") from exc

    header = normalized[4:end].splitlines()
    body = normalized[end + 5 :]
    result: dict[str, Any] = {}
    current_mapping: dict[str, Any] | None = None

    for line_number, line in enumerate(header, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  "):
            if current_mapping is None:
                raise FrontmatterError(
                    f"line {line_number}: nested key has no parent mapping"
                )
            child = line.strip()
            if ":" not in child:
                raise FrontmatterError(f"line {line_number}: expected key: value")
            key, raw = child.split(":", 1)
            current_mapping[key.strip()] = _value(raw)
            continue
        if line.startswith((" ", "\t")):
            raise FrontmatterError(f"line {line_number}: unsupported indentation")
        if ":" not in line:
            raise FrontmatterError(f"line {line_number}: expected key: value")
        key, raw = line.split(":", 1)
        key = key.strip()
        raw = raw.strip()
        if raw:
            result[key] = _value(raw)
            current_mapping = None
        else:
            mapping: dict[str, Any] = {}
            result[key] = mapping
            current_mapping = mapping
    return result, body

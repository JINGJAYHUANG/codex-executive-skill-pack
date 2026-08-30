#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def render(root: Path) -> str:
    catalog = json.loads((root / "catalog/skills.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "catalog/routes.json").read_text(encoding="utf-8"))
    outgoing: dict[str, list[dict[str, str]]] = {
        item["name"]: [] for item in catalog["skills"]
    }
    for edge in routes["edges"]:
        outgoing[edge["from"]].append(edge)

    lines = [
        "# Skill Reference",
        "",
        "> Generated from `catalog/skills.json` and `catalog/routes.json`. "
        "Run `python scripts/generate_reference.py --check` before committing.",
        "",
        "All skills are **instruction-audited** and **host-dependent**. "
        "This catalog does not certify production integrations.",
        "",
    ]
    current = None
    for skill in catalog["skills"]:
        if skill["layer"] != current:
            current = skill["layer"]
            label = next(layer["label"] for layer in catalog["layers"] if layer["id"] == current)
            lines.extend([f"## {label}", ""])
        activation = "explicit-only" if skill["explicit_only"] else "contextual"
        lines.extend(
            [
                f"### {skill['id']:02d}. `{skill['name']}`",
                "",
                f"**Purpose:** {skill['purpose']}",
                "",
                f"**Activation:** {activation} · **Risk:** {skill['risk']} · "
                f"**Runtime:** {skill['runtime_status']}",
                "",
                "**Permissions:** " + ", ".join(f"`{item}`" for item in skill["permissions"]),
                "",
            ]
        )
        if outgoing[skill["name"]]:
            lines.append("**Advisory handoffs:**")
            lines.append("")
            for edge in outgoing[skill["name"]]:
                lines.append(f"- `{edge['to']}` — {edge['when']}")
            lines.append("")
        else:
            lines.extend(["**Advisory handoffs:** none.", ""])
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    destination = root / "docs/skill-reference.md"
    expected = render(root)
    if args.check:
        try:
            actual = destination.read_text(encoding="utf-8")
        except FileNotFoundError:
            print("docs/skill-reference.md is missing", file=sys.stderr)
            return 1
        if actual != expected:
            print("docs/skill-reference.md is stale", file=sys.stderr)
            return 1
        print("skill reference is current")
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(expected, encoding="utf-8", newline="\n")
    print(f"wrote {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    failures: list[str] = []
    checked = 0

    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        checked += 1
        if "\t" in text:
            failures.append(f"{path.relative_to(root)}: tab character")
        if re.search(r"(?im)^\s*(TODO|TBD)(?:\s|:|$)", text):
            failures.append(f"{path.relative_to(root)}: unresolved TODO/TBD")
        for target in LINK.findall(text):
            target = target.split("#", 1)[0]
            if not target or target.startswith(SKIP_PREFIXES):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                failures.append(f"{path.relative_to(root)}: link escapes repository: {target}")
                continue
            if not candidate.exists():
                failures.append(f"{path.relative_to(root)}: broken link: {target}")

    if failures:
        print(f"documentation check failed: {len(failures)} issue(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"documentation check passed: {checked} Markdown file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

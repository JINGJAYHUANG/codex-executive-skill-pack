#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
    ".pytest_cache",
    ".mypy_cache",
}
TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".cff",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".rst",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh(?:p|o|u|s|r)_[A-Za-z0-9]{30,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{30,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "webhook_secret": re.compile(r"https://hooks\.[^\s/]+/services/[A-Za-z0-9/_-]{20,}"),
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "windows_home": re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+"),
    "mac_home": re.compile(r"(?<![\\w.-])/" + r"Users/[^/\\s]+"),
    "linux_home": re.compile(r"(?<![\\w.-])/" + r"home/[^/\\s]+"),
}
FORBIDDEN_MARKERS = {
    "private_production_repository": "goal49" + "-cloud-morning",
    "private_incubator_repository": "JINGJAYHUANG/" + "try",
    "local_username_marker": "h14" + "19",
}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    line: int
    excerpt: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        yield path, text


def scan(root: Path) -> tuple[int, list[Finding]]:
    root = root.resolve()
    findings: list[Finding] = []
    scanned = 0
    for path, text in iter_text_files(root):
        scanned += 1
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(text.splitlines(), 1):
            for code, pattern in PATTERNS.items():
                match = pattern.search(line)
                if match:
                    findings.append(
                        Finding(code, relative, number, match.group(0)[:120])
                    )
            for code, marker in FORBIDDEN_MARKERS.items():
                if marker in line:
                    findings.append(Finding(code, relative, number, marker))
    return scanned, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan the public tree for common secrets, PII, and private-project markers.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    scanned, findings = scan(Path(args.root))
    payload = {
        "ok": not findings,
        "scanned_files": scanned,
        "findings": [item.as_dict() for item in findings],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        if findings:
            print(f"public audit failed: {len(findings)} finding(s) in {scanned} text file(s)")
            for item in findings:
                print(f"{item.code} {item.path}:{item.line} {item.excerpt}")
        else:
            print(f"public audit passed: {scanned} text file(s) scanned")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())

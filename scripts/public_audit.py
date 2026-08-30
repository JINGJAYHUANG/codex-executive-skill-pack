#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".py", ".txt", ".cff", ".in"}
SKIP_PARTS = {".git", ".venv", "build", "dist", "__pycache__", ".pytest_cache", "htmlcov"}
ALLOW_EMAILS = {"41898282+github-actions[bot]@users.noreply.github.com"}
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer_token": re.compile(r"(?i)authorization\s*[:=]\s*bearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "windows_user_path": re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+"),
    "mac_user_path": re.compile(r"/Users/[^/\s]+"),
    "linux_user_path": re.compile(r"/home/[^/\s]+"),
    "known_private_marker": re.compile(r"(?i)h1419|goal49-cloud-morning|tushare_token|feishu_webhook"),
}
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name in {"LICENSE", "Makefile"} or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def audit(root: Path) -> list[str]:
    findings: list[str] = []
    scanned = 0
    for path in iter_text_files(root):
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"non_utf8:{path.relative_to(root)}")
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}:{path.relative_to(root)}")
        for email in EMAIL_RE.findall(text):
            if email.lower() not in {value.lower() for value in ALLOW_EMAILS}:
                findings.append(f"email:{path.relative_to(root)}:{email}")
        if "production validated" in text.lower() or "guaranteed autonomous" in text.lower():
            findings.append(f"maturity_overclaim:{path.relative_to(root)}")
    if not findings:
        print(f"public audit passed: {scanned} text files scanned")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    findings = audit(Path(args.root).resolve())
    if findings:
        print("\n".join(findings))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

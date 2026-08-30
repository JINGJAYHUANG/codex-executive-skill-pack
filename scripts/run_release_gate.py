#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from executive_skill_pack.evaluator import evaluate_routing
from executive_skill_pack.validator import validate_repository


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = validate_repository(root, strict=True)
    if not report.ok:
        for issue in report.issues:
            print(f"{issue.severity.upper()} {issue.code} {issue.path}: {issue.message}")
        return 1
    evaluation = evaluate_routing(root)
    if not evaluation.ok:
        for result in evaluation.results:
            if not result.passed:
                print(f"FAIL {result.case_id}: {result.note}")
        return 1
    commands = [
        [sys.executable, "scripts/generate_reference.py", "--root", ".", "--check"],
        [sys.executable, "scripts/check_docs.py", "--root", "."],
        [sys.executable, "scripts/public_audit.py", "."],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    ]
    for command in commands:
        subprocess.run(command, cwd=root, check=True)
    print("release gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

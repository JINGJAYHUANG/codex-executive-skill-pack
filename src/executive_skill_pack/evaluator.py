from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .catalog import load_repository_json
from .router import route_prompt


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    selected: str | None
    status: str
    expected: str | None
    forbidden: str | None
    note: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvaluationReport:
    total: int
    passed: int
    failed: int
    results: tuple[CaseResult, ...]

    @property
    def ok(self) -> bool:
        return self.failed == 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "results": [item.as_dict() for item in self.results],
        }


def load_routing_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"line {line_number}: case must be an object")
        cases.append(value)
    return cases


def evaluate_routing(root: Path) -> EvaluationReport:
    catalog = load_repository_json(root, "catalog/skills.json")
    cases = load_routing_cases(root / "evals/routing_cases.jsonl")
    results: list[CaseResult] = []
    for case in cases:
        result = route_prompt(case["prompt"], catalog=catalog)
        expected = case.get("expected")
        forbidden = case.get("forbidden")
        passed = True
        note = ""
        if expected is not None and result.selected != expected:
            passed = False
            note = f"expected {expected}, got {result.selected!r}"
        if forbidden is not None and result.selected == forbidden:
            passed = False
            note = f"forbidden route {forbidden} was selected"
        if case.get("expected_status") and result.status != case["expected_status"]:
            passed = False
            note = f"expected status {case['expected_status']}, got {result.status}"
        results.append(
            CaseResult(
                case_id=case["id"],
                passed=passed,
                selected=result.selected,
                status=result.status,
                expected=expected,
                forbidden=forbidden,
                note=note,
            )
        )
    passed_count = sum(item.passed for item in results)
    return EvaluationReport(
        total=len(results),
        passed=passed_count,
        failed=len(results) - passed_count,
        results=tuple(results),
    )

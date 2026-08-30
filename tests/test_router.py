from __future__ import annotations

import json
import unittest
from pathlib import Path

from codex_executive_skill_pack.router import route

ROOT = Path(__file__).resolve().parents[1]


def load_composites() -> list[dict]:
    path = ROOT / "evals/routing_cases.jsonl"
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and json.loads(line).get("kind") == "composite"
    ]


class RouterTests(unittest.TestCase):
    def test_explicit_auto_skill_routes(self) -> None:
        decision = route("$decision-memo-engine compare these options", root=str(ROOT))
        self.assertEqual(decision.selected, "decision-memo-engine")
        self.assertEqual(decision.disposition, "route")

    def test_natural_explicit_first_skill_is_only_suggested(self) -> None:
        decision = route("Please reorganize these files safely", root=str(ROOT))
        self.assertEqual(decision.selected, "fileops-guardian")
        self.assertEqual(decision.disposition, "suggest_explicit")
        self.assertTrue(decision.requires_explicit_invocation)

    def test_explicit_high_impact_skill_routes(self) -> None:
        decision = route("$fileops-guardian preview a safe rename plan", root=str(ROOT))
        self.assertEqual(decision.selected, "fileops-guardian")
        self.assertEqual(decision.disposition, "route")

    def test_empty_request_has_no_route(self) -> None:
        self.assertEqual(route("   ", root=str(ROOT)).disposition, "no_route")

    def test_unknown_request_has_no_route(self) -> None:
        self.assertEqual(route("Recite a short poem about rain", root=str(ROOT)).selected, None)

    def test_routing_is_deterministic(self) -> None:
        first = route("Write a decision memo comparing these options", root=str(ROOT)).to_dict()
        second = route("Write a decision memo comparing these options", root=str(ROOT)).to_dict()
        self.assertEqual(first, second)

    def test_candidate_limit_is_respected(self) -> None:
        decision = route("Collect public web evidence and compare the latest version", root=str(ROOT), limit=2)
        self.assertLessEqual(len(decision.candidates), 2)

    def test_decision_is_json_serializable(self) -> None:
        json.dumps(route("Design an experiment for this hypothesis", root=str(ROOT)).to_dict())

    def test_single_specialist_beats_mission_control(self) -> None:
        decision = route("Build a knowledge graph linking claims and sources", root=str(ROOT))
        self.assertEqual(decision.selected, "knowledge-graph-builder")

    def test_natural_mission_control_requires_explicit_invocation(self) -> None:
        decision = route("Coordinate this multi-step mission across several specialists", root=str(ROOT))
        self.assertEqual(decision.selected, "mission-control")
        self.assertEqual(decision.disposition, "suggest_explicit")


def _make_composite_test(case: dict):
    def test(self: RouterTests) -> None:
        decision = route(case["request"], root=str(ROOT))
        if case.get("expected") is not None:
            self.assertEqual(decision.selected, case["expected"])
        if case.get("disposition") is not None:
            self.assertEqual(decision.disposition, case["disposition"])
        if case.get("must_not_select") is not None:
            self.assertNotEqual(decision.selected, case["must_not_select"])
    return test


for _case in load_composites():
    setattr(RouterTests, f"test_{_case['id'].replace('-', '_')}", _make_composite_test(_case))


if __name__ == "__main__":
    unittest.main()

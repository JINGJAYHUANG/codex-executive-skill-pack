from __future__ import annotations

import copy
import json
import unittest

from executive_skill_pack.catalog import load_catalog
from executive_skill_pack.evaluator import evaluate_routing, load_routing_cases
from executive_skill_pack.router import route_prompt
from executive_skill_pack.validator import EXPLICIT_ONLY

from helpers import ROOT


class RouterTests(unittest.TestCase):
    def test_all_positive_prompts_route_to_expected_skill(self):
        for skill in load_catalog()["skills"]:
            for prompt in skill["positive_prompts"]:
                with self.subTest(skill=skill["name"], prompt=prompt):
                    result = route_prompt(prompt)
                    self.assertEqual(result.selected, skill["name"], result.as_dict())
                    self.assertEqual(result.status, "skill")

    def test_explicit_name_wins(self):
        result = route_prompt(
            "$mission-control coordinate research and implementation with gates."
        )
        self.assertEqual(result.selected, "mission-control")
        self.assertTrue(result.candidates[0].explicit)
        self.assertGreaterEqual(result.candidates[0].score, 100)

    def test_mission_control_is_never_implicit(self):
        result = route_prompt("Coordinate these skills across a multi-stage project.")
        self.assertNotEqual(result.selected, "mission-control")

    def test_all_explicit_only_skills_are_suppressed_without_name(self):
        cases = {
            "screen-macro-recorder": "Turn an authorized screen recording into a macro.",
            "desktop-pilot": "Operate the desktop app and click the final button.",
            "api-bridge-builder": "Build an API adapter for this service.",
            "fileops-guardian": "Reorganize all files in this folder.",
            "workflow-compiler": "Turn this SOP into an automated workflow.",
            "mission-control": "Coordinate multiple specialists.",
            "automation-self-healer": "Repair this failed scheduled job.",
            "inbox-negotiator": "Analyze the email negotiation and draft a reply.",
            "personal-coo": "Coordinate these work and study commitments.",
        }
        self.assertEqual(set(cases), EXPLICIT_ONLY)
        for name, prompt in cases.items():
            with self.subTest(name=name):
                self.assertNotEqual(route_prompt(prompt).selected, name)

    def test_direct_response_for_simple_summary(self):
        result = route_prompt(
            "Summarize the article pasted below without searching elsewhere."
        )
        self.assertIsNone(result.selected)
        self.assertEqual(result.status, "direct")

    def test_unknown_prompt_is_direct(self):
        result = route_prompt("Give me three names for a fictional coffee shop.")
        self.assertIsNone(result.selected)
        self.assertEqual(result.status, "direct")

    def test_result_is_json_serializable(self):
        result = route_prompt(
            "Build a competitor radar for these vendors using public evidence."
        )
        json.dumps(result.as_dict())

    def test_minimum_score_can_be_raised(self):
        result = route_prompt(
            "Build a competitor radar for these vendors using public evidence.",
            minimum_score=1000,
        )
        self.assertIsNone(result.selected)

    def test_catalog_default_threshold_is_respected(self):
        catalog = copy.deepcopy(load_catalog())
        catalog["pack"]["routing_minimum_score"] = 1000
        result = route_prompt(
            "Build a competitor radar for these vendors using public evidence.",
            catalog=catalog,
        )
        self.assertIsNone(result.selected)
        self.assertEqual(result.status, "direct")
        self.assertEqual(result.minimum_score, 1000)

    def test_explicit_invocation_bypasses_implicit_threshold(self):
        result = route_prompt(
            "$mission-control coordinate research and implementation with gates.",
            minimum_score=1000,
        )
        self.assertEqual(result.selected, "mission-control")
        self.assertEqual(result.status, "skill")
        self.assertTrue(result.candidates[0].explicit)

    def test_invalid_thresholds_are_rejected(self):
        for value in (-1, True, "6"):
            catalog = copy.deepcopy(load_catalog())
            catalog["pack"]["routing_minimum_score"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                route_prompt("Build a competitor radar.", catalog=catalog)


class EvaluationTests(unittest.TestCase):
    def test_case_count(self):
        cases = load_routing_cases(ROOT / "evals/routing_cases.jsonl")
        self.assertEqual(len(cases), 74)

    def test_full_routing_evaluation_passes(self):
        report = evaluate_routing(ROOT)
        self.assertTrue(report.ok, report.as_dict())
        self.assertEqual(report.passed, 74)
        self.assertEqual(report.failed, 0)

    def test_policy_fixture_records_exact_set(self):
        policy = json.loads((ROOT / "evals/policy_cases.json").read_text())
        explicit = next(
            item["expected"]
            for item in policy["assertions"]
            if item["id"] == "explicit-only-set"
        )
        self.assertEqual(set(explicit), EXPLICIT_ONLY)


if __name__ == "__main__":
    unittest.main()

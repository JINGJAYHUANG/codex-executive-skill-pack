from __future__ import annotations

import json
import unittest
from collections import Counter

from executive_skill_pack.catalog import load_catalog, load_routes
from executive_skill_pack.frontmatter import FrontmatterError, parse_frontmatter
from executive_skill_pack.validator import EXACT_NAMES, EXPLICIT_ONLY, validate_repository

from helpers import ROOT


class CatalogTests(unittest.TestCase):
    def test_exact_names_and_order(self):
        self.assertEqual([item["name"] for item in load_catalog()["skills"]], EXACT_NAMES)

    def test_exact_skill_count(self):
        self.assertEqual(len(load_catalog()["skills"]), 20)

    def test_names_are_unique(self):
        names = [item["name"] for item in load_catalog()["skills"]]
        self.assertEqual(len(names), len(set(names)))

    def test_layer_counts(self):
        counts = Counter(item["layer"] for item in load_catalog()["skills"])
        self.assertEqual(
            counts,
            {
                "intelligence": 4,
                "engineering-execution": 6,
                "decision-learning": 5,
                "orchestration-operations": 5,
            },
        )

    def test_explicit_only_set(self):
        explicit = {
            item["name"] for item in load_catalog()["skills"] if item["explicit_only"]
        }
        self.assertEqual(explicit, EXPLICIT_ONLY)
        self.assertEqual(len(explicit), 9)

    def test_honest_maturity_labels(self):
        for item in load_catalog()["skills"]:
            with self.subTest(item=item["name"]):
                self.assertEqual(item["maturity"], "instruction-audited")
                self.assertEqual(item["runtime_status"], "host-dependent")

    def test_versions_and_default_threshold_are_well_formed(self):
        catalog = load_catalog()
        self.assertRegex(catalog["pack"]["version"], r"^\d+\.\d+\.\d+")
        self.assertIsInstance(catalog["pack"]["routing_minimum_score"], int)
        self.assertGreaterEqual(catalog["pack"]["routing_minimum_score"], 0)
        for item in catalog["skills"]:
            with self.subTest(name=item["name"]):
                self.assertRegex(item["version"], r"^\d+\.\d+\.\d+")

    def test_descriptions_are_unique(self):
        descriptions = [item["description"] for item in load_catalog()["skills"]]
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_route_graph_references_known_skills(self):
        names = set(EXACT_NAMES)
        for edge in load_routes()["edges"]:
            with self.subTest(edge=edge):
                self.assertIn(edge["from"], names)
                self.assertIn(edge["to"], names)
                self.assertNotEqual(edge["from"], edge["to"])

    def test_route_graph_is_acyclic(self):
        names = set(EXACT_NAMES)
        graph = {name: [] for name in names}
        indegree = {name: 0 for name in names}
        for edge in load_routes()["edges"]:
            graph[edge["from"]].append(edge["to"])
            indegree[edge["to"]] += 1
        queue = [name for name, degree in indegree.items() if degree == 0]
        visited = 0
        while queue:
            node = queue.pop()
            visited += 1
            for target in graph[node]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
        self.assertEqual(visited, len(names))

    def test_plugin_manifest_is_skill_only(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "codex-executive-skill-pack")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertFalse({"apps", "mcpServers", "hooks"} & set(manifest))

    def test_marketplace_exposes_one_public_plugin(self):
        marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text()
        )
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "codex-executive-skill-pack")
        self.assertEqual(entry["source"]["source"], "url")
        self.assertTrue(entry["source"]["url"].startswith("https://github.com/"))

    def test_packaged_data_matches_repository(self):
        pairs = [
            ("catalog/skills.json", "src/executive_skill_pack/data/skills.json"),
            ("catalog/routes.json", "src/executive_skill_pack/data/routes.json"),
            (".codex-plugin/plugin.json", "src/executive_skill_pack/data/plugin.json"),
        ]
        for left, right in pairs:
            with self.subTest(left=left):
                self.assertEqual((ROOT / left).read_bytes(), (ROOT / right).read_bytes())


class SkillFileTests(unittest.TestCase):
    def test_every_skill_has_required_files(self):
        for name in EXACT_NAMES:
            with self.subTest(name=name):
                self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file())
                self.assertTrue(
                    (ROOT / "skills" / name / "agents" / "openai.yaml").is_file()
                )
                self.assertTrue((ROOT / "skills" / name / "examples.md").is_file())

    def test_frontmatter_matches_catalog(self):
        mapping = {item["name"]: item for item in load_catalog()["skills"]}
        for name in EXACT_NAMES:
            metadata, body = parse_frontmatter(
                (ROOT / "skills" / name / "SKILL.md").read_text()
            )
            with self.subTest(name=name):
                self.assertEqual(metadata["name"], name)
                self.assertEqual(metadata["description"], mapping[name]["description"])
                self.assertEqual(metadata["metadata"]["version"], mapping[name]["version"])
                self.assertIn("## Stop conditions", body)
                self.assertIn("## Evidence and honesty", body)

    def test_explicit_skills_disable_implicit_invocation(self):
        for name in EXACT_NAMES:
            text = (
                ROOT / "skills" / name / "agents" / "openai.yaml"
            ).read_text()
            with self.subTest(name=name):
                if name in EXPLICIT_ONLY:
                    self.assertIn("allow_implicit_invocation: false", text)
                else:
                    self.assertNotIn("allow_implicit_invocation: false", text)

    def test_examples_match_catalog(self):
        for skill in load_catalog()["skills"]:
            text = (ROOT / "skills" / skill["name"] / "examples.md").read_text()
            with self.subTest(name=skill["name"]):
                for prompt in [
                    *skill["positive_prompts"],
                    skill["negative_prompt"],
                ]:
                    self.assertIn(prompt, text)

    def test_frontmatter_rejects_missing_delimiter(self):
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("name: bad\n")


class ValidatorTests(unittest.TestCase):
    def test_strict_repository_validation_passes(self):
        report = validate_repository(ROOT, strict=True)
        self.assertTrue(report.ok, report.as_dict())
        self.assertEqual(report.errors, 0)
        self.assertEqual(report.warnings, 0)


if __name__ == "__main__":
    unittest.main()

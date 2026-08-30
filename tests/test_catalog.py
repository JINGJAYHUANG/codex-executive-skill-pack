from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from codex_executive_skill_pack.catalog import catalog_sha256, load_skills

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skills = load_skills(ROOT)
        cls.by_name = {skill["name"]: skill for skill in cls.skills}

    def test_exactly_twenty_skills(self) -> None:
        self.assertEqual(len(self.skills), 20)

    def test_names_are_unique(self) -> None:
        self.assertEqual(len(self.by_name), len(self.skills))

    def test_exactly_nine_explicit_first_skills(self) -> None:
        self.assertEqual(sum(skill["invocation"] == "explicit_first" for skill in self.skills), 9)

    def test_all_routes_resolve(self) -> None:
        names = set(self.by_name)
        for skill in self.skills:
            with self.subTest(skill=skill["name"]):
                self.assertNotIn(skill["name"], skill["routes_to"])
                self.assertTrue(set(skill["routes_to"]).issubset(names))

    def test_plugin_manifest_points_to_skills(self) -> None:
        plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["name"], "codex-executive-skill-pack")
        self.assertEqual(plugin["version"], "0.1.0")
        self.assertEqual(plugin["skills"], "./skills/")

    def test_catalog_hash_is_deterministic(self) -> None:
        self.assertEqual(catalog_sha256(ROOT), catalog_sha256(ROOT))
        self.assertRegex(catalog_sha256(ROOT), r"^[0-9a-f]{64}$")

    def test_all_statuses_are_spec_validated(self) -> None:
        self.assertEqual({skill["status"] for skill in self.skills}, {"spec_validated"})

    def test_expected_categories_are_represented(self) -> None:
        categories = {skill["category"] for skill in self.skills}
        self.assertTrue({"intelligence", "builders", "orchestration", "decision", "knowledge", "execution"}.issubset(categories))


def _make_contract_test(skill_name: str):
    def test(self: CatalogTests) -> None:
        skill = self.by_name[skill_name]
        self.assertRegex(skill["name"], NAME_RE)
        self.assertGreaterEqual(len(skill["triggers"]), 3)
        self.assertGreaterEqual(len(skill["avoid_when"]), 2)
        self.assertGreaterEqual(len(skill["workflow"]), 4)
        self.assertGreaterEqual(len(skill["output_contract"]), 3)
        self.assertEqual(skill["positive_example"]["expected"], skill_name)
        self.assertTrue(skill["negative_example"]["reason"])
        self.assertIn(skill["risk"], {"low", "medium", "high"})
    return test


for _skill in load_skills(ROOT):
    setattr(CatalogTests, f"test_contract_{_skill['name'].replace('-', '_')}", _make_contract_test(_skill["name"]))


if __name__ == "__main__":
    unittest.main()

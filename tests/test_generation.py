from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/generate_skill_files.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("skill_generator", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()

    def test_generated_files_are_current(self) -> None:
        self.assertEqual(self.generator.check_files(ROOT), [])

    def test_manifest_counts_match_contract(self) -> None:
        manifest = json.loads((ROOT / "catalog/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["skill_count"], 20)
        self.assertEqual(manifest["explicit_first_count"], 9)
        self.assertEqual(manifest["routing_case_count"], 74)
        self.assertRegex(manifest["catalog_sha256"], r"^[0-9a-f]{64}$")

    def test_every_skill_has_interface_metadata(self) -> None:
        skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
        interfaces = sorted((ROOT / "skills").glob("*/agents/openai.yaml"))
        self.assertEqual(len(skill_files), 20)
        self.assertEqual(len(interfaces), 20)
        for path in interfaces:
            text = path.read_text(encoding="utf-8")
            self.assertIn("interface:", text)
            self.assertIn("display_name:", text)
            self.assertIn("short_description:", text)

    def test_packaged_catalog_matches_source_catalog(self) -> None:
        packaged = json.loads((ROOT / "src/codex_executive_skill_pack/data/skills.json").read_text(encoding="utf-8"))
        self.assertEqual(packaged, self.generator.load_skills(ROOT))


if __name__ == "__main__":
    unittest.main()

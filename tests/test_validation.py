from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from codex_executive_skill_pack.validation import summary, validate_catalog

ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def test_repository_validation_passes(self) -> None:
        payload = summary(ROOT)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["errors"], 0)

    def test_validation_without_generated_surface_passes(self) -> None:
        self.assertFalse(any(item.level == "error" for item in validate_catalog(ROOT, check_generated=False)))

    def test_missing_plugin_manifest_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copytree(ROOT / "catalog", target / "catalog")
            findings = validate_catalog(target, check_generated=False)
            self.assertIn("plugin_manifest_missing", {item.code for item in findings})

    def test_unknown_route_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copytree(ROOT / "catalog", target / "catalog")
            shutil.copytree(ROOT / ".codex-plugin", target / ".codex-plugin")
            path = target / "catalog/skills-intelligence.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload[0]["routes_to"].append("missing-skill")
            path.write_text(json.dumps(payload), encoding="utf-8")
            findings = validate_catalog(target, check_generated=False)
            self.assertIn("unknown_route", {item.code for item in findings})

    def test_duplicate_name_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copytree(ROOT / "catalog", target / "catalog")
            shutil.copytree(ROOT / ".codex-plugin", target / ".codex-plugin")
            path = target / "catalog/skills-execution.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload[0]["name"] = "web-intel-harvester"
            path.write_text(json.dumps(payload), encoding="utf-8")
            findings = validate_catalog(target, check_generated=False)
            self.assertIn("duplicate_name", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()

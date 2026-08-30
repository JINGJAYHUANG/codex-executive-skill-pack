from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import ROOT


def load_public_audit_module():
    path = ROOT / "scripts/public_audit.py"
    spec = importlib.util.spec_from_file_location("public_audit_for_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load public audit module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PublicationTests(unittest.TestCase):
    def test_public_audit_passes_repository(self):
        module = load_public_audit_module()
        scanned, findings = module.scan(ROOT)
        self.assertGreater(scanned, 80)
        self.assertEqual(findings, [])

    def test_public_audit_detects_synthetic_secret(self):
        module = load_public_audit_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            synthetic = "gh" + "p_" + ("A" * 36)
            (root / "sample.txt").write_text(synthetic)
            _, findings = module.scan(root)
            self.assertTrue(any(item.code == "github_token" for item in findings))

    def test_public_audit_detects_synthetic_email(self):
        module = load_public_audit_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            synthetic = "name" + "@" + "example" + "." + "org"
            (root / "sample.txt").write_text(synthetic)
            _, findings = module.scan(root)
            self.assertTrue(any(item.code == "email_address" for item in findings))

    def test_generated_reference_is_current(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/generate_reference.py",
                "--root",
                ".",
                "--check",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_documentation_links_are_valid(self):
        result = subprocess.run(
            [sys.executable, "scripts/check_docs.py", "--root", "."],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_json_files_end_with_newline(self):
        for path in [
            ROOT / "catalog/skills.json",
            ROOT / "catalog/routes.json",
            ROOT / "evals/policy_cases.json",
            ROOT / ".codex-plugin/plugin.json",
            ROOT / ".agents/plugins/marketplace.json",
        ]:
            with self.subTest(path=path.name):
                self.assertTrue(path.read_bytes().endswith(b"\n"))

    def test_plugin_version_matches_catalog(self):
        plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        catalog = json.loads((ROOT / "catalog/skills.json").read_text())
        self.assertEqual(plugin["version"], catalog["pack"]["version"])

    def test_release_workflow_is_dynamic_and_main_bound(self):
        text = (ROOT / ".github/workflows/release.yml").read_text()
        self.assertIn("release/v*", text)
        self.assertIn("git rev-parse origin/main", text)
        self.assertIn("sha256sum -c SHA256SUMS.txt", text)
        self.assertIn("gh release upload", text)
        self.assertIn("--clobber", text)
        self.assertIn('len(catalog["skills"])', text)
        self.assertIn("routing_cases = sum(", text)
        self.assertNotIn("Codex Executive Skill Pack v0.1.0", text)

    def test_reproducible_wheel_job_derives_current_version(self):
        text = (ROOT / ".github/workflows/ci.yml").read_text()
        self.assertIn("import tomllib", text)
        self.assertIn(
            'wheel_name="codex_executive_skill_pack-${version}-py3-none-any.whl"',
            text,
        )
        self.assertNotIn("codex_executive_skill_pack-0.1.0", text)

    def test_skill_reference_contains_all_names(self):
        text = (ROOT / "docs/skill-reference.md").read_text()
        catalog = json.loads((ROOT / "catalog/skills.json").read_text())
        for item in catalog["skills"]:
            with self.subTest(name=item["name"]):
                self.assertIn(f"`{item['name']}`", text)


if __name__ == "__main__":
    unittest.main()

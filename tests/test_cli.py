from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from codex_executive_skill_pack.cli import main

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, argv: list[str]) -> tuple[int, str]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(argv)
        return code, stream.getvalue()

    def test_validate_command_passes(self) -> None:
        code, output = self.run_cli(["validate", "--root", str(ROOT)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["status"], "pass")

    def test_list_json_returns_twenty_skills(self) -> None:
        code, output = self.run_cli(["list", "--root", str(ROOT), "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(output)), 20)

    def test_show_rejects_unknown_skill(self) -> None:
        code, _ = self.run_cli(["show", "not-a-skill", "--root", str(ROOT)])
        self.assertEqual(code, 2)

    def test_route_command_returns_json(self) -> None:
        code, output = self.run_cli(["route", "Write a decision memo", "--root", str(ROOT)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["selected"], "decision-memo-engine")

    def test_eval_command_passes_all_cases(self) -> None:
        code, output = self.run_cli(["eval", "--root", str(ROOT)])
        payload = json.loads(output)
        self.assertEqual(code, 0)
        self.assertEqual(payload["cases"], 74)
        self.assertEqual(payload["failed"], 0)

    def test_install_defaults_to_preview(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            code, output = self.run_cli(["install", "--root", str(ROOT), "--target", directory])
            payload = json.loads(output)
            self.assertEqual(code, 0)
            self.assertEqual(payload["mode"], "preview")
            self.assertFalse((Path(directory) / "codex-executive-skill-pack").exists())

    def test_install_apply_copies_only_plugin_surface(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            code, output = self.run_cli(["install", "--root", str(ROOT), "--target", directory, "--apply"])
            destination = Path(json.loads(output)["destination"])
            self.assertEqual(code, 0)
            self.assertTrue((destination / ".codex-plugin/plugin.json").is_file())
            self.assertEqual(len(list((destination / "skills").glob("*/SKILL.md"))), 20)
            self.assertFalse((destination / "catalog").exists())


if __name__ == "__main__":
    unittest.main()

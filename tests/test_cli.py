from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from executive_skill_pack.cli import main

from helpers import ROOT


class CliTests(unittest.TestCase):
    def run_cli(self, argv):
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_validate_command(self):
        code, output, error = self.run_cli(
            ["validate", "--root", str(ROOT), "--strict"]
        )
        self.assertEqual(code, 0, error)
        self.assertIn("validation: PASS", output)

    def test_list_command_has_twenty_rows(self):
        code, output, error = self.run_cli(["list"])
        self.assertEqual(code, 0, error)
        rows = [line for line in output.splitlines() if line[:2].isdigit()]
        self.assertEqual(len(rows), 20)

    def test_layer_filter(self):
        code, output, error = self.run_cli(
            ["list", "--layer", "intelligence"]
        )
        self.assertEqual(code, 0, error)
        rows = [line for line in output.splitlines() if line[:2].isdigit()]
        self.assertEqual(len(rows), 4)

    def test_show_known_skill(self):
        code, output, error = self.run_cli(["show", "mission-control"])
        self.assertEqual(code, 0, error)
        self.assertIn("explicit-only", output)

    def test_show_unknown_skill(self):
        code, output, error = self.run_cli(["show", "unknown-skill"])
        self.assertEqual(code, 2)
        self.assertIn("unknown skill", error)

    def test_route_json(self):
        code, output, error = self.run_cli(
            [
                "route",
                "Write a decision memo comparing these options.",
                "--json",
            ]
        )
        self.assertEqual(code, 0, error)
        payload = json.loads(output)
        self.assertEqual(payload["selected"], "decision-memo-engine")

    def test_eval_command(self):
        code, output, error = self.run_cli(["eval", "--root", str(ROOT)])
        self.assertEqual(code, 0, error)
        self.assertIn("passed=74/74", output)

    def test_catalog_command(self):
        code, output, error = self.run_cli(["catalog", "routes"])
        self.assertEqual(code, 0, error)
        payload = json.loads(output)
        self.assertEqual(payload["default_policy"]["mode"], "direct-first")

    def test_install_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            target.mkdir()
            code, output, error = self.run_cli(
                [
                    "install",
                    "--layout",
                    "repo-skills",
                    "--target",
                    str(target),
                    "--skills",
                    "web-intel-harvester",
                ]
            )
            self.assertEqual(code, 0, error)
            self.assertIn("PREVIEW", output)
            self.assertFalse((target / ".agents").exists())


if __name__ == "__main__":
    unittest.main()

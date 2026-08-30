from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/public_audit.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("public_audit", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit_module = load_audit_module()

    def test_public_repository_passes(self) -> None:
        self.assertEqual(self.audit_module.audit(ROOT), [])

    def test_email_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.md"
            path.write_text("contact: person@example.com", encoding="utf-8")
            self.assertTrue(any(item.startswith("email:") for item in self.audit_module.audit(Path(directory))))

    def test_user_path_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.md"
            path.write_text("C:\\Users\\private-user\\project", encoding="utf-8")
            self.assertTrue(any(item.startswith("windows_user_path:") for item in self.audit_module.audit(Path(directory))))

    def test_token_shape_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456", encoding="utf-8")
            self.assertTrue(any(item.startswith("github_token:") for item in self.audit_module.audit(Path(directory))))


if __name__ == "__main__":
    unittest.main()

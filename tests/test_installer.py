from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from executive_skill_pack.installer import InstallError, plan_install
from executive_skill_pack.validator import EXACT_NAMES


class InstallerTests(unittest.TestCase):
    def test_preview_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            plan = plan_install(root, layout="repo-skills")
            self.assertGreater(plan.changes, 0)
            self.assertFalse((root / ".agents").exists())

    def test_apply_selected_repo_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            plan = plan_install(
                root,
                layout="repo-skills",
                names=["web-intel-harvester", "decision-memo-engine"],
                apply=True,
            )
            self.assertEqual(plan.skills, (
                "web-intel-harvester",
                "decision-memo-engine",
            ))
            for name in plan.skills:
                self.assertTrue(
                    (root / ".agents" / "skills" / name / "SKILL.md").is_file()
                )

    def test_second_identical_install_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            plan_install(
                root,
                layout="repo-skills",
                names=["web-intel-harvester"],
                apply=True,
            )
            second = plan_install(
                root,
                layout="repo-skills",
                names=["web-intel-harvester"],
            )
            self.assertEqual(second.changes, 0)
            self.assertEqual(second.conflicts, 0)
            self.assertTrue(all(item.action == "unchanged" for item in second.files))

    def test_conflict_blocks_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            target = root / ".agents/skills/web-intel-harvester/SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_text("different\n")
            preview = plan_install(
                root,
                layout="repo-skills",
                names=["web-intel-harvester"],
            )
            self.assertEqual(preview.conflicts, 1)
            with self.assertRaises(InstallError):
                plan_install(
                    root,
                    layout="repo-skills",
                    names=["web-intel-harvester"],
                    apply=True,
                )

    def test_explicit_replace_updates_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            target = root / ".agents/skills/web-intel-harvester/SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_text("different\n")
            plan = plan_install(
                root,
                layout="repo-skills",
                names=["web-intel-harvester"],
                apply=True,
                replace=True,
            )
            self.assertEqual(plan.conflicts, 0)
            self.assertIn("name: web-intel-harvester", target.read_text())

    def test_symlinked_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            outside = Path(tmp) / "outside"
            (root / ".agents").mkdir(parents=True)
            outside.mkdir()
            link = root / ".agents" / "skills"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symbolic links are unavailable: {exc}")
            with self.assertRaises(InstallError):
                plan_install(
                    root,
                    layout="repo-skills",
                    names=["web-intel-harvester"],
                    apply=True,
                )

    def test_symlinked_destination_is_rejected_even_with_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            outside = Path(tmp) / "outside.txt"
            outside.write_text("outside\n")
            target = root / ".agents/skills/web-intel-harvester/SKILL.md"
            target.parent.mkdir(parents=True)
            try:
                target.symlink_to(outside)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symbolic links are unavailable: {exc}")
            with self.assertRaises(InstallError):
                plan_install(
                    root,
                    layout="repo-skills",
                    names=["web-intel-harvester"],
                    apply=True,
                    replace=True,
                )
            self.assertEqual(outside.read_text(), "outside\n")

    def test_plugin_layout_contains_manifest_and_all_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "plugin"
            plan = plan_install(target, layout="plugin", apply=True)
            manifest = json.loads(
                (target / ".codex-plugin/plugin.json").read_text()
            )
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(plan.skills, tuple(EXACT_NAMES))
            self.assertEqual(
                {path.name for path in (target / "skills").iterdir()},
                set(EXACT_NAMES),
            )

    def test_unknown_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(InstallError):
                plan_install(
                    Path(tmp) / "repo",
                    layout="repo-skills",
                    names=["not-a-real-skill"],
                )

    def test_filesystem_root_is_rejected(self):
        with self.assertRaises(InstallError):
            plan_install(Path("/"), layout="repo-skills")

    def test_control_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(InstallError):
                plan_install(Path(tmp) / ".git", layout="repo-skills")

    def test_empty_selection_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(InstallError):
                plan_install(
                    Path(tmp) / "repo",
                    layout="repo-skills",
                    names=["", " "],
                )


if __name__ == "__main__":
    unittest.main()

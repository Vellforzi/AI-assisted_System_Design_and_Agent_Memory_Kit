"""Dependency-free acceptance coverage for the four adoption profiles."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


KIT = Path(__file__).resolve().parents[1]
HARNESS = KIT / "tools/documentation_harness.py"
ADOPTION_PROFILES = KIT / "ADOPTION_PROFILES.md"
sys.path.insert(0, str(KIT / "tools"))
import documentation_harness  # noqa: E402


def file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


class AdoptionProfileAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = Path(tempfile.mkdtemp(prefix="adoption-profiles-"))
        self.addCleanup(shutil.rmtree, self.temporary, True)
        self.root = self.temporary / "project"
        (self.root / "docs").mkdir(parents=True)
        (self.root / "README.md").write_text(
            "# Core acceptance\n\n"
            "[Guide](docs/guide.md#guide)\n"
            "[Secure](HTTPS://example.test/guide)\n"
            "[Transfer](ftp://example.test/archive)\n"
            "[Editor](vscode://file/C:/example.md)\n"
            "[Mail](mailto:owner@example.test)\n",
            encoding="utf-8",
        )
        (self.root / "docs/guide.md").write_text(
            "# Guide\n\n[Local anchor](#guide)\n",
            encoding="utf-8",
        )

    def test_profile_contract_keeps_core_small_and_optional_material_triggered(self) -> None:
        profiles = ADOPTION_PROFILES.read_text(encoding="utf-8")
        normalized_profiles = " ".join(profiles.split())

        for profile in ("Core", "Standard", "Workflow", "Reference Lab"):
            self.assertIn("**%s**" % profile, normalized_profiles)
        self.assertIn("never requires more than six project-created files", normalized_profiles)
        self.assertIn("Do not create a `Project Map/` for Core.", normalized_profiles)
        self.assertIn(
            "Do not add Python, evals, task contracts, `.work`, generated projections, hooks, CI, or MkDocs",
            normalized_profiles,
        )
        self.assertIn("No trigger means no installation.", normalized_profiles)
        self.assertIn("Move up one profile only when a trigger is observable.", normalized_profiles)
        self.assertIn("`TaskContractV3.workflow_profile`, documented task scale/risk", normalized_profiles)

        project_files = [path for path in self.root.rglob("*") if path.is_file()]
        self.assertLessEqual(len(project_files), 6)
        for absent in ("Project Map", ".work", "evals", "generated", "hooks", ".github", "mkdocs.yml"):
            self.assertFalse((self.root / absent).exists(), "%s is not part of Core" % absent)
        self.assertEqual(list(self.root.rglob("*.py")), [], "Core project has no Python dependency")

    def test_actual_harness_keeps_standard_workflow_and_reference_lab_opt_in(self) -> None:
        before = file_snapshot(self.root)

        completed = subprocess.run(
            [sys.executable, str(HARNESS), "--root", str(self.root), "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
        core = json.loads(completed.stdout)
        self.assertEqual(core["profiles"], ["core"])
        self.assertEqual(core["active_checks"], ["markdown_links"])
        self.assertEqual(core["status"], "passed")
        self.assertEqual(core["findings"], [])
        self.assertTrue(core["read_only"])
        self.assertEqual(file_snapshot(self.root), before, "Core harness run must be read-only")

        standard = documentation_harness.build_report(self.root, profiles=["standard"])
        self.assertEqual(standard["profiles"], ["standard"])
        self.assertIn("metadata", standard["active_checks"])
        self.assertNotIn("placeholder", standard["active_checks"])

        workflow = documentation_harness.build_report(self.root, profiles=["workflow"])
        self.assertEqual(workflow["profiles"], ["workflow"])
        self.assertIn("placeholder", workflow["active_checks"])
        self.assertIn("work_leakage", workflow["active_checks"])
        self.assertFalse(workflow["acceptance_contract"]["automatic_fix_available"])

        self.assertFalse((self.root / "reference-lab").exists())
        core_without_reference_lab = documentation_harness.build_report(self.root)
        self.assertEqual(core_without_reference_lab, core)
        self.assertEqual(file_snapshot(self.root), before, "Optional profiles must not mutate Core")


if __name__ == "__main__":
    unittest.main()

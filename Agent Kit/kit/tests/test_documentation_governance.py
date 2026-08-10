"""Dependency-free black-box integration tests for documentation governance."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


KIT = Path(__file__).resolve().parents[1]
CLI = KIT / "optional_integrations/documentation_governance/tools/documentation_governance.py"
HARNESS = KIT / "tools/documentation_harness.py"
FIXTURES = KIT / "optional_integrations/documentation_governance/fixtures"
sys.path.insert(0, str(KIT / "tools"))
import documentation_harness  # noqa: E402


def run_cli(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), "--root", str(root), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def run_harness(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HARNESS), "--root", str(root), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


class DocumentationGovernanceCliTests(unittest.TestCase):
    def copied_fixture(self, name: str) -> Path:
        temporary = Path(tempfile.mkdtemp(prefix="documentation-governance-"))
        self.addCleanup(shutil.rmtree, temporary, True)
        root = temporary / "project"
        shutil.copytree(FIXTURES / name, root)
        return root

    def test_existing_project_pilot_uses_primary_current_sources_and_safe_projections(self) -> None:
        root = self.copied_fixture("existing_project")
        before_check = file_snapshot(root)
        checked = run_cli(root, "check")
        self.assertEqual(checked.returncode, 0, checked.stderr + checked.stdout)
        self.assertIn("DG-GENERATED", checked.stdout)
        self.assertEqual(file_snapshot(root), before_check, "check must be read-only")

        fixed = run_cli(root, "fix")
        self.assertEqual(fixed.returncode, 0, fixed.stderr + fixed.stdout)
        self.assertIn("Updated 4 generated block(s).", fixed.stdout)
        after_first_fix = file_snapshot(root)
        fixed_again = run_cli(root, "fix")
        self.assertEqual(fixed_again.returncode, 0, fixed_again.stderr + fixed_again.stdout)
        self.assertIn("Updated 0 generated block(s).", fixed_again.stdout)
        self.assertEqual(file_snapshot(root), after_first_fix, "fix must be idempotent")

        index = (root / "docs/project_map/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("Current runtime", index)
        self.assertIn("Current requirement", index)
        self.assertNotIn("Legacy runtime", index)
        self.assertNotIn("Historical ADR", index)
        self.assertNotIn("Map Override", index)
        self.assertIn("KEEP INDEX BEFORE", index)
        self.assertIn("KEEP INDEX AFTER", index)

        work_board = (root / "docs/project_map/WORK_BOARD.md").read_text(encoding="utf-8")
        self.assertIn("not projected from `.work/`", work_board)
        self.assertNotIn("in_progress", work_board)
        self.assertIn("KEEP WORK BEFORE", work_board)
        self.assertIn("KEEP WORK AFTER", work_board)

        phase = (root / "docs/project_map/PHASE_STATUS.md").read_text(encoding="utf-8")
        freshness = (root / "docs/project_map/FRESHNESS.md").read_text(encoding="utf-8")
        for projection in (phase, freshness):
            self.assertIn("docs/current_runtime.md", projection)
            self.assertIn("specs/active/runtime_requirement.md", projection)
            self.assertNotIn("specs/archive/legacy_runtime.md", projection)
            self.assertNotIn("docs/adr/0001-retired-endpoint.md", projection)
            self.assertNotIn("docs/project_map/OPERATIONAL_NOTE.md", projection)

        final_check = run_cli(root, "check")
        self.assertEqual(final_check.returncode, 0, final_check.stderr + final_check.stdout)
        self.assertIn("no findings", final_check.stdout)

    def test_placeholders_are_cli_failures(self) -> None:
        root = self.copied_fixture("existing_project")
        path = root / "docs/current_runtime.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nOwner: {{ owner }}\n", encoding="utf-8")
        checked = run_cli(root, "check")
        self.assertEqual(checked.returncode, 1)
        self.assertIn("ERROR DG-PLACEHOLDER docs/current_runtime.md", checked.stdout)

    def test_empty_project_init_is_safe_and_check_is_read_only(self) -> None:
        root = self.copied_fixture("empty_project")
        (root / ".gitkeep").unlink()
        initialized = run_cli(root, "init")
        self.assertEqual(initialized.returncode, 0, initialized.stderr + initialized.stdout)
        config = root / ".documentation-governance.json"
        original_config = config.read_bytes()

        repeated = run_cli(root, "init")
        self.assertEqual(repeated.returncode, 2)
        self.assertIn("refusing to overwrite", repeated.stderr)
        self.assertEqual(config.read_bytes(), original_config, "init must refuse overwrite")

        before_check = file_snapshot(root)
        checked = run_cli(root, "check")
        self.assertEqual(checked.returncode, 0, checked.stderr + checked.stdout)
        self.assertIn("generated projection file is missing", checked.stdout)
        self.assertEqual(file_snapshot(root), before_check, "check must not create empty-project files")

    def test_fix_preserves_crlf_outside_generated_blocks(self) -> None:
        root = self.copied_fixture("existing_project")
        target = root / "docs/project_map/INDEX.md"
        original = target.read_text(encoding="utf-8").replace("\r\n", "\n")
        target.write_bytes(original.replace("\n", "\r\n").encode("utf-8"))

        fixed = run_cli(root, "fix")
        self.assertEqual(fixed.returncode, 0, fixed.stderr + fixed.stdout)
        content = target.read_bytes()
        self.assertIn(b"KEEP INDEX BEFORE\r\n", content)
        self.assertIn(b"\r\nKEEP INDEX AFTER", content)
        self.assertNotIn(b"\n", content.replace(b"\r\n", b""), "fix introduced mixed line endings")

    def test_harness_core_is_read_only_and_optional_checks_require_opt_in(self) -> None:
        root = self.copied_fixture("empty_project")
        (root / ".gitkeep").unlink()
        (root / "docs").mkdir(exist_ok=True)
        (root / "README.md").write_text("# Repository\n\n[Guide](docs/guide.md#guide)\n", encoding="utf-8")
        (root / "docs/guide.md").write_text(
            "# Guide\n\nOwner: {{ owner }}\n\nSee .work/change-1/TASKS.md.\n",
            encoding="utf-8",
        )
        before = file_snapshot(root)

        core = documentation_harness.build_report(root)
        core_ids = {item["id"] for item in core["findings"]}
        self.assertEqual(core["profiles"], ["core"])
        self.assertEqual(core["active_checks"], ["markdown_links"])
        self.assertNotIn("DOC-META-001", core_ids)
        self.assertNotIn("DOC-PLACEHOLDER-001", core_ids)
        self.assertNotIn("DOC-WORK-LEAKAGE-001", core_ids)
        self.assertNotIn("DOC-GENERATED-001", core_ids)
        self.assertEqual(file_snapshot(root), before, "Core must be read-only")

        standard = documentation_harness.build_report(root, profiles=["standard"])
        standard_ids = {item["id"] for item in standard["findings"]}
        self.assertIn("DOC-META-001", standard_ids)
        self.assertNotIn("DOC-PLACEHOLDER-001", standard_ids)
        self.assertNotIn("DOC-WORK-LEAKAGE-001", standard_ids)

        workflow = documentation_harness.build_report(root, profiles=["workflow"])
        workflow_ids = {item["id"] for item in workflow["findings"]}
        self.assertIn("DOC-META-001", workflow_ids)
        self.assertIn("DOC-PLACEHOLDER-001", workflow_ids)
        self.assertIn("DOC-WORK-LEAKAGE-001", workflow_ids)
        self.assertFalse(workflow["acceptance_contract"]["automatic_fix_available"])
        self.assertEqual(file_snapshot(root), before, "Workflow reporting must be read-only")

    def test_harness_checks_local_links_anchors_and_configured_generated_content(self) -> None:
        root = self.copied_fixture("empty_project")
        (root / ".gitkeep").unlink()
        (root / "docs").mkdir(exist_ok=True)
        readme = root / "README.md"
        readme.write_text("# Repository\n\n[Guide](docs/guide.md#guide)\n", encoding="utf-8")
        (root / "docs/guide.md").write_text("# Guide\n", encoding="utf-8")

        valid = run_harness(root, "--format", "json")
        self.assertEqual(valid.returncode, 0, valid.stderr + valid.stdout)
        self.assertNotIn("DOC-LINK", valid.stdout)
        self.assertNotIn("DOC-ANCHOR", valid.stdout)

        readme.write_text(
            "# Repository\n\n[Missing](docs/missing.md)\n[Bad anchor](docs/guide.md#absent)\n",
            encoding="utf-8",
        )
        before = file_snapshot(root)
        invalid = run_harness(root, "--format", "json")
        self.assertEqual(invalid.returncode, 0, invalid.stderr + invalid.stdout)
        report = json.loads(invalid.stdout)
        ids = {item["id"] for item in report["findings"]}
        self.assertIn("DOC-LINK-001", ids)
        self.assertIn("DOC-ANCHOR-001", ids)
        self.assertEqual(file_snapshot(root), before, "link checks must be read-only")

        config_path = root / "documentation-harness.json"
        config_path.write_text(
            json.dumps({"generated": {"index": {"path": "docs/project_map/INDEX.md"}}}),
            encoding="utf-8",
        )
        generated = run_harness(
            root,
            "--config",
            config_path.name,
            "--format",
            "json",
        )
        self.assertEqual(generated.returncode, 0, generated.stderr + generated.stdout)
        self.assertIn("DOC-GENERATED-001", generated.stdout)

    def test_markdown_uri_schemes_are_non_local_link_targets(self) -> None:
        root = self.copied_fixture("empty_project")
        (root / ".gitkeep").unlink()
        (root / "docs").mkdir(exist_ok=True)
        (root / "README.md").write_text(
            "# Repository\n\n"
            "[Secure](HTTPS://example.test/guide)\n"
            "[Transfer](ftp://example.test/archive)\n"
            "[Editor](vscode://file/C:/example.md)\n"
            "[Guide](docs/guide.md#guide)\n"
            "[Escape](../outside.md)\n",
            encoding="utf-8",
        )
        (root / "docs/guide.md").write_text(
            "# Guide\n\n"
            "[Secure](HTTPS://example.test/guide)\n"
            "[Transfer](ftp://example.test/archive)\n"
            "[Editor](vscode://file/C:/example.md)\n"
            "[Guide](#guide)\n",
            encoding="utf-8",
        )
        before = file_snapshot(root)

        report = documentation_harness.build_report(root)
        self.assertEqual([item["id"] for item in report["findings"]], ["DOC-LINK-002"])
        self.assertEqual(file_snapshot(root), before, "URI link checks must be read-only")

        (root / ".documentation-governance.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "document_globs": ["docs/**/*.md"],
                    "required_metadata": {},
                    "last_verified": {"required_for": [], "max_age_days": 90},
                    "navigation": {"required_links": {}},
                    "work_link_policy": {"allow_references_in": []},
                    "generated": {},
                }
            ),
            encoding="utf-8",
        )
        checked = run_cli(root, "check")
        self.assertEqual(checked.returncode, 0, checked.stderr + checked.stdout)
        self.assertNotIn("DG-LINK", checked.stdout)

    def test_reference_lab_legacy_self_test_command_remains_available(self) -> None:
        legacy = subprocess.run(
            [sys.executable, str(CLI), "self-test"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(legacy.returncode, 0, legacy.stderr + legacy.stdout)
        self.assertIn("self-test passed", legacy.stdout)


if __name__ == "__main__":
    unittest.main()

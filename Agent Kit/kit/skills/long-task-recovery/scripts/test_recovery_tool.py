#!/usr/bin/env python3
"""Deterministic checks for the locked recovery template and validator."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("recovery_tool.py")


class RecoveryToolTests(unittest.TestCase):
    def test_init_and_validate_locked_template(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as raw_root:
            root = Path(raw_root)
            matrix = root / "ACCEPTANCE_MATRIX.md"
            matrix.write_text(
                """# Acceptance matrix

## Closure state

| ID | Local status | Runtime status | Evidence kind |
|---|---|---|---|
| STARTUP | UNPROVEN | UNPROVEN | SOURCE_ONLY |
| STALE | PROVEN_EXECUTABLE | OPTIONAL | PRODUCTION_PATH |

## Causal proof

| ID | Gate path | Production establishment | Order/reset coverage | Anti-vacuity |
|---|---|---|---|---|
| STARTUP | producer -> transport -> consumer | UNPROVEN | UNPROVEN | UNPROVEN |
| STALE | producer -> transport -> consumer | PRODUCTION_EXECUTED | PROVEN | PROVEN |
""",
                encoding="utf-8",
            )

            init = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "init",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/example",
                    "--task-name",
                    "EXAMPLE",
                    "--goal",
                    "Startup works in both component orders.",
                    "--done",
                    "All acceptance rows have required evidence.",
                    "--acceptance-matrix",
                    "ACCEPTANCE_MATRIX.md",
                    "--active-slice",
                    "STARTUP_ROUTE",
                    "--next-action",
                    "Execute the production-path startup oracle.",
                ],
                cwd=root,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)

            validate = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "validate",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/example",
                ],
                cwd=root,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            result = json.loads(validate.stdout)
            self.assertTrue(result["ok"])
            self.assertTrue(result["capsule"]["task_identity_locked"])
            self.assertEqual(result["capsule"]["status"], "TASK_OPEN")
            self.assertEqual(result["capsule"]["acceptance_row_ids"], ["STARTUP", "STALE"])
            self.assertEqual(result["workflow"]["version"], 2)
            self.assertEqual(result["workflow"]["inventory_state"], "WORKING_INVENTORY")
            self.assertEqual(result["workflow"]["progress_total_rows"], 2)
            self.assertEqual(result["workflow"]["progress_executable_proven"], 1)
            self.assertEqual(result["workflow"]["progress_remaining_rows"], 1)
            self.assertFalse(result["acceptance_matrix"]["local_closure_allowed"])
            self.assertFalse(result["acceptance_matrix"]["runtime_closure_allowed"])

    def test_inventory_complete_requires_zero_gaps_and_final_sweep(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as raw_root:
            root = Path(raw_root)
            matrix = root / "MATRIX.md"
            matrix.write_text(
                """## Closure state

| ID | Local status | Runtime status | Evidence kind |
|---|---|---|---|
| ROUTE | UNPROVEN | UNPROVEN | SOURCE_ONLY |

## Causal proof

| ID | Gate path | Production establishment | Order/reset coverage | Anti-vacuity |
|---|---|---|---|---|
| ROUTE | producer -> transport -> consumer | UNPROVEN | UNPROVEN | UNPROVEN |
""",
                encoding="utf-8",
            )
            created = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "init",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/inventory",
                    "--task-name",
                    "INVENTORY",
                    "--goal",
                    "Inventory completeness is evidence-backed.",
                    "--done",
                    "All causal paths are mapped.",
                    "--acceptance-matrix",
                    "MATRIX.md",
                    "--active-slice",
                    "MAP_ROUTE",
                    "--next-action",
                    "Finish the read-only sweep.",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            capsule = root / ".codex/tasks/inventory/RECOVERY_CAPSULE.md"
            text = capsule.read_text(encoding="utf-8")
            text = text.replace(
                "inventory_state: WORKING_INVENTORY", "inventory_state: INVENTORY_COMPLETE"
            )
            capsule.write_text(text, encoding="utf-8")
            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "validate",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/inventory",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            result = json.loads(checked.stdout)
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("inventory_complete_with_unresolved_paths", result["issues"])
            self.assertIn("inventory_complete_without_final_sweep", result["issues"])

    def test_owner_outcome_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as raw_root:
            root = Path(raw_root)
            matrix = root / "MATRIX.md"
            matrix.write_text(
                """## Closure state

| ID | Local status | Runtime status | Evidence kind |
|---|---|---|---|
| OUTCOME | UNPROVEN | UNPROVEN | SOURCE_ONLY |

## Causal proof

| ID | Gate path | Production establishment | Order/reset coverage | Anti-vacuity |
|---|---|---|---|---|
| OUTCOME | producer -> transport -> consumer | UNPROVEN | UNPROVEN | UNPROVEN |
""",
                encoding="utf-8",
            )
            command = [
                sys.executable,
                str(SCRIPT),
                "init",
                "--repo",
                str(root),
                "--task-dir",
                ".codex/tasks/drift",
                "--task-name",
                "DRIFT",
                "--goal",
                "Original owner outcome.",
                "--done",
                "Outcome is behaviorally proven.",
                "--acceptance-matrix",
                "MATRIX.md",
                "--active-slice",
                "ONE_SLICE",
                "--next-action",
                "Test the production path.",
            ]
            created = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)

            capsule = root / ".codex/tasks/drift/RECOVERY_CAPSULE.md"
            capsule.write_text(
                capsule.read_text(encoding="utf-8").replace(
                    "Original owner outcome.", "Narrowed active-slice outcome."
                ),
                encoding="utf-8",
            )
            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "validate",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/drift",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("owner_outcome_hash_mismatch", json.loads(checked.stdout)["issues"])

    def test_precondition_injected_cannot_support_local_closure(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as raw_root:
            root = Path(raw_root)
            matrix = root / "MATRIX.md"
            matrix.write_text(
                """## Closure state

| ID | Local status | Runtime status | Evidence kind |
|---|---|---|---|
| ROUTE | UNPROVEN | UNPROVEN | JUSTIFIED_SEAM |

## Causal proof

| ID | Gate path | Production establishment | Order/reset coverage | Anti-vacuity |
|---|---|---|---|---|
| ROUTE | producer -> transport -> consumer | PRECONDITION_INJECTED | PROVEN | PROVEN |
""",
                encoding="utf-8",
            )
            command = [
                sys.executable,
                str(SCRIPT),
                "init",
                "--repo",
                str(root),
                "--task-dir",
                ".codex/tasks/injected",
                "--task-name",
                "INJECTED",
                "--goal",
                "Production establishes the prerequisite before the consumer runs.",
                "--done",
                "The production causal route is proven.",
                "--acceptance-matrix",
                "MATRIX.md",
                "--active-slice",
                "PRODUCER_ROUTE",
                "--next-action",
                "Execute the producer-to-consumer route.",
            ]
            created = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            matrix.write_text(
                matrix.read_text(encoding="utf-8").replace(
                    "| ROUTE | UNPROVEN | UNPROVEN | JUSTIFIED_SEAM |",
                    "| ROUTE | PROVEN_JUSTIFIED_SEAM | UNPROVEN | JUSTIFIED_SEAM |",
                ),
                encoding="utf-8",
            )
            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "validate",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/injected",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            result = json.loads(checked.stdout)
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn(
                "ROUTE:production_establishment_precondition_injected",
                result["acceptance_matrix"]["causal_blockers"],
            )
            self.assertFalse(result["acceptance_matrix"]["local_closure_allowed"])

    def test_init_requires_causal_proof_table(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as raw_root:
            root = Path(raw_root)
            matrix = root / "MATRIX.md"
            matrix.write_text(
                """## Closure state

| ID | Local status | Runtime status | Evidence kind |
|---|---|---|---|
| ROUTE | UNPROVEN | UNPROVEN | SOURCE_ONLY |
""",
                encoding="utf-8",
            )
            created = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "init",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/missing",
                    "--task-name",
                    "MISSING",
                    "--goal",
                    "Behavior works.",
                    "--done",
                    "Behavior is proven.",
                    "--acceptance-matrix",
                    "MATRIX.md",
                    "--active-slice",
                    "ROUTE",
                    "--next-action",
                    "Map the causal route.",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(created.returncode, 0)
            self.assertIn("Causal proof", created.stderr + created.stdout)

    def test_task_level_status_in_row_has_actionable_error(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as raw_root:
            root = Path(raw_root)
            matrix = root / "MATRIX.md"
            matrix.write_text(
                """## Closure state

| ID | Local status | Runtime status | Evidence kind |
|---|---|---|---|
| ROUTE | UNPROVEN | NOT_REQUIRED | PRODUCTION_PATH |

## Causal proof

| ID | Gate path | Production establishment | Order/reset coverage | Anti-vacuity |
|---|---|---|---|---|
| ROUTE | producer -> transport -> consumer | PRODUCTION_EXECUTED | PROVEN | PROVEN |
""",
                encoding="utf-8",
            )
            created = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "init",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/row-status",
                    "--task-name",
                    "ROW_STATUS",
                    "--goal",
                    "The production route is proven without ambiguous state labels.",
                    "--done",
                    "The row and task use their own machine-readable vocabularies.",
                    "--acceptance-matrix",
                    "MATRIX.md",
                    "--active-slice",
                    "ROUTE",
                    "--next-action",
                    "Validate the matrix vocabulary.",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            matrix.write_text(
                matrix.read_text(encoding="utf-8").replace(
                    "| ROUTE | UNPROVEN | NOT_REQUIRED | PRODUCTION_PATH |",
                    "| ROUTE | FULL_VERIFIED | NOT_REQUIRED | PRODUCTION_PATH |",
                ),
                encoding="utf-8",
            )
            checked = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "validate",
                    "--repo",
                    str(root),
                    "--task-dir",
                    ".codex/tasks/row-status",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            result = json.loads(checked.stdout)
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn(
                "invalid_local_row_status:ROUTE:FULL_VERIFIED:"
                "allowed=UNPROVEN,PROVEN_EXECUTABLE,PROVEN_JUSTIFIED_SEAM,NOT_REQUIRED;"
                "task_statuses_do_not_belong_in_rows",
                result["issues"],
            )
            self.assertEqual(
                ["UNPROVEN", "PROVEN_EXECUTABLE", "PROVEN_JUSTIFIED_SEAM", "NOT_REQUIRED"],
                result["acceptance_matrix"]["allowed_local_statuses"],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)

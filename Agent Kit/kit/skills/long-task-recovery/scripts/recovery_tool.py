#!/usr/bin/env python3
"""Initialize, validate, and snapshot compact task-local recovery state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Any


CAPSULE_NAME = "RECOVERY_CAPSULE.md"
RECEIPTS_NAME = "IMPLEMENTATION_RECEIPTS.jsonl"
DEFAULT_CAPSULE_MAX_BYTES = 12_288
DEFAULT_RECEIPT_LINE_MAX_BYTES = 8_192
DEFAULT_MAX_PATHS = 80
DEFAULT_MAX_OUTPUT_BYTES = 16_384
VALID_STATUSES = (
    "TASK_OPEN",
    "OWNER_SMOKE_FAIL_REOPENED",
    "SLICE_FIXED_TASK_OPEN",
    "NOT_STARTED",
    "DESIGN_VERIFIED",
    "CODED_UNVERIFIED",
    "TARGETED_VERIFIED",
    "FULL_VERIFIED",
    "DEPLOYED_UNACCEPTED",
    "LOCAL_VERIFIED_AWAITING_OWNER_SMOKE",
    "LOCAL_MATRIX_VERIFIED_AWAITING_OWNER_SMOKE",
    "RUNTIME_ACCEPTED",
)
REQUIRED_CAPSULE_HEADING_GROUPS = (
    ("owner_outcome", ("Goal", "Immutable owner outcome")),
    ("definition_of_done", ("Definition of done",)),
    ("scope_and_state", ("Scope and current state", "Preserved current state")),
    ("evidence_boundary", ("Evidence boundary", "Verification and acceptance boundary")),
    ("exact_next_action", ("Exact next action",)),
    ("normal_recovery", ("NORMAL_RECOVERY",)),
    ("global_recovery", ("GLOBAL_RECOVERY",)),
    ("update_rule", ("Update rule",)),
)
LOCKED_CAPSULE_HEADING_GROUPS = (
    ("active_semantic_slice", ("Active semantic slice",)),
    ("latest_owner_evidence", ("Latest owner evidence",)),
)
REOPENED_STATUSES = {"TASK_OPEN", "OWNER_SMOKE_FAIL_REOPENED", "SLICE_FIXED_TASK_OPEN"}
LOCAL_CLOSING_STATUSES = {
    "FULL_VERIFIED",
    "DEPLOYED_UNACCEPTED",
    "LOCAL_VERIFIED_AWAITING_OWNER_SMOKE",
    "LOCAL_MATRIX_VERIFIED_AWAITING_OWNER_SMOKE",
}
RUNTIME_CLOSING_STATUSES = {"RUNTIME_ACCEPTED"}
VALID_LOCAL_ROW_STATUSES = (
    "UNPROVEN",
    "PROVEN_EXECUTABLE",
    "PROVEN_JUSTIFIED_SEAM",
    "NOT_REQUIRED",
)
LOCAL_PROVEN = {"PROVEN_EXECUTABLE", "PROVEN_JUSTIFIED_SEAM", "NOT_REQUIRED"}
RUNTIME_PROVEN = {"ACCEPTED", "OPTIONAL", "NOT_REQUIRED"}
BEHAVIORAL_EVIDENCE = {"PRODUCTION_PATH", "JUSTIFIED_SEAM", "NOT_REQUIRED"}
CAUSAL_ESTABLISHMENT_PROVEN = {"PRODUCTION_EXECUTED", "NOT_REQUIRED"}
CAUSAL_ORDER_PROVEN = {"PROVEN", "NOT_REQUIRED"}
CAUSAL_ANTIVACUITY_PROVEN = {"PROVEN", "NOT_REQUIRED"}
UNMAPPED_GATE_PATHS = {"", "-", "TBD", "TODO", "UNKNOWN", "UNMAPPED", "UNPROVEN"}
CONFLICT_STATUSES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}
WORKFLOW_CONTRACT_VERSION = 2
VALID_INVENTORY_STATES = {
    "WORKING_INVENTORY",
    "INVENTORY_COMPLETE",
    "INVENTORY_INVALIDATED",
}
VALID_INVENTORY_SWEEPS = {"NOT_RUN", "PASS", "FAILED"}
VALID_EVIDENCE_LAYERS = {"NONE", "SOURCE_ONLY", "BUILD", "TESTS", "RUNTIME"}
VALID_CUMULATIVE_REGRESSION = {"NOT_RUN", "NOT_REQUIRED", "PASS", "FAILED"}
SOURCE_CLAIM_TOKENS = ("SOURCE_IMPLEMENTED", "SOURCE_VERIFIED", "SOURCE_BATCH_READY")


class RecoveryError(RuntimeError):
    """Raised for a bounded, user-actionable recovery error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def resolve_repo(value: str) -> Path:
    repo = Path(value).expanduser().resolve()
    if not repo.is_dir():
        raise RecoveryError(f"repository/workspace root is not a directory: {repo}")
    return repo


def resolve_inside(repo: Path, value: str, label: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = repo / path
    path = path.resolve()
    try:
        path.relative_to(repo)
    except ValueError as error:
        raise RecoveryError(f"{label} must stay inside repository/workspace root: {path}") from error
    return path


def display_path(repo: Path, path: Path) -> str:
    try:
        return path.relative_to(repo).as_posix()
    except ValueError:
        return str(path)


def run_process(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        argv,
        cwd=str(cwd),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
    )


def git_command(repo: Path, *args: str, required: bool = True) -> str:
    process = run_process(["git", *args], repo)
    stdout = process.stdout.decode("utf-8", errors="replace")
    if required and process.returncode != 0:
        stderr = process.stderr.decode("utf-8", errors="replace").strip()
        raise RecoveryError(f"git {' '.join(args)} failed: {stderr[:500]}")
    return stdout if process.returncode == 0 else ""


def probe_git(repo: Path) -> dict[str, Any]:
    top_text = git_command(repo, "rev-parse", "--show-toplevel", required=False).strip()
    if not top_text:
        return {"available": False, "top": None, "head": None, "branch": None}
    top = Path(top_text).resolve()
    head = git_command(repo, "rev-parse", "--verify", "HEAD", required=False).strip() or None
    branch = git_command(repo, "symbolic-ref", "--short", "-q", "HEAD", required=False).strip()
    return {
        "available": True,
        "top": str(top),
        "head": head,
        "branch": branch or None,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked_by_git(repo: Path, path: Path, git: dict[str, Any]) -> bool | None:
    if not git["available"]:
        return None
    top = Path(str(git["top"]))
    try:
        relative = path.relative_to(top).as_posix()
    except ValueError:
        return False
    process = run_process(["git", "ls-files", "--error-unmatch", "--", relative], top)
    return process.returncode == 0


def file_metadata(
    repo: Path,
    path: Path,
    git: dict[str, Any],
    include_hash: bool,
) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "path": display_path(repo, path),
        "exists": path.is_file(),
        "tracked": tracked_by_git(repo, path, git),
    }
    if path.is_file():
        metadata["bytes"] = path.stat().st_size
        if include_hash:
            metadata["sha256"] = sha256(path)
    return metadata


def markdown_list(items: list[str], empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in items)


def write_new_text(path: Path, text: str) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags, 0o644)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            descriptor = -1
            stream.write(text)
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def parse_receipts(path: Path, line_max_bytes: int) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    receipts: list[dict[str, Any]] = []
    if not path.is_file():
        return receipts, ["receipts_missing"]
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return receipts, ["receipts_not_utf8"]
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        if len(line.encode("utf-8")) > line_max_bytes:
            issues.append(f"receipt_line_too_large:{line_number}")
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            issues.append(f"receipt_invalid_json:{line_number}")
            continue
        if not isinstance(record, dict):
            issues.append(f"receipt_not_object:{line_number}")
            continue
        receipts.append(record)
    for expected, record in enumerate(receipts, start=1):
        if record.get("seq") != expected:
            issues.append(f"receipt_sequence_mismatch:expected={expected}:actual={record.get('seq')}")
            break
    return receipts, issues


def capsule_field(text: str, field: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(field)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else None


def capsule_bool_field(text: str, field: str) -> bool:
    value = capsule_field(text, field)
    return bool(value and value.strip().casefold() == "true")


def capsule_int_field(text: str, field: str) -> int | None:
    value = capsule_field(text, field)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def capsule_list_field(text: str, field: str) -> list[str]:
    value = capsule_field(text, field)
    if not value:
        return []
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def has_heading(text: str, alternatives: tuple[str, ...]) -> bool:
    headings = re.findall(r"(?m)^##\s+(.+?)\s*$", text)
    normalized = [heading.strip().casefold() for heading in headings]
    for expected in alternatives:
        prefix = expected.casefold()
        if any(heading == prefix or heading.startswith(prefix + " ") for heading in normalized):
            return True
    return False


def section_body(text: str, alternatives: tuple[str, ...]) -> str | None:
    expected = tuple(item.casefold() for item in alternatives)
    lines = text.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        heading = line[3:].strip().casefold()
        if any(heading == item or heading.startswith(item + " ") for item in expected):
            start = index + 1
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    body = "\n".join(lines[start:end]).strip()
    return body or None


def owner_outcome_sha256(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def parse_closure_rows(text: str) -> list[dict[str, str]]:
    heading = re.search(r"(?im)^##\s+Closure state\s*$", text)
    if not heading:
        return []
    tail = text[heading.end():]
    next_heading = re.search(r"(?m)^##\s+", tail)
    block = tail[: next_heading.start()] if next_heading else tail
    rows: list[dict[str, str]] = []
    for line in block.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        if cells[0].casefold() == "id" or all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append(
            {
                "id": cells[0],
                "local_status": cells[1].upper(),
                "runtime_status": cells[2].upper(),
                "evidence_kind": cells[3].upper(),
            }
        )
    return rows


def parse_causal_rows(text: str) -> list[dict[str, str]]:
    heading = re.search(r"(?im)^##\s+Causal proof\s*$", text)
    if not heading:
        return []
    tail = text[heading.end():]
    next_heading = re.search(r"(?m)^##\s+", tail)
    block = tail[: next_heading.start()] if next_heading else tail
    rows: list[dict[str, str]] = []
    for line in block.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0].casefold() == "id" or all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append(
            {
                "id": cells[0],
                "gate_path": cells[1],
                "production_establishment": cells[2].upper(),
                "order_coverage": cells[3].upper(),
                "anti_vacuity": cells[4].upper(),
            }
        )
    return rows


def row_requires_causal_proof(row: dict[str, str]) -> bool:
    return row["local_status"] != "NOT_REQUIRED" or row["evidence_kind"] != "NOT_REQUIRED"


def causal_blocker(row: dict[str, str], proof: dict[str, str] | None) -> str | None:
    if not row_requires_causal_proof(row):
        return None
    if proof is None:
        return "causal_row_missing"

    all_not_required = (
        proof["production_establishment"] == "NOT_REQUIRED"
        and proof["order_coverage"] == "NOT_REQUIRED"
        and proof["anti_vacuity"] == "NOT_REQUIRED"
    )
    gate_key = proof["gate_path"].strip().upper()
    if gate_key == "NOT_REQUIRED":
        if not all_not_required:
            return "not_required_gate_has_required_status"
    elif gate_key in UNMAPPED_GATE_PATHS:
        return "gate_path_unmapped"

    if proof["production_establishment"] not in CAUSAL_ESTABLISHMENT_PROVEN:
        return "production_establishment_" + proof["production_establishment"].casefold()
    if proof["order_coverage"] not in CAUSAL_ORDER_PROVEN:
        return "order_coverage_" + proof["order_coverage"].casefold()
    if proof["anti_vacuity"] not in CAUSAL_ANTIVACUITY_PROVEN:
        return "anti_vacuity_" + proof["anti_vacuity"].casefold()
    if row["evidence_kind"] == "JUSTIFIED_SEAM" and proof["anti_vacuity"] != "PROVEN":
        return "justified_seam_without_antivacuity"
    return None


def validate_state(
    repo: Path,
    task_dir: Path,
    capsule_max_bytes: int,
    receipt_line_max_bytes: int,
) -> dict[str, Any]:
    issues: list[str] = []
    capsule_path = task_dir / CAPSULE_NAME
    receipts_path = task_dir / RECEIPTS_NAME
    capsule_text = ""

    if not capsule_path.is_file():
        issues.append("capsule_missing")
    else:
        capsule_size = capsule_path.stat().st_size
        if capsule_size > capsule_max_bytes:
            issues.append("capsule_size_budget_exceeded")
        try:
            capsule_text = capsule_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append("capsule_not_utf8")

    receipts, receipt_issues = parse_receipts(receipts_path, receipt_line_max_bytes)
    issues.extend(receipt_issues)

    schema = capsule_field(capsule_text, "schema") if capsule_text else None
    last_seq_text = capsule_field(capsule_text, "last_receipt_seq") if capsule_text else None
    status = capsule_field(capsule_text, "status") if capsule_text else None
    phase = capsule_field(capsule_text, "phase") if capsule_text else None
    task_locked = capsule_bool_field(capsule_text, "task_identity_locked") if capsule_text else False
    declared_rows = capsule_list_field(capsule_text, "acceptance_row_ids") if capsule_text else []
    active_slice = capsule_field(capsule_text, "active_slice") if capsule_text else None
    recorded_outcome_hash = capsule_field(capsule_text, "owner_outcome_sha256") if capsule_text else None
    workflow_version = capsule_int_field(capsule_text, "workflow_contract_version") if capsule_text else None
    workflow_v2 = workflow_version == WORKFLOW_CONTRACT_VERSION
    inventory_state = capsule_field(capsule_text, "inventory_state") if capsule_text else None
    inventory_generation = capsule_int_field(capsule_text, "inventory_generation") if capsule_text else None
    inventory_unresolved_paths = (
        capsule_list_field(capsule_text, "inventory_unresolved_paths") if capsule_text else []
    )
    inventory_final_sweep = capsule_field(capsule_text, "inventory_final_sweep") if capsule_text else None
    progress_total_rows = capsule_int_field(capsule_text, "progress_total_rows") if capsule_text else None
    progress_source_implemented = (
        capsule_int_field(capsule_text, "progress_source_implemented") if capsule_text else None
    )
    progress_executable_proven = (
        capsule_int_field(capsule_text, "progress_executable_proven") if capsule_text else None
    )
    progress_runtime_accepted = (
        capsule_int_field(capsule_text, "progress_runtime_accepted") if capsule_text else None
    )
    progress_remaining_rows = (
        capsule_int_field(capsule_text, "progress_remaining_rows") if capsule_text else None
    )
    active_worker_present = (
        capsule_bool_field(capsule_text, "active_worker_present") if capsule_text else False
    )
    active_worker_scope = capsule_field(capsule_text, "active_worker_scope") if capsule_text else None
    active_worker_stopping_condition = (
        capsule_field(capsule_text, "active_worker_stopping_condition") if capsule_text else None
    )
    evidence_layer = capsule_field(capsule_text, "evidence_layer") if capsule_text else None
    source_checks_complete = (
        capsule_bool_field(capsule_text, "source_checks_complete") if capsule_text else False
    )
    cumulative_regression = (
        capsule_field(capsule_text, "cumulative_regression") if capsule_text else None
    )
    workflow_summary: dict[str, Any] = {
        "version": workflow_version,
        "inventory_state": inventory_state,
        "inventory_generation": inventory_generation,
        "inventory_unresolved_paths": inventory_unresolved_paths,
        "inventory_final_sweep": inventory_final_sweep,
        "progress_total_rows": progress_total_rows,
        "progress_source_implemented": progress_source_implemented,
        "progress_executable_proven": progress_executable_proven,
        "progress_runtime_accepted": progress_runtime_accepted,
        "progress_remaining_rows": progress_remaining_rows,
        "active_worker_present": active_worker_present,
        "active_worker_scope": active_worker_scope,
        "active_worker_stopping_condition": active_worker_stopping_condition,
        "evidence_layer": evidence_layer,
        "source_checks_complete": source_checks_complete,
        "cumulative_regression": cumulative_regression,
    }
    matrix_summary: dict[str, Any] = {
        "path": None,
        "row_ids": [],
        "causal_row_ids": [],
        "allowed_local_statuses": list(VALID_LOCAL_ROW_STATUSES),
        "causal_blockers": [],
        "causal_closure_allowed": False,
        "local_closure_allowed": False,
        "runtime_closure_allowed": False,
    }

    if capsule_text:
        if schema != "RECOVERY_CAPSULE_V1":
            issues.append("capsule_schema_invalid")
        for label, alternatives in REQUIRED_CAPSULE_HEADING_GROUPS:
            if not has_heading(capsule_text, alternatives):
                issues.append(f"capsule_heading_missing:{label}")
        if status not in VALID_STATUSES:
            issues.append("capsule_status_invalid")

    if capsule_text and task_locked:
        for label, alternatives in LOCKED_CAPSULE_HEADING_GROUPS:
            if not has_heading(capsule_text, alternatives):
                issues.append(f"capsule_heading_missing:{label}")
        if not active_slice:
            issues.append("active_slice_missing")
        if not capsule_field(capsule_text, "last_owner_evidence"):
            issues.append("last_owner_evidence_missing")
        if not declared_rows:
            issues.append("acceptance_row_ids_missing")

        if workflow_version is not None and not workflow_v2:
            issues.append("workflow_contract_version_invalid")
        if workflow_v2:
            if inventory_state not in VALID_INVENTORY_STATES:
                issues.append("inventory_state_invalid")
            if inventory_generation is None or inventory_generation < 1:
                issues.append("inventory_generation_invalid")
            if inventory_final_sweep not in VALID_INVENTORY_SWEEPS:
                issues.append("inventory_final_sweep_invalid")
            if inventory_state == "INVENTORY_COMPLETE":
                if inventory_unresolved_paths:
                    issues.append("inventory_complete_with_unresolved_paths")
                if inventory_final_sweep != "PASS":
                    issues.append("inventory_complete_without_final_sweep")
            if evidence_layer not in VALID_EVIDENCE_LAYERS:
                issues.append("evidence_layer_invalid")
            if cumulative_regression not in VALID_CUMULATIVE_REGRESSION:
                issues.append("cumulative_regression_invalid")
            if active_worker_present:
                if not active_worker_scope or active_worker_scope.upper() == "NONE":
                    issues.append("active_worker_scope_missing")
                if (
                    not active_worker_stopping_condition
                    or active_worker_stopping_condition.upper() == "NONE"
                ):
                    issues.append("active_worker_stopping_condition_missing")
            source_claim = any(token in (phase or "").upper() for token in SOURCE_CLAIM_TOKENS)
            if source_claim:
                if inventory_state != "INVENTORY_COMPLETE":
                    issues.append("source_claim_before_inventory_complete")
                if not source_checks_complete:
                    issues.append("source_claim_without_source_checks")
                if cumulative_regression not in {"PASS", "NOT_REQUIRED"}:
                    issues.append("source_claim_without_cumulative_regression")

        outcome = section_body(capsule_text, ("Immutable owner outcome", "Goal"))
        if not outcome:
            issues.append("owner_outcome_missing")
        else:
            actual_outcome_hash = owner_outcome_sha256(outcome)
            if recorded_outcome_hash != actual_outcome_hash:
                issues.append("owner_outcome_hash_mismatch")

            receipt_hashes = [
                str(record.get("owner_outcome_sha256"))
                for record in receipts
                if record.get("owner_outcome_sha256")
            ]
            if not receipt_hashes:
                issues.append("owner_outcome_receipt_anchor_missing")
            elif len(set(receipt_hashes)) != 1 or receipt_hashes[-1] != actual_outcome_hash:
                issues.append("owner_outcome_receipt_anchor_mismatch")

        matrix_raw = capsule_field(capsule_text, "acceptance_matrix")
        if not matrix_raw:
            issues.append("acceptance_matrix_missing")
        else:
            matrix_raw = matrix_raw.strip().strip("`'\"")
            try:
                matrix_path = resolve_inside(repo, matrix_raw, "acceptance matrix")
            except RecoveryError:
                matrix_path = None
                issues.append("acceptance_matrix_outside_workspace")
            matrix_summary["path"] = str(matrix_path) if matrix_path else matrix_raw
            if matrix_path is not None and not matrix_path.is_file():
                issues.append("acceptance_matrix_file_missing")
            elif matrix_path is not None:
                try:
                    matrix_text = matrix_path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    matrix_text = ""
                    issues.append("acceptance_matrix_not_utf8")
                rows = parse_closure_rows(matrix_text)
                causal_rows = parse_causal_rows(matrix_text)
                matrix_ids = [row["id"] for row in rows]
                causal_ids = [row["id"] for row in causal_rows]
                matrix_summary["row_ids"] = matrix_ids
                matrix_summary["causal_row_ids"] = causal_ids
                if not rows:
                    issues.append("acceptance_matrix_closure_state_missing")
                elif matrix_ids != declared_rows:
                    missing = [row for row in declared_rows if row not in matrix_ids]
                    extra = [row for row in matrix_ids if row not in declared_rows]
                    if missing:
                        issues.append("acceptance_matrix_rows_dropped:" + ",".join(missing))
                    if extra:
                        issues.append("acceptance_matrix_rows_undeclared:" + ",".join(extra))
                    if not missing and not extra:
                        issues.append("acceptance_matrix_row_order_changed")

                allowed_local = ",".join(VALID_LOCAL_ROW_STATUSES)
                for row in rows:
                    if row["local_status"] not in VALID_LOCAL_ROW_STATUSES:
                        issues.append(
                            f"invalid_local_row_status:{row['id']}:{row['local_status']}:"
                            f"allowed={allowed_local};task_statuses_do_not_belong_in_rows"
                        )

                if causal_rows and causal_ids != matrix_ids:
                    missing = [row for row in matrix_ids if row not in causal_ids]
                    extra = [row for row in causal_ids if row not in matrix_ids]
                    if missing:
                        issues.append("causal_rows_dropped:" + ",".join(missing))
                    if extra:
                        issues.append("causal_rows_undeclared:" + ",".join(extra))
                    if not missing and not extra:
                        issues.append("causal_row_order_changed")

                causal_by_id = {row["id"]: row for row in causal_rows}
                causal_blockers: list[str] = []
                for row in rows:
                    blocker = causal_blocker(row, causal_by_id.get(row["id"]))
                    if blocker:
                        causal_blockers.append(f"{row['id']}:{blocker}")
                        if row["local_status"] in {
                            "PROVEN_EXECUTABLE",
                            "PROVEN_JUSTIFIED_SEAM",
                            "LOCAL_VERIFIED",
                        }:
                            issues.append(
                                f"local_behavioral_pass_without_causal_proof:{row['id']}:{blocker}"
                            )
                matrix_summary["causal_blockers"] = causal_blockers
                matrix_summary["causal_closure_allowed"] = bool(rows) and not causal_blockers

                for row in rows:
                    if row["local_status"] in {"PROVEN_EXECUTABLE", "PROVEN_JUSTIFIED_SEAM"}:
                        if row["evidence_kind"] not in BEHAVIORAL_EVIDENCE:
                            issues.append("behavioral_pass_without_executable_evidence:" + row["id"])

                def has_local_proof(row: dict[str, str]) -> bool:
                    if row["local_status"] == "NOT_REQUIRED":
                        return True
                    return (
                        row["local_status"] in LOCAL_PROVEN
                        and row["evidence_kind"] in BEHAVIORAL_EVIDENCE
                        and causal_blocker(row, causal_by_id.get(row["id"])) is None
                    )

                local_allowed = bool(rows) and all(has_local_proof(row) for row in rows)
                runtime_allowed = local_allowed and all(
                    row["runtime_status"] in RUNTIME_PROVEN for row in rows
                )
                matrix_summary["local_closure_allowed"] = local_allowed
                matrix_summary["runtime_closure_allowed"] = runtime_allowed
                if workflow_v2:
                    expected_total = len(rows)
                    expected_executable = sum(
                        row["local_status"] in LOCAL_PROVEN for row in rows
                    )
                    expected_runtime_accepted = sum(
                        row["runtime_status"] == "ACCEPTED" for row in rows
                    )
                    expected_remaining = expected_total - expected_executable
                    if progress_total_rows != expected_total:
                        issues.append(
                            f"progress_total_rows_mismatch:declared={progress_total_rows}:actual={expected_total}"
                        )
                    if progress_executable_proven != expected_executable:
                        issues.append(
                            "progress_executable_proven_mismatch:"
                            f"declared={progress_executable_proven}:actual={expected_executable}"
                        )
                    if progress_runtime_accepted != expected_runtime_accepted:
                        issues.append(
                            "progress_runtime_accepted_mismatch:"
                            f"declared={progress_runtime_accepted}:actual={expected_runtime_accepted}"
                        )
                    if progress_remaining_rows != expected_remaining:
                        issues.append(
                            "progress_remaining_rows_mismatch:"
                            f"declared={progress_remaining_rows}:actual={expected_remaining}"
                        )
                    if (
                        progress_source_implemented is None
                        or progress_source_implemented < 0
                        or progress_source_implemented > expected_total
                    ):
                        issues.append("progress_source_implemented_invalid")
                if status in LOCAL_CLOSING_STATUSES and not local_allowed:
                    issues.append("local_completion_with_failed_or_unproven_rows")
                if status in RUNTIME_CLOSING_STATUSES and not runtime_allowed:
                    issues.append("runtime_completion_without_runtime_acceptance")
                if any(row["runtime_status"] == "FAILED" for row in rows):
                    if status not in REOPENED_STATUSES:
                        issues.append("owner_smoke_failed_without_reopened_task")

        receipt_row_sets = [
            [str(item) for item in record.get("acceptance_row_ids", [])]
            for record in receipts
            if isinstance(record.get("acceptance_row_ids"), list)
        ]
        if not receipt_row_sets:
            issues.append("acceptance_rows_receipt_anchor_missing")
        elif any(rows != receipt_row_sets[0] for rows in receipt_row_sets[1:]):
            issues.append("acceptance_rows_receipt_anchor_mismatch")
        elif receipt_row_sets[-1] != declared_rows:
            issues.append("acceptance_rows_changed_from_receipt_anchor")

    try:
        last_seq = int(last_seq_text) if last_seq_text is not None else None
    except ValueError:
        last_seq = None
        issues.append("capsule_last_receipt_seq_invalid")

    latest_seq = receipts[-1].get("seq") if receipts else None
    if last_seq is None and capsule_text:
        issues.append("capsule_last_receipt_seq_missing")
    elif latest_seq is not None and last_seq != latest_seq:
        issues.append(f"capsule_receipt_sequence_mismatch:capsule={last_seq}:receipts={latest_seq}")
    elif latest_seq is None and last_seq not in (None, 0):
        issues.append("capsule_references_missing_receipt")

    return {
        "ok": not issues,
        "issues": issues,
        "capsule": {
            "path": str(capsule_path),
            "exists": capsule_path.is_file(),
            "bytes": capsule_path.stat().st_size if capsule_path.is_file() else None,
            "schema": schema,
            "phase": phase,
            "status": status,
            "last_receipt_seq": last_seq,
            "task_identity_locked": task_locked,
            "owner_outcome_sha256": recorded_outcome_hash,
            "acceptance_row_ids": declared_rows,
            "active_slice": active_slice,
        },
        "workflow": workflow_summary,
        "acceptance_matrix": matrix_summary,
        "receipts": {
            "path": str(receipts_path),
            "exists": receipts_path.is_file(),
            "bytes": receipts_path.stat().st_size if receipts_path.is_file() else None,
            "count": len(receipts),
            "latest_seq": latest_seq,
            "latest": receipts[-1] if receipts else None,
        },
    }


def init_command(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    task_dir = resolve_inside(repo, args.task_dir, "task directory")
    capsule_path = task_dir / CAPSULE_NAME
    receipts_path = task_dir / RECEIPTS_NAME
    if capsule_path.exists() or receipts_path.exists():
        raise RecoveryError(
            "recovery state already exists; run validate/snapshot and recover it instead of reinitializing"
        )

    if args.capsule_max_bytes < 1 or args.receipt_line_max_bytes < 256:
        raise RecoveryError("capsule limit must be positive and receipt line limit must be >= 256")

    plans: list[Path] = []
    for value in args.plan:
        plan = resolve_inside(repo, value, "plan")
        if not plan.is_file():
            raise RecoveryError(f"plan file does not exist: {plan}")
        plans.append(plan)

    matrix_path = resolve_inside(repo, args.acceptance_matrix, "acceptance matrix")
    if not matrix_path.is_file():
        raise RecoveryError(f"acceptance matrix does not exist: {matrix_path}")
    try:
        matrix_text = matrix_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise RecoveryError(f"acceptance matrix is not UTF-8: {matrix_path}") from error
    matrix_rows = parse_closure_rows(matrix_text)
    if not matrix_rows:
        raise RecoveryError("acceptance matrix must contain a four-column '## Closure state' table")
    invalid_local_rows = [
        row for row in matrix_rows if row["local_status"] not in VALID_LOCAL_ROW_STATUSES
    ]
    if invalid_local_rows:
        row = invalid_local_rows[0]
        allowed_local = ",".join(VALID_LOCAL_ROW_STATUSES)
        raise RecoveryError(
            f"invalid local row status {row['id']}={row['local_status']}; "
            f"allowed={allowed_local}; task-level statuses do not belong in rows"
        )
    causal_rows = parse_causal_rows(matrix_text)
    if not causal_rows:
        raise RecoveryError("acceptance matrix must contain a five-column '## Causal proof' table")
    acceptance_row_ids = [row["id"] for row in matrix_rows]
    causal_row_ids = [row["id"] for row in causal_rows]
    if causal_row_ids != acceptance_row_ids:
        raise RecoveryError("causal proof row IDs and order must exactly match closure row IDs")
    matrix_state_rows = "\n".join(
        "| {id} | {local_status} | {runtime_status} | {evidence_kind} |".format(**row)
        for row in matrix_rows
    )
    immutable_outcome = args.goal.strip()
    immutable_outcome_hash = owner_outcome_sha256(immutable_outcome)
    progress_total_rows = len(matrix_rows)
    progress_executable_proven = sum(
        row["local_status"] in LOCAL_PROVEN for row in matrix_rows
    )
    progress_runtime_accepted = sum(
        row["runtime_status"] == "ACCEPTED" for row in matrix_rows
    )
    progress_remaining_rows = progress_total_rows - progress_executable_proven

    git = probe_git(repo)
    skill_root = Path(__file__).resolve().parent.parent
    template_path = skill_root / "assets" / "RECOVERY_CAPSULE.template.md"
    if not template_path.is_file():
        raise RecoveryError(f"capsule template missing: {template_path}")
    template = Template(template_path.read_text(encoding="utf-8"))
    timestamp = utc_now()
    capsule_text = template.substitute(
        TASK_NAME=args.task_name.strip(),
        UPDATED_UTC=timestamp,
        PHASE=args.phase.strip(),
        STATUS=args.status,
        CAPSULE_MAX_BYTES=args.capsule_max_bytes,
        OWNER_OUTCOME_SHA256=immutable_outcome_hash,
        ACCEPTANCE_MATRIX=display_path(repo, matrix_path),
        ACCEPTANCE_ROW_IDS=", ".join(json.dumps(row_id) for row_id in acceptance_row_ids),
        ACTIVE_SLICE=args.active_slice.strip(),
        LAST_OWNER_EVIDENCE=args.last_owner_evidence.strip(),
        PROGRESS_TOTAL_ROWS=progress_total_rows,
        PROGRESS_EXECUTABLE_PROVEN=progress_executable_proven,
        PROGRESS_RUNTIME_ACCEPTED=progress_runtime_accepted,
        PROGRESS_REMAINING_ROWS=progress_remaining_rows,
        GOAL=immutable_outcome,
        DONE_ITEMS=markdown_list([item.strip() for item in args.done], "TO_BE_DEFINED"),
        REPO_ROOT=str(repo),
        TASK_DIR=display_path(repo, task_dir),
        HEAD=git["head"] or "UNAVAILABLE",
        BRANCH=git["branch"] or "UNAVAILABLE",
        WRITER=args.writer.strip(),
        MATRIX_STATE_ROWS=matrix_state_rows,
        PLAN_ITEMS=markdown_list(
            [f"`{display_path(repo, plan)}`" for plan in plans],
            "No authoritative plan recorded.",
        ),
        NEXT_ACTION=args.next_action.strip(),
    )
    if not capsule_text.endswith("\n"):
        capsule_text += "\n"
    capsule_bytes = len(capsule_text.encode("utf-8"))
    if capsule_bytes > args.capsule_max_bytes:
        raise RecoveryError(
            f"rendered capsule exceeds limit: {capsule_bytes} > {args.capsule_max_bytes} bytes"
        )

    receipt = {
        "schema": "IMPLEMENTATION_RECEIPT_V1",
        "seq": 1,
        "recorded_utc": timestamp,
        "kind": "RECOVERY_INITIALIZED",
        "task": args.task_name.strip(),
        "scope": "recovery initialization only",
        "phase": args.phase.strip(),
        "status": args.status,
        "head": git["head"],
        "plans": [display_path(repo, plan) for plan in plans],
        "owner_outcome_sha256": immutable_outcome_hash,
        "acceptance_row_ids": acceptance_row_ids,
        "verification": {
            "capsule_rendered": True,
            "capsule_bytes": capsule_bytes,
            "existing_state_overwritten": False,
            "acceptance_matrix": display_path(repo, matrix_path),
            "matrix_row_count": len(acceptance_row_ids),
            "causal_proof_row_count": len(causal_row_ids),
            "workflow_contract_version": WORKFLOW_CONTRACT_VERSION,
            "evidence_kind": "INITIALIZATION_ONLY",
        },
        "claim_limit": "no implementation, test, build, deployment, runtime, or acceptance claim",
        "next": args.next_action.strip(),
    }
    receipt_text = json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n"
    if len(receipt_text.encode("utf-8")) > args.receipt_line_max_bytes:
        raise RecoveryError("initial receipt exceeds receipt line limit")

    task_dir.mkdir(parents=True, exist_ok=True)
    created_receipt = False
    try:
        write_new_text(receipts_path, receipt_text)
        created_receipt = True
        write_new_text(capsule_path, capsule_text)
    except Exception:
        if created_receipt and receipts_path.is_file() and not capsule_path.exists():
            if receipts_path.read_text(encoding="utf-8") == receipt_text:
                receipts_path.unlink()
        raise

    validation = validate_state(repo, task_dir, args.capsule_max_bytes, args.receipt_line_max_bytes)
    if not validation["ok"]:
        raise RecoveryError(f"created recovery state failed validation: {validation['issues']}")
    emit(
        {
            "schema": "RECOVERY_INIT_RESULT_V1",
            "ok": True,
            "task_dir": display_path(repo, task_dir),
            "capsule": display_path(repo, capsule_path),
            "receipts": display_path(repo, receipts_path),
            "capsule_bytes": capsule_bytes,
            "latest_receipt_seq": 1,
        }
    )
    return 0


def validate_command(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    task_dir = resolve_inside(repo, args.task_dir, "task directory")
    validation = validate_state(repo, task_dir, args.capsule_max_bytes, args.receipt_line_max_bytes)
    validation["schema"] = "RECOVERY_VALIDATION_V1"
    validation["task_dir"] = display_path(repo, task_dir)
    if validation["receipts"]["latest"] is not None:
        latest = validation["receipts"].pop("latest")
        validation["receipts"]["latest_summary"] = {
            "seq": latest.get("seq"),
            "kind": latest.get("kind"),
            "status": latest.get("status"),
            "next": str(latest.get("next", ""))[:500],
        }
    emit(validation)
    return 0 if validation["ok"] else 2


def parse_status(text: str) -> tuple[list[dict[str, str]], dict[str, int]]:
    entries: list[dict[str, str]] = []
    counts = {"total": 0, "staged": 0, "unstaged": 0, "untracked": 0, "conflicted": 0}
    for line in text.splitlines():
        if len(line) < 3:
            continue
        code = line[:2]
        entries.append({"code": code, "path": line[3:]})
        counts["total"] += 1
        if code == "??":
            counts["untracked"] += 1
            continue
        if code in CONFLICT_STATUSES:
            counts["conflicted"] += 1
        if code[0] != " ":
            counts["staged"] += 1
        if code[1] != " ":
            counts["unstaged"] += 1
    return entries, counts


def parse_numstat(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line in text.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        added, deleted, path = parts
        entries.append(
            {
                "path": path,
                "added": None if added == "-" else int(added),
                "deleted": None if deleted == "-" else int(deleted),
            }
        )
    return entries


def encode_bounded(payload: dict[str, Any], max_bytes: int) -> tuple[bytes, bool]:
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if len(encoded) <= max_bytes:
        return encoded, False

    payload["ok"] = False
    payload["violations"].append("output_budget_exceeded")
    payload["output_truncated"] = True
    if payload.get("git", {}).get("status"):
        payload["git"]["status"]["entries"] = payload["git"]["status"]["entries"][:10]
    if payload.get("git", {}).get("diff_numstat"):
        payload["git"]["diff_numstat"]["worktree"] = payload["git"]["diff_numstat"][
            "worktree"
        ][:10]
        payload["git"]["diff_numstat"]["index"] = payload["git"]["diff_numstat"]["index"][
            :10
        ]
    encoded = (json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )
    if len(encoded) <= max_bytes:
        return encoded, True

    minimal = {
        "schema": "RECOVERY_SNAPSHOT_V1",
        "ok": False,
        "output_truncated": True,
        "violations": ["output_budget_exceeded"],
        "head": payload.get("git", {}).get("head"),
        "status_counts": payload.get("git", {}).get("status", {}).get("counts"),
    }
    return (json.dumps(minimal, ensure_ascii=False, separators=(",", ":")) + "\n").encode(
        "utf-8"
    ), True


def snapshot_command(args: argparse.Namespace) -> int:
    if args.max_output_bytes < 512 or args.max_paths < 1:
        raise RecoveryError("max-output-bytes must be >= 512 and max-paths must be positive")
    repo = resolve_repo(args.repo)
    task_dir = resolve_inside(repo, args.task_dir, "task directory")
    validation = validate_state(repo, task_dir, args.capsule_max_bytes, args.receipt_line_max_bytes)
    violations = list(validation["issues"])
    git = probe_git(repo)

    status_entries: list[dict[str, str]] = []
    status_counts = {"total": 0, "staged": 0, "unstaged": 0, "untracked": 0, "conflicted": 0}
    worktree_numstat: list[dict[str, Any]] = []
    index_numstat: list[dict[str, Any]] = []
    if git["available"]:
        status_text = git_command(
            repo,
            "-c",
            "core.quotepath=false",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        )
        status_entries, status_counts = parse_status(status_text)
        if status_counts["total"] > args.max_paths:
            violations.append("status_path_budget_exceeded")
        worktree_numstat = parse_numstat(
            git_command(repo, "-c", "core.safecrlf=false", "diff", "--numstat", "--")
        )
        index_numstat = parse_numstat(
            git_command(
                repo,
                "-c",
                "core.safecrlf=false",
                "diff",
                "--cached",
                "--numstat",
                "--",
            )
        )

    plans: list[dict[str, Any]] = []
    for value in args.plan:
        path = resolve_inside(repo, value, "plan")
        metadata = file_metadata(repo, path, git, args.include_hashes)
        plans.append(metadata)
        if not metadata["exists"]:
            violations.append(f"plan_missing:{metadata['path']}")

    capsule_path = task_dir / CAPSULE_NAME
    receipts_path = task_dir / RECEIPTS_NAME
    latest = validation["receipts"].get("latest")
    latest_summary = None
    if isinstance(latest, dict):
        latest_summary = {
            "seq": latest.get("seq"),
            "kind": latest.get("kind"),
            "scope": str(latest.get("scope", ""))[:500],
            "status": latest.get("status"),
            "next": str(latest.get("next", ""))[:500],
        }

    payload: dict[str, Any] = {
        "schema": "RECOVERY_SNAPSHOT_V1",
        "generated_utc": utc_now(),
        "ok": not violations,
        "violations": violations,
        "repo": str(repo),
        "task_dir": display_path(repo, task_dir),
        "git": {
            "available": git["available"],
            "top": git["top"],
            "head": git["head"],
            "branch": git["branch"],
            "status": {
                "counts": status_counts,
                "entries": status_entries[: args.max_paths],
                "truncated": status_counts["total"] > args.max_paths,
            },
            "diff_numstat": {
                "worktree": worktree_numstat[: args.max_paths],
                "index": index_numstat[: args.max_paths],
            },
        },
        "validation": {
            "ok": validation["ok"],
            "issues": validation["issues"],
            "capsule_last_receipt_seq": validation["capsule"]["last_receipt_seq"],
            "latest_receipt_seq": validation["receipts"]["latest_seq"],
        },
        "capsule": file_metadata(repo, capsule_path, git, args.include_hashes),
        "receipts": {
            **file_metadata(repo, receipts_path, git, args.include_hashes),
            "count": validation["receipts"]["count"],
            "latest": latest_summary,
        },
        "plans": plans,
        "limits": {
            "capsule_max_bytes": args.capsule_max_bytes,
            "receipt_line_max_bytes": args.receipt_line_max_bytes,
            "max_paths": args.max_paths,
            "max_output_bytes": args.max_output_bytes,
        },
        "output_truncated": False,
    }
    encoded, truncated = encode_bounded(payload, args.max_output_bytes)
    sys.stdout.buffer.write(encoded)
    return 2 if violations or truncated else 0


def binding_command(args: argparse.Namespace) -> int:
    from session_task_binding import bind_task, unbind_task

    repo = Path(args.repo).resolve(strict=True)
    task_dir = resolve_inside(repo, args.task_dir, "task directory")
    session_id = args.session_id or os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SESSION_ID")
    if not session_id:
        raise RecoveryError("Supply --session-id when the native session environment is unavailable")
    capsule = task_dir / CAPSULE_NAME
    if args.command == "bind":
        locked = capsule_field(capsule.read_text(encoding="utf-8"), "task_identity_locked")
        if locked is None or locked.casefold() not in {"true", "false"}:
            raise RecoveryError("Selected capsule has no valid task_identity_locked field")
        path = bind_task(repo, capsule, session_id, replace=args.replace)
    else:
        path = unbind_task(repo, capsule, session_id)
    emit({"schema": "SESSION_TASK_BINDING_V1", "ok": True, "action": args.command,
          "binding_path": str(path), "capsule_path": str(capsule), "session_id": session_id})
    return 0


def add_common_state_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", default=".", help="Repository or workspace root")
    parser.add_argument("--task-dir", required=True, help="Task directory inside the root")
    parser.add_argument("--capsule-max-bytes", type=int, default=DEFAULT_CAPSULE_MAX_BYTES)
    parser.add_argument(
        "--receipt-line-max-bytes",
        type=int,
        default=DEFAULT_RECEIPT_LINE_MAX_BYTES,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for action in ("bind", "unbind"):
        binding_parser = subparsers.add_parser(action, help=f"{action.title()} the exact current session/task")
        binding_parser.add_argument("--repo", default=".")
        binding_parser.add_argument("--task-dir", required=True)
        binding_parser.add_argument("--session-id", help="Defaults to the native Codex session environment")
        if action == "bind":
            binding_parser.add_argument("--replace", action="store_true", help="Intentionally replace a stale or different task binding")
        binding_parser.set_defaults(handler=binding_command)

    init_parser = subparsers.add_parser("init", help="Create recovery state without overwrite")
    add_common_state_arguments(init_parser)
    init_parser.add_argument("--task-name", required=True)
    init_parser.add_argument("--goal", required=True)
    init_parser.add_argument("--done", action="append", required=True, help="Definition-of-done item")
    init_parser.add_argument("--plan", action="append", default=[], help="Authoritative plan path")
    init_parser.add_argument(
        "--acceptance-matrix",
        required=True,
        help="Acceptance matrix containing a machine-readable '## Closure state' table",
    )
    init_parser.add_argument("--phase", default="PLANNING")
    init_parser.add_argument("--status", choices=VALID_STATUSES, default="TASK_OPEN")
    init_parser.add_argument("--writer", default="current Codex task")
    init_parser.add_argument("--active-slice", default="NOT_STARTED")
    init_parser.add_argument("--last-owner-evidence", default="NONE_RECORDED")
    init_parser.add_argument("--next-action", required=True)
    init_parser.set_defaults(handler=init_command)

    validate_parser = subparsers.add_parser("validate", help="Validate capsule and receipts")
    add_common_state_arguments(validate_parser)
    validate_parser.set_defaults(handler=validate_command)

    snapshot_parser = subparsers.add_parser(
        "snapshot", help="Emit bounded read-only Git and recovery state"
    )
    add_common_state_arguments(snapshot_parser)
    snapshot_parser.add_argument("--plan", action="append", default=[])
    snapshot_parser.add_argument("--max-paths", type=int, default=DEFAULT_MAX_PATHS)
    snapshot_parser.add_argument("--max-output-bytes", type=int, default=DEFAULT_MAX_OUTPUT_BYTES)
    snapshot_parser.add_argument("--include-hashes", action="store_true")
    snapshot_parser.set_defaults(handler=snapshot_command)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.handler(args))
    except (OSError, RecoveryError, ValueError) as error:
        emit(
            {
                "schema": "RECOVERY_TOOL_ERROR_V1",
                "ok": False,
                "error": str(error)[:1500],
            }
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())

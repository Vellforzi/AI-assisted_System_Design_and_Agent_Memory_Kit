#!/usr/bin/env python3
"""Shared strict validation for verified-delivery receipts and Stop finalization."""

from __future__ import annotations

import hashlib
import fnmatch
import importlib.util
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import yaml


HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
KNOWN_GATES = {
    "characterization", "targeted", "baseline", "scope_diff",
    "independent_review", "environment_readiness", "black_box", "build",
    "deploy", "rollback_readback", "finalization",
}
CHECK_KINDS = {
    "characterization", "static", "targeted", "baseline",
    "environment_readiness", "black_box", "build", "deploy",
    "scope_diff", "encoding", "finalization",
}
COMPLETED_TOP_REQUIRED = {
    "schema_version", "task_id", "candidate_state", "baseline",
    "acceptance_contract_sha256", "changed_paths", "active_gates", "checks",
    "independent_review", "unresolved_conditions", "rollback_readback",
    "scope_diff", "final_git",
}
BLOCKED_TOP_REQUIRED = {
    "schema_version", "task_id", "outcome", "baseline",
    "acceptance_contract_sha256", "blocker", "finalization",
}
TOP_ALLOWED = COMPLETED_TOP_REQUIRED | BLOCKED_TOP_REQUIRED | {
    "environment_readiness", "pipeline_metrics", "outcome", "repair_summary", "lifecycle_evidence",
    "evidence_ceiling",
}
METRIC_FIELDS = {
    "wall_clock_seconds", "repair_iterations", "active_gate_count",
    "first_patch_passed", "false_block_count", "owner_wait_seconds",
    "human_touch_seconds", "agent_cost",
}
DECLARATION_REQUIRED = {
    "schema_version", "task_id", "required", "contract", "receipt",
    "required_check_ids", "required_gates", "require_released_lease_at_stop",
    "require_post_commit_clean_receipt", "require_exactly_one_commit",
    "required_commit_message",
}
DECLARATION_V12_REQUIRED = DECLARATION_REQUIRED | {"allowed_final_outcomes"}
FINAL_OUTCOMES = ["task_completed", "task_blocked"]
TERMINAL_BLOCKER_CODES = {
    "same_deterministic_failure_repeated",
    "two_no_progress_iterations",
    "scope_or_capability_expansion_required",
    "external_dependency_unavailable",
    "oracle_missing_or_contradictory",
    "owner_goal_or_protected_behavior_change_required",
    "total_repair_budget_exhausted",
    "authorization_or_integrity_gate",
}
BLOCKER_TERMINAL_CONDITIONS = {
    "same_deterministic_failure_repeated": "repair_budget_exhausted",
    "two_no_progress_iterations": "repair_budget_exhausted",
    "scope_or_capability_expansion_required": "new_authority_required",
    "external_dependency_unavailable": "external_state_change_required",
    "oracle_missing_or_contradictory": "objective_oracle_required",
    "owner_goal_or_protected_behavior_change_required": "new_authority_required",
    "total_repair_budget_exhausted": "repair_budget_exhausted",
    "authorization_or_integrity_gate": "integrity_gate_resolution_required",
}
ORACLE_ARTIFACT_POLICIES = {
    "command": ("command_output", ".log"),
    "state": ("state_snapshot", ".state.json"),
    "trace": ("trace_output", ".trace.jsonl"),
    "diff": ("diff_output", ".diff"),
    "visual": ("visual_output", ".png"),
    "owner": ("owner_gate_receipt", ".owner.json"),
}
REVIEW_DISPOSITIONS = {"confirmed", "rejected", "duplicate", "out_of_scope"}
ARCHITECTURE_REVIEW_COVERS = {"root_cause", "mutation_point", "dependency_neighborhood", "expected_diff", "verification_oracle"}
VERIFICATION_LEVELS = [
    "source_structure", "component_behavior", "cross_component_contract",
    "harness_runtime", "platform_runtime", "owner_acceptance",
]
HIGH_LEVEL_EVIDENCE_CLASSES = {
    "harness_runtime": {"runtime", "owner"},
    "platform_runtime": {"runtime", "owner"},
    "owner_acceptance": {"owner"},
}
VERIFICATION_LEVEL_STATUSES = {"pass", "not_run", "failed", "blocked"}
NUMERIC_CONFIDENCE = re.compile(r"\b(?:100|[1-9]?\d)\s*%")


def failure(code: str, reason: str) -> dict[str, str]:
    return {"code": code, "reason": reason}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_under(root: Path, value: str) -> Path | None:
    try:
        candidate = (root / value).resolve()
        candidate.relative_to(root.resolve())
        return candidate
    except Exception:
        return None


def strict_mapping(
    value: Any,
    required: set[str],
    allowed: set[str],
    location: str,
    failures: list[dict[str, str]],
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        failures.append(failure("MAPPING_REQUIRED", location))
        return None
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - allowed)
    if missing:
        failures.append(failure("NESTED_FIELDS_MISSING", f"{location}:{','.join(missing)}"))
    if unknown:
        failures.append(failure("UNKNOWN_FIELDS", f"{location}:{','.join(unknown)}"))
    return value


def validate_declaration(value: Any) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    version = str(value.get("schema_version") if isinstance(value, dict) else "")
    required = DECLARATION_V12_REQUIRED if version in {"1.2", "1.3"} else DECLARATION_REQUIRED
    declaration = strict_mapping(
        value,
        required,
        required,
        "declaration",
        failures,
    )
    if declaration is None:
        return failures
    if declaration.get("schema_version") not in {"1.0", "1.1", "1.2", "1.3"}:
        failures.append(failure("DECLARATION_SCHEMA_UNSUPPORTED", str(declaration.get("schema_version"))))
    if declaration.get("required") is not True:
        failures.append(failure("DECLARATION_REQUIRED_INVALID", str(declaration.get("required"))))
    for field in ("task_id", "contract", "receipt"):
        if not isinstance(declaration.get(field), str) or not declaration.get(field):
            failures.append(failure("DECLARATION_FIELD_INVALID", field))
    for field in ("required_check_ids", "required_gates"):
        item = declaration.get(field)
        if not isinstance(item, list) or not item or len(item) != len(set(item)):
            failures.append(failure("DECLARATION_LIST_INVALID", field))
    if isinstance(declaration.get("required_gates"), list) and any(
        item not in KNOWN_GATES for item in declaration["required_gates"]
    ):
        failures.append(failure("DECLARATION_GATE_INVALID", str(declaration.get("required_gates"))))
    for field in (
        "require_released_lease_at_stop",
        "require_post_commit_clean_receipt",
        "require_exactly_one_commit",
    ):
        if not isinstance(declaration.get(field), bool):
            failures.append(failure("DECLARATION_BOOLEAN_INVALID", field))
    for field in ("require_released_lease_at_stop", "require_post_commit_clean_receipt"):
        if declaration.get(field) is not True:
            failures.append(failure("DECLARATION_FINALIZATION_BYPASS", field))
    message = declaration.get("required_commit_message")
    if not isinstance(message, str) or (
        declaration.get("require_exactly_one_commit") is True and not message
    ):
        failures.append(failure("DECLARATION_COMMIT_MESSAGE_INVALID", str(message)))
    if version in {"1.2", "1.3"} and declaration.get("allowed_final_outcomes") != FINAL_OUTCOMES:
        failures.append(failure("DECLARATION_FINAL_OUTCOMES_INVALID", str(declaration.get("allowed_final_outcomes"))))
    return failures


def contract_required_sets(
    contract: Path | None,
    failures: list[dict[str, str]],
) -> tuple[set[str], set[str]] | None:
    if contract is None or not contract.is_file():
        failures.append(failure("DECLARATION_CONTRACT_UNAVAILABLE", str(contract)))
        return None
    try:
        value = yaml.safe_load(contract.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(failure("DECLARATION_CONTRACT_INVALID", str(exc)))
        return None
    if not isinstance(value, dict) or value.get("schema_version") not in {"1.1", "1.2", "1.3"}:
        failures.append(failure("DECLARATION_CONTRACT_SCHEMA_UNSUPPORTED", str(value.get("schema_version") if isinstance(value, dict) else type(value).__name__)))
        return None
    criteria = value.get("acceptance_criteria")
    profile = value.get("gate_profile")
    active = profile.get("active") if isinstance(profile, dict) else None
    if (
        not isinstance(criteria, list)
        or not criteria
        or any(not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"] for item in criteria)
        or len({item["id"] for item in criteria}) != len(criteria)
        or not isinstance(active, list)
        or not active
        or len(set(active)) != len(active)
        or any(item not in KNOWN_GATES for item in active)
    ):
        failures.append(failure("DECLARATION_CONTRACT_REQUIREMENTS_INVALID", str(contract)))
        return None
    return {item["id"] for item in criteria}, set(active)


def evidence_path(
    task_root: Path,
    ref: Any,
    contract: Path | None,
    location: str,
    failures: list[dict[str, str]],
) -> None:
    if not isinstance(ref, str) or not ref.strip():
        failures.append(failure("EVIDENCE_REF_INVALID", location))
        return
    path = safe_under(task_root, ref)
    if path is None or not path.is_file():
        failures.append(failure("EVIDENCE_REF_MISSING", f"{location}:{ref}"))
        return
    if path.stat().st_size == 0:
        failures.append(failure("EVIDENCE_REF_EMPTY", f"{location}:{ref}"))
    if contract is not None and path.stat().st_mtime + 1 < contract.stat().st_mtime:
        failures.append(failure("EVIDENCE_REF_STALE", f"{location}:{ref}"))


def validate_pass_oracle_receipt(
    task_root: Path,
    oracle: dict[str, Any],
    evidence_ref: Any,
    contract: Path | None,
    location: str,
    failures: list[dict[str, str]],
) -> Path | None:
    """Validate a deciding PASS receipt and return its identity-protected artifact."""
    evidence_path(task_root, evidence_ref, contract, location, failures)
    receipt_path = safe_under(task_root, str(evidence_ref or ""))
    if receipt_path is None or not receipt_path.is_file():
        return None
    try:
        value = json.loads(receipt_path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(failure("ORACLE_RECEIPT_INVALID", f"{location}:{exc}"))
        return None
    fields = {
        "schema_version", "oracle_id", "oracle_kind", "verification_level",
        "check", "pass_condition", "status", "observed", "artifact_kind",
        "producer", "artifact_ref", "artifact_sha256",
    }
    receipt = strict_mapping(value, fields, fields, f"{location}.oracle_receipt", failures)
    if receipt is None:
        return None
    if (
        receipt.get("schema_version") != "1.0"
        or receipt.get("oracle_id") != oracle.get("id")
        or receipt.get("oracle_kind") != oracle.get("kind")
        or receipt.get("verification_level") != oracle.get("verification_level")
        or receipt.get("check") != oracle.get("check")
        or receipt.get("pass_condition") != oracle.get("pass_condition")
        or receipt.get("status") != "pass"
        or not isinstance(receipt.get("observed"), str)
        or not receipt.get("observed", "").strip()
        or not isinstance(receipt.get("producer"), str)
        or not receipt.get("producer", "").strip()
    ):
        failures.append(failure("ORACLE_RECEIPT_MISMATCH", str(oracle.get("id"))))
    artifact_ref = receipt.get("artifact_ref")
    evidence_path(task_root, artifact_ref, contract, f"{location}.artifact", failures)
    artifact_path = safe_under(task_root, str(artifact_ref or ""))
    policy = ORACLE_ARTIFACT_POLICIES.get(str(oracle.get("kind") or ""))
    if policy is None or receipt.get("artifact_kind") != policy[0] or not str(artifact_ref or "").endswith(policy[1]):
        failures.append(failure("ORACLE_ARTIFACT_KIND_INVALID", f"{oracle.get('id')}:{artifact_ref}"))
    if artifact_path is None or not artifact_path.is_file():
        return None
    artifact_hash = receipt.get("artifact_sha256")
    if not isinstance(artifact_hash, str) or not HEX64.fullmatch(artifact_hash) or sha256_file(artifact_path) != artifact_hash:
        failures.append(failure("ORACLE_ARTIFACT_HASH_INVALID", f"{oracle.get('id')}:{artifact_ref}"))
    try:
        if artifact_path.stat().st_nlink > 1:
            failures.append(failure("ORACLE_ARTIFACT_LINK_COUNT_INVALID", str(artifact_ref)))
        control_paths = [receipt_path]
        if contract is not None and contract.is_file():
            control_paths.append(contract)
        if any(artifact_path.samefile(control_path) for control_path in control_paths):
            failures.append(failure("ORACLE_ARTIFACT_ALIAS", str(artifact_ref)))
    except OSError as exc:
        failures.append(failure("ORACLE_FILE_IDENTITY_UNAVAILABLE", f"{artifact_ref}:{exc}"))
    return artifact_path


def validate_terminal_blocker_evidence(
    task_root: Path,
    ref: Any,
    code: Any,
    contract: Path | None,
    failures: list[dict[str, str]],
    *,
    receipt_path: Path | None = None,
    control_refs: list[Any] | None = None,
) -> None:
    """Require machine-checkable facts behind every terminal blocker claim."""
    path = safe_under(task_root, str(ref or ""))
    evidence_path(task_root, ref, contract, "blocker", failures)
    if path is None or not path.is_file():
        return
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(failure("BLOCKER_EVIDENCE_INVALID", str(exc)))
        return
    proof = strict_mapping(
        value,
        {"schema_version", "blocker_code", "terminal_condition", "facts", "remaining_in_scope_actions"},
        {"schema_version", "blocker_code", "terminal_condition", "facts", "remaining_in_scope_actions"},
        "blocker_evidence",
        failures,
    )
    if proof is None:
        return
    expected_condition = BLOCKER_TERMINAL_CONDITIONS.get(str(code))
    if (
        proof.get("schema_version") != "1.0"
        or proof.get("blocker_code") != code
        or proof.get("terminal_condition") != expected_condition
        or proof.get("remaining_in_scope_actions") != []
    ):
        failures.append(failure("BLOCKER_EVIDENCE_MISMATCH", str(code)))
    facts = proof.get("facts")
    if not isinstance(facts, list) or not facts:
        failures.append(failure("BLOCKER_OBJECTIVE_FACTS_MISSING", str(code)))
        return
    try:
        contract_value = yaml.safe_load(contract.read_text(encoding="utf-8")) if contract is not None else {}
    except Exception:
        contract_value = {}
    contract_oracles = {
        item.get("id"): item
        for item in (contract_value.get("oracles") if isinstance(contract_value, dict) else []) or []
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for index, raw in enumerate(facts):
        fact = strict_mapping(
            raw,
            {"id", "oracle_id", "observation", "evidence_ref"},
            {"id", "oracle_id", "observation", "evidence_ref"},
            f"blocker_evidence.facts[{index}]",
            failures,
        )
        if fact is None:
            continue
        if any(not isinstance(fact.get(field), str) or not fact.get(field).strip() for field in ("id", "oracle_id", "observation", "evidence_ref")):
            failures.append(failure("BLOCKER_OBJECTIVE_FACT_INVALID", str(index)))
            continue
        oracle = contract_oracles.get(fact.get("oracle_id"))
        if not isinstance(oracle, dict) or oracle.get("evidence_ref") != fact.get("evidence_ref"):
            failures.append(failure("BLOCKER_FACT_ORACLE_UNRESOLVED", str(fact.get("oracle_id"))))
            continue
        evidence_path(task_root, fact.get("evidence_ref"), contract, f"blocker_evidence.facts[{index}]", failures)
        oracle_path = safe_under(task_root, fact.get("evidence_ref"))
        if oracle_path is None or not oracle_path.is_file():
            continue
        try:
            oracle_receipt_value = json.loads(oracle_path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(failure("BLOCKER_ORACLE_RECEIPT_INVALID", str(exc)))
            continue
        oracle_receipt = strict_mapping(
            oracle_receipt_value,
            {"schema_version", "oracle_id", "oracle_kind", "check", "pass_condition", "status", "observed", "artifact_kind", "producer", "artifact_ref", "artifact_sha256"},
            {"schema_version", "oracle_id", "oracle_kind", "check", "pass_condition", "status", "observed", "artifact_kind", "producer", "artifact_ref", "artifact_sha256"},
            f"blocker_oracle_receipt[{index}]",
            failures,
        )
        if oracle_receipt is None:
            continue
        if (
            oracle_receipt.get("schema_version") != "1.0"
            or oracle_receipt.get("oracle_id") != fact.get("oracle_id")
            or oracle_receipt.get("oracle_kind") != oracle.get("kind")
            or oracle_receipt.get("check") != oracle.get("check")
            or oracle_receipt.get("pass_condition") != oracle.get("pass_condition")
            or oracle_receipt.get("status") not in {"fail", "blocked"}
            or oracle_receipt.get("observed") != fact.get("observation")
            or not isinstance(oracle_receipt.get("producer"), str)
            or not oracle_receipt.get("producer").strip()
        ):
            failures.append(failure("BLOCKER_ORACLE_RECEIPT_MISMATCH", str(fact.get("oracle_id"))))
        artifact_ref = oracle_receipt.get("artifact_ref")
        evidence_path(task_root, artifact_ref, contract, f"blocker_oracle_receipt[{index}].artifact", failures)
        artifact_path = safe_under(task_root, str(artifact_ref or ""))
        policy = ORACLE_ARTIFACT_POLICIES.get(str(oracle.get("kind")))
        if policy is None or oracle_receipt.get("artifact_kind") != policy[0] or not str(artifact_ref or "").endswith(policy[1]):
            failures.append(failure("BLOCKER_ORACLE_ARTIFACT_KIND_INVALID", str(artifact_ref)))
        control_paths = {item.resolve() for item in (path, oracle_path, contract, receipt_path) if item is not None and item.is_file()}
        for control_ref in control_refs or []:
            control_path = safe_under(task_root, str(control_ref or ""))
            if control_path is not None and control_path.is_file():
                control_paths.add(control_path.resolve())
        if artifact_path is not None and artifact_path.is_file():
            try:
                if artifact_path.stat().st_nlink != 1:
                    failures.append(failure("BLOCKER_ORACLE_ARTIFACT_LINK_COUNT_INVALID", str(artifact_ref)))
                if any(artifact_path.samefile(control_path) for control_path in control_paths):
                    failures.append(failure("BLOCKER_ORACLE_ARTIFACT_ALIAS", str(artifact_ref)))
            except OSError as exc:
                failures.append(failure("BLOCKER_ORACLE_FILE_IDENTITY_UNAVAILABLE", f"{artifact_ref}:{exc}"))
        artifact_hash = oracle_receipt.get("artifact_sha256")
        if (
            artifact_path is None
            or not artifact_path.is_file()
            or not isinstance(artifact_hash, str)
            or not HEX64.fullmatch(artifact_hash)
            or sha256_file(artifact_path) != artifact_hash
        ):
            failures.append(failure("BLOCKER_ORACLE_ARTIFACT_HASH_MISMATCH", str(artifact_ref)))


def validate_v12_contract_model(
    contract: Path | None,
    failures: list[dict[str, str]],
) -> None:
    """Run the canonical contract validator before accepting a 1.2/1.3 outcome."""
    if contract is None or not contract.is_file():
        failures.append(failure("CONTRACT_VALIDATION_UNAVAILABLE", str(contract)))
        return
    try:
        value = yaml.safe_load(contract.read_text(encoding="utf-8"))
        validator_path = Path(__file__).resolve().with_name("validate_verified_delivery_contract.py")
        spec = importlib.util.spec_from_file_location("verified_delivery_contract_validator", validator_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {validator_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not isinstance(value, dict):
            raise ValueError("contract root must be a mapping")
        failures.extend(module.validate(value))
    except Exception as exc:
        failures.append(failure("CONTRACT_VALIDATION_ERROR", str(exc)))


def run_git(root: Path, *args: str, env: dict[str, str] | None = None) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        env=env,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)}: {detail}")
    return completed.stdout


def candidate_tree_without_receipt(root: Path, receipt_rel: str) -> str:
    with tempfile.TemporaryDirectory(prefix="verified-delivery-index-") as raw:
        env = dict(os.environ)
        env["GIT_INDEX_FILE"] = str(Path(raw) / "index")
        run_git(root, "read-tree", "HEAD", env=env)
        run_git(root, "rm", "-q", "--cached", "--ignore-unmatch", "--", receipt_rel, env=env)
        return run_git(root, "write-tree", env=env).decode("ascii").strip()


def validate_git_finalization(
    value: dict[str, Any],
    root: Path,
    task_root: Path,
    declaration: dict[str, Any],
    lease: dict[str, Any],
    receipt_path: Path,
    failures: list[dict[str, str]],
) -> None:
    baseline = str(value.get("baseline") or "")
    try:
        head = run_git(root, "rev-parse", "HEAD").decode("ascii").strip()
        run_git(root, "cat-file", "-e", f"{baseline}^{{commit}}")
        receipt_rel = receipt_path.resolve().relative_to(root.resolve()).as_posix()
        exclusion = f":(exclude){receipt_rel}"
        actual_paths = [
            item.decode("utf-8", errors="surrogateescape")
            for item in run_git(root, "diff", "--name-only", "-z", f"{baseline}..HEAD", "--", ".", exclusion).split(b"\0")
            if item
        ]
        expected_paths = value.get("changed_paths") if isinstance(value.get("changed_paths"), list) else []
        if sorted(actual_paths) != sorted(expected_paths):
            failures.append(failure("CHANGED_PATHS_GIT_MISMATCH", json.dumps({"actual": sorted(actual_paths), "receipt": sorted(expected_paths)}, ensure_ascii=True)))
        actual_diff_hash = hashlib.sha256(
            run_git(root, "diff", "--binary", "--no-ext-diff", f"{baseline}..HEAD", "--", ".", exclusion)
        ).hexdigest()
        if value.get("scope_diff", {}).get("diff_sha256") != actual_diff_hash:
            failures.append(failure("DIFF_SHA256_GIT_MISMATCH", actual_diff_hash))
        actual_tree = candidate_tree_without_receipt(root, receipt_rel)
        if value.get("final_git", {}).get("candidate_tree") != actual_tree:
            failures.append(failure("CANDIDATE_TREE_GIT_MISMATCH", actual_tree))
        status = run_git(root, "status", "--porcelain=v1", "-z")
        if status:
            failures.append(failure("WORKTREE_NOT_CLEAN", status.decode("utf-8", errors="replace")))
        if value.get("final_git", {}).get("worktree_status") != "clean_after_commit":
            failures.append(failure("WORKTREE_STATUS_NOT_FINAL", str(value.get("final_git", {}).get("worktree_status"))))
        if declaration.get("require_exactly_one_commit") is True:
            count = int(run_git(root, "rev-list", "--count", f"{baseline}..HEAD").decode("ascii").strip())
            if count != 1:
                failures.append(failure("COMMIT_COUNT_MISMATCH", str(count)))
        expected_message = declaration.get("required_commit_message")
        if expected_message:
            subject = run_git(root, "log", "-1", "--format=%s").decode("utf-8", errors="replace").strip()
            if subject != expected_message:
                failures.append(failure("COMMIT_MESSAGE_MISMATCH", subject))
    except Exception as exc:
        failures.append(failure("GIT_FINALIZATION_ERROR", str(exc)))
        return

    if declaration.get("require_released_lease_at_stop") is True and lease.get("state") != "released":
        failures.append(failure("LEASE_NOT_RELEASED", str(lease.get("state"))))
    final_git = value.get("final_git") if isinstance(value.get("final_git"), dict) else {}
    post_ref = final_git.get("post_commit_receipt")
    post_path = safe_under(root, str(post_ref or ""))
    try:
        post = json.loads(post_path.read_text(encoding="utf-8")) if post_path else {}
    except Exception:
        post = {}
    if declaration.get("require_post_commit_clean_receipt") is True:
        post = strict_mapping(
            post,
            {"task_id", "commit", "worktree_status", "head_matches", "git_status_clean"},
            {"schema_version", "task_id", "commit", "worktree_status", "head_matches", "git_status_clean"},
            "post_commit_receipt",
            failures,
        ) or {}
        if (
            post.get("task_id") != declaration.get("task_id")
            or post.get("commit") != head
            or post.get("worktree_status") != "clean_after_commit"
            or post.get("head_matches") is not True
            or post.get("git_status_clean") is not True
        ):
            failures.append(failure("POST_COMMIT_CLEAN_RECEIPT_INVALID", str(post_ref)))


def contract_total_repair_budget(contract: Path | None) -> int | None:
    if contract is None or not contract.is_file():
        return None
    try:
        value = yaml.safe_load(contract.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(value, dict):
        return None
    repair = value.get("repair_policy")
    total = repair.get("max_total_iterations") if isinstance(repair, dict) else None
    return total if isinstance(total, int) and not isinstance(total, bool) else None


def changed_worktree_paths(root: Path) -> list[str]:
    paths: set[str] = set()
    for args in (("diff", "--name-only", "-z"), ("diff", "--cached", "--name-only", "-z"), ("ls-files", "--others", "--exclude-standard", "-z")):
        for item in run_git(root, *args).split(b"\0"):
            if item:
                paths.add(item.decode("utf-8", errors="surrogateescape").replace("\\", "/"))
    return sorted(paths)


def path_in_declared_scope(path: str, patterns: Any) -> bool:
    if not isinstance(patterns, list):
        return False
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatchcase(normalized.casefold(), str(pattern).replace("\\", "/").casefold()) for pattern in patterns)


def validate_blocked_runtime(
    value: dict[str, Any],
    root: Path,
    declaration: dict[str, Any],
    lease: dict[str, Any],
    failures: list[dict[str, str]],
) -> None:
    try:
        head = run_git(root, "rev-parse", "HEAD").decode("ascii").strip()
        baseline = str(value.get("baseline") or "")
        if head != baseline:
            failures.append(failure("BLOCKED_HEAD_BASELINE_MISMATCH", f"{head}:{baseline}"))
        if lease.get("baseline_ref") != baseline:
            failures.append(failure("BLOCKED_LEASE_BASELINE_MISMATCH", str(lease.get("baseline_ref"))))
        if lease.get("state") != "released":
            failures.append(failure("LEASE_NOT_RELEASED", str(lease.get("state"))))
        finalization = value.get("finalization") if isinstance(value.get("finalization"), dict) else {}
        if finalization.get("lease_state") != "released":
            failures.append(failure("BLOCKED_FINALIZATION_LEASE_INVALID", str(finalization.get("lease_state"))))
        paths = changed_worktree_paths(root)
        status = finalization.get("worktree_status")
        if status == "clean" and paths:
            failures.append(failure("BLOCKED_WORKTREE_NOT_CLEAN", json.dumps(paths, ensure_ascii=True)))
        elif status == "preserved_in_scope_changes":
            if not paths:
                failures.append(failure("BLOCKED_PRESERVED_CHANGES_MISSING", "worktree is clean"))
            outside = [item for item in paths if not path_in_declared_scope(item, lease.get("write_scope"))]
            if outside:
                failures.append(failure("BLOCKED_OUT_OF_SCOPE_CHANGES", json.dumps(outside, ensure_ascii=True)))
        if declaration.get("require_released_lease_at_stop") is not True:
            failures.append(failure("BLOCKED_RELEASE_REQUIREMENT_MISSING", "declaration"))
    except Exception as exc:
        failures.append(failure("BLOCKED_RUNTIME_FINALIZATION_ERROR", str(exc)))


def validate_blocked_receipt(
    value: dict[str, Any],
    contract: Path | None,
    *,
    repo_root: Path | None,
    task_root: Path | None,
    declaration: dict[str, Any],
    lease: dict[str, Any] | None,
    verify_runtime: bool,
    receipt_path: Path | None,
) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    validate_v12_contract_model(contract, failures)
    missing = sorted(BLOCKED_TOP_REQUIRED - set(value))
    version = str(value.get("schema_version") or "")
    allowed_blocked = BLOCKED_TOP_REQUIRED | {"pipeline_metrics"}
    if version == "1.3":
        allowed_blocked |= {"lifecycle_evidence", "evidence_ceiling"}
    unknown = sorted(set(value) - allowed_blocked)
    if missing:
        failures.append(failure("BLOCKED_RECEIPT_FIELDS_MISSING", ", ".join(missing)))
    if unknown:
        failures.append(failure("UNKNOWN_FIELDS", f"blocked_receipt:{','.join(unknown)}"))
    if version not in {"1.2", "1.3"} or value.get("outcome") != "task_blocked":
        failures.append(failure("BLOCKED_OUTCOME_INVALID", f"{value.get('schema_version')}:{value.get('outcome')}"))
    if not isinstance(value.get("task_id"), str) or not value.get("task_id"):
        failures.append(failure("TASK_ID_INVALID", str(value.get("task_id"))))
    if not isinstance(value.get("baseline"), str) or not HEX40.fullmatch(value["baseline"]):
        failures.append(failure("BASELINE_INVALID", str(value.get("baseline"))))
    contract_hash = value.get("acceptance_contract_sha256")
    if not isinstance(contract_hash, str) or not HEX64.fullmatch(contract_hash):
        failures.append(failure("CONTRACT_HASH_INVALID", str(contract_hash)))
    elif contract is not None and (not contract.is_file() or sha256_file(contract) != contract_hash):
        failures.append(failure("CONTRACT_HASH_MISMATCH", str(contract)))

    contract_value: dict[str, Any] = {}
    if contract is not None and contract.is_file():
        try:
            loaded = yaml.safe_load(contract.read_text(encoding="utf-8"))
            contract_value = loaded if isinstance(loaded, dict) else {}
        except Exception as exc:
            failures.append(failure("BLOCKED_CONTRACT_INVALID", str(exc)))
        if contract_value.get("schema_version") != version:
            failures.append(failure("BLOCKED_CONTRACT_SCHEMA_UNSUPPORTED", str(contract_value.get("schema_version"))))
        if contract_value.get("task_id") != value.get("task_id"):
            failures.append(failure("BLOCKED_CONTRACT_TASK_MISMATCH", str(contract_value.get("task_id"))))
        lifecycle = contract_value.get("lifecycle_policy")
        if not isinstance(lifecycle, dict) or lifecycle.get("final_outcomes") != FINAL_OUTCOMES:
            failures.append(failure("BLOCKED_CONTRACT_OUTCOMES_INVALID", "lifecycle_policy.final_outcomes"))
    if version == "1.3":
        validate_evidence_ceiling(
            value,
            contract_value,
            task_root=task_root,
            contract=contract,
            outcome="task_blocked",
            failures=failures,
        )

    blocker = strict_mapping(
        value.get("blocker"),
        {"code", "terminal", "recoverable", "summary", "why_unrecoverable", "evidence_ref", "required_owner_action", "repair_iterations", "recovery_attempts", "remaining_in_scope_actions"},
        {"code", "terminal", "recoverable", "summary", "why_unrecoverable", "evidence_ref", "required_owner_action", "repair_iterations", "recovery_attempts", "remaining_in_scope_actions"},
        "blocker",
        failures,
    )
    if blocker is not None:
        if blocker.get("code") not in TERMINAL_BLOCKER_CODES:
            failures.append(failure("BLOCKER_CODE_INVALID", str(blocker.get("code"))))
        if blocker.get("terminal") is not True or blocker.get("recoverable") is not False:
            failures.append(failure("BLOCKER_NOT_TERMINAL", str(blocker.get("code"))))
        for field in ("summary", "why_unrecoverable", "evidence_ref", "required_owner_action"):
            if not isinstance(blocker.get(field), str) or not blocker.get(field).strip():
                failures.append(failure("BLOCKER_FIELD_INVALID", field))
        iterations = blocker.get("repair_iterations")
        if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 0:
            failures.append(failure("BLOCKER_REPAIR_ITERATIONS_INVALID", str(iterations)))
            iterations = 0
        budget = contract_total_repair_budget(contract)
        if budget is None or iterations > budget:
            failures.append(failure("BLOCKER_REPAIR_BUDGET_EXCEEDED", f"budget={budget},iterations={iterations}"))
        if blocker.get("remaining_in_scope_actions") != []:
            failures.append(failure("USEFUL_IN_SCOPE_WORK_REMAINS", str(blocker.get("remaining_in_scope_actions"))))
        attempts = blocker.get("recovery_attempts")
        if not isinstance(attempts, list):
            failures.append(failure("RECOVERY_ATTEMPTS_INVALID", "not a list"))
            attempts = []
        fingerprints: list[str] = []
        results: list[str] = []
        for index, raw in enumerate(attempts):
            attempt = strict_mapping(raw, {"id", "failure_fingerprint", "action", "result", "evidence_ref"}, {"id", "failure_fingerprint", "action", "result", "evidence_ref"}, f"recovery_attempts[{index}]", failures)
            if attempt is None:
                continue
            if any(not isinstance(attempt.get(field), str) or not attempt.get(field).strip() for field in ("id", "failure_fingerprint", "action", "result", "evidence_ref")):
                failures.append(failure("RECOVERY_ATTEMPT_FIELD_INVALID", str(index)))
            fingerprints.append(str(attempt.get("failure_fingerprint") or ""))
            results.append(str(attempt.get("result") or ""))
            if task_root is not None:
                evidence_path(task_root, attempt.get("evidence_ref"), contract, f"recovery_attempts[{index}]", failures)
        if len(attempts) < iterations:
            failures.append(failure("RECOVERY_ATTEMPT_COUNT_MISMATCH", f"iterations={iterations},attempts={len(attempts)}"))
        code = blocker.get("code")
        repair = contract_value.get("repair_policy") if isinstance(contract_value, dict) else None
        triggers = repair.get("terminal_triggers") if isinstance(repair, dict) else None
        if not isinstance(triggers, list) or code not in triggers:
            failures.append(failure("BLOCKER_NOT_DECLARED_BY_CONTRACT", str(code)))
        same_failure_threshold = repair.get("max_same_failure_repeats") if isinstance(repair, dict) else None
        no_progress_threshold = repair.get("max_no_progress_iterations") if isinstance(repair, dict) else None
        if code == "same_deterministic_failure_repeated" and (
            not isinstance(same_failure_threshold, int)
            or iterations < same_failure_threshold
            or len(fingerprints) < same_failure_threshold
            or len(set(fingerprints[-same_failure_threshold:])) != 1
        ):
            failures.append(failure("REPEATED_FAILURE_NOT_PROVEN", str(fingerprints)))
        if code == "two_no_progress_iterations" and (
            not isinstance(no_progress_threshold, int)
            or iterations < no_progress_threshold
            or len(results) < no_progress_threshold
            or any(item != "no_progress" for item in results[-no_progress_threshold:])
        ):
            failures.append(failure("NO_PROGRESS_NOT_PROVEN", str(results)))
        if code == "total_repair_budget_exhausted":
            if budget is None or iterations != budget or len(attempts) < budget:
                failures.append(failure("TOTAL_REPAIR_BUDGET_NOT_PROVEN", f"budget={budget},iterations={iterations},attempts={len(attempts)}"))
        if task_root is not None:
            finalization_value = value.get("finalization") if isinstance(value.get("finalization"), dict) else {}
            control_refs = [finalization_value.get("evidence_ref")]
            control_refs.extend(
                item.get("evidence_ref")
                for item in attempts
                if isinstance(item, dict)
            )
            validate_terminal_blocker_evidence(
                task_root,
                blocker.get("evidence_ref"),
                code,
                contract,
                failures,
                receipt_path=receipt_path,
                control_refs=control_refs,
            )

    finalization = strict_mapping(
        value.get("finalization"),
        {"lease_state", "worktree_status", "evidence_ref"},
        {"lease_state", "worktree_status", "evidence_ref"},
        "finalization",
        failures,
    )
    if finalization is not None:
        if finalization.get("lease_state") != "released" or finalization.get("worktree_status") not in {"clean", "preserved_in_scope_changes"} or not isinstance(finalization.get("evidence_ref"), str) or not finalization.get("evidence_ref"):
            failures.append(failure("BLOCKED_FINALIZATION_INVALID", "finalization"))
        if task_root is not None:
            evidence_path(task_root, finalization.get("evidence_ref"), contract, "finalization", failures)

    metrics = value.get("pipeline_metrics")
    if metrics is not None:
        metrics = strict_mapping(metrics, set(), METRIC_FIELDS, "pipeline_metrics", failures)
        if metrics is not None:
            for key, item in metrics.items():
                if key == "first_patch_passed":
                    if not isinstance(item, bool):
                        failures.append(failure("PIPELINE_METRIC_INVALID", key))
                elif key in {"repair_iterations", "active_gate_count", "false_block_count"}:
                    if not isinstance(item, int) or isinstance(item, bool) or item < 0:
                        failures.append(failure("PIPELINE_METRIC_INVALID", key))
                elif not isinstance(item, (int, float)) or isinstance(item, bool) or item < 0:
                    failures.append(failure("PIPELINE_METRIC_INVALID", key))

    if declaration:
        failures.extend(validate_declaration(declaration))
        if declaration.get("task_id") != value.get("task_id"):
            failures.append(failure("DECLARATION_TASK_MISMATCH", str(value.get("task_id"))))
        if declaration.get("allowed_final_outcomes") != FINAL_OUTCOMES:
            failures.append(failure("TASK_BLOCKED_NOT_DECLARED", str(declaration.get("allowed_final_outcomes"))))
    if version == "1.3":
        _, lifecycle = validate_bound_json_artifact(task_root, value.get("lifecycle_evidence"), "lifecycle_evidence_binding", contract, failures)
        _, ledger = validate_bound_json_artifact(task_root, lifecycle.get("repair_ledger"), "repair_ledger_binding", contract, failures) if lifecycle else (None, {})
        repair_iterations = value.get("blocker", {}).get("repair_iterations") if isinstance(value.get("blocker"), dict) else None
        cycles = ledger.get("cycles") if isinstance(ledger.get("cycles"), list) else []
        confirmed = [
            str(item.get("finding_fingerprint") or "")
            for item in cycles
            if isinstance(item, dict) and item.get("adjudication") == "confirmed"
        ]
        run = 0
        max_no_progress = 0
        for item in cycles:
            if isinstance(item, dict) and item.get("measurable_progress") is False:
                run += 1
                max_no_progress = max(max_no_progress, run)
            else:
                run = 0
        validate_lifecycle_evidence(
            value,
            contract,
            repo_root=repo_root,
            task_root=task_root,
            lease=lease,
            verify_runtime=verify_runtime,
            failures=failures,
            outcome="task_blocked",
            repair_summary_override={
                "iterations": repair_iterations,
                "same_failure_repeats": max(0, len(confirmed) - len(set(confirmed))),
                "consecutive_no_progress": max_no_progress,
            },
        )
    if verify_runtime:
        if repo_root is None or task_root is None or lease is None:
            failures.append(failure("RUNTIME_CONTEXT_MISSING", "repo_root/task_root/lease"))
        else:
            validate_blocked_runtime(value, repo_root, declaration, lease, failures)
    return failures


def validate_review_adjudication(
    task_root: Path,
    ref: Any,
    contract: Path | None,
    failures: list[dict[str, str]],
) -> None:
    path = safe_under(task_root, str(ref or ""))
    evidence_path(task_root, ref, contract, "review_adjudication", failures)
    if path is None or not path.is_file():
        return
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(failure("REVIEW_ADJUDICATION_INVALID", str(exc)))
        return
    review = strict_mapping(value, {"reviewer_role_count", "findings"}, {"reviewer_role_count", "findings"}, "review_adjudication", failures)
    if review is None:
        return
    if review.get("reviewer_role_count") != 1 or not isinstance(review.get("findings"), list):
        failures.append(failure("REVIEWER_ROLE_COUNT_INVALID", str(review.get("reviewer_role_count"))))
        return
    seen: set[str] = set()
    for index, raw in enumerate(review["findings"]):
        finding = strict_mapping(
            raw,
            {"id", "severity", "disposition", "rationale", "evidence_ref", "repair_ref", "recheck_ref"},
            {"id", "severity", "disposition", "rationale", "evidence_ref", "repair_ref", "recheck_ref"},
            f"review_adjudication.findings[{index}]",
            failures,
        )
        if finding is None:
            continue
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or not finding_id or finding_id in seen:
            failures.append(failure("REVIEW_FINDING_ID_INVALID", str(finding_id)))
        seen.add(str(finding_id))
        if finding.get("severity") not in {"high", "medium", "low"} or finding.get("disposition") not in REVIEW_DISPOSITIONS:
            failures.append(failure("REVIEW_FINDING_DISPOSITION_INVALID", str(finding_id)))
        if not isinstance(finding.get("rationale"), str) or not finding.get("rationale").strip():
            failures.append(failure("REVIEW_FINDING_RATIONALE_MISSING", str(finding_id)))
        evidence_path(task_root, finding.get("evidence_ref"), contract, f"review_finding[{index}]", failures)
        if finding.get("disposition") == "confirmed":
            evidence_path(task_root, finding.get("repair_ref"), contract, f"review_repair[{index}]", failures)
            evidence_path(task_root, finding.get("recheck_ref"), contract, f"review_recheck[{index}]", failures)
        elif finding.get("disposition") == "out_of_scope":
            failures.append(failure("OUT_OF_SCOPE_CONFIRMED_FINDING_OPEN", str(finding_id)))
        elif finding.get("repair_ref") or finding.get("recheck_ref"):
            failures.append(failure("UNCONFIRMED_FINDING_REPAIRED", str(finding_id)))


def load_contract_value(contract: Path | None, failures: list[dict[str, str]]) -> dict[str, Any]:
    if contract is None or not contract.is_file():
        return {}
    try:
        value = yaml.safe_load(contract.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception as exc:
        failures.append(failure("CONTRACT_LOAD_ERROR", str(exc)))
        return {}


def validate_evidence_ceiling(
    receipt: dict[str, Any],
    contract_value: dict[str, Any],
    *,
    task_root: Path | None,
    contract: Path | None,
    outcome: str,
    failures: list[dict[str, str]],
) -> None:
    """Bind every PASS level to deciding oracle receipts and structured production evidence."""
    target = contract_value.get("verification_target")
    extensions = contract_value.get("extensions") if isinstance(contract_value.get("extensions"), dict) else {}
    profile = extensions.get("cross_component_code_proof") if isinstance(extensions, dict) else None
    ceiling = receipt.get("evidence_ceiling")
    if target is None and profile is None and ceiling is None:
        return
    if target not in VERIFICATION_LEVELS:
        failures.append(failure("VERIFICATION_TARGET_INVALID", str(target)))
        return
    fields = {
        "requested_target", "levels", "level_oracle_results", "verified_claim",
        "residual_condition", "production_path_evidence", "lifecycle_evidence",
        "boundary_evidence", "oracle_strength_evidence",
    }
    ceiling = strict_mapping(ceiling, fields, fields, "evidence_ceiling", failures)
    if ceiling is None:
        return
    if ceiling.get("requested_target") != target:
        failures.append(failure("EVIDENCE_TARGET_MISMATCH", f"{target}:{ceiling.get('requested_target')}"))
    levels = strict_mapping(ceiling.get("levels"), set(VERIFICATION_LEVELS), set(VERIFICATION_LEVELS), "evidence_ceiling.levels", failures) or {}
    level_results = strict_mapping(ceiling.get("level_oracle_results"), set(VERIFICATION_LEVELS), set(VERIFICATION_LEVELS), "evidence_ceiling.level_oracle_results", failures) or {}
    oracle_by_id = {
        item.get("id"): item
        for item in (contract_value.get("oracles") if isinstance(contract_value.get("oracles"), list) else [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    artifact_by_oracle: dict[str, Path | None] = {}
    for level in VERIFICATION_LEVELS:
        status = levels.get(level)
        if status not in VERIFICATION_LEVEL_STATUSES:
            failures.append(failure("EVIDENCE_LEVEL_STATUS_INVALID", f"{level}:{status}"))
        results = level_results.get(level)
        if not isinstance(results, list) or len(results) != len(set(results)) or any(not isinstance(item, str) or not item for item in results):
            failures.append(failure("EVIDENCE_LEVEL_ORACLE_RESULTS_INVALID", level))
            results = []
        if status == "pass" and not results:
            failures.append(failure("EVIDENCE_LEVEL_DECIDING_ORACLE_MISSING", level))
        if status != "pass" and results:
            failures.append(failure("EVIDENCE_LEVEL_ORACLE_RESULTS_UNEXPECTED", level))
        for oracle_id in results:
            oracle = oracle_by_id.get(oracle_id)
            if not isinstance(oracle, dict) or oracle.get("authorized") is not True or oracle.get("verification_level") != level:
                failures.append(failure("EVIDENCE_LEVEL_ORACLE_MISMATCH", f"{level}:{oracle_id}"))
                continue
            allowed_classes = HIGH_LEVEL_EVIDENCE_CLASSES.get(level)
            if allowed_classes is not None and oracle.get("evidence_class") not in allowed_classes:
                failures.append(failure("EVIDENCE_LEVEL_ORACLE_CLASS_INVALID", f"{level}:{oracle_id}:{oracle.get('evidence_class')}"))
                continue
            if level == "owner_acceptance" and oracle.get("kind") != "owner":
                failures.append(failure("OWNER_ACCEPTANCE_ORACLE_KIND_INVALID", f"{oracle_id}:{oracle.get('kind')}"))
                continue
            if task_root is None:
                failures.append(failure("EVIDENCE_TASK_ROOT_REQUIRED", oracle_id))
                continue
            artifact_by_oracle[oracle_id] = validate_pass_oracle_receipt(
                task_root, oracle, oracle.get("evidence_ref"), contract,
                f"evidence_ceiling.level_oracle_results.{level}.{oracle_id}", failures,
            )
    target_index = VERIFICATION_LEVELS.index(target)
    if outcome == "task_completed":
        for level in VERIFICATION_LEVELS[:target_index + 1]:
            if levels.get(level) != "pass":
                failures.append(failure("REQUESTED_EVIDENCE_LEVEL_NOT_PROVEN", f"{level}:{levels.get(level)}"))
    elif levels.get(target) == "pass":
        failures.append(failure("BLOCKED_RECEIPT_TARGET_ALREADY_PROVEN", target))
    for field in ("verified_claim", "residual_condition"):
        text = ceiling.get(field)
        if not isinstance(text, str) or not text.strip():
            failures.append(failure("EVIDENCE_CEILING_TEXT_INVALID", field))
        elif NUMERIC_CONFIDENCE.search(text):
            failures.append(failure("NUMERIC_CONFIDENCE_CLAIM_FORBIDDEN", field))
    if not isinstance(profile, dict):
        return

    section_specs = {
        "production_path_evidence": (profile.get("production_path") or {}).get("oracle_ids"),
        "lifecycle_evidence": (profile.get("lifecycle_contract") or {}).get("oracle_ids"),
        "boundary_evidence": (profile.get("boundary_contract") or {}).get("oracle_ids"),
        "oracle_strength_evidence": (profile.get("oracle_strength") or {}).get("oracle_ids"),
    }
    evidence_items: dict[str, dict[str, Any]] = {}
    for field, expected_ids in section_specs.items():
        item = strict_mapping(
            ceiling.get(field), {"status", "oracle_ids", "evidence_refs"},
            {"status", "oracle_ids", "evidence_refs"}, f"evidence_ceiling.{field}", failures,
        ) or {}
        evidence_items[field] = item
        oracle_ids = item.get("oracle_ids")
        evidence_refs = item.get("evidence_refs")
        if item.get("status") not in VERIFICATION_LEVEL_STATUSES:
            failures.append(failure("EVIDENCE_BINDING_STATUS_INVALID", f"{field}:{item.get('status')}"))
        if oracle_ids != expected_ids or not isinstance(evidence_refs, list) or len(evidence_refs) != len(oracle_ids or []):
            failures.append(failure("EVIDENCE_BINDING_ORACLE_COVERAGE_MISMATCH", field))
            continue
        expected_refs = [oracle_by_id.get(oracle_id, {}).get("evidence_ref") for oracle_id in oracle_ids]
        if evidence_refs != expected_refs:
            failures.append(failure("EVIDENCE_BINDING_REF_MISMATCH", field))
    if outcome == "task_completed":
        for field in ("production_path_evidence", "lifecycle_evidence", "boundary_evidence"):
            if evidence_items.get(field, {}).get("status") != "pass":
                failures.append(failure("CROSS_COMPONENT_EVIDENCE_NOT_PROVEN", field))
    strength = profile.get("oracle_strength") if isinstance(profile.get("oracle_strength"), dict) else {}
    if outcome == "task_completed" and strength.get("required") is True and evidence_items.get("oracle_strength_evidence", {}).get("status") != "pass":
        failures.append(failure("ORACLE_STRENGTH_NOT_PROVEN", str(evidence_items.get("oracle_strength_evidence", {}).get("status"))))
    if outcome == "task_completed" and profile.get("platform_runtime_required") is True and levels.get("platform_runtime") != "pass":
        failures.append(failure("PLATFORM_RUNTIME_REQUIRED_BUT_MISSING", str(levels.get("platform_runtime"))))
    if outcome != "task_completed" or task_root is None:
        return

    production = profile.get("production_path") if isinstance(profile.get("production_path"), dict) else {}
    production_ids = production.get("oracle_ids") if isinstance(production.get("oracle_ids"), list) else []
    production_artifact = artifact_by_oracle.get(production_ids[0]) if len(production_ids) == 1 else None
    if production_artifact is None:
        failures.append(failure("PRODUCTION_DECIDING_ARTIFACT_MISSING", str(production_ids)))
    else:
        try:
            observed = json.loads(production_artifact.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(failure("PRODUCTION_RESULT_INVALID", str(exc)))
            observed = {}
        production_fields = {
            "schema_version", "production_entrypoint", "authoritative_initializer",
            "actual_call_route", "components", "production_artifacts",
            "executes_production_code", "test_only_reimplementation",
        }
        observed = strict_mapping(observed, production_fields, production_fields, "production_result", failures) or {}
        if any(observed.get(field) != production.get(field) for field in ("production_entrypoint", "authoritative_initializer", "actual_call_route", "components")):
            failures.append(failure("PRODUCTION_RESULT_CONTRACT_MISMATCH", "production path"))
        if observed.get("schema_version") != "1.0" or observed.get("executes_production_code") is not True or observed.get("test_only_reimplementation") is not False:
            failures.append(failure("PRODUCTION_RESULT_NOT_BOUND", "production_result"))
        artifact_rows = observed.get("production_artifacts")
        expected_refs = production.get("production_artifact_refs")
        if not isinstance(artifact_rows, list) or [row.get("ref") for row in artifact_rows if isinstance(row, dict)] != expected_refs:
            failures.append(failure("PRODUCTION_ARTIFACT_COVERAGE_MISMATCH", str(expected_refs)))
        else:
            for index, row in enumerate(artifact_rows):
                if not isinstance(row, dict) or set(row) != {"ref", "sha256"}:
                    failures.append(failure("PRODUCTION_ARTIFACT_BINDING_INVALID", str(index)))
                    continue
                path = safe_under(task_root, str(row.get("ref") or ""))
                if path is None or not path.is_file() or not isinstance(row.get("sha256"), str) or not HEX64.fullmatch(row["sha256"]) or sha256_file(path) != row["sha256"]:
                    failures.append(failure("PRODUCTION_ARTIFACT_HASH_INVALID", str(row.get("ref"))))
                else:
                    try:
                        if path.stat().st_nlink > 1:
                            failures.append(failure("PRODUCTION_ARTIFACT_LINK_COUNT_INVALID", str(row.get("ref"))))
                        control_paths = [
                            candidate
                            for candidate in (
                                [contract] if contract is not None and contract.is_file() else []
                            ) + [
                                safe_under(task_root, str(oracle.get("evidence_ref") or ""))
                                for oracle in oracle_by_id.values()
                                if isinstance(oracle, dict)
                            ] + [artifact for artifact in artifact_by_oracle.values() if artifact is not None]
                            if candidate is not None and candidate.is_file()
                        ]
                        if any(path.samefile(control_path) for control_path in control_paths):
                            failures.append(failure("PRODUCTION_ARTIFACT_ALIAS", str(row.get("ref"))))
                    except OSError as exc:
                        failures.append(failure("PRODUCTION_ARTIFACT_IDENTITY_UNAVAILABLE", str(exc)))

    lifecycle = profile.get("lifecycle_contract") if isinstance(profile.get("lifecycle_contract"), dict) else {}
    lifecycle_ids = lifecycle.get("oracle_ids") if isinstance(lifecycle.get("oracle_ids"), list) else []
    lifecycle_artifact = artifact_by_oracle.get(lifecycle_ids[0]) if len(lifecycle_ids) == 1 else None
    if lifecycle_artifact is None:
        failures.append(failure("LIFECYCLE_DECIDING_ARTIFACT_MISSING", str(lifecycle_ids)))
    else:
        try:
            observed = json.loads(lifecycle_artifact.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(failure("LIFECYCLE_RESULT_INVALID", str(exc)))
            observed = {}
        lifecycle_fields = {
            "schema_version", "typed_state", "field_ownership", "observed_transitions",
            "success_invariants", "rollback_paths", "failure_paths", "concurrency_cases",
            "instance_invariants", "deferred_trigger_independence",
        }
        observed = strict_mapping(observed, lifecycle_fields, lifecycle_fields, "lifecycle_result", failures) or {}
        comparisons = {
            "typed_state": "typed_state",
            "field_ownership": "field_ownership",
            "observed_transitions": "allowed_transitions",
            "success_invariants": "success_invariants",
            "rollback_paths": "rollback_paths",
            "failure_paths": "failure_paths",
            "concurrency_cases": "concurrency_cases",
            "instance_invariants": "instance_invariants",
        }
        if observed.get("schema_version") != "1.0" or any(observed.get(result_field) != lifecycle.get(contract_field) for result_field, contract_field in comparisons.items()):
            failures.append(failure("LIFECYCLE_RESULT_CONTRACT_MISMATCH", "lifecycle_result"))
        expected_deferred = lifecycle.get("deferred_trigger_independence_required") is True
        if observed.get("deferred_trigger_independence") is not expected_deferred:
            failures.append(failure("DEFERRED_TRIGGER_INDEPENDENCE_NOT_PROVEN", str(observed.get("deferred_trigger_independence"))))

    boundary = profile.get("boundary_contract") if isinstance(profile.get("boundary_contract"), dict) else {}
    boundary_ids = boundary.get("oracle_ids") if isinstance(boundary.get("oracle_ids"), list) else []
    boundary_artifact = artifact_by_oracle.get(boundary_ids[0]) if len(boundary_ids) == 1 else None
    if boundary_artifact is None:
        failures.append(failure("BOUNDARY_DECIDING_ARTIFACT_MISSING", str(boundary_ids)))
    else:
        try:
            observed = json.loads(boundary_artifact.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(failure("BOUNDARY_RESULT_INVALID", str(exc)))
            observed = {}
        boundary_fields = {"schema_version", "bindings", "call_route_continuity", "downstream_identity_reconstruction"}
        observed = strict_mapping(observed, boundary_fields, boundary_fields, "boundary_result", failures) or {}
        expected_bindings = boundary.get("bindings") if isinstance(boundary.get("bindings"), list) else []
        rows = observed.get("bindings")
        if observed.get("schema_version") != "1.0" or observed.get("call_route_continuity") is not True or observed.get("downstream_identity_reconstruction") is not False or not isinstance(rows, list) or len(rows) != len(expected_bindings):
            failures.append(failure("BOUNDARY_RESULT_NOT_PROVEN", "boundary_result"))
        else:
            expected_by_id = {item.get("id"): item for item in expected_bindings if isinstance(item, dict)}
            for row in rows:
                if not isinstance(row, dict) or set(row) != {"id", "matched", "compile_status"}:
                    failures.append(failure("BOUNDARY_RESULT_BINDING_INVALID", str(row)))
                    continue
                expected = expected_by_id.get(row.get("id"), {})
                compile_status = "pass" if expected.get("compile_required") is True else "not_required"
                if row.get("matched") is not True or row.get("compile_status") != compile_status:
                    failures.append(failure("BOUNDARY_RESULT_MISMATCH", str(row.get("id"))))

    if strength.get("required") is True:
        strength_ids = strength.get("oracle_ids") if isinstance(strength.get("oracle_ids"), list) else []
        strength_artifact = artifact_by_oracle.get(strength_ids[0]) if len(strength_ids) == 1 else None
        if strength_artifact is None:
            failures.append(failure("ORACLE_STRENGTH_DECIDING_ARTIFACT_MISSING", str(strength_ids)))
        else:
            try:
                observed = json.loads(strength_artifact.read_text(encoding="utf-8"))
            except Exception as exc:
                failures.append(failure("MUTATION_RESULT_INVALID", str(exc)))
                observed = {}
            observed = strict_mapping(observed, {"schema_version", "results"}, {"schema_version", "results"}, "mutation_result", failures) or {}
            mutations = strength.get("mutations") if isinstance(strength.get("mutations"), list) else []
            results = observed.get("results")
            if observed.get("schema_version") != "1.0" or not isinstance(results, list) or len(results) != len(mutations):
                failures.append(failure("MUTATION_RESULT_COVERAGE_MISMATCH", "mutation_result"))
            else:
                expected_by_id = {item.get("id"): item for item in mutations if isinstance(item, dict)}
                for row in results:
                    fields = {"mutation_id", "production_target", "killed", "killed_by_oracle_id", "observed_failure", "restored"}
                    if not isinstance(row, dict) or set(row) != fields:
                        failures.append(failure("MUTATION_RESULT_ENTRY_INVALID", str(row)))
                        continue
                    expected = expected_by_id.get(row.get("mutation_id"), {})
                    if (
                        row.get("production_target") != expected.get("production_target")
                        or row.get("killed") is not True
                        or row.get("killed_by_oracle_id") != expected.get("oracle_id")
                        or not isinstance(row.get("observed_failure"), str)
                        or not row.get("observed_failure", "").strip()
                        or row.get("restored") is not True
                    ):
                        failures.append(failure("MUTATION_SURVIVED_OR_UNPROVEN", str(row.get("mutation_id"))))


def validate_bound_json_artifact(
    task_root: Path | None,
    binding: Any,
    name: str,
    contract: Path | None,
    failures: list[dict[str, str]],
) -> tuple[Path | None, dict[str, Any]]:
    item = strict_mapping(binding, {"path", "sha256"}, {"path", "sha256"}, name, failures)
    if item is None or task_root is None:
        return None, {}
    ref = item.get("path")
    expected_hash = item.get("sha256")
    evidence_path(task_root, ref, contract, name, failures)
    path = safe_under(task_root, str(ref or ""))
    if path is None or not path.is_file():
        return path, {}
    if not isinstance(expected_hash, str) or not HEX64.fullmatch(expected_hash) or sha256_file(path) != expected_hash:
        failures.append(failure("BOUND_ARTIFACT_HASH_MISMATCH", name))
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(failure("BOUND_ARTIFACT_INVALID", f"{name}:{exc}"))
        return path, {}
    if not isinstance(value, dict):
        failures.append(failure("BOUND_ARTIFACT_INVALID", f"{name}:root"))
        return path, {}
    return path, value


def validate_repair_ledger(
    ledger: dict[str, Any],
    task_id: Any,
    repair_summary: Any,
    failures: list[dict[str, str]],
    *,
    allow_terminal_patterns: bool = False,
) -> None:
    required = {"schema_version", "task_id", "max_total_iterations", "cycles"}
    value = strict_mapping(ledger, required, required, "repair_ledger", failures)
    if value is None:
        return
    if value.get("schema_version") != "1.0" or value.get("task_id") != task_id:
        failures.append(failure("REPAIR_LEDGER_IDENTITY_INVALID", str(value.get("task_id"))))
    cycles = value.get("cycles")
    if not isinstance(cycles, list):
        failures.append(failure("REPAIR_LEDGER_CYCLES_INVALID", "not a list"))
        return
    summary = repair_summary if isinstance(repair_summary, dict) else {}
    maximum = value.get("max_total_iterations")
    if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < 0:
        failures.append(failure("REPAIR_LEDGER_BUDGET_INVALID", str(maximum)))
        maximum = -1
    if len(cycles) != summary.get("iterations") or len(cycles) > maximum:
        failures.append(failure("REPAIR_LEDGER_COUNT_MISMATCH", f"cycles={len(cycles)},summary={summary.get('iterations')}"))
    confirmed_fingerprints: list[str] = []
    consecutive_no_progress = 0
    max_no_progress = 0
    for index, raw in enumerate(cycles):
        required_cycle = {
            "cycle_number", "finding_fingerprint", "adjudication", "root_cause_or_hypothesis_change",
            "changed_files", "targeted_oracle_id", "targeted_oracle_result", "measurable_progress", "reviewer_result",
        }
        cycle = strict_mapping(raw, required_cycle, required_cycle, f"repair_ledger.cycles[{index}]", failures)
        if cycle is None:
            continue
        if cycle.get("cycle_number") != index + 1:
            failures.append(failure("REPAIR_LEDGER_SEQUENCE_INVALID", str(index)))
        if cycle.get("adjudication") not in REVIEW_DISPOSITIONS or cycle.get("targeted_oracle_result") not in {"pass", "fail", "blocked"}:
            failures.append(failure("REPAIR_LEDGER_CYCLE_INVALID", str(index)))
        for field in ("finding_fingerprint", "root_cause_or_hypothesis_change", "targeted_oracle_id", "reviewer_result"):
            if not isinstance(cycle.get(field), str) or not cycle.get(field).strip():
                failures.append(failure("REPAIR_LEDGER_CYCLE_INVALID", f"{index}:{field}"))
        if not isinstance(cycle.get("changed_files"), list) or any(not isinstance(item, str) or not item for item in cycle.get("changed_files", [])):
            failures.append(failure("REPAIR_LEDGER_CYCLE_INVALID", f"{index}:changed_files"))
        if not isinstance(cycle.get("measurable_progress"), bool):
            failures.append(failure("REPAIR_LEDGER_CYCLE_INVALID", f"{index}:measurable_progress"))
        if cycle.get("adjudication") == "confirmed":
            fingerprint = str(cycle.get("finding_fingerprint") or "")
            if not allow_terminal_patterns and fingerprint in confirmed_fingerprints:
                failures.append(failure("REPEATED_CONFIRMED_FINDING_REQUIRES_PROTECTIVE_STOP", fingerprint))
            confirmed_fingerprints.append(fingerprint)
        if cycle.get("measurable_progress") is False:
            consecutive_no_progress += 1
            max_no_progress = max(max_no_progress, consecutive_no_progress)
        else:
            consecutive_no_progress = 0
    if summary:
        if summary.get("same_failure_repeats") != max(0, len(confirmed_fingerprints) - len(set(confirmed_fingerprints))):
            failures.append(failure("REPAIR_LEDGER_REPEAT_SUMMARY_MISMATCH", "same_failure_repeats"))
        if summary.get("consecutive_no_progress") != max_no_progress:
            failures.append(failure("REPAIR_LEDGER_PROGRESS_SUMMARY_MISMATCH", "consecutive_no_progress"))


def git_diff_budget(root: Path, baseline: str, product_patterns: list[str], framework_patterns: list[str], planned_patterns: list[str]) -> tuple[int, int, bool]:
    names = [
        item.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        for item in run_git(root, "diff", "--name-only", "-z", f"{baseline}..HEAD", "--", ".").split(b"\0")
        if item
    ]
    product_names = [item for item in names if path_in_declared_scope(item, product_patterns)]
    product_lines = 0
    tokens = run_git(root, "diff", "--numstat", "-z", f"{baseline}..HEAD", "--", ".").split(b"\0")
    index = 0
    while index < len(tokens):
        raw = tokens[index]
        if not raw:
            index += 1
            continue
        parts = raw.split(b"\t", 2)
        if len(parts) != 3:
            index += 1
            continue
        if parts[2]:
            path = parts[2].decode("utf-8", errors="surrogateescape").replace("\\", "/")
            index += 1
        elif index + 2 < len(tokens):
            path = tokens[index + 2].decode("utf-8", errors="surrogateescape").replace("\\", "/")
            index += 3
        else:
            index += 1
            continue
        if path not in product_names:
            continue
        for count in parts[:2]:
            if count.isdigit():
                product_lines += int(count)
    added_names = [
        item.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        for item in run_git(root, "diff", "--name-only", "--diff-filter=A", "-z", f"{baseline}..HEAD", "--", ".").split(b"\0")
        if item
    ]
    added_framework_names = [item for item in added_names if path_in_declared_scope(item, framework_patterns)]
    unplanned = any(not path_in_declared_scope(item, planned_patterns) for item in added_framework_names)
    return len(product_names), product_lines, unplanned


def validate_architecture_review_evidence(
    task_root: Path | None,
    ref: Any,
    reviewer_role_id: Any,
    contract: Path | None,
    location: str,
    failures: list[dict[str, str]],
) -> None:
    if task_root is None:
        failures.append(failure("ARCHITECTURE_REVIEW_EVIDENCE_CONTEXT_MISSING", location))
        return
    evidence_path(task_root, ref, contract, location, failures)
    path = safe_under(task_root, str(ref or ""))
    if path is None or not path.is_file():
        return
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(failure("ARCHITECTURE_REVIEW_EVIDENCE_INVALID", f"{location}:{exc}"))
        return
    review = strict_mapping(raw, {"status", "reviewer_role_id", "covers"}, {"status", "reviewer_role_id", "covers"}, location, failures)
    if review is None or review.get("status") != "pass" or review.get("reviewer_role_id") != reviewer_role_id or set(review.get("covers") or []) != ARCHITECTURE_REVIEW_COVERS:
        failures.append(failure("ARCHITECTURE_REVIEW_EVIDENCE_INVALID", location))


def validate_forensic_evidence(
    task_root: Path | None,
    ref: Any,
    forensic: dict[str, Any],
    contract: Path | None,
    failures: list[dict[str, str]],
) -> None:
    if task_root is None:
        failures.append(failure("FORENSIC_EVIDENCE_CONTEXT_MISSING", "forensic_before_code"))
        return
    evidence_path(task_root, ref, contract, "forensic_before_code.execution_sequence_ref", failures)
    path = safe_under(task_root, str(ref or ""))
    if path is None or not path.is_file():
        return
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(failure("FORENSIC_EVIDENCE_INVALID", str(exc)))
        return
    required = {"status", "first_divergent_event", "execution_sequence", "falsifiable_hypothesis", "oracle_id"}
    evidence = strict_mapping(raw, required, required, "forensic_evidence", failures)
    if evidence is None or (
        evidence.get("status") != "pass"
        or evidence.get("first_divergent_event") != forensic.get("first_divergent_event")
        or evidence.get("falsifiable_hypothesis") != forensic.get("falsifiable_hypothesis")
        or evidence.get("oracle_id") != forensic.get("oracle_id")
        or not isinstance(evidence.get("execution_sequence"), list)
        or not evidence.get("execution_sequence")
    ):
        failures.append(failure("FORENSIC_EVIDENCE_INVALID", "forensic_before_code"))


def validate_lifecycle_evidence(
    value: dict[str, Any],
    contract: Path | None,
    *,
    repo_root: Path | None,
    task_root: Path | None,
    lease: dict[str, Any] | None,
    verify_runtime: bool,
    failures: list[dict[str, str]],
    outcome: str = "task_completed",
    repair_summary_override: dict[str, Any] | None = None,
) -> None:
    _, lifecycle_value = validate_bound_json_artifact(
        task_root,
        value.get("lifecycle_evidence"),
        "lifecycle_evidence_binding",
        contract,
        failures,
    )
    lifecycle = strict_mapping(
        lifecycle_value,
        {"events", "repair_ledger", "diff_budget", "verification_ladder", "runner_reuse", "runtime_acceptance"},
        {"events", "repair_ledger", "diff_budget", "verification_ladder", "runner_reuse", "runtime_acceptance"},
        "lifecycle_evidence",
        failures,
    )
    if lifecycle is None:
        return
    contract_value = load_contract_value(contract, failures)
    controls = contract_value.get("conditional_controls") if isinstance(contract_value.get("conditional_controls"), dict) else {}

    events = lifecycle.get("events")
    event_names: list[str] = []
    event_by_name: dict[str, dict[str, Any]] = {}
    if not isinstance(events, list):
        failures.append(failure("LIFECYCLE_EVENTS_INVALID", "not a list"))
        events = []
    for index, raw in enumerate(events):
        event = strict_mapping(raw, {"sequence", "event", "evidence_ref"}, {"sequence", "event", "evidence_ref"}, f"lifecycle_evidence.events[{index}]", failures)
        if event is None:
            continue
        if event.get("sequence") != index + 1 or not isinstance(event.get("event"), str) or not event.get("event"):
            failures.append(failure("LIFECYCLE_EVENT_SEQUENCE_INVALID", str(index)))
        event_name = str(event.get("event") or "")
        event_names.append(event_name)
        if event_name in event_by_name:
            failures.append(failure("LIFECYCLE_EVENT_DUPLICATE", event_name))
        event_by_name[event_name] = event
        if task_root is not None:
            evidence_path(task_root, event.get("evidence_ref"), contract, f"lifecycle_event[{index}]", failures)

    forensic = controls.get("forensic_before_code") if isinstance(controls.get("forensic_before_code"), dict) else {}
    if forensic.get("required") is True:
        try:
            if event_names.index("forensic_trigger") >= event_names.index("forensic_complete") or event_names.index("forensic_complete") >= event_names.index("mutation_resumed"):
                raise ValueError
        except ValueError:
            failures.append(failure("FORENSIC_EVENT_ORDER_INVALID", str(event_names)))
        forensic_complete = event_by_name.get("forensic_complete", {})
        if forensic_complete.get("evidence_ref") != forensic.get("execution_sequence_ref"):
            failures.append(failure("FORENSIC_EVIDENCE_BINDING_MISMATCH", str(forensic_complete.get("evidence_ref"))))
        else:
            validate_forensic_evidence(task_root, forensic.get("execution_sequence_ref"), forensic, contract, failures)
    architecture = controls.get("preimplementation_architecture_review") if isinstance(controls.get("preimplementation_architecture_review"), dict) else {}
    if architecture.get("required") is True:
        try:
            if event_names.index("architecture_review_complete") >= event_names.index("mutation_resumed"):
                raise ValueError
        except ValueError:
            failures.append(failure("ARCHITECTURE_REVIEW_EVENT_ORDER_INVALID", str(event_names)))
        review = value.get("independent_review") if isinstance(value.get("independent_review"), dict) else {}
        if review.get("reviewer_id") != architecture.get("reviewer_role_id"):
            failures.append(failure("REVIEWER_ROLE_REUSE_INVALID", str(review.get("reviewer_id"))))
        architecture_event = event_by_name.get("architecture_review_complete", {})
        if architecture_event.get("evidence_ref") != architecture.get("evidence_ref"):
            failures.append(failure("ARCHITECTURE_REVIEW_EVIDENCE_BINDING_MISMATCH", str(architecture_event.get("evidence_ref"))))
        else:
            validate_architecture_review_evidence(task_root, architecture.get("evidence_ref"), architecture.get("reviewer_role_id"), contract, "architecture_review_complete", failures)

    _, ledger = validate_bound_json_artifact(task_root, lifecycle.get("repair_ledger"), "repair_ledger_binding", contract, failures)
    if ledger:
        validate_repair_ledger(
            ledger,
            value.get("task_id"),
            repair_summary_override or value.get("repair_summary"),
            failures,
            allow_terminal_patterns=outcome == "task_blocked",
        )

    budget_evidence = strict_mapping(
        lifecycle.get("diff_budget"),
        {"product_files_changed", "product_lines_changed", "unplanned_task_local_framework", "replan_triggered", "scope_confirmation_ref"},
        {"product_files_changed", "product_lines_changed", "unplanned_task_local_framework", "replan_triggered", "scope_confirmation_ref"},
        "lifecycle_evidence.diff_budget",
        failures,
    )
    budget = controls.get("diff_budget") if isinstance(controls.get("diff_budget"), dict) else {}
    if budget_evidence is not None:
        if any(not isinstance(budget_evidence.get(field), int) or isinstance(budget_evidence.get(field), bool) or budget_evidence[field] < 0 for field in ("product_files_changed", "product_lines_changed")) or any(not isinstance(budget_evidence.get(field), bool) for field in ("unplanned_task_local_framework", "replan_triggered")):
            failures.append(failure("DIFF_BUDGET_EVIDENCE_INVALID", "types"))
        exceeded = budget_evidence.get("product_files_changed", 0) > budget.get("max_product_files", 0) or budget_evidence.get("product_lines_changed", 0) > budget.get("max_product_lines", 0) or budget_evidence.get("unplanned_task_local_framework") is True
        if outcome == "task_completed" and exceeded and (budget_evidence.get("replan_triggered") is not True or not str(budget_evidence.get("scope_confirmation_ref") or "").strip()):
            failures.append(failure("DIFF_BUDGET_REPLAN_REQUIRED", str(budget_evidence)))
        if outcome == "task_completed" and exceeded:
            active_gates = contract_value.get("gate_profile", {}).get("active") if isinstance(contract_value.get("gate_profile"), dict) else []
            review_extension = contract_value.get("extensions", {}).get("independent_review") if isinstance(contract_value.get("extensions"), dict) else None
            if (
                architecture.get("required") is not True
                or "independent_review" not in active_gates
                or not isinstance(review_extension, dict)
                or review_extension.get("required") is not True
                or review_extension.get("reviewer_role") != architecture.get("reviewer_role_id")
            ):
                failures.append(failure("DIFF_BUDGET_ARCHITECTURE_REVIEW_REQUIRED", "replan contract must activate architecture and final independent review"))
            try:
                if (
                    event_names.index("diff_budget_threshold") >= event_names.index("architecture_re_evaluation")
                    or event_names.index("architecture_re_evaluation") >= event_names.index("replan_complete")
                    or event_names.index("replan_complete") >= event_names.index("mutation_resumed")
                ):
                    raise ValueError
            except ValueError:
                failures.append(failure("DIFF_BUDGET_EVENT_ORDER_INVALID", str(event_names)))
            re_evaluation = event_by_name.get("architecture_re_evaluation", {})
            validate_architecture_review_evidence(
                task_root,
                re_evaluation.get("evidence_ref"),
                architecture.get("reviewer_role_id"),
                contract,
                "architecture_re_evaluation",
                failures,
            )
        if task_root is not None and budget_evidence.get("replan_triggered") is True:
            evidence_path(task_root, budget_evidence.get("scope_confirmation_ref"), contract, "diff_budget.scope_confirmation_ref", failures)
        if verify_runtime and repo_root is not None:
            try:
                actual = git_diff_budget(
                    repo_root,
                    str(value.get("baseline") or ""),
                    budget.get("product_path_patterns") or [],
                    budget.get("task_local_framework_patterns") or [],
                    budget.get("planned_task_local_framework_patterns") or [],
                )
                reported = (budget_evidence.get("product_files_changed"), budget_evidence.get("product_lines_changed"), budget_evidence.get("unplanned_task_local_framework"))
                if reported != actual:
                    failures.append(failure("DIFF_BUDGET_GIT_MISMATCH", json.dumps({"reported": reported, "actual": actual}, ensure_ascii=True)))
            except Exception as exc:
                failures.append(failure("DIFF_BUDGET_GIT_ERROR", str(exc)))

    ladder = strict_mapping(lifecycle.get("verification_ladder"), {"narrow", "targeted", "full_suite"}, {"narrow", "targeted", "full_suite"}, "lifecycle_evidence.verification_ladder", failures)
    if ladder is not None:
        statuses = []
        for name in ("narrow", "targeted", "full_suite"):
            step = strict_mapping(ladder.get(name), {"status", "evidence_ref"}, {"status", "evidence_ref"}, f"verification_ladder.{name}", failures)
            if step is None:
                statuses.append("invalid")
                continue
            status = step.get("status")
            if outcome == "task_completed":
                allowed = {"pass"} if name != "full_suite" else {"pass", "not_required"}
            else:
                allowed = {"pass", "fail", "blocked", "not_required"}
            if status not in allowed:
                failures.append(failure("VERIFICATION_LADDER_STATUS_INVALID", f"{name}:{status}"))
            statuses.append(str(status))
            if task_root is not None:
                evidence_path(task_root, step.get("evidence_ref"), contract, f"verification_ladder.{name}", failures)
        escalation = controls.get("verification_escalation") if isinstance(controls.get("verification_escalation"), dict) else {}
        if outcome == "task_completed" and statuses[:2] != ["pass", "pass"]:
            failures.append(failure("VERIFICATION_LADDER_ORDER_INVALID", str(statuses)))
        if outcome == "task_completed":
            expected_full = "pass" if escalation.get("integration_or_dependency_risk") is True else "not_required"
            if statuses[2] != expected_full:
                failures.append(failure("FULL_SUITE_TRIGGER_MISMATCH", f"risk={escalation.get('integration_or_dependency_risk')},status={statuses[2]}"))
            try:
                if event_names.index("narrow_pass") >= event_names.index("targeted_pass"):
                    raise ValueError
            except ValueError:
                failures.append(failure("VERIFICATION_LADDER_EVENT_ORDER_INVALID", str(event_names)))

    runner_fields = {"registered_runner_ids", "executed_runner_ids", "execution_evidence_ref", "task_local_replacement_created", "capability_gap_ref", "justification"}
    runner = strict_mapping(lifecycle.get("runner_reuse"), runner_fields, runner_fields, "lifecycle_evidence.runner_reuse", failures)
    if runner is not None:
        runner_ids = runner.get("registered_runner_ids")
        if not isinstance(runner_ids, list) or not runner_ids or any(not isinstance(item, str) or not item for item in runner_ids) or not isinstance(runner.get("task_local_replacement_created"), bool):
            failures.append(failure("RUNNER_REUSE_EVIDENCE_INVALID", "runner_reuse"))
            runner_ids = []
        if any(not item.startswith(("execution-profile:", "toolchain:", "launcher:")) for item in runner_ids):
            failures.append(failure("RUNNER_NOT_PROFILE_REGISTERED", str(runner_ids)))
        executed_ids = runner.get("executed_runner_ids")
        if not isinstance(executed_ids, list) or not executed_ids or any(item not in runner_ids for item in executed_ids) or not any(str(item).startswith("launcher:") for item in executed_ids):
            failures.append(failure("CANONICAL_LAUNCHER_EXECUTION_MISSING", str(executed_ids)))
        if task_root is not None:
            evidence_path(task_root, runner.get("execution_evidence_ref"), contract, "runner_reuse.execution_evidence_ref", failures)
        if verify_runtime and lease is not None:
            registered = {
                f"execution-profile:{lease.get('execution_profile')}",
                f"toolchain:{lease.get('toolchain_profile')}",
                f"launcher:{lease.get('canonical_launcher')}",
            }
            if any(item not in registered for item in runner_ids) or any(item not in registered for item in (executed_ids if isinstance(executed_ids, list) else [])):
                failures.append(failure("RUNNER_PROFILE_BINDING_MISMATCH", json.dumps({"receipt": runner_ids, "lease": sorted(registered)}, ensure_ascii=True)))
        if runner.get("task_local_replacement_created") is True and (not str(runner.get("capability_gap_ref") or "").strip() or not str(runner.get("justification") or "").strip()):
            failures.append(failure("TASK_LOCAL_RUNNER_CAPABILITY_GAP_MISSING", "runner_reuse"))
        if task_root is not None and runner.get("task_local_replacement_created") is True:
            evidence_path(task_root, runner.get("capability_gap_ref"), contract, "runner_reuse.capability_gap_ref", failures)

    runtime = strict_mapping(lifecycle.get("runtime_acceptance"), {"status", "oracle_results"}, {"status", "oracle_results"}, "lifecycle_evidence.runtime_acceptance", failures)
    runtime_policy = controls.get("runtime_acceptance") if isinstance(controls.get("runtime_acceptance"), dict) else {}
    if runtime is not None:
        expected = ("pass" if runtime_policy.get("required") is True else "not_required") if outcome == "task_completed" else ("blocked" if runtime_policy.get("required") is True else "not_required")
        if runtime.get("status") != expected:
            failures.append(failure("RUNTIME_ACCEPTANCE_NOT_PROVEN", str(runtime.get("status"))))
        if outcome == "task_completed" and runtime_policy.get("required") is True and (runtime_policy.get("authorized") is not True or runtime_policy.get("available") is not True):
            failures.append(failure("RUNTIME_ACCEPTANCE_NOT_AUTHORIZED", str(runtime_policy)))
        criteria = contract_value.get("acceptance_criteria") if isinstance(contract_value.get("acceptance_criteria"), list) else []
        oracle_by_id = {
            item.get("id"): item
            for item in (contract_value.get("oracles") if isinstance(contract_value.get("oracles"), list) else [])
            if isinstance(item, dict)
        }
        runtime_oracles = [
            oracle_by_id.get(item.get("oracle_id"), {})
            for item in criteria
            if isinstance(item, dict) and item.get("mandatory") is True and item.get("owner_visible") is True
        ]
        ceiling = value.get("evidence_ceiling") if isinstance(value.get("evidence_ceiling"), dict) else {}
        level_results = ceiling.get("level_oracle_results") if isinstance(ceiling.get("level_oracle_results"), dict) else {}
        high_level_ids = {
            str(oracle_id)
            for level in HIGH_LEVEL_EVIDENCE_CLASSES
            for oracle_id in (level_results.get(level) if isinstance(level_results.get(level), list) else [])
        }
        runtime_oracles.extend(
            oracle_by_id.get(oracle_id, {})
            for oracle_id in sorted(high_level_ids)
            if oracle_id not in {str(item.get("id") or "") for item in runtime_oracles}
        )
        if outcome == "task_completed" and runtime_policy.get("required") is True and any(oracle.get("authorized") is not True for oracle in runtime_oracles):
            failures.append(failure("OWNER_VISIBLE_ORACLE_NOT_AUTHORIZED", "contract.oracles"))
        results = runtime.get("oracle_results")
        if not isinstance(results, list):
            failures.append(failure("RUNTIME_ACCEPTANCE_RESULTS_INVALID", "not a list"))
            results = []
        result_by_id: dict[str, dict[str, Any]] = {}
        for index, raw in enumerate(results):
            result = strict_mapping(raw, {"oracle_id", "status", "evidence_ref"}, {"oracle_id", "status", "evidence_ref"}, f"runtime_acceptance.oracle_results[{index}]", failures)
            if result is None:
                continue
            oracle_id = str(result.get("oracle_id") or "")
            if not oracle_id or oracle_id in result_by_id:
                failures.append(failure("RUNTIME_ACCEPTANCE_RESULT_ID_INVALID", oracle_id or str(index)))
            result_by_id[oracle_id] = result
            if task_root is not None:
                evidence_path(task_root, result.get("evidence_ref"), contract, f"runtime_acceptance.oracle_results[{index}]", failures)
        expected_oracles = {str(oracle.get("id") or ""): oracle for oracle in runtime_oracles}
        if runtime_policy.get("required") is True and set(result_by_id) != set(expected_oracles):
            failures.append(failure("RUNTIME_ACCEPTANCE_ORACLE_COVERAGE_MISMATCH", json.dumps({"expected": sorted(expected_oracles), "actual": sorted(result_by_id)}, ensure_ascii=True)))
        if runtime_policy.get("required") is False and results:
            failures.append(failure("RUNTIME_ACCEPTANCE_RESULTS_UNEXPECTED", str(sorted(result_by_id))))
        for oracle_id, oracle in expected_oracles.items():
            result = result_by_id.get(oracle_id, {})
            expected_statuses = {"pass"} if outcome == "task_completed" else {"fail", "blocked"}
            if result.get("status") not in expected_statuses or result.get("evidence_ref") != oracle.get("evidence_ref"):
                failures.append(failure("RUNTIME_ACCEPTANCE_ORACLE_EVIDENCE_MISMATCH", oracle_id))


def validate_receipt(
    value: dict[str, Any],
    contract: Path | None = None,
    *,
    repo_root: Path | None = None,
    task_root: Path | None = None,
    declaration: dict[str, Any] | None = None,
    lease: dict[str, Any] | None = None,
    verify_runtime: bool = False,
    receipt_path: Path | None = None,
) -> list[dict[str, str]]:
    declaration = declaration or {}
    if value.get("schema_version") in {"1.2", "1.3"} and value.get("outcome") == "task_blocked":
        return validate_blocked_receipt(
            value,
            contract,
            repo_root=repo_root,
            task_root=task_root,
            declaration=declaration,
            lease=lease,
            verify_runtime=verify_runtime,
            receipt_path=receipt_path,
        )
    failures: list[dict[str, str]] = []
    version = str(value.get("schema_version") or "")
    contract_value: dict[str, Any] = {}
    if version in {"1.2", "1.3"}:
        validate_v12_contract_model(contract, failures)
    required = set(COMPLETED_TOP_REQUIRED)
    allowed = COMPLETED_TOP_REQUIRED | {"environment_readiness", "pipeline_metrics"}
    if version in {"1.2", "1.3"}:
        required |= {"outcome", "repair_summary"}
        allowed |= {"outcome", "repair_summary"}
    if version == "1.3":
        required |= {"lifecycle_evidence"}
        allowed |= {"lifecycle_evidence", "evidence_ceiling"}
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - allowed)
    if missing:
        failures.append(failure("RECEIPT_FIELDS_MISSING", ", ".join(missing)))
    if unknown:
        failures.append(failure("UNKNOWN_FIELDS", f"receipt:{','.join(unknown)}"))
    if version not in {"1.0", "1.1", "1.2", "1.3"}:
        failures.append(failure("RECEIPT_SCHEMA_UNSUPPORTED", str(value.get("schema_version"))))
    if version in {"1.2", "1.3"} and value.get("outcome") != "task_completed":
        failures.append(failure("COMPLETED_OUTCOME_INVALID", str(value.get("outcome"))))
    if not isinstance(value.get("task_id"), str) or not value.get("task_id"):
        failures.append(failure("TASK_ID_INVALID", str(value.get("task_id"))))
    if value.get("candidate_state") != "verified_delivery_candidate":
        failures.append(failure("CANDIDATE_NOT_VERIFIED", str(value.get("candidate_state"))))
    if not isinstance(value.get("baseline"), str) or not HEX40.fullmatch(value["baseline"]):
        failures.append(failure("BASELINE_INVALID", str(value.get("baseline"))))
    contract_hash = value.get("acceptance_contract_sha256")
    if not isinstance(contract_hash, str) or not HEX64.fullmatch(contract_hash):
        failures.append(failure("CONTRACT_HASH_INVALID", str(contract_hash)))
    elif contract is not None and (not contract.is_file() or sha256_file(contract) != contract_hash):
        failures.append(failure("CONTRACT_HASH_MISMATCH", str(contract)))

    changed = value.get("changed_paths")
    if not isinstance(changed, list) or not all(isinstance(item, str) and item for item in changed):
        failures.append(failure("CHANGED_PATHS_INVALID", "changed_paths"))
    elif len(changed) != len(set(changed)):
        failures.append(failure("CHANGED_PATHS_DUPLICATE", "changed_paths"))

    gates = value.get("active_gates")
    if not isinstance(gates, list) or len(gates) != len(set(gates)) or any(item not in KNOWN_GATES for item in gates):
        failures.append(failure("ACTIVE_GATES_INVALID", "active_gates"))
        gates = []

    check_ids: set[str] = set()
    checks_by_id: dict[str, dict[str, Any]] = {}
    checks = value.get("checks")
    if not isinstance(checks, list) or not checks:
        failures.append(failure("CHECKS_MISSING", "checks"))
    else:
        for index, raw in enumerate(checks):
            check = strict_mapping(raw, {"id", "kind", "status", "evidence_ref"}, {"id", "kind", "status", "evidence_ref", "artifact_or_log_id"}, f"checks[{index}]", failures)
            if check is None:
                continue
            check_id = str(check.get("id") or "")
            if not isinstance(check.get("id"), str) or not check_id or check_id in check_ids:
                failures.append(failure("CHECK_ID_INVALID_OR_DUPLICATE", check_id or str(index)))
            check_ids.add(check_id)
            checks_by_id[check_id] = check
            if check.get("kind") not in CHECK_KINDS or check.get("status") != "pass":
                failures.append(failure("CHECK_NOT_PASS", check_id or str(index)))
            if not isinstance(check.get("evidence_ref"), str) or not check["evidence_ref"]:
                failures.append(failure("CHECK_EVIDENCE_REF_INVALID", check_id or str(index)))
            if "artifact_or_log_id" in check and not isinstance(check.get("artifact_or_log_id"), str):
                failures.append(failure("CHECK_ARTIFACT_ID_INVALID", check_id or str(index)))
            if task_root is not None:
                evidence_path(task_root, check.get("evidence_ref"), contract, f"checks[{index}]", failures)

    if version == "1.3":
        contract_value = load_contract_value(contract, failures)
        oracle_by_id = {
            item.get("id"): item
            for item in (contract_value.get("oracles") if isinstance(contract_value.get("oracles"), list) else [])
            if isinstance(item, dict)
        }
        for criterion in contract_value.get("acceptance_criteria") or []:
            if not isinstance(criterion, dict):
                continue
            criterion_id = str(criterion.get("id") or "")
            oracle = oracle_by_id.get(criterion.get("oracle_id"), {})
            check = checks_by_id.get(criterion_id)
            if check is None or check.get("evidence_ref") != oracle.get("evidence_ref"):
                failures.append(failure("CRITERION_CHECK_ORACLE_EVIDENCE_MISMATCH", criterion_id))
            if criterion.get("mandatory") is True and criterion.get("owner_visible") is True and (
                oracle.get("evidence_class") not in {"runtime", "owner"} or oracle.get("authorized") is not True
            ):
                failures.append(failure("OWNER_VISIBLE_ORACLE_NOT_AUTHORIZED", criterion_id))
        validate_evidence_ceiling(
            value,
            contract_value,
            task_root=task_root,
            contract=contract,
            outcome="task_completed",
            failures=failures,
        )

    review_required = {"required", "status", "reviewer_id", "evidence_ref", "open_findings"}
    if version in {"1.2", "1.3"}:
        review_required |= {"reviewer_role_count", "adjudication_ref", "open_confirmed_material_findings"}
    review = strict_mapping(
        value.get("independent_review"),
        review_required,
        review_required,
        "independent_review",
        failures,
    )
    if review is not None:
        if (
            not isinstance(review.get("required"), bool)
            or review.get("status") not in {"pass", "not_required"}
            or not isinstance(review.get("reviewer_id"), str)
            or not isinstance(review.get("evidence_ref"), str)
            or not isinstance(review.get("open_findings"), int)
            or isinstance(review.get("open_findings"), bool)
            or review.get("open_findings") != 0
        ):
            failures.append(failure("REVIEW_INVALID", "required"))
        elif review["required"]:
            if review.get("status") != "pass" or review.get("open_findings") != 0 or not review.get("reviewer_id") or "independent_review" not in gates:
                failures.append(failure("REVIEW_NOT_CLEAN", "independent_review"))
        elif review.get("status") != "not_required":
            failures.append(failure("REVIEW_STATUS_INVALID", str(review.get("status"))))
        if version in {"1.2", "1.3"}:
            expected_roles = 1 if review.get("required") is True else 0
            if review.get("reviewer_role_count") != expected_roles or review.get("open_confirmed_material_findings") != 0:
                failures.append(failure("REVIEW_ADJUDICATION_SUMMARY_INVALID", "independent_review"))
            if not isinstance(review.get("adjudication_ref"), str) or not review.get("adjudication_ref"):
                failures.append(failure("REVIEW_ADJUDICATION_REF_INVALID", "independent_review"))
            elif task_root is not None and review.get("required") is True:
                validate_review_adjudication(task_root, review.get("adjudication_ref"), contract, failures)
        if task_root is not None:
            evidence_path(task_root, review.get("evidence_ref"), contract, "independent_review", failures)

    unresolved = value.get("unresolved_conditions")
    if not isinstance(unresolved, list):
        failures.append(failure("UNRESOLVED_CONDITIONS_MISSING", "field must be an array"))
    else:
        for index, item in enumerate(unresolved):
            condition = strict_mapping(item, {"id", "condition", "impact", "owner_or_external_gate"}, {"id", "condition", "impact", "owner_or_external_gate"}, f"unresolved_conditions[{index}]", failures)
            if condition is not None and any(not isinstance(condition.get(field), str) for field in ("id", "condition", "impact", "owner_or_external_gate")):
                failures.append(failure("UNRESOLVED_CONDITION_INVALID", str(index)))

    rollback = strict_mapping(value.get("rollback_readback"), {"required", "status", "evidence_ref"}, {"required", "status", "evidence_ref"}, "rollback_readback", failures)
    if rollback is not None:
        if not isinstance(rollback.get("required"), bool) or rollback.get("status") not in {"pass", "not_required"} or not isinstance(rollback.get("evidence_ref"), str):
            failures.append(failure("ROLLBACK_READBACK_INVALID", "rollback_readback"))
        if task_root is not None:
            evidence_path(task_root, rollback.get("evidence_ref"), contract, "rollback_readback", failures)

    readiness = value.get("environment_readiness")
    if "environment_readiness" in gates or readiness is not None:
        readiness = strict_mapping(readiness, {"required", "status", "evidence_ref"}, {"required", "status", "evidence_ref"}, "environment_readiness", failures)
        if readiness is None:
            failures.append(failure("ENVIRONMENT_READINESS_INVALID", "environment_readiness"))
        else:
            expected = "pass" if "environment_readiness" in gates else "not_required"
            if readiness.get("required") != ("environment_readiness" in gates) or readiness.get("status") != expected or not isinstance(readiness.get("evidence_ref"), str):
                failures.append(failure("ENVIRONMENT_READINESS_INVALID", "environment_readiness"))
            if task_root is not None:
                evidence_path(task_root, readiness.get("evidence_ref"), contract, "environment_readiness", failures)

    scope = strict_mapping(value.get("scope_diff"), {"status", "forbidden_paths", "diff_sha256"}, {"status", "forbidden_paths", "diff_sha256"}, "scope_diff", failures)
    if scope is not None and (scope.get("status") != "pass" or scope.get("forbidden_paths") != [] or not isinstance(scope.get("diff_sha256"), str) or not HEX64.fullmatch(scope["diff_sha256"])):
        failures.append(failure("SCOPE_DIFF_INVALID", "scope_diff"))
    final_git = strict_mapping(value.get("final_git"), {"candidate_tree", "candidate_diff_status", "worktree_status", "post_commit_receipt"}, {"candidate_tree", "candidate_diff_status", "worktree_status", "post_commit_receipt"}, "final_git", failures)
    if final_git is not None and (
        not isinstance(final_git.get("candidate_tree"), str)
        or not HEX40.fullmatch(final_git["candidate_tree"])
        or final_git.get("candidate_diff_status") != "pass"
        or final_git.get("worktree_status") not in {"candidate_staged", "clean_after_commit"}
        or not isinstance(final_git.get("post_commit_receipt"), str)
        or not final_git.get("post_commit_receipt")
    ):
        failures.append(failure("FINAL_GIT_INVALID", "final_git"))

    metrics = value.get("pipeline_metrics")
    if metrics is not None:
        metrics = strict_mapping(metrics, set(), METRIC_FIELDS, "pipeline_metrics", failures)
        if metrics is not None:
            for key, item in metrics.items():
                if key == "first_patch_passed":
                    if not isinstance(item, bool):
                        failures.append(failure("PIPELINE_METRIC_INVALID", key))
                elif key in {"repair_iterations", "active_gate_count", "false_block_count"}:
                    if not isinstance(item, int) or isinstance(item, bool) or item < 0:
                        failures.append(failure("PIPELINE_METRIC_INVALID", key))
                elif not isinstance(item, (int, float)) or isinstance(item, bool) or item < 0:
                    failures.append(failure("PIPELINE_METRIC_INVALID", key))

    if version in {"1.2", "1.3"}:
        repair_summary = strict_mapping(
            value.get("repair_summary"),
            {"iterations", "same_failure_repeats", "consecutive_no_progress"},
            {"iterations", "same_failure_repeats", "consecutive_no_progress"},
            "repair_summary",
            failures,
        )
        if repair_summary is not None:
            for field in ("iterations", "same_failure_repeats", "consecutive_no_progress"):
                item = repair_summary.get(field)
                if not isinstance(item, int) or isinstance(item, bool) or item < 0:
                    failures.append(failure("REPAIR_SUMMARY_INVALID", field))
            budget = contract_total_repair_budget(contract)
            if budget is None or repair_summary.get("iterations", 0) > budget:
                failures.append(failure("TOTAL_REPAIR_BUDGET_EXCEEDED", f"budget={budget},iterations={repair_summary.get('iterations')}"))
            if repair_summary.get("same_failure_repeats", 0) >= 2 or repair_summary.get("consecutive_no_progress", 0) >= 2:
                failures.append(failure("TERMINAL_REPAIR_TRIGGER_IGNORED", str(repair_summary)))

    if version == "1.3":
        validate_lifecycle_evidence(
            value,
            contract,
            repo_root=repo_root,
            task_root=task_root,
            lease=lease,
            verify_runtime=verify_runtime,
            failures=failures,
        )

    if declaration:
        failures.extend(validate_declaration(declaration))
        required_sets = contract_required_sets(contract, failures)
        if required_sets is not None:
            contract_checks, contract_gates = required_sets
            declared_checks = declaration.get("required_check_ids")
            declared_gates = declaration.get("required_gates")
            if not isinstance(declared_checks, list) or set(declared_checks) != contract_checks:
                failures.append(failure("DECLARATION_CONTRACT_CHECKS_MISMATCH", json.dumps({"contract": sorted(contract_checks), "declaration": declared_checks}, ensure_ascii=True)))
            if not isinstance(declared_gates, list) or set(declared_gates) != contract_gates:
                failures.append(failure("DECLARATION_CONTRACT_GATES_MISMATCH", json.dumps({"contract": sorted(contract_gates), "declaration": declared_gates}, ensure_ascii=True)))
            if set(gates) != contract_gates:
                failures.append(failure("RECEIPT_CONTRACT_GATES_MISMATCH", json.dumps({"contract": sorted(contract_gates), "receipt": sorted(gates)}, ensure_ascii=True)))
    required_gates = declaration.get("required_gates", [])
    if not isinstance(required_gates, list) or any(item not in gates for item in required_gates):
        failures.append(failure("REQUIRED_GATES_MISSING", str(required_gates)))
    required_checks = declaration.get("required_check_ids", [])
    if not isinstance(required_checks, list) or any(str(item) not in check_ids for item in required_checks):
        failures.append(failure("REQUIRED_CHECKS_MISSING", str(required_checks)))
    if verify_runtime:
        if not all((repo_root, task_root, lease, receipt_path)):
            failures.append(failure("RUNTIME_CONTEXT_MISSING", "repo_root/task_root/lease/receipt_path"))
        else:
            validate_git_finalization(value, repo_root, task_root, declaration, lease, receipt_path, failures)
    return failures

#!/usr/bin/env python3
"""Validate a generic Agent Memory Kit code-change contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

REQUIRED_IMPACT_FIELDS = (
    "callers",
    "consumers",
    "shared_state",
    "database",
    "cache_or_queue",
    "schedules_and_timezones",
    "lifecycle_and_recovery",
    "concurrency",
    "compatibility",
    "performance",
)
FINAL_TRUE_FIELDS = (
    "semantic_walkthrough_completed",
    "final_diff_reviewed",
    "causal_chain_reviewed",
    "failure_paths_reviewed",
    "performance_impact_reviewed",
    "resource_lifecycle_reviewed",
    "non_goals_preserved",
)


def mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        stripped = value.strip()
        return bool(stripped and not stripped.startswith("<"))
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return value is not None


def validate(document: Any, phase: str) -> list[str]:
    errors: list[str] = []
    root = mapping(document)
    policy_ref = mapping(root.get("policy_ref"))
    if policy_ref.get("id") != "PRODUCT_CODE_CHANGE_POLICY":
        errors.append("policy_ref.id must be PRODUCT_CODE_CHANGE_POLICY")

    skills = mapping(root.get("mandatory_skills"))
    for name in ("production-engineering-standard", "complete-technical-communication"):
        if mapping(skills.get(name)).get("applied") is not True:
            errors.append(f"mandatory skill not applied: {name}")

    task = mapping(root.get("task"))
    if not nonempty(task.get("id")):
        errors.append("task.id is required")
    if not nonempty(task.get("component")):
        errors.append("task.component is required")
    if not nonempty(task.get("owner_request_verbatim")):
        errors.append("task.owner_request_verbatim is required")

    logic = mapping(root.get("business_logic"))
    for field in ("required_behavior", "preserved_behavior", "non_goals"):
        if not nonempty(logic.get(field)):
            errors.append(f"business_logic.{field} must be non-empty")
    unresolved = logic.get("unresolved_product_questions")
    if unresolved != []:
        errors.append("business_logic.unresolved_product_questions must be an empty list")

    current = mapping(root.get("current_behavior"))
    for field in (
        "producer",
        "normalization_or_calculation",
        "storage_or_state",
        "transport",
        "consumer",
        "owner_visible_result",
        "observed_problem",
    ):
        if not nonempty(current.get(field)):
            errors.append(f"current_behavior.{field} is required")

    exact = mapping(root.get("exact_change"))
    changed = exact.get("changed_behavior")
    if not isinstance(changed, list) or not changed:
        errors.append("exact_change.changed_behavior must be a non-empty list")
    else:
        for index, item in enumerate(changed):
            row = mapping(item)
            for field in ("criterion", "files", "symbols", "required_logic"):
                if not nonempty(row.get(field)):
                    errors.append(f"exact_change.changed_behavior[{index}].{field} is required")
    if not nonempty(exact.get("forbidden_changes")):
        errors.append("exact_change.forbidden_changes must be non-empty")

    impact = mapping(root.get("impact_analysis"))
    for field in REQUIRED_IMPACT_FIELDS:
        if field not in impact or not isinstance(impact.get(field), list):
            errors.append(f"impact_analysis.{field} must be a list")

    if phase == "final":
        review = mapping(root.get("quality_review"))
        for field in FINAL_TRUE_FIELDS:
            if review.get(field) is not True:
                errors.append(f"quality_review.{field} must be true")
        if review.get("tests_used_as_specification") is not False:
            errors.append("quality_review.tests_used_as_specification must be false")
        if review.get("unexplained_production_changes") != []:
            errors.append("quality_review.unexplained_production_changes must be empty")
        if not isinstance(review.get("remaining_unverified_risks"), list):
            errors.append("quality_review.remaining_unverified_risks must be a list")

        trace = mapping(root.get("final_traceability"))
        if not nonempty(trace.get("changed_symbols")):
            errors.append("final_traceability.changed_symbols must be non-empty")
        if trace.get("unexplained_changes") != []:
            errors.append("final_traceability.unexplained_changes must be empty")
        if not isinstance(trace.get("remaining_risks"), list):
            errors.append("final_traceability.remaining_risks must be a list")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--phase", required=True, choices=("pre-edit", "final"))
    args = parser.parse_args()
    try:
        document = yaml.safe_load(args.contract.read_text(encoding="utf-8"))
        errors = validate(document, args.phase)
    except Exception as exc:
        errors = [f"contract read/parse failed: {type(exc).__name__}: {exc}"]
    result = {
        "ok": not errors,
        "phase": args.phase,
        "contract": str(args.contract),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

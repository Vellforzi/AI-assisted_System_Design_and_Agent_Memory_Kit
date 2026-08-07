#!/usr/bin/env python3
"""Dependency-free structural and semantic oracle for Project Artifact Contract V1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1] / "project_artifact_contract_v1"
FIXTURE = ROOT / "fixtures" / "project-artifact-v1-smoke.json"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, True)


def _validate(schema: dict[str, Any], value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    expected = schema.get("type")
    if expected:
        options = expected if isinstance(expected, list) else [expected]
        if not any(_type_matches(value, item) for item in options):
            return [f"{path}:type"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}:const")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}:enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}:minLength")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}:pattern")
    if isinstance(value, int) and not isinstance(value, bool) and value < schema.get("minimum", value):
        errors.append(f"{path}:minimum")
    if isinstance(value, dict):
        required = schema.get("required", [])
        errors.extend(f"{path}.{name}:required" for name in required if name not in value)
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}.{name}:additionalProperties" for name in value if name not in properties)
        for name, child in properties.items():
            if name in value:
                errors.extend(_validate(child, value[name], f"{path}.{name}"))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}:minItems")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{path}:uniqueItems")
        child = schema.get("items")
        if child:
            for index, item in enumerate(value):
                errors.extend(_validate(child, item, f"{path}[{index}]"))
    if "oneOf" in schema:
        matches = [not _validate(option, value, path) for option in schema["oneOf"]]
        if sum(matches) != 1:
            errors.append(f"{path}:oneOf")
    return errors


def _semantic_reasons(contract: str, payload: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if contract == "CommitmentLedgerV1":
        for item in payload.get("commitments", []):
            settlement = item.get("settlement")
            if item.get("status", "open") in {"settled_success", "settled_failure", "cancelled"} and (
                not isinstance(settlement, dict) or not settlement.get("evidence_refs")
            ):
                reasons.append("SETTLEMENT_EVIDENCE_REQUIRED")
            if (
                isinstance(settlement, dict)
                and settlement.get("provenance_tier") == "self"
                and item.get("memory_credit_state") == "approved"
            ):
                reasons.append("SELF_GRADE_CANNOT_APPROVE_MEMORY")
            if item.get("status") == "open" and settlement is not None:
                reasons.append("OPEN_COMMITMENT_CANNOT_HAVE_SETTLEMENT")
            expected_outcome = {"settled_success": "success", "settled_failure": "failure", "cancelled": "cancelled"}.get(item.get("status"))
            if expected_outcome and isinstance(settlement, dict) and settlement.get("outcome") != expected_outcome:
                reasons.append("SETTLEMENT_OUTCOME_STATUS_MISMATCH")
    elif contract == "ClaimLedgerV2":
        for item in payload.get("claims", []):
            if item.get("status") == "verified" and not (
                item.get("evidence_refs") or item.get("verification_receipt_refs")
            ):
                reasons.append("VERIFIED_CLAIM_SUPPORT_REQUIRED")
    elif contract == "ArtifactExcerptV1":
        if payload.get("end_line", 0) < payload.get("start_line", 0):
            reasons.append("EXCERPT_RANGE_INVALID")
        if payload.get("navigation_only") is not True:
            reasons.append("EXCERPT_MUST_BE_NAVIGATION_ONLY")
    elif contract == "MemoryDeltaV1":
        if payload.get("status") in {"approved", "applied"} and payload.get("owner_review") != "approved":
            reasons.append("MEMORY_DELTA_OWNER_APPROVAL_REQUIRED")
    return sorted(set(reasons))


def run_oracle() -> dict[str, Any]:
    fixture = _load(FIXTURE)
    base = FIXTURE.parent
    valid = _load((base / fixture["valid_examples"]).resolve())
    invalid = _load((base / fixture["invalid_examples"]).resolve())
    schemas = {
        name: _load((base / relative).resolve())
        for name, relative in fixture["schema_files"].items()
    }
    cases: list[dict[str, Any]] = []
    for name, schema in schemas.items():
        valid_errors = _validate(schema, valid[name])
        invalid_errors = _validate(schema, invalid[name]) if name in invalid else []
        cases.append({
            "case_id": f"schema:{name}",
            "valid_example_passed": not valid_errors,
            "valid_errors": valid_errors,
            "invalid_example_rejected": bool(invalid_errors) if name in invalid else None,
            "invalid_errors": invalid_errors,
        })
    semantic_by_contract = {
        name: _semantic_reasons(name, payload) for name, payload in invalid.items()
    }
    admissible = {
        item.get("id")
        for item in valid.get("CommitmentLedgerV1", {}).get("commitments", [])
        if item.get("status") == "settled_success"
        and isinstance(item.get("settlement"), dict)
        and item["settlement"].get("provenance_tier") in {"runtime", "external", "owner"}
        and item["settlement"].get("evidence_refs")
    }
    delta = invalid.get("MemoryDeltaV1", {})
    delta_reasons = _semantic_reasons("MemoryDeltaV1", delta)
    if not delta.get("commitment_refs") or any(ref not in admissible for ref in delta.get("commitment_refs", [])):
        delta_reasons.append("MEMORY_DELTA_ADMISSIBLE_SETTLEMENT_REQUIRED")
    semantic_by_contract["MemoryDeltaCross"] = sorted(set(delta_reasons))
    semantic_cases = []
    for case in fixture["semantic_cases"]:
        actual = semantic_by_contract.get(case["contract"], [])
        expected = sorted(case["expected_reason_codes"])
        semantic_cases.append({
            "case_id": case["case_id"],
            "reason_codes": actual,
            "expected_reason_codes": expected,
            "passed": actual == expected,
        })
    structural_pass = all(case["valid_example_passed"] for case in cases)
    invalid_pass = all(
        case["invalid_example_rejected"] is not False
        for case in cases
    )
    return {
        "suite_id": fixture["suite_id"],
        "status": "passed" if structural_pass and invalid_pass and all(item["passed"] for item in semantic_cases) else "failed",
        "schema_cases": cases,
        "semantic_cases": semantic_cases,
        "runtime_service_started": False,
        "files_modified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args()
    report = run_oracle()
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"{report['suite_id']}: {report['status']}")
        for case in report["schema_cases"]:
            print(f"- {case['case_id']}: valid={case['valid_example_passed']} invalid_rejected={case['invalid_example_rejected']}")
        for case in report["semantic_cases"]:
            print(f"- {case['case_id']}: {'passed' if case['passed'] else 'failed'}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

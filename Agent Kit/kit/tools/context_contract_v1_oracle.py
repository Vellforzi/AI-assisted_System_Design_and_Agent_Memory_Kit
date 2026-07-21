"""Portable Context Contract V1 fixture oracle.

The oracle is intentionally read-only and standard-library-only. It validates
the JSON Schema subset used by the V1 contracts, evaluates source-backed
cross-payload invariants, and reuses the existing context governance helper to
parse the legacy context-selection smoke suite.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, Sequence

from context_governance_helper import load_smoke_cases


KIT_DIR = Path(__file__).resolve().parent.parent
CONTRACT_DIR = KIT_DIR / "secondary_memory_governance" / "context_contract_v1"
MANIFEST_PATH = CONTRACT_DIR / "fixtures" / "context-contract-v1-smoke.json"
RETRIEVAL_POLICY_PATH = KIT_DIR / "secondary_memory_governance" / "retrieval_policy.yaml"
LEGACY_SMOKE_PATH = KIT_DIR / "secondary_memory_governance" / "context_selection_smoke_cases.yaml"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_type_matches(expected: str, value: Any) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def validate_schema_subset(schema: dict[str, Any], value: Any, path: str = "$") -> list[str]:
    """Validate only keywords used by the checked-in standalone V1 schemas."""

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"SCHEMA_CONST:{path}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"SCHEMA_ENUM:{path}")

    expected_type = schema.get("type")
    if expected_type and not _json_type_matches(str(expected_type), value):
        return [*errors, f"SCHEMA_TYPE:{path}"]

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"SCHEMA_REQUIRED:{path}.{key}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"SCHEMA_ADDITIONAL_PROPERTY:{path}.{key}")
        for key, child in properties.items():
            if key in value:
                errors.extend(validate_schema_subset(child, value[key], f"{path}.{key}"))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < int(schema["minItems"]):
            errors.append(f"SCHEMA_MIN_ITEMS:{path}")
        if "maxItems" in schema and len(value) > int(schema["maxItems"]):
            errors.append(f"SCHEMA_MAX_ITEMS:{path}")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append(f"SCHEMA_UNIQUE_ITEMS:{path}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_schema_subset(item_schema, item, f"{path}[{index}]"))

    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            errors.append(f"SCHEMA_MIN_LENGTH:{path}")
        if "pattern" in schema and re.search(str(schema["pattern"]), value) is None:
            errors.append(f"SCHEMA_PATTERN:{path}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"SCHEMA_MINIMUM:{path}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"SCHEMA_MAXIMUM:{path}")
    return errors


def _parse_inline_list(value: str) -> set[str]:
    stripped = value.strip().removeprefix("[").removesuffix("]")
    return {item.strip().strip('"').strip("'") for item in stripped.split(",") if item.strip()}


def _hard_excluded_statuses(profile: str) -> set[str]:
    in_profiles = False
    current_profile: str | None = None
    for raw_line in RETRIEVAL_POLICY_PATH.read_text(encoding="utf-8").splitlines():
        if raw_line == "profiles:":
            in_profiles = True
            continue
        if not in_profiles:
            continue
        if raw_line and not raw_line.startswith(" "):
            break
        profile_match = re.match(r"^  ([a-z][a-z0-9_]*):\s*$", raw_line)
        if profile_match:
            current_profile = profile_match.group(1)
            continue
        if current_profile == profile:
            exclude_match = re.match(r"^    hard_exclude_statuses:\s*(\[.*\])\s*$", raw_line)
            if exclude_match:
                return _parse_inline_list(exclude_match.group(1))
    return set()


def _matches_forbidden(path: str, patterns: Sequence[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(normalized == pattern or fnmatch.fnmatch(normalized, pattern) for pattern in patterns)


def evaluate_policy(request: dict[str, Any], bundle: dict[str, Any], reason_order: Sequence[str]) -> list[str]:
    reasons: set[str] = set()
    sources = bundle["sources"]
    source_paths = {source["path"] for source in sources}
    selection = request["selection"]

    if len(sources) > selection["max_sources"]:
        reasons.add("OVER_RETRIEVAL")
    if set(selection["required_paths"]) - source_paths:
        reasons.add("UNDER_RETRIEVAL")
    if any(_matches_forbidden(path, selection["forbidden_paths"]) for path in source_paths):
        reasons.add("FORBIDDEN_PATH_SELECTED")

    hard_excluded = _hard_excluded_statuses(request["profile"])
    if any(source["status"] in hard_excluded for source in sources):
        reasons.add("STALE_AUTHORITY")
    return [reason for reason in reason_order if reason in reasons]


def _legacy_smoke_ids() -> set[str]:
    with tempfile.TemporaryDirectory(prefix="context-contract-v1-") as temporary:
        root = Path(temporary)
        destination = root / "docs" / "project_map" / "eval_suite" / "context_selection_smoke_cases.yaml"
        destination.parent.mkdir(parents=True)
        shutil.copyfile(LEGACY_SMOKE_PATH, destination)
        return {case.id for case in load_smoke_cases(root)}


def _schema_paths(manifest: dict[str, Any]) -> dict[str, Path]:
    base = MANIFEST_PATH.parent
    return {name: (base / relative).resolve() for name, relative in manifest["schemas"].items()}


def _validate_examples(schemas: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    file_map = {
        "context-request-v1.json": "ContextRequestV1",
        "context-bundle-v1.json": "ContextBundleV1",
        "context-receipt-v1.json": "ContextReceiptV1",
    }
    for expectation in ("valid", "invalid"):
        for filename, contract_type in file_map.items():
            path = CONTRACT_DIR / "examples" / expectation / filename
            errors = validate_schema_subset(schemas[contract_type], _load_json(path))
            actual_valid = not errors
            expected_valid = expectation == "valid"
            passed = actual_valid == expected_valid
            if not passed:
                failures.append(f"example {expectation}/{filename} validity mismatch")
            results.append({
                "path": path.relative_to(KIT_DIR).as_posix(),
                "expected_valid": expected_valid,
                "actual_valid": actual_valid,
                "reason_codes": errors,
                "status": "passed" if passed else "failed",
            })
    return results, failures


def run_oracle() -> dict[str, Any]:
    manifest = _load_json(MANIFEST_PATH)
    schema_paths = _schema_paths(manifest)
    schemas = {name: _load_json(path) for name, path in schema_paths.items()}
    failures: list[str] = []

    for name, schema in schemas.items():
        if schema.get("$schema") != manifest["schema_dialect"]:
            failures.append(f"{name} schema dialect mismatch")
        if not str(schema.get("$id", "")).startswith("urn:agent-memory-kit:context-contract:v1:"):
            failures.append(f"{name} has an unstable or missing $id")
        if "$ref" in json.dumps(schema):
            failures.append(f"{name} must remain standalone in V1")

    legacy_ids = _legacy_smoke_ids()
    reason_order = manifest["reason_code_order"]
    case_results: list[dict[str, Any]] = []
    for case in manifest["cases"]:
        schema_errors = {
            "request": validate_schema_subset(schemas["ContextRequestV1"], case["request"]),
            "bundle": validate_schema_subset(schemas["ContextBundleV1"], case["bundle"]),
            "receipt": validate_schema_subset(schemas["ContextReceiptV1"], case["receipt"]),
        }
        schema_valid = {name: not errors for name, errors in schema_errors.items()}
        policy_reasons = evaluate_policy(case["request"], case["bundle"], reason_order)
        expected = case["expected"]
        mismatches: list[str] = []
        if schema_valid != expected["schema_valid"]:
            mismatches.append("schema_valid")
        if (not policy_reasons) != expected["policy_valid"]:
            mismatches.append("policy_valid")
        if policy_reasons != expected["reason_codes"]:
            mismatches.append("expected_reason_codes")
        if case["receipt"]["reason_codes"] != policy_reasons:
            mismatches.append("receipt_reason_codes")
        expected_outcome = "fail" if policy_reasons else "pass"
        if case["receipt"]["outcome"] != expected_outcome:
            mismatches.append("receipt_outcome")
        legacy_id = case.get("reuses_legacy_smoke_case")
        if legacy_id and legacy_id not in legacy_ids:
            mismatches.append("legacy_smoke_case_missing")
        if case["bundle"]["request_id"] != case["request"]["request_id"]:
            mismatches.append("request_bundle_link")
        if case["receipt"]["request_id"] != case["request"]["request_id"]:
            mismatches.append("request_receipt_link")
        if case["receipt"]["bundle_id"] != case["bundle"]["bundle_id"]:
            mismatches.append("bundle_receipt_link")
        if mismatches:
            failures.append(f"{case['case_id']}: {', '.join(mismatches)}")
        case_results.append({
            "case_id": case["case_id"],
            "status": "failed" if mismatches else "passed",
            "schema_valid": schema_valid,
            "schema_reason_codes": schema_errors,
            "policy_valid": not policy_reasons,
            "reason_codes": policy_reasons,
            "reuses_legacy_smoke_case": legacy_id,
            "mismatches": mismatches,
        })

    example_results, example_failures = _validate_examples(schemas)
    failures.extend(example_failures)
    return {
        "oracle_type": "context_contract_v1_fixture_oracle",
        "contract_version": manifest["contract_version"],
        "schema_dialect": manifest["schema_dialect"],
        "status": "failed" if failures else "passed",
        "case_count": len(case_results),
        "cases": case_results,
        "examples": example_results,
        "legacy_smoke_case_ids": sorted(legacy_ids),
        "failures": failures,
        "runtime_service_started": False,
        "persistent_memory_created": False,
    }


def _to_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Context Contract V1 Oracle",
        "",
        f"Status: **{result['status']}**",
        f"Cases: {result['case_count']}",
        "",
    ]
    for case in result["cases"]:
        reasons = ", ".join(case["reason_codes"]) or "none"
        lines.append(f"- `{case['case_id']}`: {case['status']} (reason codes: {reasons})")
    if result["failures"]:
        lines.extend(["", "## Failures", *[f"- {failure}" for failure in result["failures"]]])
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args(argv)
    result = run_oracle()
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(_to_markdown(result))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

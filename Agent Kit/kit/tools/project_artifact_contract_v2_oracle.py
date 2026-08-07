#!/usr/bin/env python3
"""Dependency-free oracle for Project Artifact Contract V2 (Agent Memory Kit v5)."""

from __future__ import annotations

import argparse
from fnmatch import fnmatch
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1] / "project_artifact_contract_v2"
FIXTURE = ROOT / "fixtures" / "project-artifact-v2-smoke.json"


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
    """Validate the closed-schema subset used by the Kit without dependencies."""
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
    if isinstance(value, int) and not isinstance(value, bool):
        if value < schema.get("minimum", value):
            errors.append(f"{path}:minimum")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        errors.extend(f"{path}.{key}:required" for key in schema.get("required", []) if key not in value)
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}.{key}:additionalProperties" for key in value if key not in props)
        for key, child in props.items():
            if key in value:
                errors.extend(_validate(child, value[key], f"{path}.{key}"))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}:minItems")
        if schema.get("uniqueItems"):
            normalized = {json.dumps(item, sort_keys=True) for item in value}
            if len(normalized) != len(value):
                errors.append(f"{path}:uniqueItems")
        if schema.get("items"):
            for index, item in enumerate(value):
                errors.extend(_validate(schema["items"], item, f"{path}[{index}]"))
    if "oneOf" in schema:
        matches = sum(not _validate(option, value, path) for option in schema["oneOf"])
        if matches != 1:
            errors.append(f"{path}:oneOf")
    return errors


def _has_cycle(items: list[dict[str, Any]]) -> bool:
    graph = {item.get("id"): item.get("blocked_by", []) for item in items}
    state: dict[str, int] = {}

    def visit(node: str) -> bool:
        state[node] = 1
        for dependency in graph.get(node, []):
            if dependency not in graph:
                continue
            if state.get(dependency) == 1 or (state.get(dependency, 0) == 0 and visit(dependency)):
                return True
        state[node] = 2
        return False

    return any(state.get(node, 0) == 0 and visit(node) for node in graph)


def work_item_frontier(payload: dict[str, Any]) -> list[str]:
    items = payload.get("items", [])
    status = {item.get("id"): item.get("status") for item in items}
    return sorted(
        item["id"] for item in items
        if item.get("status") == "accepted"
        and item.get("context_fit") == "fresh_context"
        and all(status.get(ref) == "verified" for ref in item.get("blocked_by", []))
    )


def exploration_frontier(payload: dict[str, Any]) -> list[str]:
    items = payload.get("items", [])
    status = {item.get("id"): item.get("status") for item in items}
    return sorted(
        item["id"] for item in items
        if item.get("status") == "open"
        and all(status.get(ref) in {"resolved", "cancelled"} for ref in item.get("blocked_by", []))
    )


def capability_statuses(payload: dict[str, Any]) -> dict[str, str]:
    current = {item.get("id"): "deprecated" if item.get("lifecycle") == "deprecated" else "unknown"
               for item in payload.get("definitions", [])}
    latest: dict[str, tuple[int, str]] = {}
    for assessment in payload.get("assessments", []):
        cap = assessment.get("capability_id")
        candidate = (assessment.get("sequence", -1), assessment.get("status", "unknown"))
        if cap not in latest or candidate[0] > latest[cap][0]:
            latest[cap] = candidate
    current.update({cap: item[1] for cap, item in latest.items()})
    return current


def _task_reasons(payload: dict[str, Any]) -> list[str]:
    profile = payload.get("workflow_profile", {})
    reasons: list[str] = []
    mode = profile.get("mode")
    if mode == "delivery" and profile.get("task_scale") == "multi_session" and not profile.get("work_item_graph_ref"):
        reasons.append("TASK_MULTI_SESSION_GRAPH_REQUIRED")
    if mode == "delivery" and profile.get("task_scale") == "multi_session" and profile.get("delivery_strategy") != "tracer_graph":
        reasons.append("TASK_MULTI_SESSION_TRACER_GRAPH_REQUIRED")
    required_ref = {
        "exploration": ("exploration_map_ref", "TASK_EXPLORATION_MAP_REQUIRED"),
        "triage": ("triage_item_ref", "TASK_TRIAGE_ARTIFACT_REQUIRED"),
        "design_probe": ("design_probe_ref", "TASK_DESIGN_PROBE_REQUIRED"),
        "review": ("review_receipt_refs", "TASK_REVIEW_RECEIPT_REQUIRED"),
    }.get(mode)
    if required_ref and not profile.get(required_ref[0]):
        reasons.append(required_ref[1])
    risk = profile.get("risk_class")
    if risk in {"high", "irreversible"}:
        if not profile.get("plan_challenge_ref"):
            reasons.append("TASK_HIGH_RISK_CHALLENGE_REQUIRED")
        if profile.get("review_policy") != "adversarial" or not profile.get("review_receipt_refs"):
            reasons.append("TASK_HIGH_RISK_ADVERSARIAL_REVIEW_REQUIRED")
    elif risk == "significant" and mode == "delivery" and (
        profile.get("review_policy") != "fresh_context" or not profile.get("review_receipt_refs")
    ):
        reasons.append("TASK_SIGNIFICANT_REVIEW_REQUIRED")
    if profile.get("capability_impact") in {"adds", "changes"} and not profile.get("capability_refs"):
        reasons.append("TASK_CAPABILITY_REGISTRY_REQUIRED")
    return reasons


def _graph_reasons(payload: dict[str, Any]) -> list[str]:
    items = payload.get("items", [])
    ids = {item.get("id") for item in items}
    reasons: list[str] = []
    if any(ref not in ids for item in items for ref in item.get("blocked_by", [])):
        reasons.append("WORK_GRAPH_UNKNOWN_BLOCKER")
    if _has_cycle(items):
        reasons.append("WORK_GRAPH_CYCLE")
    if any(item.get("status") == "accepted" and item.get("context_fit") == "requires_split" for item in items):
        reasons.append("WORK_ITEM_REQUIRES_SPLIT")
    asserted = sorted(payload.get("frontier_assertion", {}).get("item_ids", []))
    if asserted != work_item_frontier(payload):
        reasons.append("WORK_GRAPH_FRONTIER_MISMATCH")
    return reasons


def _challenge_reasons(payload: dict[str, Any]) -> list[str]:
    questions = payload.get("questions", [])
    open_questions = [item for item in questions if item.get("resolution") == "open"]
    reasons: list[str] = []
    if len(open_questions) > 1:
        reasons.append("PLAN_CHALLENGE_MULTIPLE_OPEN_QUESTIONS")
    open_ids = {item.get("id") for item in open_questions}
    if (open_ids and payload.get("current_question_id") not in open_ids) or (
        not open_ids and payload.get("current_question_id") is not None
    ):
        reasons.append("PLAN_CHALLENGE_CURRENT_QUESTION_MISMATCH")
    for item in questions:
        if item.get("resolution") == "closed" and not item.get("owner_decision"):
            reasons.append("PLAN_CHALLENGE_OWNER_DECISION_REQUIRED")
        if item.get("resolution") == "probe_required" and not item.get("design_probe_ref"):
            reasons.append("PLAN_CHALLENGE_PROBE_REF_REQUIRED")
    if payload.get("status") == "accepted" and open_questions:
        reasons.append("PLAN_CHALLENGE_ACCEPTED_WITH_OPEN_QUESTIONS")
    shared = payload.get("shared_understanding", {})
    if payload.get("status") == "accepted" and (
        not shared.get("owner_attested") or not shared.get("evidence_ref")
    ):
        reasons.append("PLAN_CHALLENGE_OWNER_ATTESTATION_REQUIRED")
    return reasons


def _review_reasons(payload: dict[str, Any]) -> list[str]:
    reasons = []
    if payload.get("author_reasoning_included") is not False:
        reasons.append("REVIEW_AUTHOR_REASONING_FORBIDDEN")
    if payload.get("mutation_performed") is not False:
        reasons.append("REVIEW_MUTATION_FORBIDDEN")
    if payload.get("repair_authorized") is not False:
        reasons.append("REVIEW_REPAIR_AUTHORITY_FORBIDDEN")
    if payload.get("status") == "passed" and any(item.get("blocking") for item in payload.get("findings", [])):
        reasons.append("REVIEW_PASSED_WITH_BLOCKING_FINDING")
    return reasons


def _exploration_reasons(payload: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if payload.get("product_mutation_allowed") is not False:
        reasons.append("EXPLORATION_DELIVERY_MUTATION_FORBIDDEN")
    if sorted(payload.get("frontier_assertion", {}).get("item_ids", [])) != exploration_frontier(payload):
        reasons.append("EXPLORATION_FRONTIER_MISMATCH")
    if payload.get("status") == "ready_for_delivery":
        if any(item.get("status") not in {"resolved", "cancelled"} for item in payload.get("items", [])):
            reasons.append("EXPLORATION_READY_WITH_OPEN_WORK")
        if any(item.get("state") == "unresolved" for item in payload.get("fog", [])):
            reasons.append("EXPLORATION_READY_WITH_UNRESOLVED_FOG")
        if payload.get("owner_acceptance") != "accepted":
            reasons.append("EXPLORATION_READY_WITHOUT_OWNER_ACCEPTANCE")
    return reasons


def _triage_reasons(payload: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for item in payload.get("items", []):
        if item.get("state") != "ready_for_agent":
            continue
        if item.get("category") == "bug" and (
            item.get("reproduction_state") != "reproducible" or not item.get("evidence_refs")
        ):
            reasons.append("TRIAGE_AGENT_READY_EVIDENCE_REQUIRED")
        if item.get("category") == "enhancement" and not item.get("brief"):
            reasons.append("TRIAGE_AGENT_READY_BRIEF_REQUIRED")
        if not item.get("verification_plan"):
            reasons.append("TRIAGE_AGENT_READY_VERIFICATION_REQUIRED")
        if item.get("delegation_blockers"):
            reasons.append("TRIAGE_AGENT_READY_BLOCKED")
        if item.get("owner_disposition") != "agent":
            reasons.append("TRIAGE_AGENT_READY_OWNER_DISPOSITION_REQUIRED")
    return reasons


def _probe_reasons(payload: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if payload.get("production_reuse") != "forbidden":
        reasons.append("DESIGN_PROBE_PRODUCTION_REUSE_FORBIDDEN")
    if payload.get("status") in {"answered", "inconclusive", "cancelled"}:
        if not payload.get("evidence_refs"):
            reasons.append("DESIGN_PROBE_TERMINAL_EVIDENCE_REQUIRED")
        if payload.get("provenance_tier") not in {"runtime", "external", "owner"}:
            reasons.append("DESIGN_PROBE_TERMINAL_PROVENANCE_REQUIRED")
    return reasons


def _capability_reasons(payload: dict[str, Any], receipts: dict[str, dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    definition_ids = [item.get("id") for item in payload.get("definitions", [])]
    if len(definition_ids) != len(set(definition_ids)):
        reasons.append("CAPABILITY_DEFINITION_DUPLICATE")
    sequence_keys: set[tuple[str, int]] = set()
    for assessment in payload.get("assessments", []):
        if assessment.get("capability_id") not in set(definition_ids):
            reasons.append("CAPABILITY_ASSESSMENT_UNKNOWN_DEFINITION")
        key = (assessment.get("capability_id"), assessment.get("sequence"))
        if key in sequence_keys:
            reasons.append("CAPABILITY_ASSESSMENT_SEQUENCE_DUPLICATE")
        sequence_keys.add(key)
        if assessment.get("status") != "passing":
            continue
        refs = assessment.get("verification_receipt_refs", [])
        if not refs or not any(
            receipts.get(ref, {}).get("verification_level") == "end_to_end"
            and receipts.get(ref, {}).get("status") == "passed"
            and receipts.get(ref, {}).get("evidence_refs")
            and assessment.get("capability_id") in receipts.get(ref, {}).get("subject_refs", [])
            for ref in refs
        ):
            reasons.append("CAPABILITY_END_TO_END_RECEIPT_REQUIRED")
    asserted = {
        item.get("capability_id"): item.get("status")
        for item in payload.get("current_status_assertion", {}).get("items", [])
    }
    if asserted != capability_statuses(payload):
        reasons.append("CAPABILITY_STATUS_ASSERTION_MISMATCH")
    return reasons


def _domain_reasons(payload: dict[str, Any]) -> list[str]:
    context_ids = {item.get("id") for item in payload.get("contexts", [])}
    current = [item for item in payload.get("terms", []) if item.get("status") == "current"]
    seen: set[tuple[str, str]] = set()
    canonical = {(item.get("context_id"), item.get("canonical_term", "").casefold()) for item in current}
    reasons: list[str] = []
    for item in current:
        key = (item.get("context_id"), item.get("canonical_term", "").casefold())
        if key in seen:
            reasons.append("DOMAIN_CANONICAL_TERM_DUPLICATE")
        seen.add(key)
        if any((item.get("context_id"), synonym.casefold()) in canonical for synonym in item.get("do_not_use", [])):
            reasons.append("DOMAIN_FORBIDDEN_SYNONYM_CONFLICT")
    if any(rel.get("from_context") not in context_ids or rel.get("to_context") not in context_ids
           for rel in payload.get("relationships", [])):
        reasons.append("DOMAIN_CONTEXT_REFERENCE_UNKNOWN")
    if reasons and payload.get("owner_review") == "accepted":
        reasons.append("DOMAIN_CONFLICT_REQUIRES_OWNER_REVIEW")
    return reasons


def _commitment_reasons(payload: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    expected = {"settled_success": "success", "settled_failure": "failure", "cancelled": "cancelled"}
    for item in payload.get("commitments", []):
        settlement = item.get("settlement")
        if item.get("status") in expected and (not isinstance(settlement, dict) or not settlement.get("evidence_refs")):
            reasons.append("SETTLEMENT_EVIDENCE_REQUIRED")
        if isinstance(settlement, dict) and settlement.get("provenance_tier") == "self" and item.get("memory_credit_state") == "approved":
            reasons.append("SELF_GRADE_CANNOT_APPROVE_MEMORY")
        if item.get("status") in expected and isinstance(settlement, dict) and settlement.get("outcome") != expected[item["status"]]:
            reasons.append("SETTLEMENT_OUTCOME_STATUS_MISMATCH")
    return reasons


def _verification_reasons(payload: dict[str, Any]) -> list[str]:
    if payload.get("status") == "passed" and not payload.get("evidence_refs"):
        return ["VERIFICATION_PASS_EVIDENCE_REQUIRED"]
    return []


def _semantic(contract: str, payload: dict[str, Any], bundle: dict[str, Any]) -> list[str]:
    receipts = {
        item.get("receipt_id"): item
        for item in (bundle.get("VerificationReceiptV2", {}) if isinstance(bundle.get("VerificationReceiptV2"), list)
                     else [bundle.get("VerificationReceiptV2", {})])
    }
    functions = {
        "TaskContractV3": _task_reasons,
        "WorkItemGraphV1": _graph_reasons,
        "PlanChallengeV1": _challenge_reasons,
        "ReviewReceiptV1": _review_reasons,
        "ExplorationMapV1": _exploration_reasons,
        "TriageLedgerV1": _triage_reasons,
        "DesignProbeV1": _probe_reasons,
        "DomainLanguageV1": _domain_reasons,
        "CommitmentLedgerV2": _commitment_reasons,
        "VerificationReceiptV2": _verification_reasons,
    }
    if contract == "CapabilityRegistryV1":
        return sorted(set(_capability_reasons(payload, receipts)))
    function = functions.get(contract)
    return sorted(set(function(payload) if function else []))


def _cross_bundle_reasons(bundle: dict[str, Any]) -> list[str]:
    """Resolve typed refs and completion gates across one artifact bundle."""
    task = bundle.get("TaskContractV3", {})
    profile = task.get("workflow_profile", {})
    reasons: list[str] = []
    mode = profile.get("mode")
    if mode in {"exploration", "triage", "design_probe", "review"} and (
        task.get("intent") in {"stage", "apply"} or task.get("permission_mode") == "apply"
    ):
        reasons.append("TASK_NON_DELIVERY_MODE_MUTATION_FORBIDDEN")
    for field, contract, id_field, code in (
        ("work_item_graph_ref", "WorkItemGraphV1", "graph_id", "TASK_GRAPH_REF_UNRESOLVED"),
        ("plan_challenge_ref", "PlanChallengeV1", "challenge_id", "TASK_CHALLENGE_REF_UNRESOLVED"),
        ("exploration_map_ref", "ExplorationMapV1", "map_id", "TASK_EXPLORATION_REF_UNRESOLVED"),
        ("design_probe_ref", "DesignProbeV1", "probe_id", "TASK_PROBE_REF_UNRESOLVED"),
    ):
        ref = profile.get(field)
        if ref and bundle.get(contract, {}).get(id_field) != ref:
            reasons.append(code)
    risk = profile.get("risk_class")
    if risk in {"high", "irreversible"}:
        challenge = bundle.get("PlanChallengeV1", {})
        shared = challenge.get("shared_understanding", {})
        accepted = (
            challenge.get("challenge_id") == profile.get("plan_challenge_ref")
            and challenge.get("status") == "accepted"
            and not any(item.get("resolution") == "open" for item in challenge.get("questions", []))
            and shared.get("owner_attested") is True
            and bool(shared.get("evidence_ref"))
        )
        if not accepted:
            reasons.append("TASK_HIGH_RISK_CHALLENGE_NOT_ACCEPTED")
    review_refs = set(profile.get("review_receipt_refs", []))
    reviews = bundle.get("ReviewReceiptV1", [])
    reviews = reviews if isinstance(reviews, list) else [reviews]
    accepted_reviews = {item.get("review_id"): item for item in reviews
                        if item.get("status") == "passed" and item.get("owner_disposition") == "accepted"}
    required_profile = "adversarial" if risk in {"high", "irreversible"} else "fresh_context" if risk == "significant" else None
    if required_profile and not any(ref in accepted_reviews and accepted_reviews[ref].get("profile") == required_profile
                                    for ref in review_refs):
        reasons.append("TASK_REQUIRED_REVIEW_NOT_ACCEPTED")
    registry = bundle.get("CapabilityRegistryV1", {})
    definitions = {item.get("id") for item in registry.get("definitions", [])}
    if any(ref not in definitions for ref in profile.get("capability_refs", [])):
        reasons.append("TASK_CAPABILITY_REF_UNRESOLVED")
    if task.get("status") == "completed" and profile.get("capability_impact") in {"adds", "changes"}:
        statuses = capability_statuses(registry)
        if any(statuses.get(ref) not in {"passing", "failing"} for ref in profile.get("capability_refs", [])):
            reasons.append("TASK_COMPLETED_CAPABILITY_ASSESSMENT_REQUIRED")
    domain = bundle.get("DomainLanguageV1", {})
    context_ids = {item.get("id") for item in domain.get("contexts", [])}
    if any(ref not in context_ids for ref in profile.get("domain_context_refs", [])):
        reasons.append("TASK_DOMAIN_CONTEXT_REF_UNRESOLVED")
    authority = bundle.get("SourceAuthorityPolicy", {})
    affected = set(authority.get("affected_bounded_context_refs", []))
    project_files = [path.replace("\\", "/") for path in task.get("scope", {}).get("project_files", [])]
    for context in authority.get("bounded_contexts", []):
        patterns = context.get("path_patterns", [])
        if any(fnmatch(path, pattern) for path in project_files for pattern in patterns):
            affected.add(context.get("id"))
    affected.discard(None)
    if affected and not affected.issubset(set(profile.get("domain_context_refs", []))):
        reasons.append("TASK_BOUNDED_CONTEXT_DOMAIN_REF_REQUIRED")
    return sorted(set(reasons))


def run_oracle() -> dict[str, Any]:
    fixture = _load(FIXTURE)
    base = FIXTURE.parent
    valid = _load((base / fixture["valid_examples"]).resolve())
    invalid = _load((base / fixture["invalid_examples"]).resolve())
    schemas = {name: _load((base / path).resolve()) for name, path in fixture["schema_files"].items()}
    schema_cases = []
    for name, schema in schemas.items():
        valid_errors = _validate(schema, valid[name])
        invalid_errors = _validate(schema, invalid[name])
        semantic_errors = _semantic(name, invalid[name], invalid)
        schema_cases.append({
            "case_id": f"schema:{name}",
            "valid_example_passed": not valid_errors,
            "valid_errors": valid_errors,
            "invalid_example_rejected": bool(invalid_errors or semantic_errors),
            "invalid_errors": invalid_errors,
        })
    valid_semantic = {name: _semantic(name, payload, valid) for name, payload in valid.items()}
    valid_semantic["CrossContractActivation"] = _cross_bundle_reasons(valid)
    semantic_cases = []
    for case in fixture["semantic_cases"]:
        actual = _semantic(case["contract"], invalid[case["contract"]], invalid)
        expected = sorted(case["expected_reason_codes"])
        semantic_cases.append({
            "case_id": case["case_id"],
            "reason_codes": actual,
            "expected_reason_codes": expected,
            "passed": actual == expected,
        })
    passed = (
        all(case["valid_example_passed"] and case["invalid_example_rejected"] for case in schema_cases)
        and not any(valid_semantic.values())
        and all(case["passed"] for case in semantic_cases)
    )
    return {
        "suite_id": fixture["suite_id"],
        "status": "passed" if passed else "failed",
        "schema_cases": schema_cases,
        "valid_semantic_reason_codes": valid_semantic,
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

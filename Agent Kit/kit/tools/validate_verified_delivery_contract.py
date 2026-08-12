#!/usr/bin/env python3
"""Validate compact verified-delivery contracts (1.1-1.3) and open 1.0 tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


LEGACY_REQUIRED = {
    "schema_version", "task_id", "owner_goal", "user_visible_outcomes",
    "developer_visible_outcomes", "non_goals", "allowed_write_scope",
    "forbidden_scope", "preserved_invariants", "dependency_entrypoints",
    "required_characterization", "acceptance_matrix", "targeted_regressions",
    "baseline_regressions", "black_box_scenarios", "build_gate", "deploy_gate",
    "rollback_readback_requirements", "independent_review_requirements",
    "unresolved_external_conditions", "owner_gate", "stop_conditions",
}
COMPACT_REQUIRED = {
    "schema_version", "task_id", "owner_goal", "allowed_change",
    "protected_behavior", "write_scope", "acceptance_criteria", "oracles",
    "stop_condition",
}
KNOWN_GATES = {
    "characterization", "targeted", "baseline", "scope_diff",
    "independent_review", "environment_readiness", "black_box", "build",
    "deploy", "rollback_readback", "finalization",
}
RISK_REQUIRED_GATES = {
    "R1": {"targeted", "scope_diff", "finalization"},
    "R2": {"targeted", "scope_diff", "environment_readiness", "finalization"},
    "R3": {"targeted", "baseline", "scope_diff", "environment_readiness", "rollback_readback", "finalization"},
    "R4": {"targeted", "baseline", "scope_diff", "environment_readiness", "rollback_readback", "independent_review", "finalization"},
}
CANONICAL_REPAIR_TRIGGERS_V11 = {
    "same_deterministic_failure_repeated",
    "two_no_progress_iterations",
    "scope_or_capability_expansion_required",
    "external_dependency_unavailable",
    "oracle_missing_or_contradictory",
    "owner_goal_or_protected_behavior_change_required",
}
CANONICAL_REPAIR_TRIGGERS_V12 = CANONICAL_REPAIR_TRIGGERS_V11 | {
    "total_repair_budget_exhausted",
    "authorization_or_integrity_gate",
}
COMPLEXITY_REPAIR_BUDGETS = {
    "simple": 1,
    "standard": 2,
    "complex_infrastructure": 3,
}
CANONICAL_ORACLE_KINDS = {"command", "state", "trace", "diff", "visual", "owner"}
EVIDENCE_CLASSES = {"static", "synthetic", "runtime", "owner"}
HIGH_LEVEL_EVIDENCE_CLASSES = {
    "harness_runtime": {"runtime", "owner"},
    "platform_runtime": {"runtime", "owner"},
    "owner_acceptance": {"owner"},
}
VERIFICATION_LEVELS = [
    "source_structure", "component_behavior", "cross_component_contract",
    "harness_runtime", "platform_runtime", "owner_acceptance",
]
VERIFICATION_LEVEL_SET = set(VERIFICATION_LEVELS)
ORACLE_STRENGTH_METHODS = {"negative_path", "fault_injection", "mutation_testing", "combined"}
TASK_SHAPES = {"simple", "implementation", "diagnostic", "repair", "runtime", "owner_visible"}
DEFECT_STRATEGIES = {"single", "separate_task_units", "explicit_coupling"}
ARCHITECTURE_REVIEW_COVERS = {
    "root_cause", "mutation_point", "dependency_neighborhood", "expected_diff", "verification_oracle",
}


def load_contract(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("contract root must be a mapping")
    return value


def failure(code: str, reason: str) -> dict[str, str]:
    return {"code": code, "reason": reason}


def validate_legacy(value: dict[str, Any]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    missing = sorted(LEGACY_REQUIRED - set(value))
    if missing:
        failures.append(failure("REQUIRED_FIELDS_MISSING", ", ".join(missing)))
    for name in (
        "user_visible_outcomes", "developer_visible_outcomes",
        "allowed_write_scope", "forbidden_scope", "preserved_invariants",
        "dependency_entrypoints", "required_characterization",
        "acceptance_matrix", "stop_conditions",
    ):
        if name in value and (not isinstance(value[name], list) or not value[name]):
            failures.append(failure("NON_EMPTY_LIST_REQUIRED", name))
    seen: set[str] = set()
    for index, criterion in enumerate(value.get("acceptance_matrix") or []):
        if not isinstance(criterion, dict):
            failures.append(failure("CRITERION_NOT_MAPPING", str(index)))
            continue
        criterion_id = str(criterion.get("id") or "").strip()
        if not criterion_id:
            failures.append(failure("CRITERION_ID_MISSING", str(index)))
        elif criterion_id in seen:
            failures.append(failure("CRITERION_ID_DUPLICATE", criterion_id))
        seen.add(criterion_id)
        oracle = criterion.get("oracle")
        if not isinstance(oracle, dict):
            failures.append(failure("ORACLE_MISSING", criterion_id or str(index)))
            continue
        for field in ("kind", "check", "pass_condition", "evidence_ref"):
            if not str(oracle.get(field) or "").strip():
                failures.append(failure("ORACLE_FIELD_MISSING", f"{criterion_id}:{field}"))
    review = value.get("independent_review_requirements")
    if not isinstance(review, dict) or "required" not in review:
        failures.append(failure("REVIEW_REQUIREMENT_INVALID", "independent_review_requirements"))
    for gate in ("build_gate", "deploy_gate"):
        item = value.get(gate)
        if not isinstance(item, dict) or "required" not in item or "oracle" not in item:
            failures.append(failure("GATE_INVALID", gate))
    return failures


def validate_compact(value: dict[str, Any]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    version = str(value.get("schema_version") or "")
    missing = sorted(COMPACT_REQUIRED - set(value))
    if missing:
        failures.append(failure("REQUIRED_FIELDS_MISSING", ", ".join(missing)))
    for name in ("allowed_change", "protected_behavior", "acceptance_criteria", "oracles", "stop_condition"):
        if name in value and (not isinstance(value[name], list) or not value[name]):
            failures.append(failure("NON_EMPTY_LIST_REQUIRED", name))
    scope = value.get("write_scope")
    if not isinstance(scope, dict) or not isinstance(scope.get("allowed"), list) or not scope.get("allowed") or not isinstance(scope.get("forbidden"), list):
        failures.append(failure("WRITE_SCOPE_INVALID", "write_scope.allowed must be non-empty and forbidden must be a list"))

    oracle_ids: set[str] = set()
    for index, oracle in enumerate(value.get("oracles") or []):
        if not isinstance(oracle, dict):
            failures.append(failure("ORACLE_NOT_MAPPING", str(index)))
            continue
        oracle_id = str(oracle.get("id") or "").strip()
        if not oracle_id:
            failures.append(failure("ORACLE_ID_MISSING", str(index)))
        elif oracle_id in oracle_ids:
            failures.append(failure("ORACLE_ID_DUPLICATE", oracle_id))
        oracle_ids.add(oracle_id)
        for field in ("kind", "check", "pass_condition", "evidence_ref"):
            if not str(oracle.get(field) or "").strip():
                failures.append(failure("ORACLE_FIELD_MISSING", f"{oracle_id}:{field}"))
        if version in {"1.2", "1.3"} and oracle.get("kind") not in CANONICAL_ORACLE_KINDS:
            failures.append(failure("ORACLE_KIND_UNSUPPORTED", f"{oracle_id}:{oracle.get('kind')}"))
        if version == "1.3":
            if oracle.get("evidence_class") not in EVIDENCE_CLASSES:
                failures.append(failure("ORACLE_EVIDENCE_CLASS_INVALID", f"{oracle_id}:{oracle.get('evidence_class')}"))
            if not isinstance(oracle.get("authorized"), bool):
                failures.append(failure("ORACLE_AUTHORIZATION_INVALID", oracle_id))
            if "verification_level" in oracle and oracle.get("verification_level") not in VERIFICATION_LEVEL_SET:
                failures.append(failure("ORACLE_VERIFICATION_LEVEL_INVALID", f"{oracle_id}:{oracle.get('verification_level')}"))
            allowed_classes = HIGH_LEVEL_EVIDENCE_CLASSES.get(str(oracle.get("verification_level") or ""))
            if allowed_classes is not None and oracle.get("evidence_class") not in allowed_classes:
                failures.append(failure("ORACLE_EVIDENCE_LEVEL_CLASS_INVALID", f"{oracle_id}:{oracle.get('verification_level')}:{oracle.get('evidence_class')}"))
            if oracle.get("verification_level") == "owner_acceptance" and oracle.get("kind") != "owner":
                failures.append(failure("OWNER_ACCEPTANCE_ORACLE_KIND_INVALID", f"{oracle_id}:{oracle.get('kind')}"))

    criterion_ids: set[str] = set()
    for index, criterion in enumerate(value.get("acceptance_criteria") or []):
        if not isinstance(criterion, dict):
            failures.append(failure("CRITERION_NOT_MAPPING", str(index)))
            continue
        criterion_id = str(criterion.get("id") or "").strip()
        oracle_id = str(criterion.get("oracle_id") or "").strip()
        if not criterion_id:
            failures.append(failure("CRITERION_ID_MISSING", str(index)))
        elif criterion_id in criterion_ids:
            failures.append(failure("CRITERION_ID_DUPLICATE", criterion_id))
        criterion_ids.add(criterion_id)
        if not str(criterion.get("outcome") or "").strip():
            failures.append(failure("CRITERION_OUTCOME_MISSING", criterion_id or str(index)))
        if not oracle_id or oracle_id not in oracle_ids:
            failures.append(failure("CRITERION_ORACLE_UNRESOLVED", f"{criterion_id}:{oracle_id}"))
        if version == "1.3":
            if not isinstance(criterion.get("mandatory"), bool) or not isinstance(criterion.get("owner_visible"), bool):
                failures.append(failure("CRITERION_CLASSIFICATION_INVALID", criterion_id or str(index)))
            if not str(criterion.get("defect_id") or "").strip():
                failures.append(failure("CRITERION_DEFECT_ID_MISSING", criterion_id or str(index)))

    risk_tier = str(value.get("risk_tier") or "R1")
    if risk_tier not in RISK_REQUIRED_GATES:
        failures.append(failure("RISK_TIER_INVALID", risk_tier))
        risk_tier = "R1"
    gate_profile = value.get("gate_profile")
    active: list[str] = []
    if gate_profile is not None:
        active = gate_profile.get("active") if isinstance(gate_profile, dict) else None
        if not isinstance(active, list) or len(active) != len(set(active)) or any(item not in KNOWN_GATES for item in active):
            failures.append(failure("GATE_PROFILE_INVALID", "gate_profile.active"))
            active = []
        else:
            missing_gates = sorted(RISK_REQUIRED_GATES[risk_tier] - set(active))
            if missing_gates:
                failures.append(failure("RISK_GATES_MISSING", f"{risk_tier}:{','.join(missing_gates)}"))
    elif "risk_tier" in value:
        failures.append(failure("GATE_PROFILE_REQUIRED", risk_tier))

    extensions = value.get("extensions")
    if extensions is not None and not isinstance(extensions, dict):
        failures.append(failure("EXTENSIONS_INVALID", "extensions"))
        extensions = {}
    extensions = extensions or {}
    extension_gates = {
        "characterization": "characterization",
        "environment_readiness": "environment_readiness",
        "black_box": "black_box",
        "build": "build",
        "deploy": "deploy",
        "rollback_readback": "rollback_readback",
    }
    for gate, extension in extension_gates.items():
        configured = extensions.get(extension)
        if gate in active and (not isinstance(configured, (list, dict)) or not configured):
            failures.append(failure("ACTIVE_GATE_EXTENSION_MISSING", f"{gate}:{extension}"))
        if configured and gate not in active:
            failures.append(failure("INACTIVE_GATE_EXTENSION_PRESENT", f"{gate}:{extension}"))
    review_extension = extensions.get("independent_review")
    if "independent_review" in active:
        if (
            not isinstance(review_extension, dict)
            or review_extension.get("required") is not True
            or not str(review_extension.get("reviewer_role") or "").strip()
            or not isinstance(review_extension.get("falsification_targets"), list)
            or not review_extension.get("falsification_targets")
        ):
            failures.append(failure("INDEPENDENT_REVIEW_EXTENSION_INVALID", "extensions.independent_review"))
        elif version in {"1.2", "1.3"} and (
            review_extension.get("max_active_reviewer_roles") != 1
            or review_extension.get("reuse_role_for_rereview") is not True
        ):
            failures.append(failure("REVIEWER_CHAIN_POLICY_INVALID", "extensions.independent_review"))
    elif isinstance(review_extension, dict) and review_extension.get("required") is True:
        failures.append(failure("INACTIVE_GATE_EXTENSION_PRESENT", "independent_review"))

    repair = value.get("repair_policy")
    if version in {"1.2", "1.3"} and repair is None:
        failures.append(failure("REPAIR_POLICY_REQUIRED", "repair_policy"))
    if repair is not None:
        if not isinstance(repair, dict):
            failures.append(failure("REPAIR_POLICY_INVALID", "repair_policy"))
        else:
            for field in ("max_same_failure_repeats", "max_no_progress_iterations"):
                item = repair.get(field)
                if not isinstance(item, int) or isinstance(item, bool) or item < 1 or item > 2:
                    failures.append(failure("REPAIR_BUDGET_INVALID", field))
            if version in {"1.2", "1.3"}:
                complexity = repair.get("complexity_class")
                total = repair.get("max_total_iterations")
                if complexity not in COMPLEXITY_REPAIR_BUDGETS:
                    failures.append(failure("REPAIR_COMPLEXITY_INVALID", str(complexity)))
                elif total != COMPLEXITY_REPAIR_BUDGETS[complexity]:
                    failures.append(failure("TOTAL_REPAIR_BUDGET_INVALID", f"{complexity}:{total}"))
            triggers = repair.get("terminal_triggers")
            expected_triggers = CANONICAL_REPAIR_TRIGGERS_V12 if version in {"1.2", "1.3"} else CANONICAL_REPAIR_TRIGGERS_V11
            if not isinstance(triggers, list) or set(triggers) != expected_triggers or len(triggers) != len(set(triggers)):
                failures.append(failure("REPAIR_TERMINALS_MISSING", "repair_policy.terminal_triggers"))
    if version in {"1.2", "1.3"}:
        lifecycle = value.get("lifecycle_policy")
        if not isinstance(lifecycle, dict):
            failures.append(failure("LIFECYCLE_POLICY_INVALID", "lifecycle_policy"))
        else:
            if lifecycle.get("lifecycle_owner") != "primary_agent":
                failures.append(failure("LIFECYCLE_OWNER_INVALID", str(lifecycle.get("lifecycle_owner"))))
            if lifecycle.get("autonomous_within_scope") is not True:
                failures.append(failure("AUTONOMOUS_CONTINUATION_REQUIRED", "lifecycle_policy.autonomous_within_scope"))
            if lifecycle.get("resolve_discoverable_details_from_project_evidence") is not True:
                failures.append(failure("AUTONOMOUS_DISCOVERY_REQUIRED", "lifecycle_policy.resolve_discoverable_details_from_project_evidence"))
            if lifecycle.get("owner_gate_only_for_material_choice_or_new_authority") is not True:
                failures.append(failure("OWNER_GATE_POLICY_INVALID", "lifecycle_policy.owner_gate_only_for_material_choice_or_new_authority"))
            if lifecycle.get("repair_only_confirmed_findings") is not True:
                failures.append(failure("REVIEW_ADJUDICATION_REQUIRED", "lifecycle_policy.repair_only_confirmed_findings"))
            outcomes = lifecycle.get("final_outcomes")
            if not isinstance(outcomes, list) or outcomes != ["task_completed", "task_blocked"]:
                failures.append(failure("FINAL_OUTCOMES_INVALID", str(outcomes)))
    if version == "1.3":
        failures.extend(validate_conditional_controls(value))
        failures.extend(validate_cross_component_code_proof(value, extensions, oracle_ids))
    metrics = value.get("metrics_policy")
    if metrics is not None and (
        not isinstance(metrics, dict)
        or not isinstance(metrics.get("enabled"), bool)
        or metrics.get("record_only_measured_values") is not True
    ):
        failures.append(failure("METRICS_POLICY_INVALID", "metrics_policy"))
    return failures


def non_empty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def validate_cross_component_code_proof(
    value: dict[str, Any],
    extensions: dict[str, Any],
    oracle_ids: set[str],
) -> list[dict[str, str]]:
    """Validate the optional evidence ceiling and production cross-component profile."""
    failures: list[dict[str, str]] = []
    target = value.get("verification_target")
    profile = extensions.get("cross_component_code_proof")
    if target is None and profile is None:
        return failures
    if target not in VERIFICATION_LEVEL_SET:
        failures.append(failure("VERIFICATION_TARGET_INVALID", str(target)))
        return failures

    oracle_by_id = {
        str(item.get("id") or ""): item
        for item in value.get("oracles") or []
        if isinstance(item, dict)
    }
    for oracle_id, oracle in oracle_by_id.items():
        if oracle.get("verification_level") not in VERIFICATION_LEVEL_SET:
            failures.append(failure("ORACLE_VERIFICATION_LEVEL_REQUIRED", oracle_id))

    if profile is None:
        if VERIFICATION_LEVELS.index(target) >= VERIFICATION_LEVELS.index("cross_component_contract"):
            failures.append(failure("CROSS_COMPONENT_PROFILE_REQUIRED", target))
        return failures
    required_profile_fields = {
        "required", "platform_runtime_required", "complex_state_machine",
        "production_path", "lifecycle_contract", "boundary_contract", "oracle_strength",
    }
    if not isinstance(profile, dict) or set(profile) != required_profile_fields:
        failures.append(failure("CROSS_COMPONENT_PROFILE_INVALID", "extensions.cross_component_code_proof"))
        return failures
    if profile.get("required") is not True:
        failures.append(failure("CROSS_COMPONENT_PROFILE_NOT_ACTIVE", str(profile.get("required"))))
    controls = value.get("conditional_controls") if isinstance(value.get("conditional_controls"), dict) else {}
    shape = controls.get("task_shape") if isinstance(controls.get("task_shape"), dict) else {}
    if shape.get("coupled") is not True:
        failures.append(failure("CROSS_COMPONENT_TASK_NOT_COUPLED", "conditional_controls.task_shape.coupled"))
    if VERIFICATION_LEVELS.index(target) < VERIFICATION_LEVELS.index("cross_component_contract"):
        failures.append(failure("CROSS_COMPONENT_TARGET_TOO_LOW", target))
    if not isinstance(profile.get("platform_runtime_required"), bool) or not isinstance(profile.get("complex_state_machine"), bool):
        failures.append(failure("CROSS_COMPONENT_PROFILE_FLAGS_INVALID", "platform_runtime_required/complex_state_machine"))
    platform_target = VERIFICATION_LEVELS.index(target) >= VERIFICATION_LEVELS.index("platform_runtime")
    if profile.get("platform_runtime_required") is not platform_target:
        failures.append(failure("PLATFORM_RUNTIME_TARGET_MISMATCH", target))

    production = profile.get("production_path")
    production_fields = {
        "production_entrypoint", "authoritative_initializer", "actual_call_route",
        "components", "production_artifact_refs", "oracle_ids",
        "executes_production_code", "test_only_reimplementation",
    }
    if not isinstance(production, dict) or set(production) != production_fields:
        failures.append(failure("PRODUCTION_PATH_CONTRACT_INVALID", "production_path"))
        production = {}
    if any(not isinstance(production.get(field), str) or not production.get(field, "").strip() for field in ("production_entrypoint", "authoritative_initializer")):
        failures.append(failure("PRODUCTION_PATH_IDENTITY_MISSING", "production_path"))
    if not non_empty_string_list(production.get("actual_call_route")) or len(production.get("actual_call_route") or []) < 2:
        failures.append(failure("PRODUCTION_CALL_ROUTE_INVALID", "actual_call_route"))
    if not non_empty_string_list(production.get("components")) or len(set(production.get("components") or [])) < 2:
        failures.append(failure("PRODUCTION_COMPONENT_SET_INVALID", "components"))
    if not non_empty_string_list(production.get("production_artifact_refs")):
        failures.append(failure("PRODUCTION_ARTIFACT_REFS_INVALID", "production_artifact_refs"))
    if production.get("executes_production_code") is not True or production.get("test_only_reimplementation") is not False:
        failures.append(failure("PRODUCTION_PATH_NOT_BOUND", "production code must be exercised; a test-only replica is insufficient"))

    lifecycle = profile.get("lifecycle_contract")
    lifecycle_fields = {
        "typed_state", "field_ownership", "allowed_transitions", "success_invariants",
        "rollback_paths", "failure_paths", "concurrency_cases", "instance_invariants",
        "deferred_trigger_independence_required", "deferred_trigger_oracle_id", "oracle_ids",
    }
    if not isinstance(lifecycle, dict) or set(lifecycle) != lifecycle_fields:
        failures.append(failure("CROSS_COMPONENT_LIFECYCLE_INVALID", "lifecycle_contract"))
        lifecycle = {}
    if not isinstance(lifecycle.get("typed_state"), str) or not lifecycle.get("typed_state", "").strip():
        failures.append(failure("TYPED_STATE_MISSING", "lifecycle_contract.typed_state"))
    ownership = lifecycle.get("field_ownership")
    if not isinstance(ownership, dict) or not ownership or any(not isinstance(k, str) or not k.strip() or not isinstance(v, str) or not v.strip() for k, v in ownership.items()):
        failures.append(failure("FIELD_OWNERSHIP_INVALID", "lifecycle_contract.field_ownership"))
    for field in ("allowed_transitions", "success_invariants", "rollback_paths", "failure_paths", "concurrency_cases", "instance_invariants"):
        if not non_empty_string_list(lifecycle.get(field)):
            failures.append(failure("LIFECYCLE_EVIDENCE_MISSING", field))
    if not isinstance(lifecycle.get("deferred_trigger_independence_required"), bool):
        failures.append(failure("DEFERRED_TRIGGER_POLICY_INVALID", "deferred_trigger_independence_required"))
    deferred_oracle = str(lifecycle.get("deferred_trigger_oracle_id") or "")
    if lifecycle.get("deferred_trigger_independence_required") is True and deferred_oracle not in oracle_ids:
        failures.append(failure("DEFERRED_TRIGGER_ORACLE_MISSING", deferred_oracle))
    if deferred_oracle not in (lifecycle.get("oracle_ids") or []):
        failures.append(failure("DEFERRED_TRIGGER_ORACLE_NOT_BOUND", deferred_oracle))

    boundary = profile.get("boundary_contract")
    boundary_fields = {
        "required", "interfaces", "bindings", "verification_methods", "regex_only",
        "authoritative_identity_fields", "downstream_reconstruction_forbidden", "oracle_ids",
    }
    if not isinstance(boundary, dict) or set(boundary) != boundary_fields:
        failures.append(failure("BOUNDARY_CONTRACT_INVALID", "boundary_contract"))
        boundary = {}
    if boundary.get("required") is not True or boundary.get("regex_only") is not False or boundary.get("downstream_reconstruction_forbidden") is not True:
        failures.append(failure("BOUNDARY_PROOF_WEAK", "boundary must be required, non-regex-only, and authoritative"))
    if not non_empty_string_list(boundary.get("interfaces")) or not non_empty_string_list(boundary.get("verification_methods")):
        failures.append(failure("BOUNDARY_EVIDENCE_MISSING", "interfaces/verification_methods"))
    if set(boundary.get("verification_methods") or []) <= {"regex", "text_search"}:
        failures.append(failure("BOUNDARY_REGEX_ONLY", "verification_methods"))
    if not non_empty_string_list(boundary.get("authoritative_identity_fields")):
        failures.append(failure("IDENTITY_AUTHORITY_FIELDS_MISSING", "authoritative_identity_fields"))
    bindings = boundary.get("bindings")
    if not isinstance(bindings, list) or not bindings:
        failures.append(failure("BOUNDARY_BINDINGS_MISSING", "boundary_contract.bindings"))
        bindings = []
    binding_ids: set[str] = set()
    parameter_fields = {"name", "type", "size_bytes", "position"}
    binding_fields = {
        "id", "import_name", "export_name", "import_parameters", "export_parameters",
        "import_return_type", "export_return_type", "import_calling_convention",
        "export_calling_convention", "import_architecture", "export_architecture",
        "import_protocol_version", "export_protocol_version", "compile_required",
        "compile_oracle_id",
    }
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict) or set(binding) != binding_fields:
            failures.append(failure("BOUNDARY_BINDING_INVALID", str(index)))
            continue
        binding_id = str(binding.get("id") or "")
        if not binding_id or binding_id in binding_ids:
            failures.append(failure("BOUNDARY_BINDING_ID_INVALID", binding_id or str(index)))
        binding_ids.add(binding_id)
        scalar_pairs = (
            ("import_name", "export_name"),
            ("import_return_type", "export_return_type"),
            ("import_calling_convention", "export_calling_convention"),
            ("import_architecture", "export_architecture"),
            ("import_protocol_version", "export_protocol_version"),
        )
        for left, right in scalar_pairs:
            if not isinstance(binding.get(left), str) or not binding.get(left, "").strip() or binding.get(left) != binding.get(right):
                failures.append(failure("BOUNDARY_ABI_MISMATCH", f"{binding_id}:{left}:{right}"))
        imported = binding.get("import_parameters")
        exported = binding.get("export_parameters")
        if not isinstance(imported, list) or not imported or not isinstance(exported, list) or imported != exported:
            failures.append(failure("BOUNDARY_PARAMETER_MISMATCH", binding_id))
            continue
        for position, parameter in enumerate(imported):
            if (
                not isinstance(parameter, dict)
                or set(parameter) != parameter_fields
                or parameter.get("position") != position
                or not isinstance(parameter.get("name"), str)
                or not parameter.get("name", "").strip()
                or not isinstance(parameter.get("type"), str)
                or not parameter.get("type", "").strip()
                or not isinstance(parameter.get("size_bytes"), int)
                or parameter.get("size_bytes", 0) <= 0
            ):
                failures.append(failure("BOUNDARY_PARAMETER_INVALID", f"{binding_id}:{position}"))
        if not isinstance(binding.get("compile_required"), bool):
            failures.append(failure("BOUNDARY_COMPILE_POLICY_INVALID", binding_id))
        compile_oracle = str(binding.get("compile_oracle_id") or "")
        if binding.get("compile_required") is True and compile_oracle not in oracle_ids:
            failures.append(failure("BOUNDARY_COMPILE_ORACLE_MISSING", f"{binding_id}:{compile_oracle}"))
        if binding.get("compile_required") is True and compile_oracle not in (boundary.get("oracle_ids") or []):
            failures.append(failure("BOUNDARY_COMPILE_ORACLE_NOT_BOUND", f"{binding_id}:{compile_oracle}"))
        if binding.get("compile_required") is False and compile_oracle:
            failures.append(failure("BOUNDARY_COMPILE_ORACLE_UNEXPECTED", binding_id))

    strength = profile.get("oracle_strength")
    strength_fields = {"required", "method", "mutations", "proportional_justification", "oracle_ids"}
    if not isinstance(strength, dict) or set(strength) != strength_fields:
        failures.append(failure("ORACLE_STRENGTH_CONTRACT_INVALID", "oracle_strength"))
        strength = {}
    expected_strength = profile.get("complex_state_machine") is True
    if strength.get("required") is not expected_strength:
        failures.append(failure("ORACLE_STRENGTH_ACTIVATION_INVALID", str(expected_strength)))
    if not isinstance(strength.get("proportional_justification"), str) or not strength.get("proportional_justification", "").strip():
        failures.append(failure("ORACLE_STRENGTH_JUSTIFICATION_MISSING", "oracle_strength"))
    if expected_strength:
        mutations = strength.get("mutations")
        if strength.get("method") not in ORACLE_STRENGTH_METHODS or not isinstance(mutations, list) or not mutations:
            failures.append(failure("ORACLE_STRENGTH_EVIDENCE_MISSING", "method/mutations"))
            mutations = []
        mutation_ids: set[str] = set()
        for index, mutation in enumerate(mutations):
            required_mutation = {"id", "production_target", "expected_failure", "oracle_id"}
            if not isinstance(mutation, dict) or set(mutation) != required_mutation:
                failures.append(failure("MUTATION_CONTRACT_INVALID", str(index)))
                continue
            mutation_id = str(mutation.get("id") or "")
            oracle_id = str(mutation.get("oracle_id") or "")
            if not mutation_id or mutation_id in mutation_ids:
                failures.append(failure("MUTATION_ID_INVALID", mutation_id or str(index)))
            mutation_ids.add(mutation_id)
            if any(not isinstance(mutation.get(field), str) or not mutation.get(field, "").strip() for field in ("production_target", "expected_failure")):
                failures.append(failure("MUTATION_TARGET_INVALID", mutation_id))
            if oracle_id not in oracle_ids:
                failures.append(failure("MUTATION_ORACLE_MISSING", f"{mutation_id}:{oracle_id}"))
    elif strength.get("method") != "not_required" or strength.get("mutations") != []:
        failures.append(failure("ORACLE_STRENGTH_OVERGATED", "simple state machine"))

    proof_sets = {
        "production_path": production.get("oracle_ids"),
        "lifecycle_contract": lifecycle.get("oracle_ids"),
        "boundary_contract": boundary.get("oracle_ids"),
        "oracle_strength": strength.get("oracle_ids"),
    }
    for location, refs in proof_sets.items():
        required = location != "oracle_strength" or expected_strength
        if not isinstance(refs, list) or (required and len(refs) != 1) or len(refs or []) != len(set(refs or [])) or any(item not in oracle_ids for item in refs or []):
            failures.append(failure("CROSS_COMPONENT_ORACLE_SET_INVALID", location))
            continue
        for oracle_id in refs:
            oracle = oracle_by_id.get(str(oracle_id), {})
            if oracle.get("authorized") is not True:
                failures.append(failure("CROSS_COMPONENT_ORACLE_UNAUTHORIZED", str(oracle_id)))
            if oracle.get("evidence_class") == "synthetic":
                failures.append(failure("CROSS_COMPONENT_SYNTHETIC_ORACLE_FORBIDDEN", f"{location}:{oracle_id}"))
            if location in {"lifecycle_contract", "boundary_contract", "oracle_strength"} and oracle.get("verification_level") != "cross_component_contract":
                failures.append(failure("CROSS_COMPONENT_ORACLE_LEVEL_INVALID", f"{location}:{oracle_id}"))
            if location == "production_path" and oracle.get("verification_level") not in {"component_behavior", "cross_component_contract"}:
                failures.append(failure("PRODUCTION_ORACLE_LEVEL_INVALID", str(oracle_id)))
    return failures


def validate_conditional_controls(value: dict[str, Any]) -> list[dict[str, str]]:
    """Validate schema-1.3 conditional gates without adding lifecycle states."""
    failures: list[dict[str, str]] = []
    controls = value.get("conditional_controls")
    if not isinstance(controls, dict):
        return [failure("CONDITIONAL_CONTROLS_REQUIRED", "conditional_controls")]
    required = {
        "task_shape", "defect_decomposition", "forensic_before_code",
        "preimplementation_architecture_review", "diff_budget",
        "verification_escalation", "runner_reuse", "runtime_acceptance",
    }
    if set(controls) != required:
        failures.append(failure("CONDITIONAL_CONTROL_FIELDS_INVALID", ",".join(sorted(set(controls) ^ required))))

    shape = controls.get("task_shape")
    if not isinstance(shape, dict) or set(shape) != {"kind", "product_mutation", "coupled", "high_risk"}:
        failures.append(failure("TASK_SHAPE_INVALID", "conditional_controls.task_shape"))
        shape = {}
    if shape.get("kind") not in TASK_SHAPES or any(not isinstance(shape.get(k), bool) for k in ("product_mutation", "coupled", "high_risk")):
        failures.append(failure("TASK_SHAPE_INVALID", str(shape)))

    criteria = [item for item in value.get("acceptance_criteria") or [] if isinstance(item, dict)]
    criterion_ids = {str(item.get("id") or "") for item in criteria}
    criterion_by_id = {str(item.get("id") or ""): item for item in criteria}
    oracle_ids = {str(item.get("id") or "") for item in value.get("oracles") or [] if isinstance(item, dict)}
    decomposition = controls.get("defect_decomposition")
    if not isinstance(decomposition, dict) or set(decomposition) != {"strategy", "coupling_justification", "units"}:
        failures.append(failure("DEFECT_DECOMPOSITION_INVALID", "conditional_controls.defect_decomposition"))
        decomposition = {}
    strategy = decomposition.get("strategy")
    units = decomposition.get("units")
    if strategy not in DEFECT_STRATEGIES or not isinstance(units, list) or not units:
        failures.append(failure("DEFECT_DECOMPOSITION_INVALID", str(strategy)))
        units = []
    seen_criteria: list[str] = []
    seen_units: set[str] = set()
    for index, unit in enumerate(units):
        if not isinstance(unit, dict) or set(unit) != {"id", "root_cause", "criterion_ids", "oracle_ids"}:
            failures.append(failure("DEFECT_UNIT_INVALID", str(index)))
            continue
        unit_id = str(unit.get("id") or "")
        unit_criteria = unit.get("criterion_ids")
        unit_oracles = unit.get("oracle_ids")
        if not unit_id or unit_id in seen_units or not str(unit.get("root_cause") or "").strip():
            failures.append(failure("DEFECT_UNIT_INVALID", unit_id or str(index)))
        seen_units.add(unit_id)
        if not isinstance(unit_criteria, list) or not unit_criteria or len(unit_criteria) != len(set(unit_criteria)):
            failures.append(failure("DEFECT_UNIT_CRITERIA_INVALID", unit_id))
        else:
            seen_criteria.extend(str(item) for item in unit_criteria)
            if any(str(item) not in criterion_ids for item in unit_criteria):
                failures.append(failure("DEFECT_UNIT_CRITERION_UNRESOLVED", unit_id))
            if any(criterion_by_id.get(str(item), {}).get("defect_id") != unit_id for item in unit_criteria):
                failures.append(failure("DEFECT_UNIT_MEMBERSHIP_MISMATCH", unit_id))
        if not isinstance(unit_oracles, list) or not unit_oracles or len(unit_oracles) != len(set(unit_oracles)) or any(str(item) not in oracle_ids for item in unit_oracles):
            failures.append(failure("DEFECT_UNIT_ORACLE_UNRESOLVED", unit_id))
        elif isinstance(unit_criteria, list):
            expected_unit_oracles = {criterion_by_id.get(str(item), {}).get("oracle_id") for item in unit_criteria}
            if set(unit_oracles) != expected_unit_oracles:
                failures.append(failure("DEFECT_UNIT_ORACLE_COVERAGE_INVALID", unit_id))
    if sorted(seen_criteria) != sorted(criterion_ids) or len(seen_criteria) != len(set(seen_criteria)):
        failures.append(failure("DEFECT_UNIT_CRITERION_COVERAGE_INVALID", str(seen_criteria)))
    if len(units) > 1 and strategy == "single":
        failures.append(failure("MULTIPLE_DEFECTS_NOT_DECOMPOSED", str(len(units))))
    if strategy == "explicit_coupling" and not str(decomposition.get("coupling_justification") or "").strip():
        failures.append(failure("DEFECT_COUPLING_JUSTIFICATION_MISSING", "defect_decomposition"))
    if strategy != "explicit_coupling" and decomposition.get("coupling_justification") not in {"", None}:
        failures.append(failure("UNNEEDED_COUPLING_JUSTIFICATION", strategy))

    forensic = controls.get("forensic_before_code")
    forensic_fields = {"required", "first_divergent_event", "execution_sequence_ref", "falsifiable_hypothesis", "oracle_id"}
    if not isinstance(forensic, dict) or set(forensic) != forensic_fields or not isinstance(forensic.get("required"), bool):
        failures.append(failure("FORENSIC_CONTROL_INVALID", "forensic_before_code"))
        forensic = {}
    forensic_expected = shape.get("product_mutation") is True and shape.get("kind") in {"diagnostic", "repair", "runtime", "owner_visible"}
    if forensic.get("required") is not forensic_expected:
        failures.append(failure("FORENSIC_GATE_ACTIVATION_INVALID", str(shape)))
    if forensic.get("required") is True and (
        any(not str(forensic.get(field) or "").strip() for field in ("first_divergent_event", "execution_sequence_ref", "falsifiable_hypothesis"))
        or forensic.get("oracle_id") not in oracle_ids
    ):
        failures.append(failure("FORENSIC_EVIDENCE_MISSING", "forensic_before_code"))

    architecture = controls.get("preimplementation_architecture_review")
    architecture_fields = {"required", "reviewer_role_id", "evidence_ref", "covers", "reuse_role_for_final_review"}
    if not isinstance(architecture, dict) or set(architecture) != architecture_fields or not isinstance(architecture.get("required"), bool):
        failures.append(failure("ARCHITECTURE_REVIEW_CONTROL_INVALID", "preimplementation_architecture_review"))
        architecture = {}
    architecture_expected = shape.get("coupled") is True or shape.get("high_risk") is True
    if architecture.get("required") is not architecture_expected:
        failures.append(failure("ARCHITECTURE_REVIEW_ACTIVATION_INVALID", str(shape)))
    if architecture.get("required") is True and (
        not str(architecture.get("reviewer_role_id") or "").strip()
        or not str(architecture.get("evidence_ref") or "").strip()
        or set(architecture.get("covers") or []) != ARCHITECTURE_REVIEW_COVERS
        or architecture.get("reuse_role_for_final_review") is not True
    ):
        failures.append(failure("ARCHITECTURE_REVIEW_EVIDENCE_MISSING", "preimplementation_architecture_review"))
    if architecture.get("required") is True:
        review_extension = value.get("extensions", {}).get("independent_review") if isinstance(value.get("extensions"), dict) else None
        active = value.get("gate_profile", {}).get("active") if isinstance(value.get("gate_profile"), dict) else []
        if "independent_review" not in active or not isinstance(review_extension, dict) or review_extension.get("required") is not True:
            failures.append(failure("ARCHITECTURE_FINAL_REVIEW_GATE_MISSING", "independent_review"))
        elif architecture.get("reviewer_role_id") != review_extension.get("reviewer_role"):
            failures.append(failure("ARCHITECTURE_REVIEWER_ROLE_MISMATCH", str(architecture.get("reviewer_role_id"))))

    budget = controls.get("diff_budget")
    budget_fields = {"max_product_files", "max_product_lines", "product_path_patterns", "task_local_framework_patterns", "planned_task_local_framework_patterns", "replan_on_unplanned_task_local_framework"}
    if not isinstance(budget, dict) or set(budget) != budget_fields:
        failures.append(failure("DIFF_BUDGET_INVALID", "diff_budget"))
    else:
        for field in ("max_product_files", "max_product_lines"):
            if not isinstance(budget.get(field), int) or isinstance(budget.get(field), bool) or budget[field] < 1:
                failures.append(failure("DIFF_BUDGET_INVALID", field))
        for field in ("product_path_patterns", "task_local_framework_patterns", "planned_task_local_framework_patterns"):
            if not isinstance(budget.get(field), list) or any(not isinstance(item, str) or not item for item in budget[field]):
                failures.append(failure("DIFF_BUDGET_INVALID", field))
        if budget.get("replan_on_unplanned_task_local_framework") is not True:
            failures.append(failure("DIFF_BUDGET_INVALID", "replan_on_unplanned_task_local_framework"))
        if shape.get("product_mutation") is True and not budget.get("product_path_patterns"):
            failures.append(failure("PRODUCT_DIFF_PATTERNS_REQUIRED", "diff_budget.product_path_patterns"))

    escalation = controls.get("verification_escalation")
    if not isinstance(escalation, dict) or set(escalation) != {"narrow_oracle_ids", "targeted_after_narrow_pass", "integration_or_dependency_risk", "full_suite_trigger"}:
        failures.append(failure("VERIFICATION_ESCALATION_INVALID", "verification_escalation"))
    else:
        narrow = escalation.get("narrow_oracle_ids")
        if not isinstance(narrow, list) or not narrow or len(narrow) != len(set(narrow)) or any(item not in oracle_ids for item in narrow):
            failures.append(failure("VERIFICATION_ESCALATION_INVALID", "narrow_oracle_ids"))
        if escalation.get("targeted_after_narrow_pass") is not True or not isinstance(escalation.get("integration_or_dependency_risk"), bool) or escalation.get("full_suite_trigger") != "final_integration_or_dependency_risk":
            failures.append(failure("VERIFICATION_ESCALATION_INVALID", "ordering"))

    runner = controls.get("runner_reuse")
    if not isinstance(runner, dict) or set(runner) != {"registered_runners_required", "task_local_replacement_only_for_capability_gap"} or runner.get("registered_runners_required") is not True or runner.get("task_local_replacement_only_for_capability_gap") is not True:
        failures.append(failure("RUNNER_REUSE_POLICY_INVALID", "runner_reuse"))

    runtime = controls.get("runtime_acceptance")
    if not isinstance(runtime, dict) or set(runtime) != {"required", "authorized", "available", "owner_gate"} or any(not isinstance(runtime.get(k), bool) for k in ("required", "authorized", "available")):
        failures.append(failure("RUNTIME_ACCEPTANCE_INVALID", "runtime_acceptance"))
        runtime = {}
    owner_visible_required = any(item.get("mandatory") is True and item.get("owner_visible") is True for item in criteria)
    extensions = value.get("extensions") if isinstance(value.get("extensions"), dict) else {}
    cross_component = extensions.get("cross_component_code_proof") if isinstance(extensions, dict) else None
    platform_runtime_required = (
        isinstance(cross_component, dict)
        and cross_component.get("platform_runtime_required") is True
    )
    high_level_target_required = value.get("verification_target") in HIGH_LEVEL_EVIDENCE_CLASSES
    runtime_required = owner_visible_required or platform_runtime_required or high_level_target_required
    if runtime.get("required") is not runtime_required:
        failures.append(failure("RUNTIME_ACCEPTANCE_ACTIVATION_INVALID", str(runtime_required)))
    if runtime.get("required") is True and not str(runtime.get("owner_gate") or "").strip():
        failures.append(failure("RUNTIME_ACCEPTANCE_OWNER_GATE_MISSING", "runtime_acceptance"))
    oracle_by_id = {item.get("id"): item for item in value.get("oracles") or [] if isinstance(item, dict)}
    for criterion in criteria:
        oracle = oracle_by_id.get(criterion.get("oracle_id"), {})
        if criterion.get("mandatory") is True and criterion.get("owner_visible") is True and oracle.get("evidence_class") not in {"runtime", "owner"}:
            failures.append(failure("OWNER_VISIBLE_ORACLE_CLASS_INVALID", str(criterion.get("id"))))
    return failures


def validate(value: dict[str, Any]) -> list[dict[str, str]]:
    version = str(value.get("schema_version") or "")
    if version == "1.0":
        return validate_legacy(value)
    if version in {"1.1", "1.2", "1.3"}:
        return validate_compact(value)
    return [failure("SCHEMA_VERSION_UNSUPPORTED", version)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.path).resolve()
    try:
        failures = validate(load_contract(path))
        result = {"status": "pass" if not failures else "fail", "path": str(path), "failures": failures}
    except Exception as exc:
        result = {"status": "fail", "path": str(path), "failures": [failure("LOAD_ERROR", str(exc))]}
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.json else None, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

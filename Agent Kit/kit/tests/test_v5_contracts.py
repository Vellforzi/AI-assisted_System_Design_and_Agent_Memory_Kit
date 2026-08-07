from __future__ import annotations

import importlib.util
import copy
import json
from pathlib import Path
import sys


KIT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, KIT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def fixture_bundle(kind: str = "valid"):
    path = KIT / f"project_artifact_contract_v2/examples/{kind}/project-artifacts-v2.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_v5_oracle_passes():
    oracle = load("project_artifact_contract_v2_oracle", "tools/project_artifact_contract_v2_oracle.py")
    assert oracle.run_oracle()["status"] == "passed"


def test_projection_is_report_only_and_derives_values():
    load("project_artifact_contract_v2_oracle", "tools/project_artifact_contract_v2_oracle.py")
    helper = load("workflow_projection_helper", "tools/workflow_projection_helper.py")
    result = helper.project(fixture_bundle())
    assert result["work_item_frontier"] == ["WI-5002"]
    assert result["capability_status"] == {"CAP-5001": "passing", "CAP-5002": "failing"}
    assert result["triage_ready_for_agent"] == ["ISSUE-1"]
    assert result["read_only"] and not result["activated"] and not result["files_modified"]


def test_v4_task_migration_preserves_truth_without_inventing_workflow_facts():
    migration = load("migrate_v4_artifact", "tools/migrate_v4_artifact.py")
    source = {"schema_version":"2.0","task_id":"TASK-42","status":"active","intent":"apply","permission_mode":"apply","goal":"Keep","scope":{"project_map":[],"project_files":[],"external_sources":[]},"commitment_refs":["COM-42"],"expected_outcomes":["Observed"],"stop_conditions":["Stop"],"rollback_or_recovery":["Recover"],"reversibility":"unknown","expected_side_effects":[],"done_definition":["Done"]}
    proposed = migration.migrate("TaskContractV2", source)
    assert proposed["task_id"] == "TASK-42" and proposed["commitment_refs"] == ["COM-42"]
    assert proposed["workflow_profile"]["mode"] == "standard"
    assert proposed["workflow_profile"]["risk_class"] == "unknown"
    assert proposed["workflow_profile"]["work_item_graph_ref"] is None
    assert "PlanChallengeV1" not in json.dumps(proposed)


def test_mocked_v5_workflow_traces_pass():
    runner = load("workflow_eval_v5", "optional_integrations/workflow_evals_mocked_tools/run_mocked_workflow_eval.py")
    fixture_dir = KIT / "optional_integrations/workflow_evals_mocked_tools/fixtures"
    for prefix in ("writer-reviewer", "exploration-delivery", "prototype-promotion"):
        case = json.loads((fixture_dir / f"{prefix}-case.json").read_text(encoding="utf-8"))
        trace = json.loads((fixture_dir / f"{prefix}-trace.json").read_text(encoding="utf-8"))
        assert runner.run(case, trace)["status"] == "pass"


def test_cross_contract_risk_review_and_mutation_gates_fail_closed():
    oracle = load("project_artifact_contract_v2_oracle", "tools/project_artifact_contract_v2_oracle.py")
    high = fixture_bundle()
    high["PlanChallengeV1"]["status"] = "open"
    assert "TASK_HIGH_RISK_CHALLENGE_NOT_ACCEPTED" in oracle._cross_bundle_reasons(high)

    exploration = copy.deepcopy(fixture_bundle())
    task = exploration["TaskContractV3"]
    task["intent"] = "apply"
    task["permission_mode"] = "apply"
    task["workflow_profile"].update({
        "mode": "exploration", "task_scale": "single_session", "risk_class": "routine",
        "delivery_strategy": "single_step", "work_item_graph_ref": None, "plan_challenge_ref": None,
        "exploration_map_ref": "EXP-5001", "review_policy": "none", "review_receipt_refs": [],
        "capability_impact": "none", "capability_refs": [], "domain_context_refs": [],
    })
    assert "TASK_NON_DELIVERY_MODE_MUTATION_FORBIDDEN" in oracle._cross_bundle_reasons(exploration)

    bounded = copy.deepcopy(fixture_bundle())
    bounded["TaskContractV3"]["workflow_profile"]["domain_context_refs"] = []
    bounded["SourceAuthorityPolicy"] = {"bounded_contexts": [{"id": "CTX-billing", "path_patterns": ["src/**"]}]}
    assert "TASK_BOUNDED_CONTEXT_DOMAIN_REF_REQUIRED" in oracle._cross_bundle_reasons(bounded)

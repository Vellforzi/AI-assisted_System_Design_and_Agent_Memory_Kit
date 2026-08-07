from __future__ import annotations

import importlib.util
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


def test_project_artifact_oracle_passes():
    oracle = load("project_artifact_oracle", "tools/project_artifact_contract_oracle.py")
    report = oracle.run_oracle()
    assert report["status"] == "passed", report


def test_context_audit_reports_growth_and_does_not_read_excluded(tmp_path):
    audit = load("context_budget_audit", "tools/context_budget_audit.py")
    (tmp_path / "large.md").write_text("x" * 100, encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=do-not-read", encoding="utf-8")
    policy = {"profiles":{"review":{"max_sources":1,"max_estimated_tokens":10}},"absolute_max_estimated_tokens":20,"relative_growth_threshold_percent":10,"excluded":[".env"]}
    result = audit.audit(tmp_path, ["large.md", ".env"], policy, "review", {"estimated_tokens":10})
    codes = {item["code"] for item in result["reasons"]}
    assert {"CTX_PATH_EXCLUDED", "CTX_PROFILE_TOKEN_LIMIT_EXCEEDED", "CTX_ABSOLUTE_TOKEN_LIMIT_EXCEEDED", "CTX_RELATIVE_GROWTH_EXCEEDED"} <= codes
    assert result["largest_sources"][0]["path"] == "large.md"


def test_progressive_disclosure_caps_and_explicit_full_gate(tmp_path):
    helper = load("context_governance_helper_v4", "tools/context_governance_helper.py")
    (tmp_path / "artifact.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
    bounded = helper.inspect_artifact(tmp_path, "artifact.txt", 100, 1, "bounded_excerpt", False)
    assert bounded["excerpt"]["truncated"] is True
    assert bounded["excerpt"]["end_line"] == 1
    full = helper.inspect_artifact(tmp_path, "artifact.txt", 1, 1, "full_if_explicit", True)
    assert full["excerpt"]["truncated"] is False
    (tmp_path / ".env").write_text("SECRET=x", encoding="utf-8")
    assert helper.inspect_artifact(tmp_path, ".env", 100, 10, "bounded_excerpt", False)["reason_code"] == "CTX_INSPECT_PATH_EXCLUDED"


def test_mocked_workflow_capability_and_canary_negative_cases():
    workflow = load("workflow_eval", "optional_integrations/workflow_evals_mocked_tools/run_mocked_workflow_eval.py")
    case = {"expected_tools":["read"],"forbidden_tools":["send"],"argument_constraints":[],"expected_terminal_outcome":"done"}
    result = workflow.run(case, {"tool_calls":[{"tool":"send","arguments":{}}],"terminal_outcome":"failed"})
    assert {r["code"] for r in result["reasons"]} == {"WF_EXPECTED_TOOL_MISSING","WF_FORBIDDEN_TOOL_CALLED","WF_TERMINAL_OUTCOME_MISMATCH"}
    capability = load("capability", "optional_integrations/tool_capability_governance/check_tool_capabilities.py")
    cap = capability.check({"schema_version":"1.0","tools":[{"name":"incomplete"}]})
    assert "CAP_METADATA_MISSING_HIGH_RISK" in {r["code"] for r in cap["reasons"]}
    assert "CAP_LETHAL_TRIFECTA_BLOCKED" in {r["code"] for r in cap["reasons"]}
    canary = load("canary", "optional_integrations/policy_canary/validate_policy_canary.py")
    bad = canary.validate({"schema_version":"1.0","baseline_identity":"a","candidate_identity":"b","baseline_cohort":"one","candidate_cohort":"two","guardrails":[],"stop_thresholds":[],"rollback_rule":"","owner_approval":"approved","live_traffic":True,"auto_activate":True})
    codes = {r["code"] for r in bad["reasons"]}
    assert {"CANARY_COHORT_MISMATCH","CANARY_GUARDRAILS_MISSING","CANARY_STOP_THRESHOLDS_MISSING","CANARY_ROLLBACK_RULE_MISSING","CANARY_RUNTIME_ACTIVATION_FORBIDDEN"} <= codes
    assert bad["rollout_authorized"] is False


def test_v38_migration_preserves_ids_and_does_not_invent_verification():
    migration = load("migration", "tools/migrate_v38_artifact.py")
    source = {"task_id":"TASK-0042","status":"active","goal":"Keep this goal","done_definition":["Evidence exists"]}
    proposed = migration.propose("task", source)
    assert proposed["task_id"] == "TASK-0042"
    assert proposed["goal"] == "Keep this goal"
    assert proposed["reversibility"] == "unknown"
    assert proposed["commitment_refs"] == []
    assert "verified" not in json.dumps(proposed).lower()

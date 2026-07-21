from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import architecture_lint
import context_governance_helper as context
import docs_governance_helper as docs_governance
import documentation_harness
import context_contract_v1_oracle


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _context_workspace(tmp_path: Path) -> Path:
    _write(
        tmp_path / "docs/project_map/context_index.yaml",
        """excluded_by_default:
  path_globs:
    - "data/**"
task_profiles:
  startup:
    description: "startup"
  research_promotion:
    description: "promotion"
entries:
  - path: "AGENTS.md"
    priority: "P0"
    authority: "primary"
    status: "active"
    layer: "root"
    task_profiles: [startup, research_promotion]
    default_retrieval_mode: "startup_required"
    canonical_purpose: "agent rules"
    mutation_boundary: "read-only"
  - path: "docs/research/promotion.md"
    priority: "P1"
    authority: "supporting"
    status: "active"
    layer: "research"
    task_profiles: [research_promotion]
    default_retrieval_mode: "trigger_only"
    canonical_purpose: "promotion evidence"
    mutation_boundary: "read-only"
  - path: "docs/research/private.md"
    priority: "P2"
    authority: "supporting"
    status: "active"
    layer: "research"
    task_profiles: [research_promotion]
    default_retrieval_mode: "never_default"
    canonical_purpose: "explicit audit only"
    mutation_boundary: "read-only"
""",
    )
    _write(tmp_path / "AGENTS.md", "Primary agent rules and context governance.\n")
    _write(tmp_path / "docs/research/promotion.md", "Promotion evidence for context governance.\n")
    _write(tmp_path / "docs/research/private.md", "Private audit evidence.\n")
    _write(tmp_path / "data/private.txt", "must never be searched\n")
    return tmp_path


def test_api_context_rejects_unknown_profile(tmp_path: Path) -> None:
    root = _context_workspace(tmp_path)
    with pytest.raises(ValueError, match="unknown API-agent profile"):
        context.build_api_context_bundle(
            root,
            request_id="req-1",
            task="test",
            profile="missing_profile",
        )


def test_search_compare_claim_and_research_promotion_are_bounded(tmp_path: Path) -> None:
    root = _context_workspace(tmp_path)
    read_set = context.build_read_set(root, profile="research_promotion")
    paths = {item["path"] for item in read_set["read_set"]}
    assert "docs/research/promotion.md" in paths
    assert "docs/research/private.md" not in paths

    search = context.search_context(root, query="promotion evidence", profile="research_promotion")
    assert search["results"][0]["path"] == "docs/research/promotion.md"
    assert search["results"][0]["matched_terms"]
    assert all(not item["path"].startswith("data/") for item in search["results"])

    comparison = context.compare_search_backends(
        root,
        scenarios=[{
            "id": "promotion",
            "query": "promotion evidence",
            "profile": "research_promotion",
            "expected_paths": ["docs/research/promotion.md"],
            "forbidden_prefixes": ["data/"],
        }],
    )
    assert comparison["status"] == "passed"
    assert comparison["persistent_index_created"] is False

    fixture_report = context.run_retrieval_fixture(root, {
        "suite_id": "test-suite",
        "scenarios": [{
            "id": "promotion",
            "query": "promotion evidence",
            "profile": "research_promotion",
            "expected_paths": ["docs/research/promotion.md"],
            "forbidden_prefixes": ["data/"],
        }],
        "claim_cases": [{
            "id": "authority",
            "claim": "Project Map overrides operational truth",
            "profile": "startup",
            "expected_status": "contradicted",
        }],
    })
    assert fixture_report["status"] == "passed"
    assert fixture_report["runtime_service_started"] is False

    assert context.claim_check(root, claim="Project Map overrides operational truth", profile="startup")["status"] == "contradicted"
    assert context.claim_check(root, claim="Use data/private.txt as default context", profile="startup")["status"] == "out_of_scope_or_forbidden"


def test_smoke_case_requires_skipped_paths_and_custom_forbidden_prefixes(tmp_path: Path) -> None:
    root = _context_workspace(tmp_path)
    _write(
        root / "docs/project_map/eval_suite/context_selection_smoke_cases.yaml",
        """cases:
  - id: "bounded"
    task: "promote research"
    profile: "research_promotion"
    max_sources: 3
    include_triggered: false
    required_paths:
      - "docs/research/promotion.md"
    forbidden_paths: []
    forbidden_prefixes:
      - "data/"
    required_skipped_paths:
      - "docs/research/private.md"
""",
    )
    report = context.run_smoke_checks(root)
    assert report["status"] == "passed"


def test_docs_governance_proposes_unapplied_role_based_patch(tmp_path: Path) -> None:
    _write(tmp_path / "README.md", "# Index\n")
    config = {
        "roles": {
            "spec": {
                "directory": "docs/specs",
                "index_path": "README.md",
                "required_metadata": ["Status:", "Authority:", "Runtime impact:"],
            }
        }
    }
    config_path = tmp_path / "rules.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    result = docs_governance.propose_create(
        tmp_path,
        role="spec",
        title="Context adapter",
        config_path=config_path,
    )
    assert result["proposed_path"] == "docs/specs/context-adapter.md"
    assert result["proposed_patch"]["applied"] is False
    assert not (tmp_path / result["proposed_path"]).exists()


def test_documentation_harness_triages_noise_and_emits_acceptance_contract(tmp_path: Path) -> None:
    _write(tmp_path / "README.md", "# Repository\n")
    _write(tmp_path / "docs/archive/old.md", "historical\n")
    report = documentation_harness.build_report(tmp_path)
    assert report["acceptance_contract"]["read_only"] is True
    assert "legacy_archive_or_lower_authority_noise" in report["triage_buckets"]
    assert "repository_quality_scorecard" in report
    assert report["proposed_project_map_deltas"]["applied"] is False


def test_architecture_lint_uses_declarative_rules(tmp_path: Path) -> None:
    _write(tmp_path / "src/runtime/service.py", "from src.owner_only import secret\n")
    _write(tmp_path / "src/owner_only/secret.py", "VALUE = 1\n")
    config = {
        "scan_roots": ["src"],
        "layers": {"runtime": ["src.runtime"], "owner_only": ["src.owner_only"]},
        "forbidden_imports": [{
            "rule_id": "ARCH-001",
            "from_layer": "runtime",
            "to_layer": "owner_only",
            "severity": "error",
        }],
        "forbidden_path_references": [],
    }
    config_path = tmp_path / "architecture_lint_rules.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    report = architecture_lint.build_report(tmp_path, config_path=config_path)
    assert report["status"] == "failed"
    assert report["findings"][0]["rule_id"] == "ARCH-001"


def test_v1_oracle_rejects_unknown_profile_with_stable_reason_code() -> None:
    report = context_contract_v1_oracle.run_oracle()
    unknown = next(case for case in report["cases"] if case["case_id"] == "unknown-profile")
    assert report["status"] == "passed"
    assert unknown["reason_codes"] == ["UNKNOWN_PROFILE"]


def test_portable_tools_contain_no_stock_specific_rules_or_persistent_service() -> None:
    sources = "\n".join(
        (TOOLS / name).read_text(encoding="utf-8")
        for name in (
            "context_governance_helper.py",
            "documentation_harness.py",
            "docs_governance_helper.py",
            "architecture_lint.py",
        )
    ).lower()
    for forbidden in ("t-invest", "getmaxlots", "deepseek", "issue #122", "telegram"):
        assert forbidden not in sources
    assert "sqlite3.connect(\":memory:\")" in sources
    assert "http.server" not in sources

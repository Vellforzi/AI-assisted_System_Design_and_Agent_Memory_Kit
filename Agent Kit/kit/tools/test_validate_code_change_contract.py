from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_code_change_contract.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("amk_code_change_validator", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_contract() -> dict:
    return {
        "policy_ref": {"id": "PRODUCT_CODE_CHANGE_POLICY", "version": "1.0.0"},
        "mandatory_skills": {
            "production-engineering-standard": {"applied": True},
            "complete-technical-communication": {"applied": True},
        },
        "task": {"id": "T-1", "component": "api", "owner_request_verbatim": "Change X only."},
        "business_logic": {
            "required_behavior": [{"id": "AC-01", "rule": "X"}],
            "preserved_behavior": [{"id": "INV-01", "rule": "Y"}],
            "non_goals": ["Z"],
            "unresolved_product_questions": [],
        },
        "current_behavior": {
            "producer": "producer",
            "normalization_or_calculation": "normalizer",
            "storage_or_state": "table",
            "transport": "route",
            "consumer": "client",
            "owner_visible_result": "result",
            "observed_problem": "problem",
        },
        "exact_change": {
            "changed_behavior": [{
                "criterion": "AC-01",
                "files": ["app.py"],
                "symbols": ["run"],
                "required_logic": "Implement X.",
            }],
            "forbidden_changes": ["Do not change Y."],
        },
        "impact_analysis": {name: [] for name in load_validator().REQUIRED_IMPACT_FIELDS},
        "quality_review": {
            "semantic_walkthrough_completed": True,
            "final_diff_reviewed": True,
            "causal_chain_reviewed": True,
            "failure_paths_reviewed": True,
            "performance_impact_reviewed": True,
            "resource_lifecycle_reviewed": True,
            "non_goals_preserved": True,
            "unexplained_production_changes": [],
            "tests_used_as_specification": False,
            "remaining_unverified_risks": [],
        },
        "final_traceability": {
            "changed_symbols": ["app.py:run"],
            "unexplained_changes": [],
            "remaining_risks": [],
        },
    }


class ContractValidatorTests(unittest.TestCase):
    def test_valid_contract_passes_both_phases(self) -> None:
        validator = load_validator()
        contract = valid_contract()
        self.assertEqual([], validator.validate(contract, "pre-edit"))
        self.assertEqual([], validator.validate(contract, "final"))

    def test_missing_owner_request_fails(self) -> None:
        validator = load_validator()
        contract = valid_contract()
        contract["task"]["owner_request_verbatim"] = "<placeholder>"
        self.assertIn("task.owner_request_verbatim is required", validator.validate(contract, "pre-edit"))

    def test_unresolved_product_question_fails(self) -> None:
        validator = load_validator()
        contract = valid_contract()
        contract["business_logic"]["unresolved_product_questions"] = ["Which fallback?"]
        self.assertIn(
            "business_logic.unresolved_product_questions must be an empty list",
            validator.validate(contract, "pre-edit"),
        )

    def test_final_review_is_required(self) -> None:
        validator = load_validator()
        contract = valid_contract()
        contract["quality_review"]["final_diff_reviewed"] = False
        self.assertIn("quality_review.final_diff_reviewed must be true", validator.validate(contract, "final"))

    def test_tests_cannot_be_used_as_specification(self) -> None:
        validator = load_validator()
        contract = valid_contract()
        contract["quality_review"]["tests_used_as_specification"] = True
        self.assertIn(
            "quality_review.tests_used_as_specification must be false",
            validator.validate(contract, "final"),
        )


if __name__ == "__main__":
    unittest.main()

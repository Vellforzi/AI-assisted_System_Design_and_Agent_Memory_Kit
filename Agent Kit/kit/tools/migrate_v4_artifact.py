#!/usr/bin/env python3
"""Read-only v4-to-v5 migration proposal helper for JSON artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _workflow_state(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "mode": "standard",
        "active_work_item_ref": None,
        "work_item_graph_ref": None,
        "frontier_input_refs": [],
        "plan_challenge_ref": None,
        "exploration_map_ref": None,
        "triage_item_ref": None,
        "design_probe_ref": None,
        "review_receipt_refs": [],
        "capability_refs": [],
        "domain_context_refs": [],
        "blockers": list(source.get("blockers", [])),
    }


def migrate(contract: str, source: dict[str, Any]) -> dict[str, Any]:
    """Return a proposal. Unknown workflow facts are never synthesized."""
    if contract == "TaskContractV2":
        keep = {
            key: source.get(key) for key in (
                "task_id", "title", "status", "intent", "permission_mode", "goal", "scope",
                "commitment_refs", "expected_outcomes", "stop_conditions", "rollback_or_recovery",
                "reversibility", "expected_side_effects", "done_definition",
            )
        }
        keep["schema_version"] = "3.0"
        keep["governance"] = {
            "contract_version": "3.0", "supersedes": "TaskContractV2",
            "effective_from": "owner_review_required", "compatibility": "breaking",
            "migration_note": "Generated as a read-only proposal; workflow unknowns require review.",
        }
        keep["workflow_profile"] = {
            "mode": "standard", "task_scale": "unknown", "risk_class": "unknown",
            "delivery_strategy": "unknown", "work_item_graph_ref": None,
            "plan_challenge_ref": None, "exploration_map_ref": None, "triage_item_ref": None,
            "design_probe_ref": None, "review_policy": "unknown", "review_receipt_refs": [],
            "capability_impact": "unknown", "capability_refs": [], "domain_context_refs": [],
        }
        return {key: value for key, value in keep.items() if value is not None or key in {"title"}}
    if contract in {"HandoffV2", "WorkingStateV2"}:
        output = dict(source)
        output["schema_version"] = "3.0"
        output.pop("governance", None)
        output["workflow_state"] = _workflow_state(source)
        return output
    if contract == "CommitmentLedgerV1":
        output = dict(source)
        output["schema_version"] = "2.0"
        output["commitments"] = [
            {**item, "workflow_mode": item.get("workflow_mode", "standard"), "subject_refs": item.get("subject_refs", [])}
            for item in source.get("commitments", [])
        ]
        return output
    if contract == "VerificationReceiptV1":
        output = dict(source)
        output["schema_version"] = "2.0"
        output.setdefault("subject_refs", [])
        output.setdefault("verification_level", "unknown")
        output.setdefault("environment_ref", None)
        return output
    raise ValueError(f"UNSUPPORTED_V4_CONTRACT:{contract}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--contract", required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    source = json.loads(raw.decode("utf-8"))
    report = {
        "migration": "v4_to_v5",
        "source_contract": args.contract,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "proposal": migrate(args.contract, source),
        "owner_review_required": True,
        "new_workflow_artifacts_created": [],
        "source_modified": False,
        "files_modified": False,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

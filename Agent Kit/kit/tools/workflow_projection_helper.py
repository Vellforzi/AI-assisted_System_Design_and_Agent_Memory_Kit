#!/usr/bin/env python3
"""Report-only v5 workflow projections; never schedules, activates, or writes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from project_artifact_contract_v2_oracle import (
    capability_statuses,
    exploration_frontier,
    work_item_frontier,
)


def project(bundle: dict[str, Any], operation: str = "all") -> dict[str, Any]:
    result: dict[str, Any] = {
        "operation": operation,
        "read_only": True,
        "navigation_only": True,
        "activated": False,
        "files_modified": False,
    }
    if operation in {"frontier", "all"}:
        graph = bundle.get("WorkItemGraphV1")
        exploration = bundle.get("ExplorationMapV1")
        result["work_item_frontier"] = work_item_frontier(graph) if isinstance(graph, dict) else []
        result["exploration_frontier"] = exploration_frontier(exploration) if isinstance(exploration, dict) else []
    if operation in {"capabilities", "all"}:
        registry = bundle.get("CapabilityRegistryV1")
        result["capability_status"] = capability_statuses(registry) if isinstance(registry, dict) else {}
    if operation in {"triage", "all"}:
        ledger = bundle.get("TriageLedgerV1", {})
        result["triage_ready_for_agent"] = sorted(
            item.get("id") for item in ledger.get("items", [])
            if item.get("state") == "ready_for_agent"
            and item.get("owner_disposition") == "agent"
            and not item.get("delegation_blockers")
            and item.get("verification_plan")
            and (item.get("category") != "enhancement" or item.get("brief"))
            and (item.get("category") != "bug" or (
                item.get("reproduction_state") == "reproducible" and item.get("evidence_refs")
            ))
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--operation", choices=("frontier", "capabilities", "triage", "all"), default="all")
    args = parser.parse_args()
    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    print(json.dumps(project(bundle, args.operation), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

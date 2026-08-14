"""Finding-delta gate that blocks only newly introduced configured rule IDs."""

from __future__ import annotations

from collections import Counter
from typing import Iterable


def _identities(report: dict[str, object], forbidden: set[str]) -> Counter[tuple[str, str, str]]:
    result: Counter[tuple[str, str, str]] = Counter()
    findings = report.get("findings", [])
    if not isinstance(findings, list):
        return result
    for item in findings:
        if not isinstance(item, dict) or str(item.get("id")) not in forbidden:
            continue
        result[(str(item.get("id")), str(item.get("path", "")), str(item.get("message", "")))] += 1
    return result


def build_delta_report(
    baseline: dict[str, object], candidate: dict[str, object], forbidden: Iterable[str]
) -> dict[str, object]:
    forbidden_set = set(forbidden)
    before, after = _identities(baseline, forbidden_set), _identities(candidate, forbidden_set)
    introduced = after - before
    items = [
        {"id": identity[0], "path": identity[1], "message": identity[2], "count": count}
        for identity, count in sorted(introduced.items())
    ]
    return {
        "report_type": "documentation_governance_delta",
        "schema_version": "documentation-governance-delta-report.v1",
        "forbidden_rule_ids": sorted(forbidden_set),
        "baseline_finding_count": sum(before.values()),
        "candidate_finding_count": sum(after.values()),
        "introduced_finding_count": sum(introduced.values()),
        "introduced_findings": items,
        "status": "passed" if not introduced else "failed",
    }

"""Report-only documentation harness for Agent Memory Kit adopters.

Copy this file into a target project as `scripts/documentation_harness.py` when
using `secondary_memory_governance/`.

The harness audits documentation metadata, reachability, and lower-authority
references. It is intentionally read-only: it does not change Project Map,
runtime behavior, data artifacts, external systems, or deployment state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Sequence


REPORT_TYPE = "documentation_harness"
HELPER_NAME = "documentation_harness"
DOC_SUFFIXES = {".md", ".yaml", ".yml"}
ROOT_DISCOVERABLE_DOCS = {"AGENTS.md", "README.md", ".codexignore", ".cursorignore"}
SKIPPED_DIRS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "data",
    "node_modules",
    "output",
}
MARKDOWN_METADATA_FIELDS = (
    "Status:",
    "Last aligned:",
    "Audience:",
    "Runtime impact:",
    "Authority:",
)
YAML_METADATA_FIELDS = ("status:", "authority:")
LOWER_AUTHORITY_PREFIXES = (
    "docs/archive/",
    "docs/planned/",
    "docs/project_map/",
    "docs/proposals/",
    "docs/research/",
)
LOWER_AUTHORITY_LABEL_TERMS = (
    "advisory",
    "archive",
    "defer",
    "deferred",
    "evidence",
    "historical",
    "hypothesis",
    "inventory",
    "lower-authority",
    "lower authority",
    "not runtime",
    "not source of truth",
    "planning",
    "planned",
    "proposal",
    "research",
    "secondary",
    "subordinate",
)
LOWER_AUTHORITY_PATH_RE = re.compile(
    r"docs/(?:archive|planned|project_map|proposals|research)/[^\s`'\"),\]]+\.(?:md|ya?ml)",
    re.IGNORECASE,
)
INVENTORY_RE = re.compile(r"docs/documentation_inventory_\d{4}-\d{2}-\d{2}\.md$")

PRIMARY_OPERATIONAL_SOURCE_PATHS = {
    "AGENTS.md",
    "docs/NEXT_STEPS.md",
    "docs/source_of_truth_hierarchy.md",
    "docs/context_packs/current_status.md",
}
NAVIGATION_INDEX_PATHS = {
    "README.md",
    "docs/architecture/README.md",
    "docs/project_map/README.md",
    "docs/research/README.md",
    "docs/specs/README.md",
    "docs/validation/README.md",
}
WORKFLOW_RULE_PATHS = {
    "docs/context_governance_rules.md",
    "docs/rules/ai_development_rules.md",
    "docs/rules/codex_prompt_rules.md",
}
SCOPE_FLAGS = {
    "runtime_behavior_changed": False,
    "external_system_state_changed": False,
    "data_artifacts_changed": False,
    "project_map_changed": False,
}


def build_report(root: Path | str = Path.cwd()) -> dict[str, object]:
    """Build a deterministic, read-only documentation harness report."""

    root_path = Path(root).resolve()
    managed_paths = _managed_doc_paths(root_path)
    text_by_path = {rel: _read_text(root_path / rel) for rel in managed_paths}
    findings: list[dict[str, object]] = []

    findings.extend(_metadata_findings(text_by_path))
    findings.extend(_reachability_findings(text_by_path))
    findings.extend(_authority_findings(text_by_path))
    _annotate_findings(findings)
    findings.sort(key=lambda item: (str(item["id"]), str(item.get("path", "")), int(item.get("line", 0))))

    backlog_items = [
        {
            "id": item["id"],
            "path": item.get("path"),
            "priority": item.get("priority"),
            "authority": item.get("authority"),
            "layer": item.get("layer"),
            "summary": item["message"],
        }
        for item in findings
        if item.get("severity") in {"warning", "error"}
    ]
    triage_buckets = _triage_buckets(backlog_items)
    actionable_count = sum(
        triage_buckets[name]["count"]
        for name in (
            "p0_p1_source_of_truth_gaps",
            "active_supporting_doc_backlog",
            "retrieval_route_gaps",
            "other_harness_findings",
        )
    )
    acceptance_contract = {
        "contract_version": "1.0",
        "read_only": True,
        "blocking_bucket_count": actionable_count,
        "lower_authority_noise_is_blocking": False,
        "project_map_mutation_allowed": False,
        "accepted": actionable_count == 0,
    }
    scorecard = {
        "metadata": "pass" if not any(item["id"].startswith("DOC-META") for item in findings) else "needs_review",
        "reachability": "pass" if not any(item["id"].startswith("DOC-REACH") for item in findings) else "needs_review",
        "authority_labels": "pass" if not any(item["id"].startswith("DOC-AUTH") for item in findings) else "needs_review",
        "retrieval_routes": "pass" if triage_buckets["retrieval_route_gaps"]["count"] == 0 else "needs_review",
    }

    return {
        "report_type": REPORT_TYPE,
        "helper": HELPER_NAME,
        "root": str(root_path),
        "status": "needs_review" if actionable_count else "passed",
        "read_only": True,
        "scope_flags": dict(SCOPE_FLAGS),
        "managed_docs_scanned": len(managed_paths),
        "finding_count": len(findings),
        "findings": findings,
        "summary_by_id": _summary_by_key(findings, "id"),
        "summary_by_severity": _summary_by_key(findings, "severity"),
        "summary_by_priority": _summary_by_key(findings, "priority"),
        "summary_by_authority": _summary_by_key(findings, "authority"),
        "summary_by_layer": _summary_by_key(findings, "layer"),
        "backlog_items": backlog_items,
        "triage_buckets": triage_buckets,
        "acceptance_contract": acceptance_contract,
        "repository_quality_scorecard": scorecard,
        "proposed_project_map_deltas": {
            "applied": False,
            "items": [
                {
                    "path": item.get("path"),
                    "reason": item.get("summary"),
                }
                for item in triage_buckets["retrieval_route_gaps"]["items"]
            ],
        },
        "notes": [
            "Report-only diagnostic for secondary memory governance.",
            "Does not mutate runtime, external-system state, data artifacts, or Project Map.",
        ],
    }


def _triage_buckets(backlog_items: Sequence[dict[str, object]]) -> dict[str, dict[str, object]]:
    names = (
        "p0_p1_source_of_truth_gaps",
        "active_supporting_doc_backlog",
        "legacy_archive_or_lower_authority_noise",
        "retrieval_route_gaps",
        "other_harness_findings",
    )
    buckets: dict[str, dict[str, object]] = {
        name: {"count": 0, "items": []} for name in names
    }
    for item in backlog_items:
        rule_id = str(item.get("id", ""))
        authority = str(item.get("authority", ""))
        priority = str(item.get("priority", ""))
        if rule_id.startswith("DOC-REACH"):
            bucket = "retrieval_route_gaps"
        elif priority in {"P0", "P1"}:
            bucket = "p0_p1_source_of_truth_gaps"
        elif authority in {"archive", "secondary_memory", "research_context", "planning_or_proposal"}:
            bucket = "legacy_archive_or_lower_authority_noise"
        elif priority == "P2":
            bucket = "active_supporting_doc_backlog"
        else:
            bucket = "other_harness_findings"
        typed_items = buckets[bucket]["items"]
        assert isinstance(typed_items, list)
        typed_items.append(item)
        buckets[bucket]["count"] = int(buckets[bucket]["count"]) + 1
    return buckets


def _managed_doc_paths(root: Path) -> list[str]:
    paths: list[Path] = []
    for rel in ROOT_DISCOVERABLE_DOCS:
        candidate = root / rel
        if candidate.exists() and candidate.is_file():
            paths.append(candidate)

    docs_root = root / "docs"
    if docs_root.exists():
        for path in docs_root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in DOC_SUFFIXES:
                continue
            if any(part in SKIPPED_DIRS for part in path.relative_to(root).parts):
                continue
            paths.append(path)

    return sorted({_relative_path(path, root) for path in paths})


def _metadata_findings(text_by_path: dict[str, str]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for rel_path, text in text_by_path.items():
        if not _requires_metadata(rel_path):
            continue
        if rel_path.endswith((".yaml", ".yml")):
            lowered = text.lower()
            missing = [field for field in YAML_METADATA_FIELDS if field not in lowered]
            runtime_present = "runtime_impact:" in lowered or "runtime impact:" in lowered
            if not runtime_present:
                missing.append("runtime_impact:")
            rule_id = "DOC-META-002"
        else:
            missing = [field for field in MARKDOWN_METADATA_FIELDS if field not in text]
            rule_id = "DOC-META-001"
        if missing:
            findings.append(
                _finding(
                    rule_id,
                    "warning",
                    rel_path,
                    f"Missing documentation metadata fields: {', '.join(missing)}.",
                )
            )
    return findings


def _reachability_findings(text_by_path: dict[str, str]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for target in text_by_path:
        if not _requires_reachability(target):
            continue
        inbound_sources = _inbound_sources(target, text_by_path)
        if not inbound_sources:
            findings.append(
                _finding(
                    "DOC-REACH-001",
                    "warning",
                    target,
                    "Active managed documentation has no inbound reference from an active managed source.",
                )
            )
    return findings


def _authority_findings(text_by_path: dict[str, str]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for rel_path, text in text_by_path.items():
        if not _is_operational_authority_source(rel_path):
            continue
        lines = text.splitlines()
        for index, line in enumerate(lines, start=1):
            references = _lower_authority_references(line)
            if not references:
                continue
            surrounding = _surrounding_text(lines, index)
            if _has_lower_authority_label(surrounding):
                continue
            findings.append(
                _finding(
                    "DOC-AUTH-001",
                    "warning",
                    rel_path,
                    "Lower-authority documentation reference lacks an explicit proposal/archive/research/secondary authority label.",
                    line=index,
                    details={"references": references},
                )
            )
    return findings


def _requires_metadata(rel_path: str) -> bool:
    if rel_path in {".codexignore", ".cursorignore"}:
        return False
    if _is_archive_or_inventory(rel_path):
        return False
    if rel_path.startswith("docs/project_map/") and rel_path.endswith((".yaml", ".yml")):
        return False
    return rel_path in {"AGENTS.md", "README.md"} or rel_path.startswith("docs/")


def _requires_reachability(rel_path: str) -> bool:
    if rel_path in ROOT_DISCOVERABLE_DOCS:
        return False
    if _is_archive_or_inventory(rel_path):
        return False
    return rel_path.startswith("docs/")


def _inbound_sources(target: str, text_by_path: dict[str, str]) -> list[str]:
    inbound: list[str] = []
    target_variants = {target, "\\".join(target.split("/"))}
    for source, text in text_by_path.items():
        if source == target:
            continue
        if not _is_active_reference_source(source):
            continue
        if any(variant in text for variant in target_variants):
            inbound.append(source)
    return sorted(inbound)


def _is_operational_authority_source(rel_path: str) -> bool:
    if not _is_active_reference_source(rel_path):
        return False
    return (
        rel_path in PRIMARY_OPERATIONAL_SOURCE_PATHS
        or rel_path in NAVIGATION_INDEX_PATHS
        or rel_path in WORKFLOW_RULE_PATHS
    )


def _is_active_reference_source(rel_path: str) -> bool:
    if _is_archive_or_inventory(rel_path):
        return False
    return rel_path in {"AGENTS.md", "README.md"} or rel_path.startswith("docs/")


def _is_archive_or_inventory(rel_path: str) -> bool:
    return rel_path.startswith("docs/archive/") or bool(INVENTORY_RE.match(rel_path))


def _lower_authority_references(line: str) -> list[str]:
    refs = LOWER_AUTHORITY_PATH_RE.findall(line)
    return sorted(set(ref.replace("\\", "/") for ref in refs))


def _has_lower_authority_label(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in LOWER_AUTHORITY_LABEL_TERMS)


def _surrounding_text(lines: Sequence[str], line_number: int) -> str:
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 1)
    return "\n".join(lines[start:end])


def _annotate_findings(findings: list[dict[str, object]]) -> None:
    for item in findings:
        path = str(item.get("path", ""))
        item["priority"] = _priority_for_path(path)
        item["authority"] = _authority_for_path(path)
        item["layer"] = _layer_for_path(path)


def _priority_for_path(path: str) -> str:
    if path in PRIMARY_OPERATIONAL_SOURCE_PATHS or path == "AGENTS.md":
        return "P0"
    if path in NAVIGATION_INDEX_PATHS or path in WORKFLOW_RULE_PATHS:
        return "P1"
    if path.startswith(LOWER_AUTHORITY_PREFIXES):
        return "P3"
    return "P2"


def _authority_for_path(path: str) -> str:
    if path in PRIMARY_OPERATIONAL_SOURCE_PATHS or path == "AGENTS.md":
        return "primary_operational_source_of_truth"
    if path in NAVIGATION_INDEX_PATHS:
        return "navigation_or_layer_index"
    if path in WORKFLOW_RULE_PATHS:
        return "workflow_rule"
    if path.startswith("docs/project_map/"):
        return "secondary_memory"
    if path.startswith("docs/research/"):
        return "research_context"
    if path.startswith("docs/proposals/") or path.startswith("docs/planned/"):
        return "planning_or_proposal"
    if path.startswith("docs/archive/"):
        return "archive"
    return "supporting_doc"


def _layer_for_path(path: str) -> str:
    if path in {"AGENTS.md", "README.md"}:
        return "root"
    if path.startswith("docs/project_map/"):
        return "project_map"
    if path.startswith("docs/research/"):
        return "research"
    if path.startswith("docs/archive/"):
        return "archive"
    if path.startswith("docs/"):
        return path.split("/")[1] if "/" in path.removeprefix("docs/") else "docs"
    return "other"


def _finding(
    rule_id: str,
    severity: str,
    path: str,
    message: str,
    *,
    line: int | None = None,
    details: dict[str, object] | None = None,
) -> dict[str, object]:
    item: dict[str, object] = {
        "id": rule_id,
        "severity": severity,
        "path": path,
        "message": message,
    }
    if line is not None:
        item["line"] = line
    if details:
        item["details"] = details
    return item


def _summary_by_key(findings: Sequence[dict[str, object]], key: str) -> dict[str, int]:
    summary: dict[str, int] = {}
    for item in findings:
        value = str(item.get(key, "unknown"))
        summary[value] = summary.get(value, 0) + 1
    return dict(sorted(summary.items()))


def _relative_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def _format_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Documentation Harness Report",
        "",
        f"- status: `{report['status']}`",
        f"- helper: `{report['helper']}`",
        f"- read_only: `{report['read_only']}`",
        f"- managed_docs_scanned: `{report['managed_docs_scanned']}`",
        f"- finding_count: `{report['finding_count']}`",
        "",
    ]
    lines.extend(["## Findings", ""])
    findings = report.get("findings", [])
    if isinstance(findings, list) and findings:
        for item in findings:
            if not isinstance(item, dict):
                continue
            location = item.get("path")
            if item.get("line"):
                location = f"{location}:{item['line']}"
            lines.append(
                "- "
                f"`{item.get('id')}` `{item.get('severity')}` "
                f"priority=`{item.get('priority')}` {location}: {item.get('message')}"
            )
    else:
        lines.append("- No findings.")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args(argv)

    report = build_report(args.root)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_format_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

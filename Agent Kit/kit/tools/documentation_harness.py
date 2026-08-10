"""Report-only documentation harness for Agent Memory Kit adopters.

Copy this file into a target project as `scripts/documentation_harness.py` when
using `secondary_memory_governance/`.

The default Core profile checks bounded local Markdown links and heading
anchors. Standard and Workflow opt into progressively broader governance
diagnostics. Generated-content checks require either the generated-content
profile or explicit local generated configuration. This harness is intentionally read-only: it does not change
Project Map, runtime behavior, data artifacts, external systems, or deployment
state, and it intentionally has no automatic repair command. The optional
``documentation_governance.py`` CLI remains the separate Reference Lab tool
for configured generated-projection comparison and controlled writes.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote
from typing import Mapping, Sequence


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
MARKDOWN_LINK_RE = re.compile(
    r"(?<!!)\[[^\]]*\]\(\s*(<[^>\n]+>|[^)\s]+)(?:\s+['\"][^)]*['\"])?\s*\)"
)
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
MARKDOWN_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"\{\{[^}\n]+\}\}|<(?!(?:/?(?:a|abbr|article|aside|b|br|code|details|div|em|h[1-6]|i|img|kbd|li|ol|p|pre|span|strong|table|td|th|tr|ul)\b))[^>\n]+>", re.IGNORECASE)

CHECKS_BY_PROFILE = {
    "core": ("markdown_links",),
    "standard": ("markdown_links", "metadata", "reachability", "authority"),
    "workflow": (
        "markdown_links",
        "metadata",
        "reachability",
        "authority",
        "placeholder",
        "work_leakage",
    ),
    "generated-content": ("markdown_links", "generated"),
}
KNOWN_CHECKS = frozenset(check for checks in CHECKS_BY_PROFILE.values() for check in checks)

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


def build_report(
    root: Path | str = Path.cwd(),
    *,
    profiles: Sequence[str] | None = None,
    config: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Build a deterministic, read-only documentation harness report."""

    root_path = Path(root).resolve()
    active_profiles, active_checks = _active_configuration(profiles, config)
    managed_paths = _managed_doc_paths(root_path)
    text_by_path = {rel: _read_text(root_path / rel) for rel in managed_paths}
    findings: list[dict[str, object]] = []

    if "markdown_links" in active_checks:
        findings.extend(_markdown_link_findings(root_path, text_by_path))
    if "metadata" in active_checks:
        findings.extend(_metadata_findings(text_by_path))
    if "reachability" in active_checks:
        findings.extend(_reachability_findings(text_by_path))
    if "authority" in active_checks:
        findings.extend(_authority_findings(text_by_path))
    if "placeholder" in active_checks:
        findings.extend(_placeholder_findings(text_by_path))
    if "work_leakage" in active_checks:
        findings.extend(_work_leakage_findings(text_by_path, config))
    if "generated" in active_checks:
        findings.extend(_generated_content_findings(root_path, config))
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
        "automatic_fix_available": False,
        "blocking_bucket_count": actionable_count,
        "lower_authority_noise_is_blocking": False,
        "project_map_mutation_allowed": False,
        "accepted": actionable_count == 0,
    }
    scorecard = {
        "markdown_links": _scorecard_status(findings, "DOC-LINK", "DOC-ANCHOR", active="markdown_links" in active_checks),
        "metadata": _scorecard_status(findings, "DOC-META", active="metadata" in active_checks),
        "reachability": _scorecard_status(findings, "DOC-REACH", active="reachability" in active_checks),
        "authority_labels": _scorecard_status(findings, "DOC-AUTH", active="authority" in active_checks),
        "retrieval_routes": _scorecard_status(findings, "DOC-REACH", active="reachability" in active_checks),
        "placeholder": _scorecard_status(findings, "DOC-PLACEHOLDER", active="placeholder" in active_checks),
        "work_leakage": _scorecard_status(findings, "DOC-WORK-LEAKAGE", active="work_leakage" in active_checks),
        "generated_content": _scorecard_status(findings, "DOC-GENERATED", active="generated" in active_checks),
    }

    return {
        "report_type": REPORT_TYPE,
        "helper": HELPER_NAME,
        "root": str(root_path),
        "status": "needs_review" if actionable_count else "passed",
        "read_only": True,
        "profiles": list(active_profiles),
        "active_checks": list(active_checks),
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
            "Report-only diagnostic; Core is the default profile.",
            "Does not mutate runtime, external-system state, data artifacts, or Project Map.",
            "The optional documentation-governance CLI is the Reference Lab surface for generated projection comparison and controlled writes.",
        ],
    }


def _active_configuration(
    profiles: Sequence[str] | None,
    config: Mapping[str, object] | None,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    configured_profiles = _string_list(config.get("profiles"), "profiles") if config else []
    selected = [profiles] if isinstance(profiles, str) else (list(profiles) if profiles is not None else configured_profiles)
    selected = [profile.lower() for profile in selected]
    if not selected:
        selected = ["core"]
    unknown_profiles = sorted(set(selected).difference(CHECKS_BY_PROFILE))
    if unknown_profiles:
        raise ValueError("unknown documentation profile(s): %s" % ", ".join(unknown_profiles))
    configured_checks = _string_list(config.get("checks"), "checks") if config else []
    unknown_checks = sorted(set(configured_checks).difference(KNOWN_CHECKS))
    if unknown_checks:
        raise ValueError("unknown documentation check(s): %s" % ", ".join(unknown_checks))
    active_checks = {check for profile in selected for check in CHECKS_BY_PROFILE[profile]}
    active_checks.update(configured_checks)
    if config and "generated" in config:
        # Declaring generated paths is itself an explicit local opt-in. The
        # profile remains useful when configuration is supplied separately.
        active_checks.add("generated")
    return tuple(dict.fromkeys(selected)), tuple(sorted(active_checks))


def _string_list(value: object, name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("documentation harness config %s must be a list of strings" % name)
    return value


def _scorecard_status(
    findings: Sequence[dict[str, object]], *prefixes: str, active: bool
) -> str:
    if not active:
        return "not_checked"
    return "pass" if not any(str(item["id"]).startswith(prefixes) for item in findings) else "needs_review"


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


def _markdown_link_findings(root: Path, text_by_path: Mapping[str, str]) -> list[dict[str, object]]:
    """Validate only repository-local Markdown destinations and anchors."""

    findings: list[dict[str, object]] = []
    for rel_path, text in text_by_path.items():
        if not rel_path.endswith(".md"):
            continue
        source = root / rel_path
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group(1)
            target, fragment, escaped = _resolve_local_markdown_link(root, source, raw_target)
            line = text.count("\n", 0, match.start()) + 1
            if escaped:
                findings.append(
                    _finding(
                        "DOC-LINK-002",
                        "warning",
                        rel_path,
                        "Markdown link escapes the repository and was not followed.",
                        line=line,
                        details={"target": raw_target},
                    )
                )
                continue
            if target is None:
                continue
            if not target.exists():
                findings.append(
                    _finding(
                        "DOC-LINK-001",
                        "warning",
                        rel_path,
                        "Markdown link target does not exist.",
                        line=line,
                        details={"target": raw_target},
                    )
                )
                continue
            if fragment and (not target.is_file() or fragment not in _markdown_anchor_set(_read_text(target))):
                findings.append(
                    _finding(
                        "DOC-ANCHOR-001",
                        "warning",
                        rel_path,
                        "Markdown link heading anchor does not exist in its local target.",
                        line=line,
                        details={"target": raw_target, "anchor": fragment},
                    )
                )
    return findings


def _resolve_local_markdown_link(root: Path, source: Path, raw_target: str) -> tuple[Path | None, str | None, bool]:
    target = unquote(raw_target.strip().strip("<>"))
    if URI_SCHEME_RE.match(target):
        return None, None, False
    destination, separator, fragment = target.partition("#")
    destination = destination.partition("?")[0]
    candidate = (source.parent / destination).resolve() if destination else source.resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None, fragment if separator else None, True
    return candidate, fragment if separator else None, False


def _markdown_anchor_set(text: str) -> set[str]:
    anchors: set[str] = set()
    used: dict[str, int] = {}
    for heading in MARKDOWN_HEADING_RE.findall(text):
        label = re.sub(r"`([^`]*)`", r"\1", heading).lower()
        label = re.sub(r"[^\w\- ]", "", label, flags=re.UNICODE)
        label = re.sub(r"\s+", "-", label.strip())
        count = used.get(label, 0)
        used[label] = count + 1
        anchors.add(label if count == 0 else "%s-%d" % (label, count))
    return anchors


def _placeholder_findings(text_by_path: Mapping[str, str]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for rel_path, text in text_by_path.items():
        if not rel_path.endswith(".md"):
            continue
        match = PLACEHOLDER_RE.search(re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL))
        if match:
            findings.append(
                _finding(
                    "DOC-PLACEHOLDER-001",
                    "warning",
                    rel_path,
                    "Markdown contains an unresolved placeholder.",
                    line=text.count("\n", 0, match.start()) + 1,
                )
            )
    return findings


def _work_leakage_findings(
    text_by_path: Mapping[str, str], config: Mapping[str, object] | None
) -> list[dict[str, object]]:
    allow_patterns: list[str] = []
    if config:
        policy = config.get("work_link_policy", {})
        if not isinstance(policy, Mapping):
            raise ValueError("documentation harness config work_link_policy must be an object")
        allow_patterns = _string_list(policy.get("allow_references_in"), "work_link_policy.allow_references_in")
    findings: list[dict[str, object]] = []
    for rel_path, text in text_by_path.items():
        if ".work/" not in text or any(_matches_path(rel_path, pattern) for pattern in allow_patterns):
            continue
        line = text.index(".work/")
        findings.append(
            _finding(
                "DOC-WORK-LEAKAGE-001",
                "warning",
                rel_path,
                "Documentation references ephemeral .work content outside its configured allowance.",
                line=text.count("\n", 0, line) + 1,
            )
        )
    return findings


def _generated_content_findings(root: Path, config: Mapping[str, object] | None) -> list[dict[str, object]]:
    """Check only locally declared generated paths and marker cardinality.

    Projection freshness and every write path remain owned by the optional
    Reference Lab CLI. The shared ``generated`` shape intentionally accepts
    that CLI's configuration entries without executing it.
    """

    if not config or "generated" not in config:
        return []
    generated = config["generated"]
    if not isinstance(generated, Mapping):
        raise ValueError("documentation harness config generated must be an object")
    findings: list[dict[str, object]] = []
    for name, entry in sorted(generated.items()):
        if not isinstance(name, str) or not isinstance(entry, Mapping) or not isinstance(entry.get("path"), str):
            raise ValueError("documentation harness config generated entries need a string path")
        path = (root / str(entry["path"])).resolve()
        try:
            relative = _relative_path(path, root)
        except ValueError:
            findings.append(
                _finding("DOC-GENERATED-002", "warning", str(entry["path"]), "Configured generated path escapes the repository.")
            )
            continue
        if not path.is_file():
            findings.append(
                _finding("DOC-GENERATED-001", "warning", relative, "Configured generated content file is missing.")
            )
            continue
        start = "<!-- documentation-governance:%s:start -->" % name
        end = "<!-- documentation-governance:%s:end -->" % name
        text = _read_text(path)
        if text.count(start) != 1 or text.count(end) != 1 or text.find(start) > text.find(end):
            findings.append(
                _finding(
                    "DOC-GENERATED-003",
                    "warning",
                    relative,
                    "Configured generated content lacks one ordered marker pair.",
                    details={"name": name},
                )
            )
    return findings


def _matches_path(relative: str, pattern: str) -> bool:
    pure = PurePosixPath(relative)
    return pure.match(pattern) or fnmatch.fnmatchcase(relative, pattern) or (
        pattern.startswith("**/") and fnmatch.fnmatchcase(relative, pattern[3:])
    )


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
        f"- profiles: `{', '.join(report['profiles'])}`",
        f"- active_checks: `{', '.join(report['active_checks'])}`",
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
    parser.add_argument(
        "--profile",
        action="append",
        type=str.lower,
        choices=tuple(CHECKS_BY_PROFILE),
        help="opt into a named read-only check profile; defaults to Core",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="optional JSON configuration relative to --root; may add profiles, checks, generated paths, and .work allowances",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    try:
        config = _load_config(root, args.config) if args.config else None
        report = build_report(root, profiles=args.profile, config=config)
    except ValueError as error:
        parser.error(str(error))
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_format_markdown(report), end="")
    return 0


def _load_config(root: Path, config_path: Path) -> Mapping[str, object]:
    path = config_path if config_path.is_absolute() else root / config_path
    try:
        value = json.loads(_read_text(path))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("cannot read documentation harness config %s: %s" % (path, error)) from error
    if not isinstance(value, Mapping):
        raise ValueError("documentation harness config must be a JSON object")
    return value


if __name__ == "__main__":
    raise SystemExit(main())

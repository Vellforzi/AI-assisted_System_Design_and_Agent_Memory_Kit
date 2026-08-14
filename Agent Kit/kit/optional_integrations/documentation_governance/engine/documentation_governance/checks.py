"""Lifecycle, navigation, local-link and exception checks."""

from __future__ import annotations

import datetime as dt
import fnmatch
import re
from collections import deque
from pathlib import PurePosixPath
from typing import Mapping
from urllib.parse import unquote

from .config import ExceptionRule, Policy, PolicyError, Registry, load_exceptions, load_policy, load_registry
from .findings import Finding
from .git_snapshot import Snapshot
from .adapters.baseline_prefix import adapt_exceptions, adapt_registry


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*(<[^>\n]+>|[^)\s]+)(?:\s+['\"][^)]*['\"])?\s*\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _matches(path: str, pattern: str) -> bool:
    pure = PurePosixPath(path)
    return pure.match(pattern) or fnmatch.fnmatchcase(path, pattern) or (
        pattern.startswith("**/") and fnmatch.fnmatchcase(path, pattern[3:])
    )


def _managed_paths(paths: set[str] | frozenset[str], policy: Policy) -> list[str]:
    result = []
    for path in paths:
        in_root = any(path.startswith(root) for root in policy.document_roots)
        if in_root or path in policy.root_documents:
            result.append(path)
    return sorted(result)


def _classify(paths: list[str], registry: Registry) -> tuple[dict[str, str], list[Finding]]:
    classifications: dict[str, str] = {}
    findings: list[Finding] = []
    for path in paths:
        matches = [rule for rule in registry.rules if path in rule.paths or any(_matches(path, pattern) for pattern in rule.globs)]
        if not matches:
            findings.append(Finding("DOC-LIFECYCLE-001", path, "Managed document has no lifecycle classification."))
        elif len(matches) > 1:
            ids = ", ".join(rule.rule_id for rule in matches)
            findings.append(Finding("DOC-LIFECYCLE-002", path, f"Managed document matches multiple lifecycle rules: {ids}."))
        else:
            classifications[path] = matches[0].lifecycle
    return classifications, findings


def _anchors(text: str) -> set[str]:
    result: set[str] = set()
    used: dict[str, int] = {}
    for heading in HEADING.findall(text):
        label = re.sub(r"`([^`]*)`", r"\1", heading).lower()
        label = re.sub(r"[^\w\- ]", "", label, flags=re.UNICODE)
        label = re.sub(r"\s+", "-", label.strip())
        count = used.get(label, 0)
        used[label] = count + 1
        result.add(label if not count else f"{label}-{count}")
    return result


def _resolve_link(source: str, raw: str) -> tuple[str | None, str | None, bool]:
    target = unquote(raw.strip().strip("<>"))
    if URI_SCHEME.match(target):
        return None, None, False
    destination, separator, fragment = target.partition("#")
    destination = destination.partition("?")[0]
    parent = PurePosixPath(source).parent
    candidate = parent.joinpath(destination) if destination else PurePosixPath(source)
    parts: list[str] = []
    escaped = False
    for part in candidate.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            else:
                escaped = True
        else:
            parts.append(part)
    return "/".join(parts), fragment if separator else None, escaped


def _markdown_edges(source: str, text: str) -> set[str]:
    result: set[str] = set()
    for match in MARKDOWN_LINK.finditer(text):
        target, _, escaped = _resolve_link(source, match.group(1))
        if target is not None and not escaped:
            result.add(target)
    return result


def _link_findings(paths: list[str], files: Mapping[str, str], all_paths: set[str] | frozenset[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        if not path.lower().endswith(".md"):
            continue
        for match in MARKDOWN_LINK.finditer(files[path]):
            raw = match.group(1)
            target, fragment, escaped = _resolve_link(path, raw)
            if escaped:
                findings.append(Finding("DOC-LINK-002", path, f"Local link escapes repository: {raw}."))
            elif target is not None and not _snapshot_path_exists(target, all_paths):
                findings.append(Finding("DOC-LINK-001", path, f"Local link target does not exist: {raw}."))
            elif target is not None and fragment and (target not in files or fragment not in _anchors(files[target])):
                findings.append(Finding("DOC-ANCHOR-001", path, f"Local link anchor does not exist: {raw}."))
    return findings


def _snapshot_path_exists(path: str, all_paths: set[str] | frozenset[str]) -> bool:
    """Git stores files, not directories; a tracked child proves a directory target exists."""
    prefix = path.rstrip("/") + "/"
    return path in all_paths or any(candidate.startswith(prefix) for candidate in all_paths)


def _navigation_findings(
    files: Mapping[str, str], all_paths: set[str] | frozenset[str], policy: Policy, registry: Registry,
    classifications: Mapping[str, str],
) -> list[Finding]:
    findings: list[Finding] = []
    graph: dict[str, set[str]] = {}
    active = {path for path, lifecycle in classifications.items() if lifecycle in policy.active_lifecycles}
    for entrypoint in policy.entrypoints:
        if entrypoint not in all_paths:
            findings.append(Finding("DOC-NAV-001", entrypoint, "Configured entrypoint does not exist."))
    for source in sorted(active.union(policy.entrypoints)):
        if source in files and source.lower().endswith(".md"):
            graph.setdefault(source, set()).update(_markdown_edges(source, files[source]))
    for source, target in registry.routes:
        if source not in all_paths or target not in all_paths:
            findings.append(Finding("DOC-NAV-002", source, f"Declared navigation route has a missing endpoint: {source} -> {target}."))
        else:
            graph.setdefault(source, set()).add(target)
    reached: set[str] = set()
    queue = deque(path for path in policy.entrypoints if path in files)
    while queue:
        path = queue.popleft()
        if path in reached:
            continue
        reached.add(path)
        queue.extend(sorted(graph.get(path, set()).difference(reached)))
    for path in sorted(active.difference(reached).difference(policy.root_documents)):
        findings.append(Finding("DOC-REACH-001", path, "Active document is not reachable from an approved entrypoint or route."))
    return findings


def _registry_invariant_findings(
    all_paths: set[str] | frozenset[str], registry: Registry, classifications: Mapping[str, str]
) -> list[Finding]:
    findings: list[Finding] = []
    superseded = {path for path, lifecycle in classifications.items() if lifecycle == "superseded"}
    for path in sorted(superseded):
        successor = registry.successors.get(path)
        if successor is None:
            findings.append(Finding("DOC-SUCCESSOR-001", path, "Superseded document has no registered successor."))
        elif successor not in all_paths:
            findings.append(Finding("DOC-SUCCESSOR-002", path, f"Registered successor does not exist: {successor}."))
    for path in sorted(set(registry.successors).difference(superseded)):
        findings.append(Finding("DOC-SUCCESSOR-004", path, "Successor mapping source is not classified as superseded."))
    for old, new in sorted(registry.moved_paths.items()):
        if old in all_paths:
            findings.append(Finding("DOC-MOVE-001", old, "Moved-path source still exists in the candidate snapshot."))
        if new not in all_paths:
            findings.append(Finding("DOC-MOVE-002", old, f"Moved-path destination does not exist: {new}."))
    return findings


def _apply_exceptions(
    findings: list[Finding], exceptions: tuple[ExceptionRule, ...], today: dt.date
) -> tuple[list[Finding], list[Finding]]:
    active = [item for item in exceptions if item.expires >= today]
    expired = [
        Finding("DOC-EXCEPTION-001", item.path, f"Exception for {item.rule_id} expired on {item.expires.isoformat()}.")
        for item in exceptions if item.expires < today
    ]
    remaining: list[Finding] = []
    suppressed: list[Finding] = []
    for finding in findings:
        match = next((item for item in active if item.rule_id == finding.rule_id and item.path == finding.path and item.message == finding.message), None)
        (suppressed if match else remaining).append(finding)
    return remaining + expired, suppressed


def build_report(
    snapshot: Snapshot,
    *,
    policy_path: str,
    include_history: bool = False,
    today: dt.date | None = None,
) -> dict[str, object]:
    """Build one deterministic report from one immutable content view."""
    if policy_path not in snapshot.files:
        raise PolicyError(f"policy is missing from snapshot: {policy_path}")
    policy = load_policy(snapshot.files[policy_path])
    if policy.lifecycle_registry not in snapshot.files:
        raise PolicyError(f"lifecycle registry is missing from snapshot: {policy.lifecycle_registry}")
    if policy.exceptions_registry not in snapshot.files:
        raise PolicyError(f"exceptions registry is missing from snapshot: {policy.exceptions_registry}")
    managed = _managed_paths(snapshot.paths, policy)
    if policy.registry_adapter == "baseline-prefix-v1":
        registry = adapt_registry(
            snapshot.files[policy.lifecycle_registry], managed_paths=managed,
            baseline_paths=snapshot.baseline_paths, root_documents=policy.root_documents,
            entrypoints=policy.entrypoints, all_paths=snapshot.paths,
        )
        exceptions = adapt_exceptions(snapshot.files[policy.exceptions_registry])
    else:
        registry = load_registry(snapshot.files[policy.lifecycle_registry])
        exceptions = load_exceptions(snapshot.files[policy.exceptions_registry])
    classifications, findings = _classify(managed, registry)
    findings.extend(_registry_invariant_findings(snapshot.paths, registry, classifications))
    findings.extend(_navigation_findings(snapshot.files, snapshot.paths, policy, registry, classifications))
    body_lifecycles = set(policy.active_lifecycles)
    if include_history:
        body_lifecycles.update(policy.history_lifecycles)
    body_paths = sorted(
        path for path in managed
        if classifications.get(path) in body_lifecycles
        and (path in policy.root_documents or PurePosixPath(path).suffix.lower() in policy.document_suffixes)
    )
    findings.extend(_link_findings(body_paths, snapshot.files, snapshot.paths))
    remaining, suppressed = _apply_exceptions(findings, exceptions, today or dt.date.today())
    remaining.sort()
    suppressed.sort()
    counts = {name: sum(1 for lifecycle in classifications.values() if lifecycle == name) for name in sorted(set(policy.active_lifecycles + policy.history_lifecycles))}
    return {
        "report_type": "documentation_governance",
        "schema_version": "documentation-governance-report.v1",
        "snapshot": snapshot.label,
        "revision": snapshot.revision,
        "policy_path": policy_path,
        "include_history": include_history,
        "managed_document_count": len(managed),
        "body_document_count": len(body_paths),
        "lifecycle_counts": counts,
        "finding_count": len(remaining),
        "suppressed_finding_count": len(suppressed),
        "findings": [item.as_dict() for item in remaining],
        "suppressed_findings": [item.as_dict() for item in suppressed],
        "status": "passed" if not remaining else "needs_review",
    }

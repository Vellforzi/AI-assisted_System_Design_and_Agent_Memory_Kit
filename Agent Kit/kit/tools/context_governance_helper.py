"""Read-only context governance helper for Agent Memory Kit adopters.

Copy this file into a target project as `scripts/ai_context_helper.py` after
installing `secondary_memory_governance/`.

The helper intentionally uses only the Python standard library and a narrow
YAML subset. It is a reference implementation for deterministic read-set
selection, receipts, API-agent context bundles, and context-selection smoke
checks. It does not mutate files, call external services, or read high-risk
artifacts by default.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import fnmatch
import json
from pathlib import Path
import re
import sqlite3
from typing import Sequence


CONTEXT_INDEX_PATH = Path("docs/project_map/context_index.yaml")
SMOKE_CASES_PATH = Path("docs/project_map/eval_suite/context_selection_smoke_cases.yaml")

DEFAULT_HIGH_RISK_GLOBS = (
    "data/**",
    "output/**",
    ".env",
    ".env.*",
    "**/.env",
    "**/.env.*",
    "**/*.sqlite",
    "**/*.sqlite3",
    "**/*.db",
    "**/*.log",
    ".git/**",
    ".venv/**",
    "**/__pycache__/**",
    "**/.pytest_cache/**",
    "**/*.pyc",
    "**/desktop.ini",
)

TRIGGERED_MODES = {"trigger_only", "secondary_memory_triggered", "never_default"}
PROJECT_MAP_PROFILES = {"project_map_governance", "drift_analysis", "memory_update"}
DEFAULT_TRIGGERED_READ_SET_PROFILES = {"research_promotion"}
SEARCH_BACKENDS = ("lexical", "profile_filtered_semantic", "sqlite_fts")

PROFILE_ALIASES = {
    "api-agent": "api_agent_design",
    "api_agent": "api_agent_design",
    "api_agent_design": "api_agent_design",
    "codex": "context_governance",
    "context": "context_governance",
    "context-governance": "context_governance",
    "context_governance": "context_governance",
    "docs": "docs_governance",
    "docs-only": "docs_governance",
    "docs_governance": "docs_governance",
    "implementation": "implementation",
    "memory-update": "project_map_governance",
    "memory_update": "project_map_governance",
    "plan": "planning",
    "planning": "planning",
    "project-map": "project_map_governance",
    "project_map": "project_map_governance",
    "project_map_governance": "project_map_governance",
    "research": "research",
    "research-promotion": "research_promotion",
    "research_promotion": "research_promotion",
    "review": "review",
    "startup": "startup",
    "validation": "validation",
}

PROFILE_KEYWORDS = (
    ("docs_governance", ("docs-only", "documentation", "reachability", "metadata")),
    ("context_governance", ("context helper", "context index", "retrieval receipt", "read set", "smoke check")),
    ("project_map_governance", ("project map", "memory-update", "memory update", "drift")),
    ("api_agent_design", ("api-agent", "api agent", "request envelope", "context bundle")),
    ("validation", ("validation", "test run", "checks")),
    ("research", ("research", "evidence", "synthesis")),
    ("review", ("review", "inspect", "audit")),
    ("planning", ("plan", "planning", "proposed delta")),
    ("implementation", ("implement", "fix", "change code", "code/test")),
)


@dataclass(frozen=True)
class IndexEntry:
    path: str
    priority: str
    authority: str
    status: str
    layer: str
    task_profiles: tuple[str, ...]
    default_retrieval_mode: str
    canonical_purpose: str
    mutation_boundary: str


@dataclass(frozen=True)
class SmokeCase:
    id: str
    task: str
    profile: str
    max_sources: int
    required_paths: tuple[str, ...] = ()
    forbidden_paths: tuple[str, ...] = ()
    forbidden_prefixes: tuple[str, ...] = ("data/", "output/", "docs/archive/")
    required_skipped_paths: tuple[str, ...] = ()
    include_triggered: bool = False


@dataclass(frozen=True)
class SearchEvaluationScenario:
    id: str
    query: str
    profile: str
    expected_paths: tuple[str, ...] = ()
    forbidden_prefixes: tuple[str, ...] = ()


def build_read_set(
    root: Path | str,
    *,
    task: str | None = None,
    profile: str | None = None,
    max_sources: int = 20,
    include_triggered: bool = False,
) -> dict[str, object]:
    """Build a deterministic read set from the project context index."""

    root_path = Path(root).resolve()
    entries = load_context_index(root_path)
    resolved_profile = _resolve_profile(task=task, profile=profile, entries=entries)
    skipped_high_risk = _skipped_high_risk_context(root_path)

    read_set: list[dict[str, object]] = []
    skipped_trigger_only: list[dict[str, object]] = []

    for entry in entries:
        if _is_high_risk_path(entry.path, root_path):
            continue
        reason = _read_set_inclusion_reason(
            entry,
            profile=resolved_profile,
            include_triggered=include_triggered,
        )
        if reason:
            read_set.append(_entry_to_source(entry, reason))
            continue
        if (
            entry.default_retrieval_mode in TRIGGERED_MODES
            and _entry_matches_profile(entry, resolved_profile)
        ):
            skipped_trigger_only.append(
                _entry_to_source(entry, "trigger-only context skipped by default")
            )

    omitted_count = max(0, len(read_set) - max_sources)
    read_set = read_set[:max_sources]
    missing_read_set_paths = _missing_existing_paths(
        root_path,
        [str(item["path"]) for item in read_set if isinstance(item, dict)],
    )

    return {
        "check_type": "read_set",
        "scope": {
            "profile": resolved_profile,
            "reason": _profile_reason(task, profile, resolved_profile),
            "fallback_used": not bool(profile or _infer_profile_from_task(task, entries)),
        },
        "task": task or "",
        "max_sources": max_sources,
        "omitted_source_count": omitted_count,
        "read_set": read_set,
        "missing_read_set_paths": missing_read_set_paths,
        "skipped_trigger_only_context": skipped_trigger_only,
        "skipped_high_risk_context": skipped_high_risk,
        "runtime_scope_expanded": False,
        "external_system_scope_expanded": False,
        "data_scope_expanded": False,
        "project_map_mutated": False,
    }


def build_receipt(
    root: Path | str,
    *,
    task: str | None,
    profile: str | None,
    read_paths: Sequence[str],
    changed_paths: Sequence[str],
    checks: Sequence[str],
    max_sources: int = 20,
) -> dict[str, object]:
    root_path = Path(root).resolve()
    read_set_result = build_read_set(
        root_path,
        task=task,
        profile=profile,
        max_sources=max_sources,
    )
    return {
        "receipt_type": "context_governance_receipt",
        "task": task or "",
        "scope": read_set_result["scope"],
        "read_set": read_set_result["read_set"],
        "manual_read_paths": [_manual_path_receipt(path, root_path) for path in read_paths],
        "changed_paths": [_normalize_relative_path(path, root_path) for path in changed_paths],
        "checks": list(checks),
        "missing_read_set_paths": read_set_result["missing_read_set_paths"],
        "skipped_trigger_only_context": read_set_result["skipped_trigger_only_context"],
        "skipped_high_risk_context": read_set_result["skipped_high_risk_context"],
        "runtime_scope_expanded": False,
        "external_system_scope_expanded": False,
        "data_scope_expanded": False,
        "project_map_mutated": False,
    }


def build_api_context_bundle(
    root: Path | str,
    *,
    request_id: str,
    task: str | None,
    profile: str | None,
    mutation_scope: str = "read-only",
    max_sources: int = 20,
    requested_tools: Sequence[str] = (),
) -> dict[str, object]:
    if not request_id.strip():
        raise ValueError("request_id is required for API-agent context runs")
    root_path = Path(root).resolve()
    normalized_profile = _require_explicit_api_profile(profile, root_path)
    if mutation_scope != "read-only":
        raise ValueError("API-agent context wrapper is read-only")
    if max_sources < 1:
        raise ValueError("max_sources must be at least 1 for API-agent context runs")

    read_set_result = build_read_set(
        root_path,
        task=task,
        profile=normalized_profile,
        max_sources=max_sources,
    )
    envelope = {
        "request_id": request_id.strip(),
        "task": task or "",
        "task_type": "api-agent context",
        "profile": read_set_result["scope"]["profile"],
        "mutation_scope": mutation_scope,
        "include_triggered_context": False,
        "max_sources": max_sources,
        "requested_tools": list(requested_tools),
        "forbidden_paths": [item["path_glob"] for item in read_set_result["skipped_high_risk_context"]],
    }
    denied_tools = [
        {"tool": tool, "reason": "mutation tools are denied by the read-only API context wrapper"}
        for tool in requested_tools
    ]
    receipt = {
        "receipt_type": "api_agent_context_receipt",
        "request_id": envelope["request_id"],
        "task": task or "",
        "profile": envelope["profile"],
        "request_envelope": envelope,
        "scope": read_set_result["scope"],
        "read_set": read_set_result["read_set"],
        "missing_read_set_paths": read_set_result["missing_read_set_paths"],
        "skipped_trigger_only_context": read_set_result["skipped_trigger_only_context"],
        "skipped_high_risk_context": read_set_result["skipped_high_risk_context"],
        "requested_tools": list(requested_tools),
        "allowed_tools": [],
        "denied_tools": denied_tools,
        "changed_paths": [],
        "checks": [],
        "mutation_tools_allowed": False,
        "runtime_scope_expanded": False,
        "external_system_scope_expanded": False,
        "data_scope_expanded": False,
        "project_map_mutated": False,
    }
    return {
        "bundle_type": "api_agent_context_bundle",
        "request_id": envelope["request_id"],
        "task": task or "",
        "profile": envelope["profile"],
        "mutation_scope": mutation_scope,
        "mutation_tools_allowed": False,
        "request_envelope": envelope,
        "context": {
            "read_set": read_set_result["read_set"],
            "missing_read_set_paths": read_set_result["missing_read_set_paths"],
            "skipped_trigger_only_context": read_set_result["skipped_trigger_only_context"],
            "skipped_high_risk_context": read_set_result["skipped_high_risk_context"],
        },
        "read_set": read_set_result["read_set"],
        "missing_read_set_paths": read_set_result["missing_read_set_paths"],
        "skipped_trigger_only_context": read_set_result["skipped_trigger_only_context"],
        "skipped_high_risk_context": read_set_result["skipped_high_risk_context"],
        "receipt": receipt,
        "fallback_used": read_set_result["scope"]["fallback_used"],
        "runtime_scope_expanded": False,
        "external_system_scope_expanded": False,
        "data_scope_expanded": False,
        "project_map_mutated": False,
    }


def search_context(
    root: Path | str,
    *,
    query: str,
    profile: str,
    backend: str = "lexical",
    max_results: int = 8,
    include_triggered: bool = False,
) -> dict[str, object]:
    """Search only the profile-bounded, hard-gated read set.

    All backends are local and ephemeral. ``sqlite_fts`` builds an in-memory
    index for this call and never creates a database file.
    """

    if backend not in SEARCH_BACKENDS:
        raise ValueError(f"unsupported search backend: {backend}")
    if max_results < 1:
        raise ValueError("max_results must be at least 1")
    root_path = Path(root).resolve()
    normalized_profile = _normalize_profile(profile)
    if not normalized_profile or normalized_profile not in _known_task_profiles(root_path):
        raise ValueError(f"unknown context profile: {normalized_profile or profile}")
    bounded = build_read_set(
        root_path,
        profile=normalized_profile,
        max_sources=10000,
        include_triggered=include_triggered,
    )
    documents: list[tuple[dict[str, object], str]] = []
    for source in bounded["read_set"]:
        if not isinstance(source, dict):
            continue
        path = str(source["path"])
        candidate = root_path / path
        if candidate.is_file() and not _is_high_risk_path(path, root_path):
            documents.append((source, _read_text(candidate)))

    tokens = _tokenize(query)
    if backend == "sqlite_fts":
        scores = _sqlite_fts_scores(documents, query)
    else:
        scores = {
            str(source["path"]): _search_score(
                source,
                text,
                tokens,
                semantic=(backend == "profile_filtered_semantic"),
            )
            for source, text in documents
        }

    results: list[dict[str, object]] = []
    for source, body in documents:
        path = str(source["path"])
        score = scores.get(path, 0.0)
        matched = sorted({token for token in tokens if token in body.lower() or token in path.lower()})
        if score <= 0 or not matched:
            continue
        results.append({
            **source,
            "score": round(float(score), 6),
            "matched_terms": matched,
            "snippet": _snippet(body, matched),
        })
    results.sort(key=lambda item: (-float(item["score"]), str(item["path"])))
    return {
        "check_type": "context_search",
        "backend": backend,
        "profile": bounded["scope"]["profile"],
        "query": query,
        "candidate_count": len(documents),
        "results": results[:max_results],
        "persistent_index_created": False,
        "scope_expanded": False,
    }


def compare_search_backends(
    root: Path | str,
    *,
    scenarios: Sequence[SearchEvaluationScenario | dict[str, object]],
    backends: Sequence[str] = SEARCH_BACKENDS,
) -> dict[str, object]:
    """Evaluate interchangeable local backends against shared scenarios."""

    results: list[dict[str, object]] = []
    failures: list[str] = []
    for raw in scenarios:
        scenario = raw if isinstance(raw, SearchEvaluationScenario) else SearchEvaluationScenario(
            id=str(raw["id"]),
            query=str(raw["query"]),
            profile=str(raw["profile"]),
            expected_paths=tuple(str(value) for value in raw.get("expected_paths", ())),
            forbidden_prefixes=tuple(str(value) for value in raw.get("forbidden_prefixes", ())),
        )
        for backend in backends:
            search = search_context(
                root,
                query=scenario.query,
                profile=scenario.profile,
                backend=backend,
                max_results=max(8, len(scenario.expected_paths)),
            )
            paths = [str(item["path"]) for item in search["results"]]
            missing = sorted(set(scenario.expected_paths) - set(paths))
            forbidden = sorted(path for path in paths if path.startswith(scenario.forbidden_prefixes))
            passed = not missing and not forbidden
            if not passed:
                failures.append(f"{scenario.id}/{backend}")
            results.append({
                "scenario_id": scenario.id,
                "backend": backend,
                "status": "passed" if passed else "failed",
                "expected_hit_rate": (
                    1.0 if not scenario.expected_paths
                    else (len(scenario.expected_paths) - len(missing)) / len(scenario.expected_paths)
                ),
                "missing_expected_paths": missing,
                "selected_forbidden_paths": forbidden,
                "candidate_count": search["candidate_count"],
                "result_paths": paths,
            })
    return {
        "check_type": "search_backend_comparison",
        "status": "failed" if failures else "passed",
        "results": results,
        "failures": failures,
        "persistent_index_created": False,
        "decision": "Backends remain local adapters; no persistent retrieval service is introduced.",
    }


def claim_check(
    root: Path | str,
    *,
    claim: str,
    profile: str,
    max_results: int = 5,
) -> dict[str, object]:
    """Classify a claim and attach bounded supporting context when available."""

    lowered = claim.lower()
    if "project map" in lowered and any(word in lowered for word in ("override", "overrides", "wins")):
        status = "contradicted"
        evidence: list[dict[str, object]] = []
    elif _claim_mentions_forbidden_scope(lowered):
        status = "out_of_scope_or_forbidden"
        evidence = []
    else:
        search = search_context(
            root,
            query=claim,
            profile=profile,
            max_results=max_results,
        )
        evidence = list(search["results"])
        status = "supported" if evidence else "insufficient_evidence"
    return {
        "check_type": "claim_check",
        "claim": claim,
        "profile": profile,
        "status": status,
        "evidence": evidence,
        "scope_expanded": False,
    }


def run_retrieval_fixture(
    root: Path | str,
    fixture: dict[str, object],
    *,
    backends: Sequence[str] = SEARCH_BACKENDS,
) -> dict[str, object]:
    """Run the language-neutral retrieval and claim fixture corpus."""

    scenarios = fixture.get("scenarios", [])
    if not isinstance(scenarios, list):
        raise ValueError("retrieval fixture scenarios must be an array")
    comparison = compare_search_backends(root, scenarios=scenarios, backends=backends)
    claim_results: list[dict[str, object]] = []
    claim_failures: list[str] = []
    raw_claims = fixture.get("claim_cases", [])
    if not isinstance(raw_claims, list):
        raise ValueError("retrieval fixture claim_cases must be an array")
    for raw in raw_claims:
        if not isinstance(raw, dict):
            raise ValueError("retrieval fixture claim case must be an object")
        result = claim_check(
            root,
            claim=str(raw["claim"]),
            profile=str(raw["profile"]),
        )
        expected = str(raw["expected_status"])
        passed = result["status"] == expected
        if not passed:
            claim_failures.append(str(raw["id"]))
        claim_results.append({
            "case_id": str(raw["id"]),
            "status": "passed" if passed else "failed",
            "expected_status": expected,
            "actual_status": result["status"],
        })
    failed = comparison["status"] == "failed" or bool(claim_failures)
    return {
        "check_type": "context_retrieval_fixture",
        "suite_id": fixture.get("suite_id", "unnamed"),
        "status": "failed" if failed else "passed",
        "backend_comparison": comparison,
        "claim_results": claim_results,
        "persistent_index_created": False,
        "runtime_service_started": False,
    }


def run_smoke_checks(
    root: Path | str,
    *,
    case_ids: Sequence[str] = (),
) -> dict[str, object]:
    root_path = Path(root).resolve()
    cases = load_smoke_cases(root_path)
    selected = [case for case in cases if not case_ids or case.id in case_ids]
    results = [_run_smoke_case(root_path, case) for case in selected]
    backlog_items = [
        f"Context smoke case '{case['id']}' failed: {failure}"
        for case in results
        for failure in case["failures"]
    ]
    return {
        "check_type": "context_selection_smoke_checks",
        "status": "failed" if backlog_items else "passed",
        "case_count": len(results),
        "cases": results,
        "backlog_items": backlog_items,
        "runtime_scope_expanded": False,
        "external_system_scope_expanded": False,
        "data_scope_expanded": False,
        "project_map_mutated": False,
    }


def load_context_index(root: Path | str) -> list[IndexEntry]:
    root_path = Path(root).resolve()
    index_path = root_path / CONTEXT_INDEX_PATH
    if not index_path.exists():
        return []

    entries: list[IndexEntry] = []
    current: dict[str, object] | None = None
    in_entries = False
    for raw_line in _read_text(index_path).splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "entries:":
            in_entries = True
            continue
        if not in_entries:
            continue
        if stripped.startswith("- path:"):
            if current:
                entries.append(_entry_from_mapping(current))
            current = {"path": _parse_scalar(stripped.split(":", 1)[1])}
            continue
        if current is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        if key in {
            "priority",
            "authority",
            "status",
            "layer",
            "task_profiles",
            "default_retrieval_mode",
            "canonical_purpose",
            "mutation_boundary",
        }:
            current[key] = _parse_yaml_value(value)
    if current:
        entries.append(_entry_from_mapping(current))
    return [entry for entry in entries if entry.path]


def load_smoke_cases(root: Path | str) -> list[SmokeCase]:
    root_path = Path(root).resolve()
    smoke_path = root_path / SMOKE_CASES_PATH
    if not smoke_path.exists():
        return [
            SmokeCase(
                id="startup_read_set_builtin",
                task="Start a fresh project session.",
                profile="startup",
                max_sources=8,
                required_paths=("AGENTS.md",),
            )
        ]

    cases: list[SmokeCase] = []
    current: dict[str, object] | None = None
    current_list_key: str | None = None
    in_cases = False
    for raw_line in _read_text(smoke_path).splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "cases:":
            in_cases = True
            continue
        if not in_cases:
            continue
        if stripped.startswith("- id:"):
            if current:
                cases.append(_smoke_case_from_mapping(current))
            current = {"id": _parse_scalar(stripped.split(":", 1)[1])}
            current_list_key = None
            continue
        if current is None:
            continue
        if stripped.startswith("- ") and current_list_key:
            current.setdefault(current_list_key, [])
            assert isinstance(current[current_list_key], list)
            current[current_list_key].append(_parse_scalar(stripped.removeprefix("- ")))
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        if key in {
            "required_paths",
            "forbidden_paths",
            "forbidden_prefixes",
            "required_skipped_paths",
        } and not value.strip():
            current[key] = []
            current_list_key = key
            continue
        current[key] = _parse_yaml_value(value)
        current_list_key = None
    if current:
        cases.append(_smoke_case_from_mapping(current))
    return cases


def _run_smoke_case(root: Path, smoke_case: SmokeCase) -> dict[str, object]:
    result = build_read_set(
        root,
        task=smoke_case.task,
        profile=smoke_case.profile,
        max_sources=1000,
        include_triggered=smoke_case.include_triggered,
    )
    read_set = result["read_set"]
    paths = {str(item["path"]) for item in read_set if isinstance(item, dict)}
    failures: list[str] = []

    if len(read_set) > smoke_case.max_sources:
        failures.append(
            f"over_retrieval: selected {len(read_set)} sources; limit is {smoke_case.max_sources}"
        )
    missing_required = sorted(set(smoke_case.required_paths) - paths)
    if missing_required:
        failures.append("under_retrieval: missing required paths " + ", ".join(missing_required))
    missing_required_files = _missing_existing_paths(root, smoke_case.required_paths)
    if missing_required_files:
        failures.append(
            "missing_required_files: required paths do not exist "
            + ", ".join(missing_required_files)
        )
    missing_read_set_paths = _missing_existing_paths(root, sorted(paths))
    if missing_read_set_paths:
        failures.append(
            "missing_read_set_files: selected paths do not exist "
            + ", ".join(missing_read_set_paths)
        )
    selected_forbidden = sorted(set(smoke_case.forbidden_paths) & paths)
    if selected_forbidden:
        failures.append("task_scope_miss: selected forbidden paths " + ", ".join(selected_forbidden))
    selected_forbidden_prefixes = sorted(
        path for path in paths if path.startswith(smoke_case.forbidden_prefixes)
    )
    if selected_forbidden_prefixes:
        failures.append(
            "wrong_retrieval: selected forbidden path prefixes "
            + ", ".join(selected_forbidden_prefixes)
        )
    skipped_paths = {
        str(item["path"])
        for item in result["skipped_trigger_only_context"]
        if isinstance(item, dict)
    }
    missing_skipped = sorted(set(smoke_case.required_skipped_paths) - skipped_paths)
    if missing_skipped:
        failures.append(
            "scope_leak: required skipped paths were not reported " + ", ".join(missing_skipped)
        )

    return {
        "id": smoke_case.id,
        "task": smoke_case.task,
        "profile": smoke_case.profile,
        "status": "failed" if failures else "passed",
        "failures": failures,
        "max_sources": smoke_case.max_sources,
        "read_set": read_set,
        "missing_read_set_paths": missing_read_set_paths,
        "skipped_trigger_only_context": result["skipped_trigger_only_context"],
    }


def _read_set_inclusion_reason(
    entry: IndexEntry,
    *,
    profile: str,
    include_triggered: bool,
) -> str | None:
    if entry.default_retrieval_mode == "startup_required":
        return "startup_required from context index"
    if not _entry_matches_profile(entry, profile):
        return None
    if entry.default_retrieval_mode in {"startup_optional", "task_triggered"}:
        return f"task profile '{profile}' matched; task-local scope applied"
    if entry.default_retrieval_mode == "secondary_memory_triggered":
        if include_triggered or profile in PROJECT_MAP_PROFILES:
            return f"explicit secondary-memory retrieval for profile '{profile}'"
        return None
    if entry.default_retrieval_mode == "trigger_only" and (
        include_triggered or profile in DEFAULT_TRIGGERED_READ_SET_PROFILES
    ):
        return f"explicit triggered retrieval for profile '{profile}'"
    return None


def _entry_matches_profile(entry: IndexEntry, profile: str) -> bool:
    return profile in entry.task_profiles


def _resolve_profile(
    *,
    task: str | None,
    profile: str | None,
    entries: Sequence[IndexEntry],
) -> str:
    normalized = _normalize_profile(profile)
    if normalized:
        return normalized
    inferred = _infer_profile_from_task(task, entries)
    if inferred:
        return inferred
    return "startup"


def _infer_profile_from_task(task: str | None, entries: Sequence[IndexEntry]) -> str | None:
    if not task:
        return None
    task_lower = task.lower()
    for profile, keywords in PROFILE_KEYWORDS:
        if any(keyword in task_lower for keyword in keywords):
            return profile
    known_profiles = sorted({profile for entry in entries for profile in entry.task_profiles})
    for profile in known_profiles:
        profile_text = profile.replace("_", " ")
        if profile in task_lower or profile_text in task_lower:
            return profile
    return None


def _normalize_profile(profile: str | None) -> str | None:
    if not profile:
        return None
    normalized = profile.strip().lower().replace("-", "_")
    return PROFILE_ALIASES.get(normalized, normalized)


def _profile_reason(task: str | None, profile: str | None, resolved: str) -> str:
    if profile:
        return f"explicit profile '{resolved}' supplied"
    if task and _infer_profile_from_task(task, ()):
        return f"profile '{resolved}' inferred from task text"
    return f"default fallback profile '{resolved}'"


def _entry_to_source(entry: IndexEntry, inclusion_reason: str) -> dict[str, object]:
    return {
        "path": entry.path,
        "priority": entry.priority,
        "authority": entry.authority,
        "status": entry.status,
        "layer": entry.layer,
        "retrieval_mode": entry.default_retrieval_mode,
        "inclusion_reason": inclusion_reason,
        "canonical_purpose": entry.canonical_purpose,
        "mutation_boundary": entry.mutation_boundary,
    }


def _manual_path_receipt(path: str, root: Path) -> dict[str, str]:
    rel_path = _normalize_relative_path(path, root)
    entry = next((item for item in load_context_index(root) if item.path == rel_path), None)
    metadata = _metadata_for_path(rel_path, entry)
    return {
        "path": rel_path,
        "authority": metadata["authority"],
        "status": metadata["status"],
        "inclusion_reason": "manual read path supplied to receipt command",
    }


def _metadata_for_path(rel_path: str, entry: IndexEntry | None) -> dict[str, str]:
    if entry is not None:
        return {"authority": entry.authority, "status": entry.status}
    if rel_path.startswith("docs/archive/"):
        return {"authority": "archive_context_not_operational", "status": "archive"}
    if rel_path.startswith("docs/proposals/"):
        return {"authority": "proposal_only_not_operational", "status": "proposal"}
    if rel_path.startswith("docs/project_map/"):
        return {"authority": "secondary_memory_or_navigation", "status": "trigger_only_unindexed"}
    if rel_path.startswith("docs/research"):
        return {"authority": "research_context_not_runtime", "status": "non_runtime_context"}
    if rel_path.startswith("docs/"):
        return {"authority": "unindexed_repository_doc", "status": "unindexed"}
    return {"authority": "root_repository_doc", "status": "unindexed"}


def _entry_from_mapping(value: dict[str, object]) -> IndexEntry:
    return IndexEntry(
        path=str(value.get("path", "")),
        priority=str(value.get("priority", "unindexed")),
        authority=str(value.get("authority", "unknown")),
        status=str(value.get("status", "unknown")),
        layer=str(value.get("layer", "unknown")),
        task_profiles=tuple(value.get("task_profiles", ())),
        default_retrieval_mode=str(value.get("default_retrieval_mode", "trigger_only")),
        canonical_purpose=str(value.get("canonical_purpose", "")),
        mutation_boundary=str(value.get("mutation_boundary", "")),
    )


def _smoke_case_from_mapping(value: dict[str, object]) -> SmokeCase:
    return SmokeCase(
        id=str(value.get("id", "unnamed_case")),
        task=str(value.get("task", "")),
        profile=str(_normalize_profile(str(value.get("profile", "startup"))) or "startup"),
        max_sources=int(value.get("max_sources", 20)),
        required_paths=tuple(value.get("required_paths", ())),
        forbidden_paths=tuple(value.get("forbidden_paths", ())),
        forbidden_prefixes=tuple(
            value.get("forbidden_prefixes", ("data/", "output/", "docs/archive/"))
        ),
        required_skipped_paths=tuple(value.get("required_skipped_paths", ())),
        include_triggered=_parse_bool(value.get("include_triggered", False)),
    )


def _require_explicit_api_profile(profile: str | None, root: Path) -> str:
    normalized = _normalize_profile(profile)
    if not normalized:
        raise ValueError("profile is required for API-agent context runs")
    if normalized not in _known_task_profiles(root):
        raise ValueError(f"unknown API-agent profile: {normalized}")
    return normalized


def _known_task_profiles(root: Path) -> set[str]:
    return {
        profile
        for entry in load_context_index(root)
        for profile in entry.task_profiles
    }


def _context_index_excluded_globs(root: Path) -> list[str]:
    index_path = root / CONTEXT_INDEX_PATH
    if not index_path.exists():
        return []
    globs: list[str] = []
    in_path_globs = False
    for raw_line in _read_text(index_path).splitlines():
        stripped = raw_line.strip()
        if stripped == "path_globs:":
            in_path_globs = True
            continue
        if in_path_globs and stripped.startswith("- "):
            globs.append(_parse_scalar(stripped.removeprefix("- ")))
            continue
        if in_path_globs and stripped and not stripped.startswith("- "):
            break
    return globs


def _skipped_high_risk_context(root: Path) -> list[dict[str, str]]:
    globs = _dedupe([*DEFAULT_HIGH_RISK_GLOBS, *_context_index_excluded_globs(root)])
    return [{"path_glob": glob, "reason": "excluded by default"} for glob in globs]


def _is_high_risk_path(path: str, root: Path) -> bool:
    normalized = path.replace("\\", "/").lower()
    return any(_matches_glob(normalized, glob) for glob in _dedupe([*DEFAULT_HIGH_RISK_GLOBS, *_context_index_excluded_globs(root)]))


def _tokenize(value: str) -> tuple[str, ...]:
    return tuple(token for token in re.findall(r"[a-zA-Z0-9_]+", value.lower()) if len(token) > 1)


def _search_score(
    source: dict[str, object],
    body: str,
    tokens: Sequence[str],
    *,
    semantic: bool,
) -> float:
    searchable = " ".join((
        str(source.get("path", "")),
        str(source.get("canonical_purpose", "")),
        body,
    )).lower()
    score = sum(min(searchable.count(token), 5) for token in tokens)
    if semantic:
        purpose = str(source.get("canonical_purpose", "")).lower()
        score += 1.5 * sum(token in purpose for token in tokens)
        score += 0.5 * sum(token in str(source.get("path", "")).lower() for token in tokens)
    return float(score)


def _sqlite_fts_scores(
    documents: Sequence[tuple[dict[str, object], str]],
    query: str,
) -> dict[str, float]:
    tokens = _tokenize(query)
    if not tokens:
        return {}
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE VIRTUAL TABLE context_docs USING fts5(path UNINDEXED, content)")
        connection.executemany(
            "INSERT INTO context_docs(path, content) VALUES (?, ?)",
            [
                (
                    str(source["path"]),
                    f"{source.get('canonical_purpose', '')} {body}",
                )
                for source, body in documents
            ],
        )
        expression = " OR ".join(f'"{token}"' for token in tokens)
        rows = connection.execute(
            "SELECT path, bm25(context_docs) FROM context_docs WHERE context_docs MATCH ?",
            (expression,),
        ).fetchall()
        return {str(path): max(0.000001, -float(rank) + 1.0) for path, rank in rows}
    except sqlite3.OperationalError:
        return {
            str(source["path"]): _search_score(source, body, tokens, semantic=False)
            for source, body in documents
        }
    finally:
        connection.close()


def _snippet(body: str, matched_terms: Sequence[str], max_chars: int = 320) -> str:
    lines = [
        line.strip()
        for line in body.splitlines()
        if any(term in line.lower() for term in matched_terms)
    ][:3]
    snippet = " ".join(lines) or " ".join(body.split())
    return snippet if len(snippet) <= max_chars else snippet[: max_chars - 3].rstrip() + "..."


def _claim_mentions_forbidden_scope(claim: str) -> bool:
    normalized = claim.replace("\\", "/")
    terms = (
        "data/",
        "output/",
        ".env",
        "secret",
        "token",
        "raw account",
        "broker mutation",
        "external-system mutation",
    )
    return any(term in normalized for term in terms)


def _missing_existing_paths(root: Path, paths: Sequence[str]) -> list[str]:
    missing: list[str] = []
    for path in paths:
        normalized = _normalize_project_path(path)
        if not normalized:
            continue
        if not _project_path_exists(root, normalized):
            missing.append(normalized)
    return sorted(_dedupe(missing))


def _project_path_exists(root: Path, rel_path: str) -> bool:
    parts = Path(rel_path).parts
    if any(part == ".." for part in parts):
        return False
    return (root / rel_path).exists()


def _normalize_project_path(path: str | Path) -> str:
    return Path(str(path).replace("\\", "/")).as_posix().lstrip("./")


def _matches_glob(path: str, pattern: str) -> bool:
    normalized_pattern = pattern.replace("\\", "/").lower()
    if fnmatch.fnmatch(path, normalized_pattern):
        return True
    if normalized_pattern.startswith("**/") and fnmatch.fnmatch(path, normalized_pattern.removeprefix("**/")):
        return True
    if normalized_pattern.endswith("/**"):
        prefix = normalized_pattern.removesuffix("/**")
        return path == prefix or path.startswith(prefix + "/")
    return False


def _parse_yaml_value(value: str) -> object:
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        raw_items = stripped.removeprefix("[").removesuffix("]").split(",")
        return tuple(item.strip().strip('"').strip("'") for item in raw_items if item.strip())
    return _parse_scalar(stripped)


def _parse_scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1"}


def _normalize_relative_path(path: str | Path, root: Path) -> str:
    path_value = Path(path)
    try:
        if path_value.is_absolute():
            path_value = path_value.relative_to(root)
    except ValueError:
        pass
    return path_value.as_posix().lstrip("./")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def _dedupe(values: Sequence[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _print_payload(payload: dict[str, object], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))
        return
    print(_to_markdown(payload))


def _to_markdown(payload: dict[str, object]) -> str:
    lines = ["# Context Governance Helper Output", ""]
    for key in ("check_type", "receipt_type", "bundle_type", "status"):
        if payload.get(key):
            lines.append(f"- {key}: `{payload.get(key)}`")
    scope = payload.get("scope")
    if isinstance(scope, dict):
        lines.append(f"- profile: `{scope.get('profile')}`")
        lines.append(f"- fallback_used: `{scope.get('fallback_used')}`")
    lines.append("")

    sources = payload.get("read_set")
    if isinstance(sources, list) and sources:
        lines.extend(["## Read Set", ""])
        for item in sources:
            if not isinstance(item, dict):
                continue
            lines.append(
                "- "
                f"`{item.get('path')}` | authority=`{item.get('authority')}` | "
                f"status=`{item.get('status')}` | reason={item.get('inclusion_reason')}"
            )
        lines.append("")

    missing_paths = payload.get("missing_read_set_paths")
    if isinstance(missing_paths, list) and missing_paths:
        lines.extend(["## Missing Read Set Paths", ""])
        for path in missing_paths:
            lines.append(f"- `{path}`")
        lines.append("")

    cases = payload.get("cases")
    if isinstance(cases, list) and cases:
        lines.extend(["## Smoke Cases", ""])
        for item in cases:
            if isinstance(item, dict):
                lines.append(f"- `{item.get('id')}` status=`{item.get('status')}`")
        lines.append("")

    backlog = payload.get("backlog_items")
    if isinstance(backlog, list) and backlog:
        lines.extend(["## Backlog Items", ""])
        for item in backlog:
            lines.append(f"- {item}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    read_set_parser = subparsers.add_parser("read-set")
    read_set_parser.add_argument("--task", default="")
    read_set_parser.add_argument("--profile")
    read_set_parser.add_argument("--max-sources", type=int, default=20)
    read_set_parser.add_argument("--include-triggered", action="store_true")
    read_set_parser.add_argument("--format", choices=("json", "markdown"), default="markdown")

    receipt_parser = subparsers.add_parser("receipt")
    receipt_parser.add_argument("--task", default="")
    receipt_parser.add_argument("--profile")
    receipt_parser.add_argument("--read", action="append", default=[])
    receipt_parser.add_argument("--changed", action="append", default=[])
    receipt_parser.add_argument("--check", action="append", default=[])
    receipt_parser.add_argument("--max-sources", type=int, default=20)
    receipt_parser.add_argument("--format", choices=("json", "markdown"), default="markdown")

    api_parser = subparsers.add_parser("api-context")
    api_parser.add_argument("--request-id", required=True)
    api_parser.add_argument("--task", default="")
    api_parser.add_argument("--profile", required=True)
    api_parser.add_argument("--mutation-scope", default="read-only")
    api_parser.add_argument("--max-sources", type=int, default=20)
    api_parser.add_argument("--requested-tool", action="append", default=[])
    api_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    smoke_parser = subparsers.add_parser("smoke-check")
    smoke_parser.add_argument("--case", action="append", default=[])
    smoke_parser.add_argument("--format", choices=("json", "markdown"), default="markdown")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--profile", required=True)
    search_parser.add_argument("--backend", choices=SEARCH_BACKENDS, default="lexical")
    search_parser.add_argument("--max-results", type=int, default=8)
    search_parser.add_argument("--include-triggered", action="store_true")
    search_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    compare_parser = subparsers.add_parser("compare-search")
    compare_parser.add_argument("--fixture", type=Path, required=True)
    compare_parser.add_argument("--backend", action="append", choices=SEARCH_BACKENDS, default=[])
    compare_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    claim_parser = subparsers.add_parser("claim-check")
    claim_parser.add_argument("--claim", required=True)
    claim_parser.add_argument("--profile", required=True)
    claim_parser.add_argument("--max-results", type=int, default=5)
    claim_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    args = parser.parse_args(argv)
    if args.command == "read-set":
        payload = build_read_set(
            args.root,
            task=args.task,
            profile=args.profile,
            max_sources=args.max_sources,
            include_triggered=args.include_triggered,
        )
    elif args.command == "receipt":
        payload = build_receipt(
            args.root,
            task=args.task,
            profile=args.profile,
            read_paths=args.read,
            changed_paths=args.changed,
            checks=args.check,
            max_sources=args.max_sources,
        )
    elif args.command == "api-context":
        try:
            payload = build_api_context_bundle(
                args.root,
                request_id=args.request_id,
                task=args.task,
                profile=args.profile,
                mutation_scope=args.mutation_scope,
                max_sources=args.max_sources,
                requested_tools=args.requested_tool,
            )
        except ValueError as exc:
            api_parser.error(str(exc))
    elif args.command == "smoke-check":
        payload = run_smoke_checks(args.root, case_ids=args.case)
    elif args.command == "search":
        payload = search_context(
            args.root,
            query=args.query,
            profile=args.profile,
            backend=args.backend,
            max_results=args.max_results,
            include_triggered=args.include_triggered,
        )
    elif args.command == "compare-search":
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        payload = run_retrieval_fixture(
            args.root,
            fixture,
            backends=args.backend or SEARCH_BACKENDS,
        )
    elif args.command == "claim-check":
        payload = claim_check(
            args.root,
            claim=args.claim,
            profile=args.profile,
            max_results=args.max_results,
        )
    else:
        parser.error("unknown command")

    _print_payload(payload, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

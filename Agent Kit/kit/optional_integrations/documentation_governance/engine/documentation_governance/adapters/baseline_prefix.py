"""Strict adapter for frozen-baseline registries with prefix rules."""

from __future__ import annotations

import datetime as dt
from pathlib import PurePosixPath
from typing import Mapping

from ..config import (
    LIFECYCLES, ExceptionRule, LifecycleRule, PolicyError, Registry,
    _exact_keys, _object, _repo_path, _strings, parse_json_document,
)


REGISTRY_VERSION = "documentation_lifecycle_registry.v1"
EXCEPTIONS_VERSION = "documentation_validation_exceptions.v1"


def _matches(path: str, rule: Mapping[str, object]) -> bool:
    paths = set(_strings(rule.get("paths", []), "rule paths"))
    prefixes = _strings(rule.get("prefixes", []), "rule prefixes")
    excluded_paths = set(_strings(rule.get("exclude_paths", []), "rule exclude_paths"))
    excluded_prefixes = _strings(rule.get("exclude_prefixes", []), "rule exclude_prefixes")
    selected = path in paths or any(path.startswith(prefix) for prefix in prefixes)
    excluded = path in excluded_paths or any(path.startswith(prefix) for prefix in excluded_prefixes)
    return selected and not excluded


def adapt_registry(
    raw: str, *, managed_paths: list[str], baseline_paths: frozenset[str] | None,
    root_documents: tuple[str, ...], entrypoints: tuple[str, ...], all_paths: frozenset[str],
) -> Registry:
    value = parse_json_document(raw, "baseline-prefix lifecycle registry")
    _exact_keys(value, {"schema_version", "documentation_metadata", "baseline", "review_metadata", "rules", "navigation"}, "registry")
    if value.get("schema_version") != REGISTRY_VERSION:
        raise PolicyError(f"registry schema_version must be {REGISTRY_VERSION}")
    raw_rules = value.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise PolicyError("registry rules must be a non-empty list")
    parsed: list[Mapping[str, object]] = []
    ids: set[str] = set()
    for index, raw_rule in enumerate(raw_rules):
        rule = _object(raw_rule, f"rules[{index}]")
        _exact_keys(rule, {"id", "lifecycle", "paths", "prefixes", "exclude_paths", "exclude_prefixes", "baseline_only", "fallback_for_baseline"}, f"rules[{index}]")
        rule_id, lifecycle = str(rule.get("id", "")), str(rule.get("lifecycle", ""))
        if not rule_id or rule_id in ids:
            raise PolicyError("registry rule ids must be non-empty and unique")
        if lifecycle not in LIFECYCLES:
            raise PolicyError(f"rules[{index}].lifecycle is unsupported")
        if not rule.get("paths") and not rule.get("prefixes"):
            raise PolicyError(f"rules[{index}] needs paths or prefixes")
        for field in ("paths", "exclude_paths"):
            for item in _strings(rule.get(field, []), f"rules[{index}].{field}"):
                _repo_path(item, f"rules[{index}].{field} entry")
        for field in ("prefixes", "exclude_prefixes"):
            for item in _strings(rule.get(field, []), f"rules[{index}].{field}"):
                _repo_path(item, f"rules[{index}].{field} entry", directory=True)
        for field in ("baseline_only", "fallback_for_baseline"):
            if field in rule and not isinstance(rule[field], bool):
                raise PolicyError(f"rules[{index}].{field} must be boolean")
        ids.add(rule_id)
        parsed.append(rule)
    if any(bool(rule.get("baseline_only")) for rule in parsed) and baseline_paths is None:
        raise PolicyError("baseline-prefix registry requires a resolvable baseline.revision")

    classified: dict[str, str] = {}
    explicit = [rule for rule in parsed if not rule.get("fallback_for_baseline")]
    fallback = [rule for rule in parsed if rule.get("fallback_for_baseline")]
    for path in managed_paths:
        if path in root_documents:
            classified[path] = "current-source" if path in entrypoints else "active-support"
            continue
        eligible = [rule for rule in explicit if (not rule.get("baseline_only") or path in baseline_paths) and _matches(path, rule)]
        if not eligible:
            eligible = [rule for rule in fallback if path in baseline_paths and _matches(path, rule)]
        if len(eligible) > 1:
            names = ", ".join(str(rule["id"]) for rule in eligible)
            raise PolicyError(f"managed path matches multiple baseline-prefix rules: {path}: {names}")
        if eligible:
            classified[path] = str(eligible[0]["lifecycle"])
    compact_rules = tuple(
        LifecycleRule(f"adapted-{lifecycle}", lifecycle, tuple(sorted(path for path, value in classified.items() if value == lifecycle)), ())
        for lifecycle in sorted(LIFECYCLES)
        if any(value == lifecycle for value in classified.values())
    )

    navigation = _object(value.get("navigation"), "navigation")
    _exact_keys(navigation, {"approved_entrypoints", "routes", "superseded_successors", "moved_paths"}, "navigation")
    routes: list[tuple[str, str]] = []
    raw_routes = navigation.get("routes", [])
    if not isinstance(raw_routes, list):
        raise PolicyError("navigation.routes must be a list")
    for index, raw_route in enumerate(raw_routes):
        route = _object(raw_route, f"navigation.routes[{index}]")
        _exact_keys(route, {"id", "from", "paths", "prefixes"}, f"navigation.routes[{index}]")
        source = _repo_path(str(route.get("from", "")), "route from")
        targets = {_repo_path(item, "route path") for item in _strings(route.get("paths", []), "route paths")}
        prefixes = tuple(_repo_path(item, "route prefix", directory=True) for item in _strings(route.get("prefixes", []), "route prefixes"))
        targets.update(path for path in classified if path in all_paths and any(path.startswith(prefix) for prefix in prefixes))
        routes.extend((source, target) for target in sorted(targets))

    successors = _navigation_map(navigation.get("superseded_successors", []), "path", "successor", "superseded_successors")
    moved = _navigation_map(navigation.get("moved_paths", []), "from", "to", "moved_paths")
    return Registry(compact_rules, tuple(routes), successors, moved)


def _navigation_map(raw: object, source_key: str, target_key: str, label: str) -> dict[str, str]:
    if not isinstance(raw, list):
        raise PolicyError(f"{label} must be a list")
    result: dict[str, str] = {}
    for index, raw_item in enumerate(raw):
        item = _object(raw_item, f"{label}[{index}]")
        _exact_keys(item, {source_key, target_key}, f"{label}[{index}]")
        source = _repo_path(str(item.get(source_key, "")), f"{label} {source_key}")
        target = _repo_path(str(item.get(target_key, "")), f"{label} {target_key}")
        if source in result:
            raise PolicyError(f"{label} contains duplicate source {source}")
        result[source] = target
    return result


def adapt_exceptions(raw: str) -> tuple[ExceptionRule, ...]:
    value = parse_json_document(raw, "baseline-prefix exceptions registry")
    _exact_keys(value, {"schema_version", "documentation_metadata", "review_metadata", "exceptions"}, "exceptions registry")
    if value.get("schema_version") != EXCEPTIONS_VERSION:
        raise PolicyError(f"exceptions schema_version must be {EXCEPTIONS_VERSION}")
    raw_items = value.get("exceptions", [])
    if not isinstance(raw_items, list):
        raise PolicyError("exceptions must be a list")
    result: list[ExceptionRule] = []
    for index, raw_item in enumerate(raw_items):
        item = _object(raw_item, f"exceptions[{index}]")
        _exact_keys(item, {"id", "rule_id", "target", "reason", "owner", "created", "expires"}, f"exceptions[{index}]")
        target = _object(item.get("target"), f"exceptions[{index}].target")
        _exact_keys(target, {"path", "line", "details"}, f"exceptions[{index}].target")
        details = _object(target.get("details"), f"exceptions[{index}].target.details")
        _exact_keys(details, {"destination"}, f"exceptions[{index}].target.details")
        if item.get("rule_id") != "DOC-REFERENCE-001":
            raise PolicyError(f"exceptions[{index}] uses an unsupported adapted rule_id")
        destination = details.get("destination")
        owner = item.get("owner")
        if not isinstance(destination, str) or not destination or not isinstance(owner, str) or not owner:
            raise PolicyError(f"exceptions[{index}] requires destination and owner")
        try:
            expires = dt.date.fromisoformat(str(item.get("expires", "")))
        except ValueError as error:
            raise PolicyError(f"exceptions[{index}].expires must be YYYY-MM-DD") from error
        path = _repo_path(str(target.get("path", "")), "exception target path")
        result.append(ExceptionRule("DOC-LINK-001", path, f"Local link target does not exist: {destination}.", owner, expires))
    return tuple(result)

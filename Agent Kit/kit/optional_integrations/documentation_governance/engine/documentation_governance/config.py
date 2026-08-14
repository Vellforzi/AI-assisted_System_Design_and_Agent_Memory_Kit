"""Strict loaders for repository-owned documentation governance policy."""

from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Mapping


POLICY_VERSION = "documentation-governance-policy.v1"
REGISTRY_VERSION = "documentation-lifecycle-registry.v1"
EXCEPTIONS_VERSION = "documentation-validation-exceptions.v1"
LIFECYCLES = frozenset({"current-source", "active-support", "historical-record", "superseded"})


class PolicyError(ValueError):
    pass


def _object(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise PolicyError(f"{label} must be an object")
    return value


def _exact_keys(value: Mapping[str, object], allowed: set[str], label: str) -> None:
    unknown = sorted(set(value).difference(allowed))
    if unknown:
        raise PolicyError(f"{label} contains unsupported fields: {', '.join(unknown)}")


def _strings(value: object, label: str, *, non_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise PolicyError(f"{label} must be a list of non-empty strings")
    result = tuple(value)
    if non_empty and not result:
        raise PolicyError(f"{label} must not be empty")
    if len(result) != len(set(result)):
        raise PolicyError(f"{label} must not contain duplicates")
    return result


def _repo_path(value: str, label: str, *, directory: bool = False) -> str:
    normalized = value.replace("\\", "/").strip("/")
    pure = PurePosixPath(normalized)
    if not normalized or pure.is_absolute() or ".." in pure.parts or ":" in normalized:
        raise PolicyError(f"{label} must be a safe repository-relative path")
    return normalized + "/" if directory else normalized


def parse_json_document(raw: str, label: str) -> Mapping[str, object]:
    try:
        return _object(json.loads(raw), label)
    except json.JSONDecodeError as error:
        raise PolicyError(f"{label} is not valid JSON: {error}") from error


@dataclass(frozen=True)
class Policy:
    document_roots: tuple[str, ...]
    root_documents: tuple[str, ...]
    entrypoints: tuple[str, ...]
    lifecycle_registry: str
    exceptions_registry: str
    active_lifecycles: tuple[str, ...]
    history_lifecycles: tuple[str, ...]
    delta_forbid: tuple[str, ...]
    document_suffixes: tuple[str, ...]
    registry_adapter: str | None


def load_policy(raw: str) -> Policy:
    value = parse_json_document(raw, "documentation governance policy")
    _exact_keys(value, {
        "schema_version", "document_roots", "root_documents", "entrypoints",
        "lifecycle_registry", "exceptions_registry", "active_lifecycles",
        "history_lifecycles", "delta_forbid", "document_suffixes",
        "registry_adapter",
    }, "policy")
    if value.get("schema_version") != POLICY_VERSION:
        raise PolicyError(f"policy schema_version must be {POLICY_VERSION}")
    roots = tuple(_repo_path(item, "document_roots entry", directory=True) for item in _strings(value.get("document_roots"), "document_roots", non_empty=True))
    root_docs = tuple(_repo_path(item, "root_documents entry") for item in _strings(value.get("root_documents", []), "root_documents"))
    entrypoints = tuple(_repo_path(item, "entrypoints entry") for item in _strings(value.get("entrypoints"), "entrypoints", non_empty=True))
    registry = _repo_path(str(value.get("lifecycle_registry", "")), "lifecycle_registry")
    exceptions = _repo_path(str(value.get("exceptions_registry", "")), "exceptions_registry")
    active = _strings(value.get("active_lifecycles"), "active_lifecycles", non_empty=True)
    history = _strings(value.get("history_lifecycles"), "history_lifecycles", non_empty=True)
    if set(active + history) != LIFECYCLES or set(active).intersection(history):
        raise PolicyError("active_lifecycles and history_lifecycles must partition the four supported lifecycles")
    suffixes = _strings(value.get("document_suffixes", [".md", ".yaml", ".yml", ".json"]), "document_suffixes", non_empty=True)
    if any(not item.startswith(".") for item in suffixes):
        raise PolicyError("document_suffixes entries must start with a dot")
    adapter = value.get("registry_adapter")
    if adapter not in {None, "baseline-prefix-v1"}:
        raise PolicyError("registry_adapter must be baseline-prefix-v1 when present")
    return Policy(roots, root_docs, entrypoints, registry, exceptions, active, history,
                  _strings(value.get("delta_forbid", []), "delta_forbid"), suffixes, adapter)


@dataclass(frozen=True)
class LifecycleRule:
    rule_id: str
    lifecycle: str
    paths: tuple[str, ...]
    globs: tuple[str, ...]


@dataclass(frozen=True)
class Registry:
    rules: tuple[LifecycleRule, ...]
    routes: tuple[tuple[str, str], ...]
    successors: Mapping[str, str]
    moved_paths: Mapping[str, str]


def load_registry(raw: str) -> Registry:
    value = parse_json_document(raw, "lifecycle registry")
    _exact_keys(value, {"schema_version", "rules", "navigation"}, "registry")
    if value.get("schema_version") != REGISTRY_VERSION:
        raise PolicyError(f"registry schema_version must be {REGISTRY_VERSION}")
    raw_rules = value.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise PolicyError("registry rules must be a non-empty list")
    rules: list[LifecycleRule] = []
    ids: set[str] = set()
    for index, raw_rule in enumerate(raw_rules):
        rule = _object(raw_rule, f"rules[{index}]")
        _exact_keys(rule, {"id", "lifecycle", "paths", "globs"}, f"rules[{index}]")
        rule_id = str(rule.get("id", ""))
        lifecycle = str(rule.get("lifecycle", ""))
        if not rule_id or rule_id in ids:
            raise PolicyError("registry rule ids must be non-empty and unique")
        if lifecycle not in LIFECYCLES:
            raise PolicyError(f"rules[{index}].lifecycle is unsupported")
        paths = tuple(_repo_path(item, f"rules[{index}].paths entry") for item in _strings(rule.get("paths", []), f"rules[{index}].paths"))
        globs = _strings(rule.get("globs", []), f"rules[{index}].globs")
        if not paths and not globs:
            raise PolicyError(f"rules[{index}] needs paths or globs")
        if any(PurePosixPath(pattern).is_absolute() or ".." in PurePosixPath(pattern).parts for pattern in globs):
            raise PolicyError(f"rules[{index}].globs contains an unsafe pattern")
        ids.add(rule_id)
        rules.append(LifecycleRule(rule_id, lifecycle, paths, globs))
    navigation = _object(value.get("navigation"), "navigation")
    _exact_keys(navigation, {"routes", "superseded_successors", "moved_paths"}, "navigation")
    raw_routes = navigation.get("routes", [])
    if not isinstance(raw_routes, list):
        raise PolicyError("navigation.routes must be a list")
    routes: list[tuple[str, str]] = []
    for index, raw_route in enumerate(raw_routes):
        route = _object(raw_route, f"navigation.routes[{index}]")
        _exact_keys(route, {"from", "to"}, f"navigation.routes[{index}]")
        routes.append((_repo_path(str(route.get("from", "")), "route from"), _repo_path(str(route.get("to", "")), "route to")))
    successors = _path_map(navigation.get("superseded_successors", []), "path", "successor", "superseded_successors")
    moved = _path_map(navigation.get("moved_paths", []), "old", "new", "moved_paths")
    return Registry(tuple(rules), tuple(routes), successors, moved)


def _path_map(raw: object, source_key: str, target_key: str, label: str) -> Mapping[str, str]:
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


@dataclass(frozen=True)
class ExceptionRule:
    rule_id: str
    path: str
    message: str
    owner: str
    expires: dt.date


def load_exceptions(raw: str) -> tuple[ExceptionRule, ...]:
    value = parse_json_document(raw, "exceptions registry")
    _exact_keys(value, {"schema_version", "exceptions"}, "exceptions registry")
    if value.get("schema_version") != EXCEPTIONS_VERSION:
        raise PolicyError(f"exceptions schema_version must be {EXCEPTIONS_VERSION}")
    items = value.get("exceptions", [])
    if not isinstance(items, list):
        raise PolicyError("exceptions must be a list")
    result: list[ExceptionRule] = []
    identities: set[tuple[str, str, str]] = set()
    for index, raw_item in enumerate(items):
        item = _object(raw_item, f"exceptions[{index}]")
        _exact_keys(item, {"rule_id", "path", "message", "owner", "expires"}, f"exceptions[{index}]")
        try:
            expiry = dt.date.fromisoformat(str(item.get("expires", "")))
        except ValueError as error:
            raise PolicyError(f"exceptions[{index}].expires must be YYYY-MM-DD") from error
        rule_id, owner = str(item.get("rule_id", "")), str(item.get("owner", ""))
        path = _repo_path(str(item.get("path", "")), "exception path")
        message = item.get("message")
        if not rule_id or not owner or not isinstance(message, str) or not message:
            raise PolicyError(f"exceptions[{index}] requires rule_id, path, exact message, owner and expires")
        identity = (rule_id, path, message)
        if identity in identities:
            raise PolicyError("exceptions must be unique")
        identities.add(identity)
        result.append(ExceptionRule(rule_id, path, message, owner, expiry))
    return tuple(result)

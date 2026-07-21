"""Read-only documentation placement and discoverability proposals.

The helper reports issues and emits unapplied patches. It never creates,
updates, moves, or archives repository files.
"""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
import re
from typing import Sequence


DEFAULT_CONFIG_PATH = Path("docs/project_map/docs_governance_rules.json")
DEFAULT_RULES: dict[str, object] = {
    "roles": {
        "spec": {
            "directory": "docs/specs",
            "index_path": "docs/specs/README.md",
            "required_metadata": ["Status:", "Last aligned:", "Audience:", "Runtime impact:", "Authority:"],
        },
        "research": {
            "directory": "docs/research",
            "index_path": "docs/research/README.md",
            "required_metadata": ["Status:", "Last aligned:", "Audience:", "Runtime impact:", "Authority:"],
        },
        "proposal": {
            "directory": "docs/proposals",
            "index_path": "README.md",
            "required_metadata": ["Status:", "Last aligned:", "Audience:", "Runtime impact:", "Authority:"],
        },
        "archive": {
            "directory": "docs/archive",
            "index_path": "README.md",
            "required_metadata": [],
        },
    }
}


def build_report(
    root: Path | str,
    paths: Sequence[str],
    *,
    config_path: Path | str | None = None,
) -> dict[str, object]:
    root_path = Path(root).resolve()
    rules = _load_rules(root_path, config_path)
    reports: list[dict[str, object]] = []
    for raw_path in paths:
        relative = _safe_relative_path(root_path, raw_path)
        candidate = root_path / relative
        role = _infer_role(relative, rules)
        rule = _role_rule(rules, role) if role else None
        text = _read_text(candidate) if candidate.is_file() else ""
        required = list(rule.get("required_metadata", [])) if rule else []
        missing_metadata = [field for field in required if field not in text]
        inbound = _inbound_references(root_path, relative)
        suggested: list[str] = []
        if not candidate.exists():
            suggested.append("Create the document only after owner approval.")
        if missing_metadata:
            suggested.append("Add missing compact metadata: " + ", ".join(missing_metadata))
        if candidate.exists() and not inbound and not relative.endswith("README.md"):
            suggested.append("Add an inbound link from the nearest active index.")
        reports.append({
            "path": relative,
            "exists": candidate.is_file(),
            "role": role or "unclassified",
            "placement": "matched" if role else "unclassified",
            "missing_metadata": missing_metadata,
            "inbound_references": inbound,
            "suggested_actions": suggested,
        })
    return {
        "report_type": "docs_governance_report",
        "status": "needs_review" if any(item["suggested_actions"] for item in reports) else "passed",
        "read_only": True,
        "files": reports,
        "proposed_patch": {
            "applied": False,
            "patch_type": "review_only_unapplied",
            "diffs": [],
        },
    }


def propose_create(
    root: Path | str,
    *,
    role: str,
    title: str,
    config_path: Path | str | None = None,
) -> dict[str, object]:
    root_path = Path(root).resolve()
    rules = _load_rules(root_path, config_path)
    rule = _role_rule(rules, role)
    slug = _slugify(title)
    proposed_path = f"{str(rule['directory']).rstrip('/')}/{slug}.md"
    _safe_relative_path(root_path, proposed_path)
    metadata = [str(field) + " <value>" for field in rule.get("required_metadata", [])]
    body = "\n".join([f"# {title}", "", *metadata, "", "## Purpose", "", "<describe purpose>", ""])
    index_path = str(rule.get("index_path", "README.md"))
    index_text = _read_text(root_path / index_path) if (root_path / index_path).is_file() else ""
    index_new = index_text.rstrip() + f"\n\n- `{proposed_path}` - {title}.\n"
    diffs = [
        _unified_diff("", body, "/dev/null", proposed_path),
        _unified_diff(index_text, index_new, index_path, index_path),
    ]
    return {
        "report_type": "docs_governance_create_proposal",
        "read_only": True,
        "role": role,
        "proposed_path": proposed_path,
        "index_path": index_path,
        "metadata_template": metadata,
        "proposed_patch": {
            "applied": False,
            "patch_type": "review_only_unapplied",
            "diffs": diffs,
        },
    }


def _load_rules(root: Path, config_path: Path | str | None) -> dict[str, object]:
    if config_path is None:
        candidate = root / DEFAULT_CONFIG_PATH
    else:
        raw = Path(config_path)
        candidate = raw if raw.is_absolute() else root / raw
    if not candidate.is_file():
        return DEFAULT_RULES
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    if not isinstance(payload.get("roles"), dict):
        raise ValueError("docs governance config requires a roles object")
    return payload


def _role_rule(rules: dict[str, object], role: str) -> dict[str, object]:
    roles = rules.get("roles", {})
    if not isinstance(roles, dict) or role not in roles or not isinstance(roles[role], dict):
        raise ValueError(f"unknown documentation role: {role}")
    return roles[role]


def _infer_role(path: str, rules: dict[str, object]) -> str | None:
    roles = rules.get("roles", {})
    if not isinstance(roles, dict):
        return None
    matches = [
        role
        for role, raw in roles.items()
        if isinstance(raw, dict) and path.startswith(str(raw.get("directory", "")).rstrip("/") + "/")
    ]
    return sorted(matches)[0] if matches else None


def _safe_relative_path(root: Path, value: str | Path) -> str:
    raw = Path(value)
    resolved = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"path is outside repository root: {value}") from exc


def _inbound_references(root: Path, target: str) -> list[str]:
    inbound: list[str] = []
    docs = [path for path in root.rglob("*.md") if ".git" not in path.parts]
    for path in docs:
        relative = path.relative_to(root).as_posix()
        if relative != target and target in _read_text(path):
            inbound.append(relative)
    return sorted(inbound)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("title must contain at least one ASCII letter or digit")
    return slug


def _unified_diff(old: str, new: str, old_path: str, new_path: str) -> str:
    return "".join(difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=old_path,
        tofile=new_path,
    ))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)
    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("paths", nargs="+")
    create_parser = subparsers.add_parser("propose-create")
    create_parser.add_argument("--role", required=True)
    create_parser.add_argument("--title", required=True)
    args = parser.parse_args(argv)
    if args.command == "report":
        payload = build_report(args.root, args.paths, config_path=args.config)
    else:
        payload = propose_create(args.root, role=args.role, title=args.title, config_path=args.config)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

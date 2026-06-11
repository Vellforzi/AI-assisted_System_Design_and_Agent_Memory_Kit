#!/usr/bin/env python3
"""
Agent Memory Kit eval smoke checklist runner.

v3.9.4 change: smoke categories are read from eval_trigger_policy.yaml.
The script must not maintain a separate hardcoded category list.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover
    print("ERROR: PyYAML is required to read eval_trigger_policy.yaml", file=sys.stderr)
    raise SystemExit(2) from exc

REQUIRED_CASE_FIELDS = (
    "id",
    "suite_id",
    "kit_version",
    "schema_version",
    "category",
    "title",
    "severity",
    "fixture",
    "grading",
)


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def extract_smoke_categories(policy: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Return category contract from policy, with no hardcoded category names."""
    smoke_policy = policy.get("smoke_policy")
    if not isinstance(smoke_policy, dict):
        raise ValueError("eval_trigger_policy.yaml must contain smoke_policy mapping")

    raw = smoke_policy.get("categories")
    if raw is None:
        raise ValueError("smoke_policy.categories is required")

    categories: Dict[str, Dict[str, Any]] = {}
    if isinstance(raw, dict):
        for name, contract in raw.items():
            if not isinstance(name, str) or not name.strip():
                raise ValueError("smoke_policy.categories contains an empty category name")
            if contract is None:
                contract = {}
            if not isinstance(contract, dict):
                raise ValueError(f"category contract for {name!r} must be a mapping")
            categories[name] = contract
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, str):
                categories[item] = {}
            elif isinstance(item, dict) and "name" in item:
                name = item["name"]
                if not isinstance(name, str) or not name.strip():
                    raise ValueError("smoke_policy.categories item has invalid name")
                contract = {k: v for k, v in item.items() if k != "name"}
                categories[name] = contract
            else:
                raise ValueError("smoke_policy.categories list items must be strings or mappings with name")
    else:
        raise ValueError("smoke_policy.categories must be a mapping or list")

    if not categories:
        raise ValueError("smoke_policy.categories must not be empty")
    return categories


def iter_case_files(cases_dir: Path) -> Iterable[Path]:
    if not cases_dir.exists():
        raise FileNotFoundError(f"missing cases directory: {cases_dir}")
    yield from sorted(p for p in cases_dir.rglob("*.yaml") if p.is_file())
    yield from sorted(p for p in cases_dir.rglob("*.yml") if p.is_file())


def load_cases(cases_dir: Path) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    for path in iter_case_files(cases_dir):
        case = load_yaml(path)
        case["_path"] = str(path)
        cases.append(case)
    return cases


def validate_case_schema(case: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for field in REQUIRED_CASE_FIELDS:
        if field not in case or case[field] in (None, "", [], {}):
            errors.append(f"{case.get('id', case.get('_path', '<unknown>'))}: missing required field {field}")
    grading = case.get("grading")
    if isinstance(grading, dict):
        if not grading.get("method"):
            errors.append(f"{case.get('id')}: grading.method is required")
        if not grading.get("pass_criteria"):
            errors.append(f"{case.get('id')}: grading.pass_criteria is required")
    else:
        errors.append(f"{case.get('id')}: grading must be a mapping")
    fixture = case.get("fixture")
    if isinstance(fixture, dict):
        if not fixture.get("type"):
            errors.append(f"{case.get('id')}: fixture.type is required")
    else:
        errors.append(f"{case.get('id')}: fixture must be a mapping")
    return errors


def selected_by_policy(cases: List[Dict[str, Any]], categories: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    names = set(categories)
    selected: List[Dict[str, Any]] = []
    for case in cases:
        case_category = case.get("category")
        tags = case.get("tags") or []
        tag_set = set(tags) if isinstance(tags, list) else set()
        if case_category in names or (tag_set & names):
            selected.append(case)
    return selected


def validate_category_contract(selected: List[Dict[str, Any]], categories: Dict[str, Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    by_category: Dict[str, int] = {name: 0 for name in categories}
    for case in selected:
        matched = set()
        cat = case.get("category")
        if cat in by_category:
            matched.add(cat)
        tags = case.get("tags") or []
        if isinstance(tags, list):
            matched.update(tag for tag in tags if tag in by_category)
        for name in matched:
            by_category[name] += 1
    for name, contract in categories.items():
        required = bool(contract.get("required", True))
        min_cases = int(contract.get("min_cases", 1 if required else 0))
        if by_category.get(name, 0) < min_cases:
            errors.append(
                f"smoke category {name!r} requires at least {min_cases} case(s), found {by_category.get(name, 0)}"
            )
    return errors


def check_suite_version(manifest: Dict[str, Any], policy: Dict[str, Any], cases: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    manifest_suite = manifest.get("suite_id")
    manifest_version = str(manifest.get("kit_version", ""))
    policy_suite = policy.get("suite_id")
    policy_version = str(policy.get("kit_version", ""))
    if manifest_suite and policy_suite and manifest_suite != policy_suite:
        errors.append(f"suite_id mismatch: manifest={manifest_suite!r}, policy={policy_suite!r}")
    if manifest_version and policy_version and manifest_version != policy_version:
        errors.append(f"kit_version mismatch: manifest={manifest_version!r}, policy={policy_version!r}")
    for case in cases:
        if manifest_suite and case.get("suite_id") != manifest_suite:
            errors.append(f"{case.get('id')}: suite_id {case.get('suite_id')!r} != {manifest_suite!r}")
        if manifest_version and str(case.get("kit_version", "")) != manifest_version:
            errors.append(f"{case.get('id')}: kit_version {case.get('kit_version')!r} != {manifest_version!r}")
    return errors


def render_markdown(
    manifest: Dict[str, Any],
    categories: Dict[str, Dict[str, Any]],
    selected: List[Dict[str, Any]],
    errors: List[str],
) -> str:
    lines: List[str] = []
    lines.append(f"# Eval smoke checklist — {manifest.get('suite_id', '<unknown suite>')} / kit {manifest.get('kit_version', '<unknown>')}")
    lines.append("")
    lines.append("Smoke categories are loaded from `eval_trigger_policy.yaml`.")
    lines.append("")
    lines.append("## Smoke categories")
    for name, contract in categories.items():
        lines.append(f"- `{name}` — required={contract.get('required', True)}, min_cases={contract.get('min_cases', 1)}")
    lines.append("")
    lines.append("## Selected cases")
    if selected:
        for case in selected:
            lines.append(f"- [ ] `{case.get('id')}` `{case.get('category')}` `{case.get('severity')}` — {case.get('title')}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Validation")
    if errors:
        lines.append("FAIL")
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("PASS")
    lines.append("")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build AMK eval smoke checklist from eval_trigger_policy.yaml")
    parser.add_argument("--root", default=None, help="eval_suite root directory; defaults to this script directory")
    parser.add_argument("--policy", default=None, help="path to eval_trigger_policy.yaml")
    parser.add_argument("--manifest", default=None, help="path to manifest.yaml")
    parser.add_argument("--cases-dir", default=None, help="path to cases directory")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--no-fail", action="store_true", help="print validation output but return zero")
    args = parser.parse_args(argv)

    root = Path(args.root) if args.root else Path(__file__).resolve().parent
    policy_path = Path(args.policy) if args.policy else root / "eval_trigger_policy.yaml"
    manifest_path = Path(args.manifest) if args.manifest else root / "manifest.yaml"
    cases_dir = Path(args.cases_dir) if args.cases_dir else root / "cases"

    errors: List[str] = []
    try:
        policy = load_yaml(policy_path)
        manifest = load_yaml(manifest_path)
        categories = extract_smoke_categories(policy)
        cases = load_cases(cases_dir)
        selected = selected_by_policy(cases, categories)
        for case in cases:
            errors.extend(validate_case_schema(case))
        errors.extend(validate_category_contract(selected, categories))
        errors.extend(check_suite_version(manifest, policy, cases))
    except Exception as exc:
        if args.format == "json":
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 0 if args.no_fail else 2

    if args.format == "json":
        payload = {
            "status": "pass" if not errors else "fail",
            "suite_id": manifest.get("suite_id"),
            "kit_version": manifest.get("kit_version"),
            "smoke_categories": list(categories.keys()),
            "selected_cases": [
                {
                    "id": case.get("id"),
                    "category": case.get("category"),
                    "severity": case.get("severity"),
                    "title": case.get("title"),
                    "path": case.get("_path"),
                }
                for case in selected
            ],
            "errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(manifest, categories, selected, errors))

    if errors and not args.no_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

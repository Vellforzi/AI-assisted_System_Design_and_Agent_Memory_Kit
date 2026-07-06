#!/usr/bin/env python3
"""
Agent Memory Kit eval checklist runner.

Creates a timestamped eval run folder and Markdown checklist from eval cases.

Smoke mode reads required categories from eval_trigger_policy.yaml and must not
maintain an independent hardcoded smoke-category list.

Legacy mode: --suite may point to a bundled YAML file with an embedded cases list
(for example core_behavior_eval_cases.yaml). Legacy smoke still uses policy
categories when --policy is supplied; otherwise it falls back to category tags
and critical severity only.

This helper does not call model APIs and does not grade automatically.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

LEGACY_SMOKE_CATEGORIES = {
    "action_intent",
    "grounding",
    "retrieval",
    "side_effect_safety",
    "owner_control",
}

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


def _load_yaml(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise RuntimeError("PyYAML is required to read eval YAML files") from exc
    if not path.exists():
        raise FileNotFoundError(f"missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def extract_smoke_categories(policy: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
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
            categories[name] = contract if isinstance(contract, dict) else {}
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, str):
                categories[item] = {}
            elif isinstance(item, dict) and "name" in item:
                name = item["name"]
                if not isinstance(name, str) or not name.strip():
                    raise ValueError("smoke_policy.categories item has invalid name")
                categories[name] = {k: v for k, v in item.items() if k != "name"}
            else:
                raise ValueError("smoke_policy.categories list items must be strings or mappings with name")
    else:
        raise ValueError("smoke_policy.categories must be a mapping or list")
    if not categories:
        raise ValueError("smoke_policy.categories must not be empty")
    return categories


def legacy_smoke_categories() -> Dict[str, Dict[str, Any]]:
    return {name: {"required": False, "min_cases": 0} for name in sorted(LEGACY_SMOKE_CATEGORIES)}


def _case_tags(case: Dict[str, Any]) -> Set[str]:
    tags = case.get("tags") or []
    return set(tags) if isinstance(tags, list) else set()


def case_matches_categories(case: Dict[str, Any], category_names: Set[str]) -> bool:
    category = str(case.get("category", ""))
    if category in category_names:
        return True
    return bool(_case_tags(case) & category_names)


def count_category_matches(cases: Iterable[Dict[str, Any]], categories: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
    names = set(categories)
    counts: Dict[str, int] = {name: 0 for name in names}
    for case in cases:
        matched: Set[str] = set()
        category = case.get("category")
        if category in counts:
            matched.add(str(category))
        matched.update(tag for tag in _case_tags(case) if tag in counts)
        for name in matched:
            counts[name] += 1
    return counts


def validate_category_contract(cases: Iterable[Dict[str, Any]], categories: Dict[str, Dict[str, Any]]) -> List[str]:
    counts = count_category_matches(cases, categories)
    errors: List[str] = []
    for name, contract in categories.items():
        required = bool(contract.get("required", True))
        min_cases = int(contract.get("min_cases", 1 if required else 0))
        if counts.get(name, 0) < min_cases:
            errors.append(
                f"smoke category {name!r} requires at least {min_cases} case(s), found {counts.get(name, 0)}"
            )
    return errors


def inherited_case_metadata_allowed(manifest: Dict[str, Any]) -> bool:
    invariants = manifest.get("version_invariants")
    if not isinstance(invariants, dict):
        return False
    note = invariants.get("inherited_case_metadata_note")
    return isinstance(note, str) and bool(note.strip())


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
    if inherited_case_metadata_allowed(manifest):
        return errors
    for case in cases:
        if manifest_suite and case.get("suite_id") != manifest_suite:
            errors.append(f"{case.get('id')}: suite_id {case.get('suite_id')!r} != {manifest_suite!r}")
        if manifest_version and str(case.get("kit_version", "")) != manifest_version:
            errors.append(f"{case.get('id')}: kit_version {case.get('kit_version')!r} != {manifest_version!r}")
    return errors


def validate_case_schema(case: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    case_id = case.get("id", case.get("_path", "<unknown>"))
    for field in REQUIRED_CASE_FIELDS:
        if field not in case or case[field] in (None, "", [], {}):
            errors.append(f"{case_id}: missing required field {field}")
    grading = case.get("grading")
    if isinstance(grading, dict):
        if not grading.get("method") and not grading.get("pass_if") and not grading.get("pass_criteria"):
            errors.append(f"{case_id}: grading must include method or pass criteria")
    else:
        errors.append(f"{case_id}: grading must be a mapping")
    fixture = case.get("fixture")
    if not isinstance(fixture, dict):
        errors.append(f"{case_id}: fixture must be a mapping")
    return errors


def iter_case_files(cases_dir: Path) -> Iterable[Path]:
    if not cases_dir.exists():
        raise FileNotFoundError(f"missing cases directory: {cases_dir}")
    yield from sorted(p for p in cases_dir.rglob("*.yaml") if p.is_file())
    yield from sorted(p for p in cases_dir.rglob("*.yml") if p.is_file())


def load_manifest_cases(manifest: Dict[str, Any], manifest_path: Path) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    entries = manifest.get("cases")
    if not isinstance(entries, list):
        raise ValueError("manifest.yaml must contain a cases list")
    base = manifest_path.parent
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        rel = entry.get("path")
        if not isinstance(rel, str) or not rel.strip():
            continue
        case_path = (base / rel).resolve()
        case = _load_yaml(case_path)
        case["_path"] = str(case_path)
        cases.append(case)
    return cases


def load_cases_dir(cases_dir: Path) -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    for path in iter_case_files(cases_dir):
        case = _load_yaml(path)
        case["_path"] = str(path)
        cases.append(case)
    return cases


def _extract_block_value(block: str, key: str) -> str:
    m = re.search(rf"^\s{{4}}{re.escape(key)}:\s*\"?(.*?)\"?\s*$", block, re.M)
    return m.group(1).strip() if m else ""


def _fallback_parse_embedded_cases(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    starts = [m.start() for m in re.finditer(r"^\s{2}- id:\s*", text, flags=re.M)]
    cases: List[Dict[str, Any]] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        block = text[start:end]
        cases.append(
            {
                "id": _extract_block_value(block, "id"),
                "category": _extract_block_value(block, "category"),
                "severity": _extract_block_value(block, "severity"),
                "title": _extract_block_value(block, "title"),
                "prompt": _extract_block_value(block, "prompt"),
            }
        )
    return [c for c in cases if c.get("id")]


def load_embedded_cases(path: Path) -> List[Dict[str, Any]]:
    data = _load_yaml(path)
    cases = data.get("cases", []) if isinstance(data, dict) else []
    return [c for c in cases if isinstance(c, dict)]


def resolve_eval_paths(
    suite: Path | None,
    policy: Path | None,
    manifest: Path | None,
    cases_dir: Path | None,
    kit_root: Path | None,
) -> Tuple[Path, Path, Path, Path, Path]:
    if kit_root is None:
        kit_root = Path(__file__).resolve().parents[1]
    eval_root = kit_root / "eval_suite"
    policy_path = policy or eval_root / "eval_trigger_policy.yaml"
    manifest_path = manifest or eval_root / "manifest.yaml"
    cases_path = cases_dir or eval_root / "cases"
    suite_path = suite or manifest_path
    return kit_root, policy_path, manifest_path, cases_path, suite_path


def load_case_corpus(suite_path: Path, manifest_path: Path, cases_path: Path) -> Tuple[List[Dict[str, Any]], str]:
    if suite_path.name == "manifest.yaml" or suite_path.resolve() == manifest_path.resolve():
        manifest = _load_yaml(manifest_path)
        return load_manifest_cases(manifest, manifest_path), "manifest"
    if suite_path.is_dir():
        return load_cases_dir(suite_path), "cases_dir"
    data = _load_yaml(suite_path)
    if isinstance(data.get("cases"), list):
        return load_embedded_cases(suite_path), "embedded"
    return _fallback_parse_embedded_cases(suite_path), "embedded_fallback"


def select_cases(
    cases: Iterable[Dict[str, Any]],
    mode: str,
    smoke_categories: Dict[str, Dict[str, Any]],
    explicit_categories: Set[str],
) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    smoke_names = set(smoke_categories)
    for case in cases:
        if mode == "full":
            selected.append(case)
        elif mode == "smoke":
            if case_matches_categories(case, smoke_names) or str(case.get("severity", "")) == "critical":
                selected.append(case)
        elif mode == "category":
            if case_matches_categories(case, explicit_categories):
                selected.append(case)
    return selected


def write_checklist(
    out_dir: Path,
    selected: List[Dict[str, Any]],
    mode: str,
    source: Path,
    smoke_categories: Dict[str, Dict[str, Any]],
    validation_errors: List[str],
) -> Path:
    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = out_dir / f"eval_run_{timestamp}_{mode}"
    run_dir.mkdir(parents=True, exist_ok=False)
    checklist = run_dir / "checklist.md"
    lines = [
        f"# Agent Memory Kit Eval Run — {timestamp}",
        "",
        f"Mode: `{mode}`",
        f"Source suite: `{source}`",
        "",
        "## Smoke categories (from eval_trigger_policy.yaml)",
        "",
    ]
    for name, contract in smoke_categories.items():
        lines.append(
            f"- `{name}` — required={contract.get('required', True)}, min_cases={contract.get('min_cases', 1)}"
        )
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "PASS" if not validation_errors else "FAIL",
        ]
    )
    for error in validation_errors:
        lines.append(f"- {error}")
    lines.extend(
        [
            "",
            "## How to use",
            "",
            "For each case, paste the prompt and fixture into the target agent/client, capture the output and any tool calls, then mark pass/partial/fail.",
            "",
            "## Cases",
            "",
        ]
    )
    for case in selected:
        case_id = case.get("id", "")
        title = case.get("title", "")
        category = case.get("category", "")
        severity = case.get("severity", "")
        prompt = case.get("prompt", "")
        lines.extend(
            [
                f"### {case_id} — {title}",
                "",
                f"- Category: `{category}`",
                f"- Severity: `{severity}`",
                "- Outcome: `[ ] pass  [ ] partial  [ ] fail  [ ] blocked`",
                "- Tool calls observed: ",
                "- Notes: ",
                "",
                "Prompt:",
                "",
                "```text",
                str(prompt),
                "```",
                "",
            ]
        )
    checklist.write_text("\n".join(lines), encoding="utf-8")
    return checklist


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an Agent Memory Kit eval checklist run.")
    parser.add_argument(
        "--suite",
        default=None,
        help="Path to manifest.yaml, cases directory, or legacy embedded cases YAML",
    )
    parser.add_argument("--out", required=True, help="Output directory for eval runs")
    parser.add_argument("--mode", choices=["smoke", "full", "category"], default="smoke")
    parser.add_argument(
        "--category",
        action="append",
        default=[],
        help="Category to include when --mode category is used. May repeat.",
    )
    parser.add_argument("--policy", default=None, help="Path to eval_trigger_policy.yaml")
    parser.add_argument("--manifest", default=None, help="Path to manifest.yaml")
    parser.add_argument("--cases-dir", default=None, help="Path to cases directory")
    parser.add_argument("--kit-root", default=None, help="Path to Agent Kit/kit root")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--validate-only", action="store_true", help="Validate smoke policy without writing a checklist")
    args = parser.parse_args()

    suite_arg = Path(args.suite) if args.suite else None
    policy_arg = Path(args.policy) if args.policy else None
    manifest_arg = Path(args.manifest) if args.manifest else None
    cases_arg = Path(args.cases_dir) if args.cases_dir else None
    kit_root_arg = Path(args.kit_root) if args.kit_root else None

    _, policy_path, manifest_path, cases_path, suite_path = resolve_eval_paths(
        suite_arg, policy_arg, manifest_arg, cases_arg, kit_root_arg
    )

    errors: List[str] = []
    try:
        policy = _load_yaml(policy_path)
        manifest = _load_yaml(manifest_path)
        cases, corpus_mode = load_case_corpus(suite_path, manifest_path, cases_path)
        use_policy_contract = corpus_mode == "manifest" or args.policy is not None
        smoke_categories = extract_smoke_categories(policy) if use_policy_contract else legacy_smoke_categories()
        if corpus_mode == "manifest":
            for case in cases:
                errors.extend(validate_case_schema(case))
        if use_policy_contract:
            errors.extend(validate_category_contract(cases, smoke_categories))
        errors.extend(check_suite_version(manifest, policy, cases))
        selected = select_cases(cases, args.mode, smoke_categories, set(args.category))
    except Exception as exc:
        if args.format == "json":
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not selected and args.mode != "full":
        errors.append("No eval cases selected. Check suite path, mode, categories, and eval_trigger_policy.yaml.")

    if args.format == "json":
        payload = {
            "status": "pass" if not errors else "fail",
            "mode": args.mode,
            "suite_id": manifest.get("suite_id"),
            "kit_version": manifest.get("kit_version"),
            "smoke_categories": list(smoke_categories.keys()),
            "category_counts": count_category_matches(cases, smoke_categories),
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
    elif args.validate_only:
        if errors:
            print("FAIL")
            for error in errors:
                print(f"- {error}")
        else:
            print("PASS")
            print(f"Cases selected ({args.mode}): {len(selected)}")
    else:
        if not selected:
            raise SystemExit("No eval cases selected. Check suite path, mode, and categories.")
        out = Path(args.out)
        checklist = write_checklist(out, selected, args.mode, suite_path, smoke_categories, errors)
        print(f"Created eval checklist: {checklist}")
        print(f"Cases selected: {len(selected)}")
        if errors:
            print("Validation warnings:")
            for error in errors:
                print(f"- {error}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

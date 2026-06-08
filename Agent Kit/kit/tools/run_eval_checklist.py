#!/usr/bin/env python3
"""
Agent Memory Kit eval checklist runner.

Creates a timestamped eval run folder and Markdown checklist from a YAML eval case file.

This helper intentionally does not call model APIs and does not grade automatically.
It is meant for owner-controlled manual or semi-automated eval runs.

It uses PyYAML if installed. If PyYAML is absent, it falls back to a simple parser
that extracts case id/category/severity/title/prompt fields from the starter YAML.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

SMOKE_CATEGORIES = {
    "action_intent",
    "grounding",
    "retrieval",
    "side_effect_safety",
    "owner_control",
}


def _load_with_yaml(path: Path) -> List[Dict[str, Any]] | None:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    cases = data.get("cases", []) if isinstance(data, dict) else []
    return [c for c in cases if isinstance(c, dict)]


def _extract_block_value(block: str, key: str) -> str:
    m = re.search(rf"^\s{{4}}{re.escape(key)}:\s*\"?(.*?)\"?\s*$", block, re.M)
    return m.group(1).strip() if m else ""


def _fallback_parse(path: Path) -> List[Dict[str, Any]]:
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


def load_cases(path: Path) -> List[Dict[str, Any]]:
    return _load_with_yaml(path) or _fallback_parse(path)


def select_cases(cases: Iterable[Dict[str, Any]], mode: str, categories: set[str]) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    for case in cases:
        category = str(case.get("category", ""))
        severity = str(case.get("severity", ""))
        if mode == "full":
            selected.append(case)
        elif mode == "smoke":
            if category in SMOKE_CATEGORIES or severity == "critical":
                selected.append(case)
        elif mode == "category":
            if category in categories:
                selected.append(case)
    return selected


def write_checklist(out_dir: Path, selected: List[Dict[str, Any]], mode: str, source: Path) -> Path:
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
        "## How to use",
        "",
        "For each case, paste the prompt and fixture into the target agent/client, capture the output and any tool calls, then mark pass/partial/fail.",
        "",
        "## Cases",
        "",
    ]
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an Agent Memory Kit eval checklist run.")
    parser.add_argument("--suite", required=True, help="Path to core_behavior_eval_cases.yaml")
    parser.add_argument("--out", required=True, help="Output directory for eval runs")
    parser.add_argument("--mode", choices=["smoke", "full", "category"], default="smoke")
    parser.add_argument("--category", action="append", default=[], help="Category to include when --mode category is used. May repeat.")
    args = parser.parse_args()

    suite = Path(args.suite)
    out = Path(args.out)
    cases = load_cases(suite)
    selected = select_cases(cases, args.mode, set(args.category))
    if not selected:
        raise SystemExit("No eval cases selected. Check suite path, mode, and categories.")
    checklist = write_checklist(out, selected, args.mode, suite)
    print(f"Created eval checklist: {checklist}")
    print(f"Cases selected: {len(selected)}")


if __name__ == "__main__":
    main()

"""Command-line surface for deterministic documentation governance checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .checks import build_report
from .config import PolicyError, load_policy
from .delta import build_delta_report
from .git_snapshot import GitSnapshotError, baseline_snapshot, candidate_snapshot


def _mode(args: argparse.Namespace) -> tuple[str, str | None]:
    if args.staged:
        return "staged", None
    if args.worktree:
        return "worktree", None
    if args.changed is not None:
        return "changed", args.changed
    return "full", None


def _render_markdown(report: dict[str, object]) -> str:
    lines = [
        f"# {report['report_type'].replace('_', ' ').title()}", "",
        f"- status: `{report['status']}`",
    ]
    for key in ("snapshot", "managed_document_count", "body_document_count", "finding_count", "introduced_finding_count"):
        if key in report:
            lines.append(f"- {key}: `{report[key]}`")
    lines.extend(["", "## Findings", ""])
    items = report.get("introduced_findings", report.get("findings", []))
    if isinstance(items, list) and items:
        for item in items:
            if isinstance(item, dict):
                lines.append(f"- `{item.get('id')}` {item.get('path')}: {item.get('message')}")
    else:
        lines.append("- No findings.")
    return "\n".join(lines) + "\n"


def _emit(report: dict[str, object], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(_render_markdown(report), end="")


def _add_mode(parser: argparse.ArgumentParser, *, allow_full: bool) -> None:
    selectors = parser.add_mutually_exclusive_group()
    selectors.add_argument("--staged", action="store_true", help="Read exactly the Git index.")
    selectors.add_argument("--worktree", action="store_true", help="Explicitly read tracked and untracked worktree files.")
    selectors.add_argument("--changed", metavar="BASE", help="Read HEAD and compare against its merge base with BASE.")
    if allow_full:
        selectors.add_argument("--full", action="store_true", help="Read the committed HEAD snapshot (default).")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", default="docs/documentation_governance_policy.json")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Build a lifecycle and body-validation report.")
    _add_mode(check, allow_full=True)
    check.add_argument("--include-history", action="store_true")
    check.add_argument("--fail-on", choices=("never", "finding"), default="finding")
    delta = sub.add_parser("delta", help="Reject newly introduced findings of selected rule IDs.")
    _add_mode(delta, allow_full=False)
    delta.add_argument("--forbid", action="append", dest="forbidden")
    args = parser.parse_args(argv)
    mode, base = _mode(args)
    if args.command == "delta" and mode == "full":
        parser.error("delta requires --staged, --worktree, or --changed BASE")
    if getattr(args, "include_history", False) and mode != "full":
        parser.error("--include-history requires committed --full mode")
    root = args.root.resolve()
    try:
        candidate_view = candidate_snapshot(root, mode, base, args.policy)
        candidate = build_report(candidate_view, policy_path=args.policy, include_history=getattr(args, "include_history", False))
        if args.command == "check":
            _emit(candidate, args.format)
            return 1 if args.fail_on == "finding" and candidate["finding_count"] else 0
        baseline_view = baseline_snapshot(root, mode, base, args.policy)
        baseline = build_report(baseline_view, policy_path=args.policy)
        if args.forbidden:
            forbidden = args.forbidden
        else:
            policy = load_policy(candidate_view.files[args.policy])
            forbidden = list(policy.delta_forbid)
        report = build_delta_report(baseline, candidate, forbidden)
        report["baseline_snapshot"] = baseline_view.label
        report["candidate_snapshot"] = candidate_view.label
        _emit(report, args.format)
        return 1 if report["status"] == "failed" else 0
    except (PolicyError, GitSnapshotError, OSError) as error:
        print(f"documentation governance error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

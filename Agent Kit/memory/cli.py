#!/usr/bin/env python3
"""Explicit local memory operations. Writes require a writable project profile."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from engine import Memory, MemoryError, VERSION, load_json


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", required=True, help="Exact local checkout; never inferred from a cached task")
    p.add_argument("--config", default="Project Map/memory.config.json")
    sub = p.add_subparsers(dest="action", required=True)
    for name in ["search", "context"]:
        a = sub.add_parser(name)
        a.add_argument("--query", action="append", required=True)
        a.add_argument("--scope")
        a.add_argument("--branch")
        a.add_argument("--history", action="store_true", help="Include retired/candidate/historical material, labelled")
        a.add_argument("--limit", type=int, default=8)
        a.add_argument("--offset", type=int, default=0)
        a.add_argument("--budget", type=int, default=8000, help="Maximum characters in returned hit objects")
    a = sub.add_parser("read"); a.add_argument("id"); a.add_argument("--history", action="store_true")
    a = sub.add_parser("source"); a.add_argument("path")
    a = sub.add_parser("stage"); a.add_argument("--input", required=True); a.add_argument("--operation-id", required=True); a.add_argument("--expected-revision", required=True, type=int)
    a = sub.add_parser("lifecycle"); a.add_argument("id"); a.add_argument("--status", choices=["active", "stale", "revoked", "superseded", "rejected"], required=True)
    a.add_argument("--operation-id", required=True); a.add_argument("--expected-revision", required=True, type=int); a.add_argument("--reason", required=True); a.add_argument("--successor")
    sub.add_parser("audit"); sub.add_parser("index"); sub.add_parser("status")
    args = p.parse_args(argv)
    try:
        memory = Memory(args.project, args.config)
        if args.action in {"search", "context"}:
            result = memory.search(args.query, scope=args.scope, branch=args.branch, include_history=args.history, limit=args.limit, offset=args.offset, budget=args.budget)
        elif args.action == "read":
            result = memory.read(args.id, args.history)
        elif args.action == "source":
            result = memory.source(args.path)
        elif args.action == "stage":
            result = memory.stage(load_json(Path(args.input)), args.operation_id, args.expected_revision)
        elif args.action == "lifecycle":
            result = memory.transition(args.id, args.status, args.operation_id, args.expected_revision, args.reason, args.successor)
        elif args.action == "audit":
            result = memory.audit()
        elif args.action == "index":
            result = memory.index()
        else:
            result = {"version": VERSION, "project_id": memory.project_id, "write_enabled": memory.writable,
                      "record_language": memory.config.get("record_language", "en"), "query_languages": ["ru", "en"],
                      "model_calls": 0, "background_collection": False, "records": len(memory.all_records())}
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except (MemoryError, OSError, ValueError, TypeError, KeyError) as exc:
        # Do not echo input content, credentials or complete parser exceptions.
        result = {"ok": False, "error": getattr(exc, "code", type(exc).__name__),
                  "message": str(exc) if isinstance(exc, MemoryError) else "Check the explicit path, schema and current source; input content was not printed"}
        print(json.dumps(result, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    # A JSON protocol must not inherit a Windows console/pipe code page.
    # Keep original RU/EN/mixed text intact, including characters outside cp1251.
    sys.stdout.reconfigure(encoding="utf-8", errors="strict")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    raise SystemExit(main())

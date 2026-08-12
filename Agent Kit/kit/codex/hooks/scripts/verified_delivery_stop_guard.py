#!/usr/bin/env python3
"""Fail-closed Stop gate for explicitly declared verified-delivery tasks.

The hook delegates receipt semantics to the shared strict validator and binds
finalization claims to current Git and filesystem evidence. Product semantics
remain in the task-specific oracles referenced by the receipt.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


def read_input() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def repo_root(cwd: Path) -> Path:
    for candidate in [cwd, *cwd.parents]:
        if (candidate / ".git").exists() and (candidate / ".codex").exists():
            return candidate
    return cwd


def safe_under(root: Path, value: str) -> Path | None:
    try:
        candidate = (root / value).resolve()
        candidate.relative_to(root.resolve())
        return candidate
    except Exception:
        return None


def load_common(root: Path):
    candidates = [
        root / "Agent Kit" / "kit" / "tools" / "validate_verified_delivery_common.py",
        Path(__file__).resolve().parents[2] / "Agent Kit" / "kit" / "tools" / "validate_verified_delivery_common.py",
    ]
    for path in candidates:
        if not path.is_file():
            continue
        spec = importlib.util.spec_from_file_location("verified_delivery_common", path)
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError("shared verified-delivery validator is unavailable")


def newest_declared_task(root: Path) -> tuple[Path, Path, dict[str, Any]] | None:
    lease_root = root / ".codex" / "runtime" / "scope_leases"
    if not lease_root.exists():
        return None
    candidates: list[tuple[float, Path, Path, dict[str, Any]]] = []
    for lease_path in lease_root.glob("*.json"):
        try:
            lease = json.loads(lease_path.read_text(encoding="utf-8"))
            task_root = safe_under(root, str(lease.get("task_output_root") or ""))
            declaration = task_root / "verified_delivery.requirements.json" if task_root else None
            if declaration and declaration.is_file():
                candidates.append((lease_path.stat().st_mtime, declaration, lease_path, lease))
        except Exception:
            continue
    if not candidates:
        return None
    _, declaration, lease_path, lease = max(candidates, key=lambda item: item[0])
    return declaration, lease_path, lease


def stop(code: str, reason: str) -> None:
    print(json.dumps({
        "continue": False,
        "stopReason": reason,
        "systemMessage": (
            f"{code}: verified-delivery finalization is incomplete. "
            "Do not claim completion or a terminal blocker. Continue useful in-scope repair, "
            "or record a schema-1.2/1.3 task_blocked receipt only when a canonical terminal trigger "
            "and safe final state are proven, then retry Stop."
        ),
    }, ensure_ascii=False))


def main() -> int:
    data = read_input()
    root = repo_root(Path(data.get("cwd") or os.getcwd()).resolve())
    selected = newest_declared_task(root)
    if selected is None:
        print(json.dumps({}))
        return 0
    declaration_path, _, lease = selected
    try:
        declaration = json.loads(declaration_path.read_text(encoding="utf-8"))
        if not isinstance(declaration, dict):
            raise ValueError("declaration root must be an object")
    except Exception as exc:
        stop("VERIFIED_DELIVERY_DECLARATION_INVALID", str(exc))
        return 0
    if declaration.get("required") is not True:
        print(json.dumps({}))
        return 0
    task_root = declaration_path.parent
    if declaration.get("task_id") != lease.get("task_id"):
        stop("VERIFIED_DELIVERY_TASK_MISMATCH", "declaration task_id does not match the lease")
        return 0
    contract = task_root / str(declaration.get("contract") or "")
    receipt_path = task_root / str(declaration.get("receipt") or "")
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            raise ValueError("receipt root must be an object")
        common = load_common(root)
    except Exception as exc:
        stop("VERIFIED_DELIVERY_RECEIPT_MISSING", str(exc))
        return 0
    if receipt.get("task_id") != declaration.get("task_id"):
        stop("VERIFIED_DELIVERY_TASK_MISMATCH", "receipt task_id does not match the declaration")
        return 0
    failures = common.validate_receipt(
        receipt,
        contract,
        repo_root=root,
        task_root=task_root,
        declaration=declaration,
        lease=lease,
        verify_runtime=True,
        receipt_path=receipt_path,
    )
    if failures:
        reason = ";".join(f"{item['code']}:{item['reason']}" for item in failures)
        stop("VERIFIED_DELIVERY_RECEIPT_REJECTED", reason)
        return 0
    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    raise SystemExit(main())

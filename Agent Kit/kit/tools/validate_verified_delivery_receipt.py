#!/usr/bin/env python3
"""Validate one verified-delivery receipt through the shared strict validator."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


def load_common():
    path = Path(__file__).with_name("validate_verified_delivery_common.py")
    spec = importlib.util.spec_from_file_location("verified_delivery_common", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load shared validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COMMON = load_common()
validate_receipt = COMMON.validate_receipt


def load_json(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True)
    parser.add_argument("--contract")
    parser.add_argument("--repo-root")
    parser.add_argument("--task-root")
    parser.add_argument("--declaration")
    parser.add_argument("--lease")
    parser.add_argument("--receipt-path")
    parser.add_argument("--verify-runtime", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.path).resolve()
    contract = Path(args.contract).resolve() if args.contract else None
    repo_root = Path(args.repo_root).resolve() if args.repo_root else None
    task_root = Path(args.task_root).resolve() if args.task_root else None
    receipt_path = Path(args.receipt_path).resolve() if args.receipt_path else path
    try:
        value = load_json(path)
        if value is None:
            raise ValueError("receipt missing")
        failures = validate_receipt(
            value,
            contract,
            repo_root=repo_root,
            task_root=task_root,
            declaration=(load_json(Path(args.declaration).resolve()) or {}) if args.declaration else {},
            lease=load_json(Path(args.lease).resolve()) if args.lease else None,
            verify_runtime=args.verify_runtime,
            receipt_path=receipt_path,
        )
        result = {"status": "pass" if not failures else "fail", "path": str(path), "failures": failures}
    except Exception as exc:
        result = {"status": "fail", "path": str(path), "failures": [{"code": "LOAD_ERROR", "reason": str(exc)}]}
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.json else None, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

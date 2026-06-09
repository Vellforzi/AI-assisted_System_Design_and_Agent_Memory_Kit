#!/usr/bin/env python3
"""Block likely secrets in files or stdin.

This is an optional example script for hooks/CI/manual checks.
Agent Memory Kit does not require Python.
"""
from __future__ import annotations
import argparse, os, re, sys
from pathlib import Path

PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd|private[_-]?key)\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)postgres(?:ql)?://[^\s]+:[^\s]+@"),
]
EXCLUDE_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.mypy_cache', '.pytest_cache'}
TEXT_EXTS = {'.py', '.md', '.txt', '.yaml', '.yml', '.json', '.toml', '.env', '.ini', '.cfg', '.sql', '.js', '.ts', '.tsx', '.jsx', '.sh', '.ps1'}

def iter_files(paths):
    for p in paths:
        path = Path(p)
        if not path.exists():
            continue
        if path.is_file():
            yield path
        elif path.is_dir():
            for child in path.rglob('*'):
                if any(part in EXCLUDE_DIRS for part in child.parts):
                    continue
                if child.is_file() and (child.suffix.lower() in TEXT_EXTS or child.name.startswith('.env')):
                    yield child

def scan_text(label, text):
    hits = []
    for idx, line in enumerate(text.splitlines(), 1):
        for pat in PATTERNS:
            if pat.search(line):
                hits.append(f"{label}:{idx}: possible secret pattern")
                break
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--paths', nargs='*', default=[])
    ap.add_argument('--stdin', action='store_true')
    args = ap.parse_args()
    hits = []
    if args.stdin:
        hits.extend(scan_text('<stdin>', sys.stdin.read()))
    for f in iter_files(args.paths):
        try:
            hits.extend(scan_text(str(f), f.read_text(encoding='utf-8', errors='ignore')))
        except Exception as exc:
            print(f"WARN: could not read {f}: {exc}", file=sys.stderr)
    if hits:
        print("BLOCKED: possible secrets detected", file=sys.stderr)
        for h in hits[:50]:
            print(h, file=sys.stderr)
        if len(hits) > 50:
            print(f"... {len(hits)-50} more", file=sys.stderr)
        return 2
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Block changed files outside allowed glob patterns.

Optional example script. Agent Memory Kit does not require Python.
"""
from __future__ import annotations
import argparse, os, sys, fnmatch
from pathlib import PurePosixPath

def split_env(value: str) -> list[str]:
    return [x.strip() for x in value.replace('\n', ',').split(',') if x.strip()]

def norm(p: str) -> str:
    return p.replace('\\', '/').lstrip('./')

def match_any(path: str, patterns: list[str]) -> bool:
    path = norm(path)
    for pat in patterns:
        pat = norm(pat)
        if fnmatch.fnmatch(path, pat) or path.startswith(pat.rstrip('/') + '/'):
            return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--allowed', nargs='*', default=[])
    ap.add_argument('--changed', nargs='*', default=[])
    ap.add_argument('--allowed-from-env', default='')
    ap.add_argument('--changed-from-env', default='')
    args = ap.parse_args()
    allowed = list(args.allowed)
    changed = list(args.changed)
    if args.allowed_from_env:
        allowed += split_env(os.environ.get(args.allowed_from_env, ''))
    if args.changed_from_env:
        changed += split_env(os.environ.get(args.changed_from_env, ''))
    if not changed:
        stdin = sys.stdin.read().strip()
        if stdin:
            changed += split_env(stdin)
    if not allowed:
        print('BLOCKED: no allowed scope patterns supplied.', file=sys.stderr)
        return 2
    outside = [p for p in changed if not match_any(p, allowed)]
    if outside:
        print('BLOCKED: changed files outside allowed scope:', file=sys.stderr)
        for p in outside:
            print(f'- {p}', file=sys.stderr)
        print('Allowed patterns:', ', '.join(allowed), file=sys.stderr)
        return 2
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

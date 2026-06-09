#!/usr/bin/env python3
"""Block Project Map writes unless explicitly authorized.

Optional example script. Agent Memory Kit does not require Python.
"""
from __future__ import annotations
import argparse, os, sys

def split(value: str) -> list[str]:
    return [x.strip().replace('\\','/') for x in value.replace('\n', ',').split(',') if x.strip()]

def is_project_map(path: str) -> bool:
    p = path.replace('\\','/').lstrip('./')
    return p.startswith('Project Map/') or p == 'Project Map'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--changed', nargs='*', default=[])
    ap.add_argument('--changed-from-env', default='')
    ap.add_argument('--allow-env', default='AGENT_MEMORY_ALLOW_PROJECT_MAP_WRITE')
    args = ap.parse_args()
    changed = list(args.changed)
    if args.changed_from_env:
        changed += split(os.environ.get(args.changed_from_env, ''))
    if not changed:
        stdin = sys.stdin.read().strip()
        if stdin:
            changed += split(stdin)
    if os.environ.get(args.allow_env, '').lower() in {'1','true','yes','approved','map-apply'}:
        return 0
    pm = [p for p in changed if is_project_map(p)]
    if pm:
        print('BLOCKED: Project Map write requires explicit /map-apply or scoped owner approval.', file=sys.stderr)
        for p in pm:
            print(f'- {p}', file=sys.stderr)
        return 2
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

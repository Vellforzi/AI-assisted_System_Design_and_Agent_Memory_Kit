#!/usr/bin/env python3
"""Block dangerous git commands unless explicitly allowed.

Optional example script. Agent Memory Kit does not require Python.
"""
from __future__ import annotations
import argparse, os, re, sys

DANGEROUS = re.compile(r"(?i)\bgit\s+(push|reset\s+--hard|clean\s+-[fdx]+|rebase|filter-branch|branch\s+-D|checkout\s+--\s+\.|restore\s+\.)\b")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--command', default='')
    ap.add_argument('--allow-env', default='AGENT_MEMORY_ALLOW_GIT_DANGER')
    args = ap.parse_args()
    command = args.command or os.environ.get('COMMAND', '') or sys.stdin.read()
    if os.environ.get(args.allow_env, '').lower() in {'1','true','yes','approved'}:
        return 0
    if DANGEROUS.search(command):
        print('BLOCKED: dangerous git command requires explicit owner approval.', file=sys.stderr)
        print(command[:1000], file=sys.stderr)
        return 2
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

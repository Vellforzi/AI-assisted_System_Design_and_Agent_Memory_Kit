#!/usr/bin/env python3
"""Block likely database write commands or dangerous SQL.

Optional example script. Agent Memory Kit does not require Python.
"""
from __future__ import annotations
import argparse, os, re, sys

DANGEROUS = re.compile(r"(?i)\b(INSERT|UPDATE|DELETE|ALTER|DROP|TRUNCATE|CREATE\s+INDEX|CREATE\s+TABLE|REINDEX|VACUUM\s+FULL|GRANT|REVOKE|alembic\s+upgrade|alembic\s+downgrade|migrate|psql\b|mysql\b)\b")
READONLY_OK = re.compile(r"(?i)\b(SELECT|EXPLAIN|SHOW|DESCRIBE|PRAGMA)\b")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--command', default='')
    ap.add_argument('--allow-env', default='AGENT_MEMORY_ALLOW_DB_WRITE')
    args = ap.parse_args()
    command = args.command or os.environ.get('COMMAND', '') or sys.stdin.read()
    if os.environ.get(args.allow_env, '').lower() in {'1','true','yes','approved'}:
        return 0
    if DANGEROUS.search(command):
        print('BLOCKED: possible DB write or dangerous DB command. Set explicit owner approval and allow env to proceed.', file=sys.stderr)
        print(command[:1000], file=sys.stderr)
        return 2
    return 0
if __name__ == '__main__':
    raise SystemExit(main())

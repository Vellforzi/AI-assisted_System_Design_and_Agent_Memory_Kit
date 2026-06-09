# Codex Scope Control

This directory contains templates and helper scripts for managing `.codex/ALLOWED_SCOPE.txt`.

The owner should not normally edit `ALLOWED_SCOPE.txt` by hand. An agent can update it safely when the owner explicitly requests `/scope-set`, `/scope-reset`, `/apply`, or `/map-apply` and provides or approves the exact write scope.

## Files

- `ALLOWED_SCOPE.safe-default.txt` — generic safe default.
- `ALLOWED_SCOPE.option-profit-default.txt` — OPTION PROFIT safe default.
- `update_allowed_scope.py` — optional helper to set or reset scope.
- `scope_update_request_template.yaml` — structured request template.

## Important

Scope does not authorize action by itself. It only limits writes after the owner has authorized an action.

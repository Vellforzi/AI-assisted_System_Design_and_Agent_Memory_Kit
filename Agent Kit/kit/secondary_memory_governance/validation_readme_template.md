# Validation

Status: Active validation navigation index
Last aligned: <YYYY-MM-DD>
Audience: owner, AI/Codex sessions
Runtime impact: none
Authority: validation routing only; does not imply production behavior

---

## Local Checks

- Context read set: `python scripts/ai_context_helper.py read-set --profile startup --format json`
- Context smoke: `python scripts/ai_context_helper.py smoke-check --format json`
- Documentation harness: `python scripts/documentation_harness.py --format json`

## Evidence Rules

- Record command, date, result, and relevant artifact path.
- Keep raw large outputs out of always-loaded docs; use compact references.
- Do not treat validation artifacts as product truth without source-authority
  promotion.

## Current Status

- Last checked: <YYYY-MM-DD>
- Passing checks: <commands>
- Known failures: <commands or none>

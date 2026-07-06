# Hook Recovery Playbook

Status: generic hook recovery contract
Purpose: make blocking hooks actionable instead of opaque.

---

## Core Rule

A blocking hook should tell the agent what happened, what it will not do, and
the exact safe next action.

Recovery payloads may use either snake_case or camelCase field names. Consumers
should accept both:

- `violation_code` / `violationCode`
- `why_blocked` / `whyBlocked`
- `required_next_response` / `requiredNextResponse`
- `allowed_next_actions` / `allowedNextActions`
- `forbidden_next_actions` / `forbiddenNextActions`
- `playbook`

## Recommended Response Shape

```json
{
  "violationCode": "MISSING_APPLY_SCOPE",
  "whyBlocked": "Changing work was requested without explicit scope.",
  "requiredNextResponse": "Ask for a task contract with Mode, Allowed, Forbidden, Evidence to read, Stop condition, and Verification.",
  "allowedNextActions": ["ask owner for scope", "answer/analyze without mutation"],
  "forbiddenNextActions": ["edit files", "run mutating commands", "infer scope from prior chat"],
  "playbook": "Agent Kit/kit/HOOK_RECOVERY_PLAYBOOK.md"
}
```

## Common Blocks

### Missing Apply Scope

Owner-facing response:

```text
Blocked: changing work was requested without an explicit scope. I need Mode,
Allowed, Forbidden, Evidence to read, Stop condition, and Verification before
editing or executing.
```

### Secret Access

Owner-facing response:

```text
Blocked: potential secret access. I will not read or expose secret values.
Next safe action: provide a sanitized value or approve a current-task credential
allowance with credential, purpose, target, and action.
```

### Project Memory Write

Owner-facing response:

```text
Blocked: durable memory writes need explicit owner approval. I can propose a
memory delta, but I will not write it now.
```

### Recover From Files

Owner-facing response:

```text
HANDOFF CHECKPOINT. Context was compacted. I will not continue from the summary.
Next allowed action: recover from files only. Evidence to read: repository
instructions, current state, working state, source authority, and the active
task contract/result/handoff/log.
```

## Shell Harness Errors

If a check failed because the shell parser, quoting, path splitting, unsupported
option, locale/date parsing, or encoding failed, classify it as
`command_harness_error`. Rewrite the command with a stable pattern before
retrying. Do not report the project check as failed until the command itself
actually ran.

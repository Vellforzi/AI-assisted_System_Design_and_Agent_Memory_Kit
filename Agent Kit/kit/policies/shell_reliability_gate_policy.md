# Shell Reliability Gate Policy (AMK v3.9.6)

## Why this policy exists

Shell-dependent audit and commit workflows become unsafe when command transport is degraded (unknown status, missing output, missing exit code). v3.9.6 treats this as a hard safety boundary.

## Reliability gate

Before any shell-dependent audit/apply/commit verdict, run:

```bash
echo AMK_SHELL_OK; pwd; git rev-parse HEAD
```

The result must include reliable output and exit code.

## Hard-fail conditions

Treat the run as failed (not PASS) when any shell command returns:

- unknown result;
- missing stdout/stderr needed for verification;
- missing exit code;
- transport ambiguity that prevents deterministic interpretation.

When this happens:

1. Stop shell-dependent flow.
2. Report `shell_sandbox_transport_failure`.
3. Do not commit.
4. Do not infer PASS from partial/noisy output.

## Run mode routing

- Preferred recovery route: `Run Mode = Allowlist`.
- Use only explicitly approved commands.
- Do not use Run Everything.

## Scope impact

This policy applies to any task where shell output determines PASS/FAIL, especially:

- git audits;
- diff/stat/check validation;
- commit eligibility checks;
- post-commit verification.

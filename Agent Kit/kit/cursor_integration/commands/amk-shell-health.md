# /amk-shell-health

Run AMK v3.9.6 shell reliability gate before shell-dependent audit/apply/commit steps.

Mode: read-only check by default.

## Command

```bash
echo AMK_SHELL_OK; pwd; git rev-parse HEAD
```

## Pass conditions

- command output is visible and coherent;
- exit code is present and reliable.

## Fail conditions

- unknown shell result;
- missing stdout/stderr needed for interpretation;
- missing exit code.

On fail: report `shell_sandbox_transport_failure`, stop shell-dependent flow, do not mark PASS, do not commit.

Preferred route after fail: Run Mode `Allowlist` with explicit commands.

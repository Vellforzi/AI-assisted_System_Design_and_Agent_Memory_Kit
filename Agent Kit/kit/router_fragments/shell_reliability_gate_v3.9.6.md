## Shell reliability gate (v3.9.6)

When task correctness depends on shell output (audit/apply/commit):

1. Run health check first: `echo AMK_SHELL_OK; pwd; git rev-parse HEAD`.
2. Require reliable stdout/stderr and exit code.
3. Treat unknown/no-output/no-exit-code as hard failure (not PASS).
4. Report `shell_sandbox_transport_failure` when sandbox transport is unreliable.
5. Route to `Run Mode: Allowlist` with explicit command allowlist.
6. Do not use Run Everything.
7. Do not proceed to commit while shell reliability is unresolved.

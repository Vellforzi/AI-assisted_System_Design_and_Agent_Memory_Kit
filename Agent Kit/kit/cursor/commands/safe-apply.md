# /safe-apply

Purpose: check whether a requested mutation is safe to start.

Mode: analyze
Mutations: forbidden by this command; it only gates a later apply.

Check:

- explicit owner apply intent;
- exact target and write scope;
- allowed and forbidden paths/actions;
- verification method;
- product code gate if applicable;
- DB/deploy/git/external side-effect approval;
- secrets exclusion;
- branch/checkpoint lineage;
- side-effect receipts / idempotency;
- implicit IDE context is not being used to expand write scope without owner approval.

Output:

```text
Safe apply gate: green|amber|red|blocked
Missing:
Blockers:
Allowed scope:
Forbidden:
Verification:
Next safe action:
```

Do not perform the apply step from this command.

# /amk-session-close

Prepare AMK session close / checkpoint material.

Mode: read-only summary unless the owner explicitly requests Project Map apply.

Output sections:

1. Completed work.
2. Verification performed.
3. Open risks / missing evidence.
4. Proposed `docs/WORKLOG.md` entry.
5. Proposed Project Map delta, clearly marked as proposed only.
6. Eval trigger: yes/no and reason.

Do not write Project Map or worklog unless the owner explicitly authorizes apply mode.

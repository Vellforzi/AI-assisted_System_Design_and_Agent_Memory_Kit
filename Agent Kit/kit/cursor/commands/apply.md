# /apply

Purpose: perform one bounded change.

Mode: apply
Mutations: allowed only inside explicit scope

Before acting, verify that the owner provided:

- target;
- exact scope;
- allowed files/actions;
- forbidden files/actions;
- verification method.

If scope is missing or ambiguous, stop and ask for clarification.

After work:

- summarize diff;
- report verification;
- state whether Project Map delta is needed;
- state whether checkpoint/handoff is recommended;
- state Eval trigger yes/no.

Do not push, deploy, write DB, touch secrets, or update unrelated files unless explicitly authorized.

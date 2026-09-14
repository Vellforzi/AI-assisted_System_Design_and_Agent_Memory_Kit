# Optional capabilities

The short workflow is sufficient for ordinary work. Add only what has a
specific use in the adopting project; record the decision in project context.

| Capability | Use when | What to verify |
|---|---|---|
| Durable task recovery | Work may cross restarts or compaction | Exact session/task identity and source state |
| Stronger delivery proof | A failure is hard to reproduce or affects critical behavior | Production-linked checks and explicit evidence limits |
| Action hooks | Repeated concrete mistakes justify automation | Native event schema, cwd, activation, ordinary allow and boundary deny |
| Eval scenarios | A repeated agent failure needs measurement | Actual captured behavior; a schema check is not a model score |
| Evidence connector | Relevant evidence cannot be read conveniently | Repository identity, read-only surface and unavailable-source behavior |
| Delegation or orchestration | A bounded task has a concrete benefit | Owner constraints, exact scope, independent result verification |

The larger Kit repository includes reference material for these capabilities.
Those guides are not an instruction to install all of them. Provider models,
pricing and client features change; verify their current official sources.
Project-specific settings and history belong to the adopting project.

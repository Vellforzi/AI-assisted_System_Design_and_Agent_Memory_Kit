# Plain-Language Glossary

Status: reader support document  
Purpose: explain common terms in simple language.

---

| Term | Plain meaning |
|---|---|
| Agent | The AI system acting through a chat, IDE, tools, or scripts. It is the worker, not the source of project truth. |
| Owner | The human who controls the project and decides what is true, allowed, and useful. |
| Project Map | The external memory folder for the project: current state, decisions, facts, tasks, risks, source authority, and handoffs. |
| Memory card | A small durable record: one fact, decision, constraint, risk, question, or note with evidence and lifecycle state. |
| Durable memory | Information meant to survive beyond the current chat. |
| Working state | The compact "where are we now" state used to resume work without reading the whole transcript. |
| Checkpoint | A safe stopping point with enough state to continue later. |
| Significant work | Work that changed or discovered something future sessions should know. |
| Source authority | The rule that says which source wins when sources disagree. Example: current code may beat old notes. |
| Grounding | The rule that project claims must be supported by project evidence, not model guesses. |
| Retrieval | Reading the relevant memory or files needed for the current answer. |
| Retrieval profile | A named retrieval mode. Example: answer mode reads current facts; audit mode may also read stale history. |
| Stale fact | An old fact that may be historically useful but must not be treated as current truth. |
| Superseded fact | A fact replaced by a newer verified fact or decision. |
| Action intent | What the owner is asking for now: answer, analyze, plan, stage, apply, or research. |
| Permission mode | What access is allowed: explain-only, read-only, dry-run, or apply. Permission does not create intent. |
| Mutation | Any change to files, memory, git state, database, deployment, external systems, or durable project state. |
| Side effect | A change outside the model response: file write, command, API call, database action, deployment, message, purchase. |
| Eval | A test case for agent behavior. It checks whether the agent followed the rules. |
| Eval-suite | A set of eval cases that check important behavior categories. |
| Grader | The checker that decides whether an eval passed. It may be code-based, model-based, or human. |
| Deterministic grader | A strict checker, usually code or exact rules. Fast and repeatable. |
| Model-based grader | Another model checks the answer using a rubric. More flexible but less stable. |
| Human review | The owner or expert checks the result. Slower, but often most reliable. |
| Harness | The runner that feeds eval prompts to an agent, captures output/tool calls, and grades results. |
| Trace | A record of what happened during an eval or task: prompt, answer, tool calls, observed outcome. |
| Provider memory | Memory stored by the AI service itself. Useful for personalization, not authoritative project truth. |
| External research | Web/docs/public sources retrieved for general knowledge. Not project truth unless owner promotes it. |
| Handoff | A short package for continuing a task in a new session. |
| Long-running task | A task that spans many steps, sessions, or autonomous runs. It needs a task contract and checkpoints. |

---

## Additional v3.8 terms

## Additional v4.0 terms

- **Commitment** — a pre-action record connecting a goal and retrieved context to a planned action and expected outcome.
- **Settlement** — immutable terminal evidence that a commitment succeeded, failed, or was cancelled.
- **Verification receipt** — a structured record of a deterministic check supporting one or more claims.
- **Context budget** — explicit source/token limits applied before assembling context.
- **Progressive disclosure** — metadata-first access followed by bounded excerpts and explicit full loading.
- **Policy canary** — an offline baseline/candidate comparison proposal; this Kit never sends live traffic.

## Additional v5.0 terms

- **Workflow profile** — the TaskContractV3 classification that activates only the contracts relevant to a task.
- **Work-item graph** — vertical, independently verifiable work connected by blockers; its frontier is calculated, not scheduled.
- **Plan challenge** — an owner decision gate that keeps only one unresolved question active at once.
- **Fresh-context review** — result review without the author's reasoning history or mutation authority.
- **Exploration map** — a bounded map of destination, decisions, fog, and investigations that cannot mutate the product.
- **Design probe** — a disposable isolated artifact answering one design question; production reuse is forbidden.
- **Capability assessment** — an append-only observation of capability health; passing requires end-to-end evidence.
- **Bounded context** — a domain boundary within which terms have canonical meanings.

### Workspace

The folder or workspace file the IDE opens. It defines what the agent can see as the current project area. It is not the same as permission.

### Permission profile

A Codex access profile such as `:read-only` or `:workspace`. It controls what local actions Codex can perform.

### Sandbox

A technical access boundary around tool execution. In this kit, the recommended Codex default is the built-in permission profile `:read-only`; no separate sandbox installation is needed for the basic workflow.

### Allowed scope

A task-level whitelist of paths an agent may write during an approved apply task. It limits an already-approved action; it does not authorize action by itself.

### Scope reset

Returning the allowed write scope to a safe default after a task ends.

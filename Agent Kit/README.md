# Agent Memory Kit

Version: v3.12.1

Agent Memory Kit is the project-memory and agent-behavior layer of the package.

It helps a project owner maintain a structured Project Map containing:

- current state;
- working state;
- source authority;
- permissions policy;
- retrieval policy;
- decisions;
- facts;
- constraints;
- risks;
- open questions;
- task contracts;
- handoffs;
- claim ledgers;
- eval cases and eval run notes.

---

## Start here

1. `kit/MOTIVE_AND_ANALOGY.md`
2. `kit/QUESTIONS_THIS_KIT_ANSWERS.md`
3. `START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md`
4. `kit/README.md`
5. `kit/OWNER_USAGE_GUIDE.md`
6. `kit/CAPABILITY_MANAGEMENT.md`
7. `kit/BEHAVIORAL_ORACLES.md`
8. `kit/PROPOSED_SPECIALIST_FUNCTIONS.md`
9. `kit/SCHEMES_AND_COVERAGE_ATLAS.md`
10. `kit/WORKING_METHOD_CATALOG.md`
11. `kit/CONSTRAINT_CATALOG.md`
12. `kit/proposed_hooks/README.md`
13. `kit/PROJECT_MEMORY_STORAGE_GUIDE.md`
14. `kit/ACTION_INTENT_CONTRACT.md`
15. `kit/SIGNIFICANT_WORK_AND_CHECKPOINTS.md`
16. `kit/EVAL_SUITE_GUIDE.md`
17. `kit/EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`
18. `kit/SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`
19. `kit/WORKSPACE_SELECTION_GUIDE.md`
20. `kit/CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`
21. `kit/AI_AGENT_ROLE_STACK_GUIDE.md`
22. `kit/EXECUTOR_ROUTING_GATE.md`
23. `kit/EXECUTION_PROFILE_GATE.md`
24. `kit/VERIFIED_DELIVERY_PIPELINE.md`
25. `kit/WINDOWS_ENCODING_AND_SHELL_HYGIENE.md`
26. `kit/HOOK_RECOVERY_PLAYBOOK.md`
27. `kit/CODEX_CONNECTOR_POLICY.md`
28. `kit/GENERATED_RETRIEVAL_EVIDENCE_GUIDE.md`
29. `kit/CURSOR_INTEGRATION_OWNER_GUIDE.md`
30. `kit/codex/README.md`

---

## Default behavior

The agent must answer only unless the owner explicitly asks for a concrete action. Reading memory for context is not the same as permission to modify memory, files, database state, git state, cloud resources, or external systems.

After meaningful work, the agent may propose a Project Map delta and identify whether evals should run. It must not apply memory or rule changes unless the owner explicitly asks.

---

## Use in a repository

Use `kit/AGENT_INSTRUCTION_FILES_GUIDE.md` and `kit/AGENTS.md_TEMPLATE.md` to create a short root instruction file for repository-aware coding agents.

Use `kit/CURSOR_RULE_TEMPLATE.mdc` for Cursor projects.

Do not commit private local preferences, secrets, credentials, raw personal data, or provider-specific session dumps.

---

## Positioning

Agent Memory Kit is useful when the owner wants a visible, editable, portable project memory rather than hidden provider memory or a loose chat summary.

It is not a full agent runtime. It can later be implemented through a memory framework, vector store, knowledge graph, IDE hook, eval harness, or agent platform, but the core value is the operating contract: what counts as project truth, what may be remembered, when the agent may act, and how failures become eval cases.
---

## Cursor, Codex, and GPT role stack

Recommended default:

```text
Cursor/Composer = strong scoped implementation executor; ChatGPT Codex may also execute when task evidence makes it the best or an equally good route
ChatGPT Codex = ChatGPT desktop app in Codex mode for analysis, planning, task contracts, review, evidence verification, and controlled repair/recovery
GPT web chat = research, design, and task specs
Project Map = shared project truth
```

Use one shared workspace root when one Project Map governs multiple components. Use task scope and permission gates for safety.



## v3.8 Cursor settings and workspace authority

This release adds an owner-controlled Cursor Agent settings profile, `.cursorignore` guidance, settings audit commands, and the rule that an existing authoritative workspace file must be inspected and used rather than replaced by a generated fallback.

## v3.12.1 focus

Adds `ORCHESTRATION_CHOICE.md`: the kit during orchestration; offer the host
Agents window before building a custom queue/App Server host.

## v3.12.0 focus

Adds the portable execution runtime: Execution Profile Gate, path/toolchain/scope
templates, CAS write lock, verified-delivery pipeline, Windows command-launch
hygiene, and matching evals. Does not include private product evals or App
Server controllers.

## v3.11.3 focus

Adds the capability-management guide layer: FAQ, motive, behavioral oracles,
schemes as a method to offer, numbered CN facts, combat-method hook cards
with example bytes, specialist function cards, and eval `AMK-CM-001`.
Did not include the execution runtime (added in v3.12.0).

## v3.11.2 patch focus

Normalizes current release-facing package and eval metadata after the v3.11.1
publication. Routing behavior, provider snapshots, policies, tools, and eval
cases are unchanged.

## v3.11.1 focus

Adds source-qualified GPT-5.6 Codex routing with Luna/Terra/Sol task classes,
Max/Ultra/Cursor-Max separation, Fast evidence-conflict handling, current
ChatGPT desktop Codex plus distinct IDE/CLI/web surface naming, stale Cursor
evidence guards, and routing/label behavior evals.

## v3.11.0 focus

Adds generic operational hardening:

- Executor Routing Gate and validator.
- Windows encoding and shell hygiene.
- Hook recovery payload compatibility.
- Connector side-effect policy.
- Generated retrieval evidence boundary.
- Eval coverage for these behaviors.

## v3.10.0 focus

Adds the local deterministic ChatGPT Project sources manifest workflow and
`AMK-GPS-001`.

## v3.9.4 focus

Adds eval parity, live Cursor adoption checks, and explicit model-escalation triggers. Start with the lowest sufficient route and escalate only after reporting a concrete trigger (validation failure, schema/router conflict, insufficient context window, missing model control, repeated scoped failure, or task reclassification to audit/repair/protocol design).

## v3.9.4 Cursor provider model snapshot

v3.9.4 keeps dated Cursor model-routing snapshots as volatile capability observations. Exact Cursor model/settings advice must show snapshot date/ref and must not treat provider/model data as permanent project truth.

## v3.9.4

Adds stale-mirror eval-suite authority checks and live `.cursor` adoption guidance for rules and commands.

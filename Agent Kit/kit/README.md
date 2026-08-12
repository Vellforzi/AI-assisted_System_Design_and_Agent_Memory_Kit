# Agent Memory Kit Starter Package

Version: v3.12.1
Release metadata date: 2026-08-13
Publication proof: matching repository tag and release receipts; this file alone is not proof

Agent Memory Kit is a portable memory operating layer for project owners who work with AI agents across long projects.

The standing motive: you lay your knowledge and method out at the physical
level (folders, files, schemes, gates). The more accurately you do that,
the more accurately a capable agent looks like you — a copy that does not
forget and does not get confused. Sub-agents multiply that copy. The tool
is for models that can use the layout. See `MOTIVE_AND_ANALOGY.md`.

Its purpose is structured, meaningful, interconnected duplication of owner-provided and project-verified information so the project is less vulnerable to:

- context loss;
- confusion between old and new facts;
- forgotten decisions;
- false assumptions;
- ungrounded project answers;
- accidental execution when the owner only asked a question;
- overloading the model with irrelevant context;
- treating generic model knowledge as project truth;
- forgetting to convert repeated agent failures into eval cases;
- wrong scope/model/settings choices before heavy agent work.

---

## Core rules

### 1. Grounding

For project-specific claims, the agent must use only:

1. current user input;
2. Project Map memory;
3. project files or tool outputs opened in the current run;
4. external sources explicitly retrieved in the current run and valid for the claim type;
5. owner-approved durable memory.

If evidence is missing, the agent must not guess.

Generic model knowledge may support general reasoning and language, but it is not evidence for the owner's project.

### 2. Action intent

Answer-only is the default intent.

If the owner asks a question, requests analysis, asks for a review, or asks what should be done, the agent must answer, analyze, or propose. It must not perform mutating actions unless the owner explicitly asks for an action with target, mode, and scope.

Read-only memory/context intake is allowed only within granted scope. It must not become implementation.

### 3. Significant work and checkpoints

After meaningful project work, the agent should detect whether a Project Map update, handoff, checkpoint, or eval trigger should be proposed.

It must not apply memory or rule changes unless the owner explicitly asks.

### 4. Evals

Evals are behavior checks, not intelligence tests. They help detect regressions in action intent, grounding, retrieval, memory compilation, side-effect safety, and owner control.

Evals do not run automatically unless the owner wires them to a script, hook, CI job, API harness, or agent runtime.

---

## What is included

| File | Purpose |
|---|---|
| `MOTIVE_AND_ANALOGY.md` | Standing analogy: lay your consciousness on disk; a capable model looks like you. |
| `OWNER_USAGE_GUIDE.md` | Day-to-day owner workflow and safe prompts. |
| `QUESTIONS_THIS_KIT_ANSWERS.md` | What the kit is, why it exists, capabilities, Cursor/Codex setup. |
| `CAPABILITY_MANAGEMENT.md` | Output quality is a constraint contour, not model IQ. |
| `BEHAVIORAL_ORACLES.md` | Confidence without reading every line: oracles, pins, owner smoke. |
| `PROPOSED_SPECIALIST_FUNCTIONS.md` | How to create limited specialist agents; copy the method, not a private roster. |
| `SCHEMES_AND_COVERAGE_ATLAS.md` | Offer schemes: cheap, accurate, human+agent readable. Not a replacement for the rest. |
| `WORKING_METHOD_CATALOG.md` | Catalog of the rest of the working method (smoke, contract, modes, locks). |
| `ORCHESTRATION_CHOICE.md` | How the kit is used during orchestration; offer host UI vs a custom queue host. |
| `CONSTRAINT_CATALOG.md` | Numbered CN facts: retrieve by id; product CNs stay in the adopting project. |
| `proposed_hooks/` | Combat-method hook cards and example bytes (wrapper, contract, profile, finalization, encoding). |
| `coverage_atlas/` | Scheme template and a generic example. |
| `PLATFORM_CONTEXT_COMPACTION_BOUNDARY.md` | Platform summaries, compacted chat history, and provider memory are non-authoritative hints, not project truth. |
| `CURSOR_INTEGRATION_OWNER_GUIDE.md` | How to use the kit with Cursor Rules, Commands, Skills, Subagents, and Hooks. |
| `cursor/` | Cursor Integration Pack: rules, commands, skills, read-only subagents, and optional hook examples. |
| `ACTION_INTENT_CONTRACT.md` | Default answer-only behavior and explicit-action gate. |
| `SIGNIFICANT_WORK_AND_CHECKPOINTS.md` | Defines meaningful work, checkpoints, Project Map delta proposals, and eval triggers. |
| `PROJECT_GROUNDING_CONTRACT.md` | Strict evidence contract for project-specific claims. |
| `CONTEXT_SCOPE_MODEL_ADVISOR.md` | Pre-hydration advisor for context, scope, model/settings, and token/fuel use. |
| `CONTEXT_ADVISOR_TEMPLATE.yaml` | Machine-readable advisor policy template for projects. |
| `PROVIDER_CAPABILITY_SNAPSHOT_TEMPLATE.yaml` | Template for volatile model/provider capability snapshots. |
| `context_advisor/` | Profile matrix, hint policy, TypeScript contract, example run, current Codex/provider-surface snapshots, and provider snapshot example. |
| `PROJECT_MEMORY_OPERATING_PROTOCOL.md` | Runtime behavior for memory intake, grounded answers, memory updates, checkpoints, and eval review. |
| `PROJECT_MEMORY_STORAGE_GUIDE.md` | File-based Project Map structure and memory lifecycle. |
| `SOURCE_AUTHORITY_TEMPLATE.yaml` | Machine-readable source authority template. |
| `PERMISSIONS_POLICY_TEMPLATE.yaml` | Machine-readable permission and action-intent policy template. |
| `RETRIEVAL_POLICY_TEMPLATE.yaml` | Machine-readable retrieval profile template. |
| `TASK_CONTRACT_TEMPLATE.yaml` | Long-task contract template. |
| `EXECUTOR_ROUTING_GATE.md` | Evidence-based executor/service routing gate for non-trivial contracts and bootstraps. |
| `EXECUTION_PROFILE_GATE.md` | Unique mode + task class + path zone route, toolchain, and write lock. |
| `PATH_ZONES_TEMPLATE.yaml` | Path-zone registry template (most-specific match, fail closed). |
| `AGENT_EXECUTION_PROFILES_TEMPLATE.yaml` | Execution-profile registry template. |
| `SCOPE_PROFILES_TEMPLATE.yaml` | Scope/lease profile template. |
| `WINDOWS_TOOLCHAIN_PROFILE_TEMPLATE.yaml` | Registered launcher/toolchain template. |
| `VERIFIED_DELIVERY_PIPELINE.md` | Conditional verified-delivery inspect/repair/oracle loop. |
| `WINDOWS_ENCODING_AND_SHELL_HYGIENE.md` | Byte-safe file mutation and readback guide for Windows and non-ASCII text. |
| `HOOK_RECOVERY_PLAYBOOK.md` | Generic recovery field contract for blocking hooks. |
| `CODEX_CONNECTOR_POLICY.md` | Connector read/write scope, draft-first outbound workflow, and receipt policy. |
| `GENERATED_RETRIEVAL_EVIDENCE_GUIDE.md` | Generated search/index output boundary and canonical re-read rule. |
| `CLAIM_LEDGER_TEMPLATE.yaml` | Claim support and final-answer gate template. |
| `HANDOFF_TEMPLATE.yaml` | Clean-slate handoff packet template. |
| `LONG_RUNNING_TASKS_GUIDE.md` | Design guide for long tasks without simulating consciousness. |
| `MEMORY_SCHEMA_REFERENCE.yaml` | Canonical schema reference for memory units and indexes. |
| `memory_card_examples.yaml` | Copyable examples of decisions, facts, constraints, risks, questions, and stale facts. |
| `RETRIEVAL_POLICY_PROFILES.md` | Retrieval behavior for answer, analyze, plan, resume, recover, fork, audit, and repair modes. |
| `WORKING_STATE_AND_REPLAY_GUIDE.md` | Working State as compact replay root. |
| `MEMORY_COMPILER_GUIDE.md` | Session-to-memory consolidation process. |
| `MEMORY_TOOL_INTERFACE_CONTRACT.md` | Expected behavior for a memory tool or memory API. |
| `PROVIDER_MEMORY_AND_RUNTIME_BOUNDARY.md` | Boundary between Project Map, provider memory, runtime state, and external research. |
| `SERVICE_RULE_PLACEMENT_GUIDE.md` | Where to place global rules vs project-specific memory in AI services. |
| `START_MESSAGE_TEMPLATES.md` | Reusable owner messages for safe starts and continuations. |
| `PROJECT_WORKSPACE_LAYOUT.md` | Recommended folder roles and layout. |
| `MANUAL_OWNER_REVIEW_CHECKLIST.md` | Manual review checklist that complements evals. |
| `EVAL_SUITE_GUIDE.md` | How to run the portable eval-suite. |
| `EVAL_AUTOMATION_AND_TRIGGER_POLICY.md` | Eval automation levels, trigger matrix, and repair loop. |
| `eval_suite/` | Core behavior eval cases, trigger policy, grader rubric, run report template, and trace template. |
| `tools/` | Optional local helper scripts. |
| `tools/verify_executor_routing_gate.py` | Validates Executor Routing Gate blocks in task contracts/bootstrap artifacts. |
| `CHATGPT_PROJECT_SOURCES_WORKFLOW.md` | Generate ChatGPT Project sources manifest and owner TODO (local, deterministic). |
| `CHATGPT_PROJECT_SOURCES_CONFIG.template.json` | Project config template for the sources generator. |
| `PROJECT_GPT_OPERATING_CONTRACT.template.md` | GPT operating contract template for project sources. |
| `GPT_PROJECT_INSTRUCTIONS_COMPACT.template.md` | Compact ChatGPT Project Instructions template (manual UI paste). |
| `policies/chatgpt_project_sources_policy.md` | Policy for ChatGPT Project sources maintenance. |
| `SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md` | How agents should manage `.codex/ALLOWED_SCOPE.txt` without forcing the owner to edit it manually. |
| `CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md` | Plain explanation of Codex permission profiles, sandbox terminology, and safe defaults. |
| `WORKSPACE_SELECTION_GUIDE.md` | How to choose IDE workspaces for single-root and multi-component projects. |
| `AI_AGENT_ROLE_STACK_GUIDE.md` | Default split: Cursor implements, Codex reviews, GPT researches, Project Map stores truth. |
| `HOOK_REQUEST_WORKFLOW.md` | How an agent should respond when the owner asks for hooks. |
| `HOOK_GENERATION_QUESTIONS.md` | Minimal questions to ask before generating hooks. |
| `HOOK_PACKAGING_GUIDE.md` | How to package project-local hook bundles. |
| `CURSOR_AGENT_SETTINGS_GUIDE.md` | Recommended Cursor Agent settings for owner-controlled work. |
| `CURSORIGNORE_AND_CONTEXT_BOUNDARY_GUIDE.md` | How to use `.cursorignore` without hiding project truth. |
| `cursor/CURSOR_OWNER_CONTROLLED_DEFAULTS.md` | Cursor settings profile summary. |
| `cursor/settings/owner_controlled_profile.yaml` | Machine-readable owner-controlled Cursor settings profile. |

| `EXISTING_PROJECT_ADOPTION_GUIDE.md` | How to adopt the kit in an already active project. |
| `NEW_PROJECT_ADOPTION_GUIDE.md` | How to start an empty project with the kit. |
| `SOLO_OWNER_WORKFLOW_GUIDE.md` | High-control workflow for a solo owner using local IDE agents plus research chat. |
| `AGENT_INSTRUCTION_FILES_GUIDE.md` | How to connect the kit to AGENTS.md, Cursor rules, CLAUDE.md, and similar files. |
| `AGENTS.md_TEMPLATE.md` | Root repository instruction template. |
| `CURSOR_RULE_TEMPLATE.mdc` | Cursor rule template. |
| `POSITIONING_AND_ALTERNATIVES.md` | How the kit differs from provider memory, vector stores, agent runtimes, and open-source memory frameworks. |
| `PLAIN_LANGUAGE_GLOSSARY.md` | Simple explanations of common terms. |
| `README_AUTHORING_GUIDE.md` | Concise README structure for publishing the toolkit. |
| `GIT_PUBLISHING_GUIDE.md` | Repository hygiene and safe publishing guide. |
| `RESEARCH_BASIS.md` | Research and engineering basis used for this release. |

---

## Eval-suite

Use `EVAL_SUITE_GUIDE.md`, `EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`, and `eval_suite/` to check whether an agent actually follows the kit.

The suite is intentionally small and failure-mode based. It is designed for manual or semi-automated use by a project owner. It should be copied into `Project Map/eval_suite/` when a project starts using the kit.

v3.12.0 adds the execution runtime (Execution Profile Gate, registries,
write lock, verified delivery, command-launch hygiene). v3.11.3 adds the FAQ/thesis/oracle/scheme/CN/hook guides and eval
`AMK-CM-001`. v3.11.2 normalizes current release-facing package and eval metadata without
changing behavior. v3.11.1 adds GPT-5.6 model-routing and exact-label evals,
while v3.11.0 adds
eval cases for executor routing gates, Windows encoding hygiene,
hook recovery payloads, connector side-effect policy, and generated retrieval
evidence.

Optional checklist helper:

```bash
python3 "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Project Map/eval_suite/core_behavior_eval_cases.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```

---

## How to start

The owner provides:

- where `Agent Kit/` is unpacked;
- where the project is or should be located;
- where `Project Map/` is or should be located;
- where project materials live;
- a free-form explanation of the project;
- the current permission mode;
- the exact scope for any read/write action.

For command execution, the owner must also provide OS, shell/runtime, tools, stack, and versions when relevant.

---

## Continuation rule

A later work session should continue from documented Project Map state, not from undocumented chat memory.

Use:

1. `Project Map/current_state.md`
2. `Project Map/working_state.yaml`
3. `Project Map/tasks/<active-task>.yaml` if present
4. active workstream file
5. relevant memory cards
6. latest handoff packet if resuming or recovering
7. raw sources only when necessary

---

## Recommended service setup

Put the short runtime-core rules in service-level instructions. Keep project-specific facts in `Project Map/`.

Do not put the only copy of project knowledge into ChatGPT Custom Instructions, Cursor Personal Rules, Claude Project Instructions, or another service-specific prompt.


---

## Cursor Integration Pack

Use `cursor/` to install small, explicit Cursor building blocks instead of pasting the whole kit into one prompt.

Recommended minimum:

- Rules: core memory rule, platform context boundary, safety defaults.
- Commands: `/answer`, `/plan`, `/apply`, `/checkpoint`, `/handoff`, `/map-apply`, `/recover`, `/eval-smoke`.
- Hooks: start as warnings, then block secrets, DB writes, dangerous git commands, out-of-scope edits, and unauthorized Project Map writes.

See `CURSOR_INTEGRATION_OWNER_GUIDE.md` and `cursor/README.md`.

---

## Python is not required

Agent Memory Kit is language-agnostic and file-based. Python helper scripts are optional examples only. They are included because the original owner works in Python. Replace them with another language if that fits your project better.


---

## Codex integration

This release includes a Codex Integration Pack under `codex/`. It provides:

- recommended Codex settings;
- `config.toml` templates;
- custom instructions;
- global and project `AGENTS.md` examples;
- hook setup guide and optional hook scripts;
- Skills and read-only Subagent templates;
- a Cursor + Codex workflow.

Use Codex as an independent reviewer, auditor, recovery assistant, or controlled executor. Do not use Codex memory, platform summaries, or compressed chat as project truth.

## v3.9.4 focus

v3.9.4 adds eval-suite parity checks, live `.cursor` adoption verification, and explicit model escalation wording. Start with the lowest sufficient model/settings class and escalate only after reporting a concrete trigger (validation failure, schema/router conflict, insufficient context window, missing model control, repeated scoped failure, or task reclassification to audit/repair/protocol design).


## Context Advisor

Use `CONTEXT_SCOPE_MODEL_ADVISOR.md` and `context_advisor/` when a task may be under-scoped, over-scoped, or dependent on model/provider settings.

Compact owner commands:

```text
settings?   explain surface/model/reasoning/speed/context choice, cost class, escalation trigger, and cheaper alternative
scope?      list mandatory/recommended/optional/forbidden context
fuel?       show keep/defer/drop and Max/IDE context advice
safe apply? check mutation gate before edits
```

Optional helper:

```bash
python3 "Agent Kit/kit/tools/context_advisor_preflight.py" \
  --intent apply \
  --have project_map_core,source_authority,active_workstream,tests \
  --scope "Options_api/app/routes/example.py" \
  --owner-ok \
  --verification "pytest"
```

## v3.9.4 Cursor provider model snapshot

v3.9.4 keeps dated Cursor model-routing snapshots as volatile capability observations. Exact Cursor model/settings advice must show snapshot date/ref and must not treat provider/model data as permanent project truth.

## v3.9.4 model/surface routing

Adds explicit escalation-trigger routing and stale-mirror evaluation authority checks for kit/project-map parity.

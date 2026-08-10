# Agent Memory Kit Starter Package

Version: v5.0.0
Status: portable project-owner toolkit
Last aligned: 2026-08-07
Audience: project owners, adopters, and maintainers
Runtime impact: none until explicitly adopted
Authority: navigation index; operational project evidence and owner instructions remain authoritative
Release date: 2026-06-09  
Package: `AI-assisted_System_Design_and_Agent_Memory_Kit_v5.0.0_EN.zip`

Agent Memory Kit is a portable memory operating layer for project owners who work with AI agents across long projects.

## Adoption profiles

Read `ADOPTION_PROFILES.md` before selecting material from this directory.

- **Core** is a genuinely small, useful, dependency-free operating layer:
  grounding, explicit action approval, and ordinary durable project notes. It
  requires no Project Map, Python, evals, task contracts, `.work`, generated
  projections, hooks, CI, or MkDocs.
- **Standard** adds `secondary_memory_governance/` only when repeated sessions,
  contributors, or a documented context-selection error need bounded routing.
- **Workflow** adds only the particular v5 artifact activated by task scale,
  risk, review/dependency need, or `TaskContractV3.workflow_profile`.
- **Reference Lab** is for explicitly owned optional evals, helpers,
  integrations, hooks, CI, or MkDocs work.

The presence of a mechanism in the Kit is not a recommendation to install it.
Greenfield removes migration cost, not operating cost. Optional artifacts
require observable activation triggers, a named purpose, and an owner. For an
existing project, preserve source authority: when Project Map is
`secondary_memory`, operational docs, code, tests, specs, issues, and current
owner instructions win. Context Contract V1 remains a compatible read-only
projection, and v5 contracts retain their existing schema and migration
boundaries.

Its purpose is structured, meaningful, interconnected duplication of owner-provided and project-verified information so the project is less vulnerable to:

- context loss;
- confusion between old and new facts;
- forgotten decisions;
- false assumptions;
- ungrounded project answers;
- accidental execution when the owner only asked a question;
- overloading the model with irrelevant context;
- treating generic model knowledge as project truth;
- forgetting to convert repeated agent failures into eval cases.

---

## Operating rules for any adopted profile

### 1. Grounding

For project-specific claims, the agent must use only sources allowed by the
project's `source_authority.yaml` or equivalent source-of-truth hierarchy:

1. current user input;
2. Project Map memory only in its declared authority role;
3. project files or tool outputs opened in the current run;
4. external sources explicitly retrieved in the current run and valid for the claim type;
5. owner-approved durable memory.

If Project Map is `secondary_memory`, it summarizes and navigates; operational
docs, code, tests, specs, issues, and current owner instructions win.

If evidence is missing, the agent must not guess.

Generic model knowledge may support general reasoning and language, but it is not evidence for the owner's project.

### 2. Action intent

Answer-only is the default intent.

If the owner asks a question, requests analysis, asks for a review, or asks what should be done, the agent must answer, analyze, or propose. It must not perform mutating actions unless the owner explicitly asks for an action with target, mode, and scope.

Read-only memory/context intake is allowed only within granted scope. It must not become implementation.

### 3. Significant work and checkpoints

After meaningful project work, the agent should detect whether a Project Map update, handoff, checkpoint, or eval trigger should be proposed.

It must not apply memory or rule changes unless the owner explicitly asks.

### 4. Evals when activated

Evals are behavior checks, not intelligence tests. Adopt them in Reference Lab
only when a repeated or material failure mode has a concrete behavior to
check. They help detect regressions in action intent, grounding, retrieval,
memory compilation, side-effect safety, and owner control.

Evals do not run automatically unless the owner wires them to a script, CI job, API harness, or agent runtime.

---

## What is included

| File | Purpose |
|---|---|
| `OWNER_USAGE_GUIDE.md` | Day-to-day owner workflow and safe prompts. |
| `secondary_memory_governance/` | Single repo-centric secondary-memory governance baseline: secondary Project Map, operational source authority, context index, receipts, smoke checks, and documentation harnesses. |
| `optional_integrations/` | Optional modules for ChatGPT Project sources, cost/model routing, Cursor settings, and owner-adopted documentation governance. They do not change core behavior or the baseline. |
| `PLATFORM_CONTEXT_COMPACTION_BOUNDARY.md` | Platform summaries, compacted chat history, and provider memory are non-authoritative hints, not project truth. |
| `CURSOR_INTEGRATION_OWNER_GUIDE.md` | How to use the kit with Cursor Rules, Commands, Skills, and Subagents. |
| `cursor/` | Cursor Integration Pack: rules, commands, skills, and read-only subagents. |
| `ACTION_INTENT_CONTRACT.md` | Default answer-only behavior and explicit-action gate. |
| `SIGNIFICANT_WORK_AND_CHECKPOINTS.md` | Defines meaningful work, checkpoints, Project Map delta proposals, and eval triggers. |
| `PROJECT_GROUNDING_CONTRACT.md` | Strict evidence contract for project-specific claims. |
| `PROJECT_MEMORY_OPERATING_PROTOCOL.md` | Runtime behavior for memory intake, grounded answers, memory updates, checkpoints, and eval review. |
| `PROJECT_MEMORY_STORAGE_GUIDE.md` | File-based Project Map structure and memory lifecycle. |
| `SOURCE_AUTHORITY_TEMPLATE.yaml` | Machine-readable source authority template. |
| `PERMISSIONS_POLICY_TEMPLATE.yaml` | Machine-readable permission and action-intent policy template. |
| `RETRIEVAL_POLICY_TEMPLATE.yaml` | Machine-readable retrieval profile template. |
| `RETRIEVAL_SCORING_POLICY_TEMPLATE.yaml` | Machine-readable hard-gated retrieval scoring template. |
| `TASK_CONTRACT_TEMPLATE.yaml` | Long-task contract template. |
| `project_artifact_contract_v2/` | Closed v5 schemas, valid/invalid examples, and the shared fixture corpus. |
| `WORK_ITEM_GRAPH_TEMPLATE.yaml` | Vertical multi-session delivery DAG and derived frontier projection. |
| `PLAN_CHALLENGE_TEMPLATE.yaml` | Owner-owned question and shared-understanding gate for risky work. |
| `REVIEW_RECEIPT_TEMPLATE.yaml` | Fresh-context/adversarial review without mutation or repair authority. |
| `EXPLORATION_MAP_TEMPLATE.yaml`, `TRIAGE_LEDGER_TEMPLATE.yaml`, `DESIGN_PROBE_TEMPLATE.yaml` | Non-delivery discovery, readiness, and disposable-probe contracts. |
| `CAPABILITY_REGISTRY_TEMPLATE.yaml`, `DOMAIN_LANGUAGE_TEMPLATE.yaml` | Evidence-based capability health and bounded-context terminology. |
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
| `SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md` | How agents should manage `.codex/ALLOWED_SCOPE.txt` without forcing the owner to edit it manually. |
| `CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md` | Plain explanation of Codex permission profiles, sandbox terminology, and safe defaults. |
| `WORKSPACE_SELECTION_GUIDE.md` | How to choose IDE workspaces for single-root and multi-component projects. |
| `AI_AGENT_ROLE_STACK_GUIDE.md` | Role profiles for Cursor, Codex, GPT, single-agent implementer mode, and Project Map authority modes. |
| `CURSOR_AGENT_SETTINGS_GUIDE.md` | Recommended Cursor Agent settings for owner-controlled work. |
| `CURSORIGNORE_AND_CONTEXT_BOUNDARY_GUIDE.md` | How to use `.cursorignore` without hiding project truth. |
| `cursor/CURSOR_OWNER_CONTROLLED_DEFAULTS.md` | Cursor settings profile summary. |
| `cursor/settings/owner_controlled_profile.yaml` | Machine-readable owner-controlled Cursor settings profile. |

| `EXISTING_PROJECT_ADOPTION_GUIDE.md` | How to add the repo-centric secondary-memory governance baseline to an already active project. |
| `MATURE_EXISTING_PROJECT_ADOPTION_PROFILE.md` | Reference profile for mature projects; prefer `secondary_memory_governance/` as the concrete baseline package. |
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

## Eval-suite (Reference Lab only when activated)

Use `EVAL_SUITE_GUIDE.md`, `EVAL_AUTOMATION_AND_TRIGGER_POLICY.md`, and
`eval_suite/` only when a repeated or material failure mode supplies an
observable behavior to check and the owner adopts that evaluation work. Evals
are not part of Core.

The suite is intentionally small and failure-mode based. It is designed for
manual or semi-automated use by a project owner. An adopting Reference Lab
owner may copy it into `Project Map/eval_suite/`; the Kit does not require that
copy or a Project Map for Core.

Optional checklist helper for that adopted evaluation:

```bash
python3 "Agent Kit/kit/tools/run_eval_checklist.py" \
  --suite "Project Map/eval_suite/core_behavior_eval_cases.yaml" \
  --out "Project Map/eval_runs" \
  --mode smoke
```

---

## Repo-centric context governance

For repo-centric projects with the Standard profile's observable
context-routing trigger, use `secondary_memory_governance/` as the
secondary-memory baseline. It reproduces a standalone repo-centric workflow
without copying adopter-specific domain rules.

The baseline includes:

- secondary navigation metadata in `docs/project_map/context_index.yaml` for task-profile routing;
- bounded read-set selection;
- retrieval receipts;
- API-agent context bundle shape;
- context-selection smoke cases;
- report-only documentation harness checks.

The reference scripts live in `tools/` and are copied into the target project
as `scripts/ai_context_helper.py` and `scripts/documentation_harness.py`:

```bash
python3 "Agent Kit/kit/tools/context_governance_helper.py" --root "<Project Root>" read-set --profile startup --format json
python3 "Agent Kit/kit/tools/documentation_harness.py" --root "<Project Root>" --format json
```

Agent Memory Kit remains file-based. The helper scripts are local read-only
reference implementations, not runtime memory or security enforcement.

---

## Optional integrations

Install these only when their observable activation triggers are met and the
owner approves the integration boundary:

- `optional_integrations/chatgpt_project_sources/` - local generator for
  ChatGPT Project source manifests, context packs, and owner TODOs.
- `optional_integrations/cost_model_routing/` - advisory guide for choosing the
  lowest sufficient model/settings class.
- `optional_integrations/cursor_settings/` - Cursor settings integration that
  points to `CURSOR_AGENT_SETTINGS_GUIDE.md`.
- `optional_integrations/workflow_evals_mocked_tools/` - recorded mock-trace checks.
- `optional_integrations/tool_capability_governance/` - report-only risk classification.
- `optional_integrations/policy_canary/` - offline policy comparison validation.
- `optional_integrations/documentation_governance/` - owner-adopted policy and optional report-first tooling for documentation zones, generated blocks, and review boundaries. Read `ADOPTION_GUIDE.md` for adoption and rollback.

These modules are intentionally outside `secondary_memory_governance/`. They
must not become required startup context. Optional tooling may have its own
dependencies; the core Kit remains language-agnostic and Python-optional. The
documentation-governance checker is a dependency-free Python 3 convenience
tool only for adopters who choose to run it.

---

## How to start

The owner provides:

- where `Agent Kit/` is unpacked;
- where the project is or should be located;
- where `Project Map/` is or should be located, if adopting Standard or a
  higher profile;
- where project materials live;
- a free-form explanation of the project;
- the current permission mode;
- the exact scope for any read/write action.

For command execution, the owner must also provide OS, shell/runtime, tools, stack, and versions when relevant.

---

## Continuation rule

When a Project Map is adopted, a later work session should continue from its
documented state rather than undocumented chat memory. Core can instead
continue from its ordinary project documentation.

For the `secondary_memory_governance` baseline in existing repo-centric projects,
start from operational docs plus:

1. `AGENTS.md`
2. `docs/NEXT_STEPS.md`
3. `docs/source_of_truth_hierarchy.md`
4. `docs/context_packs/current_status.md`
5. `docs/context_governance_rules.md` when context routing, docs lifecycle, or memory promotion is in scope
6. secondary navigation: `docs/project_map/context_index.yaml`
7. secondary authority policy: `docs/project_map/source_authority.yaml`
8. secondary permission policy: `docs/project_map/permissions_policy.yaml`
9. secondary retrieval policy: `docs/project_map/retrieval_policy.yaml`
10. secondary scoring policy: `docs/project_map/retrieval_scoring_policy.yaml`
11. secondary lifecycle policy: `docs/project_map/memory_lifecycle_policy.yaml`
12. secondary state pointer: `docs/project_map/working_state.yaml`

Use the fuller flow below only when the project has explicitly adopted a full
Project Map, task, handoff, or durable-memory profile:

1. `Project Map/current_state.md`
2. `Project Map/working_state.yaml`
3. `Project Map/tasks/<active-task>.yaml` if present
4. active workstream file
5. relevant memory cards
6. latest handoff packet if resuming or recovering
7. raw sources only when necessary

---

## Recommended service setup

Put the short runtime-core rules in service-level instructions. For profiles
that adopt Project Map, keep project-specific facts there; Core may keep them
in ordinary project documentation.

Do not put the only copy of project knowledge into ChatGPT Custom Instructions, Cursor Personal Rules, Claude Project Instructions, or another service-specific prompt.


---

## Cursor Integration Pack

Use `cursor/` only when the project actually uses Cursor and the owner adopts
that integration boundary. Select small, explicit building blocks rather than
pasting the whole kit into one prompt.

Choose commands by profile and observable need:

- Core can use only grounding and safety rules, plus `/answer`, `/plan`, and
  `/apply` if the owner chooses Cursor support.
- Add `/checkpoint`, `/handoff`, `/map-apply`, or `/recover` only with the
  adopted Project Map or workflow need that makes each command useful.
- Add `/eval-smoke` only after the Reference Lab eval trigger is met.

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
- Skills and read-only Subagent templates;
- a Cursor + Codex workflow.

Use Codex as an independent reviewer, auditor, recovery assistant, or controlled executor. Do not use Codex memory, platform summaries, or compressed chat as project truth.

## v5.0.0 focus

v5.0.0 adds Project Artifact Contract V2 and conditionally activated workflow contracts for delivery graphs, plan challenge, clean-context review, exploration, triage, disposable design probes, capability health, and bounded-context terminology. Routine single-session work may use only TaskContractV3. Context Contract V1 and the file-based/provider-neutral architecture remain unchanged.

# Questions This Kit Must Answer

Status: canonical owner/agent FAQ for the package itself
Purpose: any user or agent who opens this package must be able to answer
what the kit is, why it exists, what it can and cannot do, and how to
install it on Cursor and Codex. This file is the first reply surface for
questions about the tool, not about the owner's product.

If the user asks what this toolkit is for, answer from
`MOTIVE_AND_ANALOGY.md` first (the consciousness-on-disk analogy, in
those words), then this file and the linked guides. Do not invent a
product pitch. Do not bind the answer to one private project.

---

## 1. What is this package?

Two coordinated layers in one repository:

| Layer | Path | Role |
|---|---|---|
| AI-assisted System Design | `AI-assisted System Design/` | Method: make a project AI-readable and owner-governed. |
| Agent Memory Kit | `Agent Kit/` | Operating contract: Project Map memory, grounding, action gates, evals, and surface setup. |

Together they are a **guide plus operating contract**, not a library that
"does memory" in the background.

A library would give you files to import. This package tells you:

- why those files exist;
- what the agent is forbidden to treat as truth;
- when the agent may only answer;
- when it may mutate;
- how to wire Cursor, Codex, and ChatGPT so the contract actually loads;
- how to know work is done without reading every generated line.

If a copy of the kit cannot answer those questions, the copy is incomplete.

---

## 2. Why does it exist?

Default agent setups fail in a predictable way:

- chat history and provider memory become fake project truth;
- a question turns into an unauthorized edit;
- the model fills gaps from training data;
- "done" means "it compiled" or "the agent said PASS";
- the owner then concludes that agents are stupid.

The kit exists so the owner can lay their knowledge and method out at the
physical level — folders, files, schemes, gates, oracles — until a capable
model operates like a copy that does not forget and does not get confused.
Sub-agents multiply that copy. See `MOTIVE_AND_ANALOGY.md`.

The kit also exists to move the failure from **the model** to **the missing
constraint contour**. See `CAPABILITY_MANAGEMENT.md`.

The public claim this package is built to test:

> Agent output quality is dominated by how capabilities are gated, grounded,
> reviewed, and oracled — not by whether the current model is "smart" or
> "dumb".

---

## 3. Essence in one paragraph

The owner keeps intent and acceptance. Durable project truth is a role
the owner of this instrument assigns. The recommended holder is Project
Map. The folder path is a recommendation, not the definition. Current
owner instruction, opened project files, and current tool output in this
run still outrank stale map memory. A local checkout and "whatever is in
git" are not automatically truth. In a team, one clone does not own the
project; the map remains truth and only the owner may write it. **Offer
schemes** when a causal path fits a map — cheap, accurate, readable by
human and agent. A scheme does not replace constraints, hooks, or
contracts. The agent is an execution engine with an
answer-only default. Mutation needs an explicit command, exact scope, and
the gates in this kit. Repeated failures become eval cases. Cursor and
Codex are first-class setup targets, not afterthoughts.

---

## 4. What it is not

- not a vector database;
- not ChatGPT/Cursor "memory" with a nicer name;
- not an autonomous agent runtime that runs while you sleep;
- not a promise that any model will obey instructions;
- not a replacement for tests, git, sandboxes, or owner smoke;
- not a dump of one private product's names, hosts, or secrets.

Live work from a real project may be **extracted** into this kit only after
project names, accounts, hosts, and secrets are stripped. Keep the invariant,
the gate, and the oracle shape. See `GIT_PUBLISHING_GUIDE.md`.

---

## 5. What it can do

| Capability | Where |
|---|---|
| Ground project answers | `PROJECT_GROUNDING_CONTRACT.md` |
| Default answer-only; explicit apply | `ACTION_INTENT_CONTRACT.md` |
| Durable memory units and stale facts | `PROJECT_MEMORY_STORAGE_GUIDE.md` |
| Source authority when files conflict | `SOURCE_AUTHORITY_TEMPLATE.yaml` |
| Retrieval profiles by mode | `RETRIEVAL_POLICY_PROFILES.md` |
| Long-task contracts | `TASK_CONTRACT_TEMPLATE.yaml` |
| Executor / surface routing | `EXECUTOR_ROUTING_GATE.md` |
| Execution profile / write lock | `EXECUTION_PROFILE_GATE.md` |
| Verified delivery | `VERIFIED_DELIVERY_PIPELINE.md` |
| Checkpoints and handoffs | `SIGNIFICANT_WORK_AND_CHECKPOINTS.md`, `HANDOFF_TEMPLATE.yaml` |
| Behavior evals from real failures | `eval_suite/`, `EVAL_SUITE_GUIDE.md` |
| Cursor rules, commands, hooks | `cursor/`, `CURSOR_INTEGRATION_OWNER_GUIDE.md` |
| Codex config, hooks, scope, skills | `codex/`, `codex/README.md` |
| ChatGPT Project sources | `CHATGPT_PROJECT_SOURCES_WORKFLOW.md` |
| Confidence without reading every line | `BEHAVIORAL_ORACLES.md` |
| Proposed specialist functions and limits | `PROPOSED_SPECIALIST_FUNCTIONS.md`, `cursor/subagents/` |
| Schemes as a method to offer | `SCHEMES_AND_COVERAGE_ATLAS.md`, `coverage_atlas/` |
| Rest of the working method | `WORKING_METHOD_CATALOG.md` |
| Orchestration as a choice, not a second product | `ORCHESTRATION_CHOICE.md` |
| Numbered CN facts | `CONSTRAINT_CATALOG.md`, `constraint_catalog/` |
| Hook functions and example bytes | `proposed_hooks/` |

---

## 6. What it cannot do

- make a model follow rules the host does not load;
- prove a runtime UI change from compile receipts alone;
- replace owner acceptance of look-and-feel;
- authorize commit, push, deploy, credentials, or production writes;
- turn a hybrid chat paste into a lease or a publication.

Hooks count only on a surface proven to load them. Unproven hooks are
fail-closed for hook-dependent work. See `HOOK_RECOVERY_PLAYBOOK.md`.

---

## 7. How a new user starts

1. Read `START_HERE.md` at the package root.
2. Read `MOTIVE_AND_ANALOGY.md`, then this file, then `CAPABILITY_MANAGEMENT.md`, `BEHAVIORAL_ORACLES.md`,
   `SCHEMES_AND_COVERAGE_ATLAS.md`, `PROPOSED_SPECIALIST_FUNCTIONS.md`, and
   `WORKING_METHOD_CATALOG.md`.
3. Adopt with `EXISTING_PROJECT_ADOPTION_GUIDE.md` or `NEW_PROJECT_ADOPTION_GUIDE.md`.
4. Copy templates into the project's `Project Map/`.
5. Add a short router (`AGENTS.md` or Cursor rules). Do not paste the whole kit
   into one always-loaded prompt.
6. Install the Cursor pack and/or the Codex pack from the folders below.
7. Run eval smoke before trusting the setup.

---

## 8. Cursor setup (this kit includes it)

The kit is incomplete if Cursor-only users cannot set it up from the package.

Start here:

- `CURSOR_INTEGRATION_OWNER_GUIDE.md`
- `cursor/README.md`
- `cursor/COMMAND_VOCABULARY.md`
- `CURSOR_AGENT_SETTINGS_GUIDE.md`
- `HOOK_REQUEST_WORKFLOW.md`

Install only the rules and commands you need. Project-specific overlays stay
in the adopting project, not in the published kit.

---

## 9. Codex setup (this kit includes it)

The kit is incomplete if Codex-only users cannot set it up from the package.

Start here:

- `codex/README.md`
- `codex/CODEX_SETTINGS_RECOMMENDATIONS.md`
- `codex/CODEX_HOOKS_SETUP_GUIDE.md`
- `CODEX_SANDBOX_AND_PERMISSION_PROFILES_GUIDE.md`
- `SCOPE_CONTROL_AND_ALLOWED_SCOPE_GUIDE.md`
- `CODEX_CONNECTOR_POLICY.md`

Treat Codex desktop, IDE, CLI, and web as distinct clients. Do not collapse
them into one invented surface name.

---

## 10. Questions an agent must be able to answer from the kit

| User question | Answer from |
|---|---|
| What is this? Why should I care? | `MOTIVE_AND_ANALOGY.md`, this file, `POSITIONING_AND_ALTERNATIVES.md` |
| Are agents just bad at code? | `CAPABILITY_MANAGEMENT.md` |
| Can I trust output I did not read line by line? | `BEHAVIORAL_ORACLES.md` |
| What may the agent do without asking? | `ACTION_INTENT_CONTRACT.md` |
| What is project truth? | `MOTIVE_AND_ANALOGY.md` (durable-truth role), this file §3, `PROJECT_GROUNDING_CONTRACT.md`, `SOURCE_AUTHORITY_TEMPLATE.yaml` |
| How do I install Cursor? | `CURSOR_INTEGRATION_OWNER_GUIDE.md` |
| How do I install Codex? | `codex/README.md` |
| How do I start on an existing repo? | `EXISTING_PROJECT_ADOPTION_GUIDE.md` |
| How do I know the agent follows the kit? | `EVAL_SUITE_GUIDE.md` |
| How do I publish kit changes without leaking a private project? | `GIT_PUBLISHING_GUIDE.md` |
| How do I create limited agents like a high-control owner? | `PROPOSED_SPECIALIST_FUNCTIONS.md` |
| How do I give agents a compact picture of a causal path? | `SCHEMES_AND_COVERAGE_ATLAS.md` |
| What else from a live high-control method should I copy? | `WORKING_METHOD_CATALOG.md` |
| Do I need to build my own orchestrator? | `ORCHESTRATION_CHOICE.md` |
| How do I keep limits as numbered facts? | `CONSTRAINT_CATALOG.md` |
| Which hooks should I create? | `proposed_hooks/README.md` |

If the user asks a product question about *their* repo, stop using this FAQ as
evidence. Switch to their Project Map and current source.

---

## 11. Maintainer extraction rule

When live work in a private project produces a durable practice:

1. Keep the invariant, gate, oracle, and failure mode.
2. Strip product names, hosts, account ids, paths that identify the owner,
   and any secret or credential.
3. Write or update a kit guide so a stranger can use the practice.
4. Add an eval case if the failure is repeatable.
5. Point `START_HERE.md` and this FAQ at the new file.
6. Do not ship a private Project Map as the kit.

That is the intended update path: live diff → abstract projection → kit
guide. A kit that only accumulates templates without explaining them has
drifted into a library and should be repaired.

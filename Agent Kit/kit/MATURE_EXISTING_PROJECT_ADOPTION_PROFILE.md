# Mature Existing Project Adoption Profile

Status: lightweight adoption profile
Purpose: strengthen an already AI-readable project without replacing its existing documentation, workflow, or source-of-truth system.

Reference-only note: this file is not the baseline package. Use
`secondary_memory_governance/` for the single reusable system where Project Map
is secondary memory and operational docs win. The authority modes and role
profiles below are for projects that explicitly need a different shape.

---

## 1. When to use this profile

Use this profile when the target project already has:

- a project-specific `AGENTS.md`, Cursor rule, `CLAUDE.md`, or equivalent;
- a current roadmap, status pack, issue system, or source-of-truth hierarchy;
- domain-specific safety boundaries that are more precise than generic kit rules;
- a small Project Map, context pack, or owner-memory layer already in use;
- a clear reason to avoid process growth.

The goal is reinforcement, not replacement.

Do not expand Project Map adoption beyond secondary memory by default when the existing project already works well. First identify what the current system is missing.

---

## 2. Six-question intake

Before proposing files or edits, answer these questions from current project evidence or owner input:

1. What is the current source-of-truth hierarchy?
2. Is Project Map authoritative, navigational, or absent?
3. What read-only exploration is normal for the coding agent?
4. What actions require explicit apply scope or owner approval?
5. What files, data, logs, artifacts, or secrets must stay out of routine agent context?
6. What are the top domain-specific agent failure modes?

If the answers are missing, run an inventory-only pass. Do not create a large memory layout from guesses.

---

## 3. Reference-Only Authority Modes

Do not use this section for the `secondary_memory_governance` baseline. In that
baseline, Project Map is already fixed as `secondary_memory`. Choose among these
modes only for a different project class or with explicit owner direction.

### Project Map as authority

Use when the project lacks stronger operational docs and Project Map is intended to hold current decisions, facts, constraints, tasks, and handoffs.

Recommended artifacts:

```text
Project Map/
  README.md
  current_state.md
  working_state.yaml
  source_authority.yaml
  permissions_policy.yaml
  retrieval_policy.yaml
  memory/
  tasks/
  handoffs/
  eval_suite/
```

### Project Map as secondary memory

Use when operational docs, specs, issues, tests, and project-specific instruction files already define project truth.

Rule:

```text
Project Map summarizes and navigates. Operational docs, specs, tests, code,
issues, and current owner instructions remain authoritative.
```

Recommended thin overlay:

```text
<existing docs or Project Map location>/
  source_authority.yaml
  permissions_policy.yaml
  retrieval_policy.yaml
  working_state.yaml

.codexignore
.cursorignore
```

Optional:

```text
eval_suite/manual_smoke_cases.md
```

Do not add `memory/`, `tasks/`, `handoffs/`, `raw_sources/`, or hybrid runtime files unless the project has a real continuity problem they solve.

---

## 4. Thin adoption slice

For a mature project, the first useful slice is usually:

1. Add or adapt `source_authority.yaml` as an index over existing authoritative docs.
2. Add or adapt `permissions_policy.yaml` to encode action intent, read-only exploration, write gates, and external-research boundaries.
3. Add or adapt `retrieval_policy.yaml` to keep context intake small and task-specific.
4. Add `working_state.yaml` only if fresh sessions need a compact replay root.
5. Add `.codexignore` and `.cursorignore` for context hygiene.
6. Add 5-10 manual smoke eval cases for the project's real boundary failures.
7. Add a short rule to the existing `AGENTS.md` or tool rule only if it is missing.

This slice should not change product code, runtime behavior, deployment,
external API behavior, database state, or user-facing semantics.

---

## 5. Coding-agent read-only exploration

For coding agents, scoped local read-only repository inspection is normal when needed to answer, review, plan, or implement the user's task.

Allowed read-only exploration may include:

- listing relevant files;
- reading project docs and source files in scope;
- using `rg` or equivalent search;
- inspecting `git status`, `git diff`, and test names;
- discovering available verification commands.

This does not imply permission to:

- write files;
- update Project Map or durable memory;
- run destructive commands;
- call external services;
- publish, deploy, commit, push, or send messages;
- modify databases, external accounts, credentials, or local artifacts outside
  scope.

---

## 6. Declared policy versus enforcement

Before recommending scope files or permission settings, classify the runtime capability:

```text
enforced: the runtime, wrapper, or permission profile can technically block the action
advisory: the file records policy but cannot block the action by itself
unknown: the agent has not verified runtime support
```

Examples:

- `.codexignore` and `.cursorignore` are context hygiene files, not security boundaries.
- `ALLOWED_SCOPE.txt` is useful only with a workflow, wrapper, or runtime checks that respect it.
- Permission-policy YAML describes expected behavior; it does not protect the filesystem by itself.
- If the active environment has broad write access and no approval prompts, report that before claiming a workflow is protected.

---

## 7. Reference-Only Role Profiles

Do not force one role stack on every project. For the
`secondary_memory_governance` baseline, prefer the package's
`single-agent-local-implementer` default unless the owner explicitly chooses a
different profile.

Supported profiles:

| Profile | Use when | Default |
|---|---|---|
| `single-agent-local-implementer` | One local agent reads, edits, and verifies under explicit task scope. | Allowed for small solo projects. |
| `codex-reviewer` | Codex is used as a second opinion or audit surface. | Good for risky diffs. |
| `cursor-implements-codex-reviews` | Cursor is primary implementer and Codex reviews diffs. | Good for owner-controlled multi-agent work. |
| `research-only-agent` | External/domain research should not mutate the repo. | Good for market, legal, security, or architecture research. |

The project owner may switch profiles per task. Role profile does not override action intent, permission policy, or source authority.

---

## 8. Manual smoke evals

For mature projects, start with manual smoke cases before building a full eval harness.

Each case should target a real project failure mode:

- stale navigation memory overrides current docs;
- external research changes runtime behavior without review;
- public/product framing leaks into private/internal work;
- private/internal behavior leaks into public/user-facing docs;
- AI changes execution or safety logic without a task contract;
- answer-only request triggers implementation;
- memory update happens without explicit memory-write intent;
- broad read or write scope hides a smaller task-specific path.

Store these cases near the existing Project Map or docs layer. Promote them into the full eval suite only after they prove useful.

---

## 9. Stop criteria

Stop the first adoption slice when the project has:

- machine-readable source authority for existing docs;
- explicit action and permission gates;
- context hygiene for noisy or sensitive files;
- a compact working-state or current-status entrypoint if needed;
- domain-specific smoke cases;
- no new duplicate source-of-truth layer.

Do not continue into expanded memory or workflow trees unless the owner can name the repeated problem those layers solve.

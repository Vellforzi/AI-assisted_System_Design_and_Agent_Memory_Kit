## Repo-Centric Context Governance Baseline

Status: Active repository agent guidance snippet
Last aligned: <YYYY-MM-DD>
Audience: AI/Codex sessions and maintainers
Runtime impact: none; governs agent context selection and handoff behavior only
Authority: agent bootstrap guidance; subordinate to current owner instructions and repository source-of-truth docs

This project uses `docs/project_map/` as secondary memory and navigation.
Operational docs, code, tests, specs, issues, and current owner instructions win
over Project Map on conflicts.

### Task-Local Scope Gate

Before choosing the current action, classify the user's current request:

- `answer`: answer only; no mutation.
- `review`: read-only inspection and findings unless fixes are explicitly
  requested.
- `planning`: plans and proposed deltas only.
- `docs-only`: documentation edits only when explicitly requested.
- `implementation`: scoped code/test/docs edits only inside the requested
  layer.
- `research`: evidence collection and synthesis only.
- `memory-update`: Project Map update only when explicitly scoped.

The current task-local scope controls action selection before any global next
step, backlog item, Project Map working state, or compact handoff.

### Required Startup Context

Read in this order unless the current task defines a narrower trusted read set:

1. `AGENTS.md`
2. `docs/NEXT_STEPS.md`
3. `docs/source_of_truth_hierarchy.md`
4. `docs/context_packs/current_status.md`

Then read only task-specific docs, code, tests, specs, or secondary Project Map
policy files.

Minimum secondary lower-authority governance refs:

- secondary lower-authority `docs/project_map/context_index.yaml`
- secondary lower-authority `docs/project_map/source_authority.yaml`
- secondary lower-authority `docs/project_map/permissions_policy.yaml`
- secondary lower-authority `docs/project_map/retrieval_policy.yaml`
- secondary lower-authority `docs/project_map/retrieval_scoring_policy.yaml`
- secondary lower-authority `docs/project_map/memory_lifecycle_policy.yaml`
- secondary lower-authority `docs/project_map/working_state.yaml`

Use the secondary `docs/project_map/context_index.yaml` and the local context
helper when the task needs bounded read-set selection, retrieval receipts,
context smoke checks, API-agent context bundles, or drift analysis.

### Retrieval Rules

Apply retrieval hard gates before scoring. Similarity, entity links, or
embeddings must not override source authority, stale suppression, scope,
branch, permission, security, privacy, or owner-decision boundaries.

Do not read or mutate by default:

- `data/**`
- raw logs
- local databases
- `.env*`
- secrets and credentials
- raw external-system payloads
- generated artifacts
- archive docs
- proposal docs
- research notes
- Project Map memory beyond policy/index files

Read these only when the task explicitly scopes them and source authority allows
it.

### Mutation Rules

Question, analyze, review, and plan requests do not authorize mutation. Scoped
read-only repository exploration is allowed when needed for the current coding
task, but it does not authorize file writes, durable memory updates, external
service calls, database writes, account/payment/credential or external-system
mutations, commits, pushes, or deploys.

Project Map updates require explicit memory-update intent or an approved delta.
New durable memory starts as candidate or staged unless evidence and owner or
review rules explicitly promote it. Stale, superseded, rejected, and archived
records are not current truth in normal answer, plan, or resume profiles.
Ignore files are context hygiene only, not secret protection.

If completed work changes what a future agent should do next, update the primary
handoff/status docs in the same scoped task: `docs/NEXT_STEPS.md`,
`docs/context_packs/current_status.md`, and the relevant roadmap/status/spec
entrypoint. Evidence notes remain proof; they must not be the only carrier of
next-step-critical state.

### Reporting

For non-trivial work, report:

- task-local scope used;
- selected read set or files read;
- skipped trigger-only or high-risk context;
- files changed;
- checks run and results;
- assumptions and authority conflicts;
- confirmation that runtime, external-system, data, and Project Map scope were
  not expanded unless explicitly authorized.

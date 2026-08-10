# Agent Memory Kit

Version: v5.0.0

Agent Memory Kit is the project-memory and agent-behavior layer of the package.
Start with the smallest adoption profile that has an observable need; see
`kit/ADOPTION_PROFILES.md`.

- **Core** is useful without a Project Map or tools: grounding,
  explicit-action control, and ordinary durable project notes.
- **Standard** adds the repo-centric secondary-memory governance baseline for
  observed context-routing needs.
- **Workflow** adds only the v5 contracts activated by task scale, risk, or
  `TaskContractV3.workflow_profile`.
- **Reference Lab** contains explicitly owned eval, automation, and integration work.

Core has no Project Map, Python, evals, task contracts, `.work`, generated
projections, hooks, CI, or MkDocs. The presence of a mechanism in the Kit is
not a recommendation to install it. Greenfield removes migration cost, not
operating cost; optional artifacts require observable activation triggers.

For existing projects, the current authority system remains in force. Where
Project Map is `secondary_memory`, operational docs, code, tests, specs,
issues, and current owner instructions remain authoritative.

---

## Start here

1. `kit/ADOPTION_PROFILES.md`
2. `kit/README.md`
3. The selected profile's guide or module, only after its activation trigger is observable.

---

## Default behavior

The agent must answer only unless the owner explicitly asks for a concrete action. Reading memory for context is not the same as permission to modify memory, files, database state, git state, cloud resources, or external systems.

After meaningful work, the agent may propose a Project Map delta when Standard
or a higher profile is adopted, and may identify whether an observable eval
trigger is met. It must not apply memory or rule changes unless the owner
explicitly asks.

---

## Use in a repository

Use `kit/secondary_memory_governance/AGENTS_SNIPPET.md` when a mature existing project already has a project-specific `AGENTS.md`.

Use `kit/AGENT_INSTRUCTION_FILES_GUIDE.md` and `kit/AGENTS.md_TEMPLATE.md` only when the project does not already have a suitable root instruction file.

Use `kit/CURSOR_RULE_TEMPLATE.mdc` for Cursor projects.

For mature existing projects, patch the existing instruction file and add the secondary-memory governance overlay instead of replacing the project's current source-of-truth system.

Do not commit private local preferences, secrets, credentials, raw personal data, or provider-specific session dumps.

---

## Positioning

Agent Memory Kit is useful when the owner wants a visible, editable, portable project memory rather than hidden provider memory or a loose chat summary.

It is not a full agent runtime. The core value is the operating contract: what counts as project truth, what may be remembered, when the agent may act, and how failures become eval cases.

For existing repo-centric projects, start with Core. Adopt
`kit/secondary_memory_governance/` as Standard only when its observable
context-routing trigger is met.

Optional tool-specific modules live in `kit/optional_integrations/`. Add them
only after the core baseline works and only when the target project uses the
matching surface.
---

## Cursor, Codex, and GPT role stack

Recommended default:

```text
Cursor = primary implementation agent
Codex = restricted reviewer/auditor/recovery helper
GPT web chat = research, design, and task specs
Project Map = shared memory boundary, or source of truth only when the project's authority policy says so
```

Use one shared workspace root when one Project Map governs multiple components. Use task scope and permission gates for safety.



## v3.8 Cursor settings and workspace authority

This release adds an owner-controlled Cursor Agent settings profile, `.cursorignore` guidance, settings audit commands, and the rule that an existing authoritative workspace file must be inspected and used rather than replaced by a generated fallback.

## v5 workflow contracts

Project Artifact Contract V2 adds conditionally activated, file-based contracts for multi-session delivery, plan challenge, independent review, exploration, triage, design probes, capability health, and domain language. A routine single-session task does not need those extra artifacts. The Kit remains provider-neutral and does not schedule or mutate work automatically.

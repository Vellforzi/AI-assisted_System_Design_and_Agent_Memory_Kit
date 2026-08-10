# AI-assisted System Design and Agent Memory Kit

Version: v5.0.0
Release date: 2026-08-07
Status: portable project-owner toolkit
Last aligned: 2026-08-07
Audience: project owners, adopters, and maintainers
Runtime impact: none until explicitly adopted
Authority: navigation index; operational project evidence and owner instructions remain authoritative

This package contains two complementary tools:

1. **AI-assisted System Design** — a method for making a project readable and governable by AI assistants.
2. **Agent Memory Kit** — a file-based operating layer for project memory, grounding, retrieval, task continuity, action gates, and behavior checks.

The package is designed for owners who want high control over AI-assisted work. It does not assume autonomous long-running agents. The default mode is controlled, evidence-first, answer-only work unless the owner explicitly asks for a concrete action.

Repository context routing is indexed in [`docs/project_map/context_index.yaml`](docs/project_map/context_index.yaml); it is secondary navigation, not project truth.

---

## Core idea

A language model is not the source of truth for your project.

The agent should operate from:

- current owner input;
- an adopted Project Map, only in its declared authority role;
- opened project files and tool outputs;
- explicitly allowed external research;
- explicit owner approval for mutating actions.

The kit turns project context into structured, inspectable memory so that future sessions can restore the right context without relying on fragile chat history, hidden provider memory, or generic model guesses.

For existing repo-centric projects, start with Core. Adopt the
`secondary_memory_governance/` Standard baseline only when an observable
context-routing need warrants it. Then Project Map summarizes and navigates,
while operational docs/code/tests/specs/issues/current owner instructions
remain authoritative. Optional integrations remain separate, explicitly
triggered choices.

---

## What makes this different

Agent Memory Kit is not mainly a vector database, not mainly a chat memory feature, and not mainly an autonomous agent runtime.

It is strongest when the owner wants:

- a visible Project Map instead of opaque provider memory;
- source authority when project sources conflict;
- answer-only default behavior;
- explicit permission before any mutation;
- small durable memory records instead of long chat summaries;
- stale and superseded facts preserved but not used as current truth;
- checkpoints and handoffs across sessions;
- behavior evals based on real failure modes.

See `Agent Kit/kit/POSITIONING_AND_ALTERNATIVES.md`.

---

## Repository layout

```text
AI-assisted System Design and Agent Memory Kit/
  README.md
  START_HERE.md
  RELEASE_NOTES_v5.0.0.md

  AI-assisted System Design/
    README.md
    AI-assisted System Design.md

  Agent Kit/
    README.md
    START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md
    kit/
      README.md
      ...contracts, templates, guides, eval suite, Cursor integration, Codex integration, optional integrations, optional tools...
```

---

## Fast start

1. Read `START_HERE.md`.
2. Read `AI-assisted System Design/README.md` if you are setting up a project workflow.
3. Read `Agent Kit/kit/ADOPTION_PROFILES.md` and choose the smallest profile with an observable need.
4. Read `Agent Kit/README.md` if you are setting up project memory.

Agent Memory Kit starts with **Core**: a small, useful, dependency-free layer
for grounding, explicit action approval, and ordinary durable project notes.
Core has no Project Map, Python, evals, task contracts, `.work`, generated
projections, hooks, CI, or MkDocs. **Standard** adds secondary-memory
governance for observed context-routing needs; **Workflow** adds only the v5
artifacts demanded by task scale or risk; **Reference Lab** is for explicitly
owned evaluation, automation, and integrations.

The presence of a mechanism in the Kit is not a recommendation to install it.
Greenfield removes migration cost, not operating cost. Optional artifacts need
observable activation triggers before adoption. For existing repo-centric
projects, preserve the existing authority system: Project Map is secondary
memory when the project policy says so, and operational docs, code, tests,
specs, issues, and current owner instructions remain authoritative.

---

## What v3.8.0 adds

- Cursor Agent settings profile for owner-controlled work.
- Settings audit and `.cursorignore` audit command templates.
- Authoritative existing workspace rule: inspect and use the project workspace referenced by Project Map or AGENTS.md instead of replacing it with a generated fallback.
- `.cursorignore` context-boundary guide and safe default template.
- Scope Control layer for agent-managed `.codex/ALLOWED_SCOPE.txt` updates.
- `/scope-set`, `/scope-reset`, and `/workspace-check` command templates.
- Codex sandbox and permission profile guide explaining `default_permissions`, `:read-only`, `:workspace`, and why not to mix them with old `sandbox_mode` settings.
- Cursor workspace templates, including an OPTION PROFIT / JOB single-root workspace example.
- Workspace selection guide for multi-component projects with one Project Map.
- Default role stack guide: Cursor as primary implementation agent, Codex as restricted reviewer/auditor/recovery helper, GPT web chat as research/design layer, Project Map as shared memory/navigation; truth role follows `source_authority`, and for existing repo-centric projects it is secondary.
- Codex scope-control templates and optional helper script for safe scope updates and resets.
- Eval cases for scope control, Codex permissions, workspace selection, and role orchestration.

---

## Non-goals

This package is not:

- a vector database;
- an autonomous-agent framework;
- a replacement for project documentation;
- a guarantee that any model will always comply;
- a security sandbox;
- a place to store secrets;
- a license to let agents mutate files without owner intent.

Use technical enforcement where possible: permissions, sandboxing, read-only modes, and review gates.


---

## Python is not required

Agent Memory Kit is language-agnostic and file-based. Python helper scripts are optional examples only. They are included because the original owner works in Python. Replace them with another language if that fits your project better.


## v3.8 Cursor settings and workspace authority

This release adds an owner-controlled Cursor Agent settings profile, `.cursorignore` guidance, settings audit commands, and the rule that an existing authoritative workspace file must be inspected and used rather than replaced by a generated fallback.

## v3.8.0 focus

v3.8.0 adds Cursor owner-controlled settings, authoritative existing workspace handling, `.cursorignore` / `.codexignore` context-boundary templates, and desktop metadata ignore patterns for Windows/Google Drive projects.

## v5.0.0 focus

v5.0.0 adds Project Artifact Contract V2 and eight conditionally activated coding-workflow contracts: work-item graphs, plan challenges, independent reviews, exploration maps, triage ledgers, design probes, capability registries, and bounded-context language. Simple routine tasks remain artifact-light. See `RELEASE_NOTES_v5.0.0.md` and `Agent Kit/kit/MIGRATION_v4_TO_v5.md`.

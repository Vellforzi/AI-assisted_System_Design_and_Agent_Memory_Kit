# AI-assisted System Design and Agent Memory Kit

Version: v3.7.0  
Release date: 2026-06-09  
Status: portable project-owner toolkit

This package contains two complementary tools:

1. **AI-assisted System Design** — a method for making a project readable and governable by AI assistants.
2. **Agent Memory Kit** — a file-based operating layer for project memory, grounding, retrieval, task continuity, action gates, and behavior checks.

The package is designed for owners who want high control over AI-assisted work. It does not assume autonomous long-running agents. The default mode is controlled, evidence-first, answer-only work unless the owner explicitly asks for a concrete action.

---

## Core idea

A language model is not the source of truth for your project.

The agent should operate from:

- current owner input;
- the Project Map;
- opened project files and tool outputs;
- explicitly allowed external research;
- explicit owner approval for mutating actions.

The kit turns project context into structured, inspectable memory so that future sessions can restore the right context without relying on fragile chat history, hidden provider memory, or generic model guesses.

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
  RELEASE_NOTES_v3.7.0.md

  AI-assisted System Design/
    README.md
    AI-assisted System Design.md

  Agent Kit/
    README.md
    START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md
    kit/
      README.md
      ...contracts, templates, guides, eval suite, Cursor integration, Codex integration, optional tools...
```

---

## Fast start

1. Read `START_HERE.md`.
2. Read `AI-assisted System Design/README.md` if you are setting up a project workflow.
3. Read `Agent Kit/README.md` if you are setting up project memory.
4. For an existing project, read `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`.
5. For a new empty project, read `Agent Kit/kit/NEW_PROJECT_ADOPTION_GUIDE.md`.
6. Copy the needed templates from `Agent Kit/kit/` into your project's `Project Map/`.
7. Add only a short agent-instruction entrypoint to your coding tool, such as `AGENTS.md` or Cursor rules. Do not paste the whole kit into one always-loaded prompt.

---

## What v3.7.0 adds

- Scope Control layer for agent-managed `.codex/ALLOWED_SCOPE.txt` updates.
- `/scope-set`, `/scope-reset`, and `/workspace-check` command templates.
- Codex sandbox and permission profile guide explaining `default_permissions`, `:read-only`, `:workspace`, and why not to mix them with old `sandbox_mode` settings.
- Cursor workspace templates, including an OPTION PROFIT / JOB single-root workspace example.
- Workspace selection guide for multi-component projects with one Project Map.
- Default role stack guide: Cursor as primary implementation agent, Codex as restricted reviewer/auditor/recovery helper, GPT web chat as research/design layer, Project Map as shared truth.
- Hook request workflow, hook generation questions, and hook packaging guide.
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

Use technical enforcement where possible: permissions, hooks, sandboxing, branch isolation, read-only modes, and review gates.


---

## Python is not required

Agent Memory Kit is language-agnostic and file-based. Python helper scripts are optional examples only. They are included because the original owner works in Python. Replace them with another language if that fits your project better.

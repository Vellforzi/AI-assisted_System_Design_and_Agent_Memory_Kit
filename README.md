# AI-assisted System Design and Agent Memory Kit

Version: v3.11.0
Release date: 2026-07-05
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
  Agent Kit/kit/CHANGELOG_v3.11.0.md
  Agent Kit/kit/CHANGELOG_v3.10.0.md
  RELEASE_NOTES_v3.9.3.md
  RELEASE_NOTES_v3.9.1.md
  RELEASE_NOTES_v3.9.0.md

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

## What v3.11.0 adds

- **Executor Routing Gate** for evidence-based executor/service selection in
  non-trivial contracts, bootstraps, task blocks, and model/service advice.
- **Windows encoding and shell hygiene** for byte-safe edits, non-ASCII text,
  and readback verification.
- **Hook recovery playbook** with actionable recovery payload fields and
  snake_case/camelCase compatibility.
- **Codex connector policy**: connectors default forbidden, scoped reads,
  explicit write gates, draft-first outbound messaging, and receipts.
- **Generated retrieval evidence guide**: generated index/search output can
  narrow candidates but requires canonical source re-read before claims.
- New eval coverage for routing gates, encoding hygiene, hook recovery,
  connector safety, and generated retrieval evidence.

## What v3.10.0 adds

- Generic ChatGPT Project sources manifest workflow: local, config-driven, and
  deterministic.
- Compact ChatGPT Project Instructions template, project operating contract
  template, source policy, generator, fixture, and eval case `AMK-GPS-001`.

## What v3.9.3 adds

- **Cost-Aware Model Router**: the agent must recommend the lowest sufficient model/settings class, not the most expensive model by default.
- Premium/frontier/high/pro reasoning recommendations require explicit escalation reasons and a cheaper alternative.
- Narrow Project Map updates, owner-provided fact recording, version refs, and small docs/router edits default to medium reasoning with Max Mode and implicit IDE context off.
- The `/settings` and `settings?` flow must show cost class, escalation triggers, and “why not cheaper” when a premium route is recommended.
- v3.9.1 implicit IDE context boundary and v3.9.0 Context Advisor functionality remain included.

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


## v3.9.3 Context Advisor focus

This release clarifies cost-aware model routing. The agent should use the lowest sufficient model/settings class, escalate only with concrete reasons, and show a cheaper alternative when recommending premium/frontier/high/pro modes. v3.9.1 implicit IDE context boundary and v3.9.0 automatic/on-demand guidance remain included.


## v3.9.3 Cursor provider model snapshot

v3.9.3 adds a dated Cursor model-routing snapshot captured on 2026-06-10. Exact Cursor model/settings advice must show snapshot date/ref. The core Cursor Agent model set is considered sufficient with surplus; optional models require a concrete capability gap and owner approval before default routing.

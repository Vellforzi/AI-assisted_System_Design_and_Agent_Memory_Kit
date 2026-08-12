# AI-assisted System Design and Agent Memory Kit

Version: v4.0.0 published
Release date: v4.0.0 published 2026-08-13; previous tag `v3.12.1` published 2026-08-13
Status: portable project-owner toolkit. Published tag is `v4.0.0`.

This package is a **guide plus operating contract**, not a library that runs in the background.

Two layers:

1. **AI-assisted System Design** — a method for making a project readable and governable by AI assistants.
2. **Agent Memory Kit** — a file-based operating contract for project memory, grounding, retrieval, task continuity, action gates, and behavior checks.

If you ask what this tool is, start with `Agent Kit/kit/MOTIVE_AND_ANALOGY.md`, then `Agent Kit/kit/QUESTIONS_THIS_KIT_ANSWERS.md`.

---

## What the instrument is

You lay your knowledge and method out on disk: folders, files, schemes, gates. The more accurately you do that, the more accurately a capable model looks like you. A copy that does not forget and does not get confused. Sub-agents multiply that copy. The tool is for models that can use the layout. Stuffing folders around a weak model does not make a twin.

It exists so owners manage agent **capability** (truth, gates, oracles, Cursor/Codex setup) instead of blaming "stupid models" when unconstrained chat produces junk.

Default mode is controlled, evidence-first, answer-only work unless the owner explicitly asks for a concrete action.

---

## Where durable truth lives

Durable project truth is a **role** the owner of this instrument assigns. The recommended name is Project Map. The recommended folder is `Project Map/`. The path is a recommendation. A left or right step in folder names does not change efficiency if the role stays one place, owner-assigned, and agents do not invent a parallel truth.

A programmer's local checkout is not team truth. The git repository as a pile of committed files is not truth. A file is not true because it is in git. Current owner instruction and current opened evidence in this run outrank stale map memory.

Solo: the owner of the instrument is the owner of the project. Local map and project coincide.

Team: the project does not belong to whoever has a clone. The map remains truth. Only the owner, or an owner-accepted team agreement, may write it. Do not demote the map so that unmarked repo docs win by default.

See `Agent Kit/kit/MOTIVE_AND_ANALOGY.md` and `Agent Kit/kit/SOURCE_AUTHORITY_TEMPLATE.yaml`.

---

## What makes this different

Not a vector database. Not ChatGPT or Cursor "memory" with a nicer name. Not an autonomous runtime.

It is strongest when the owner wants:

- a visible Project Map instead of opaque provider memory;
- source authority when project sources conflict;
- answer-only default behavior;
- explicit permission before any mutation;
- behavioral oracles, independent review, and owner smoke instead of "it compiled";
- Cursor and Codex setup in the package so the contour actually loads;
- orchestration as a choice, not a second product to build.

See `Agent Kit/kit/POSITIONING_AND_ALTERNATIVES.md`, `Agent Kit/kit/CAPABILITY_MANAGEMENT.md`, `Agent Kit/kit/BEHAVIORAL_ORACLES.md`, and `Agent Kit/kit/ORCHESTRATION_CHOICE.md`.

---

## Repository layout

```text
AI-assisted System Design and Agent Memory Kit/
  README.md
  START_HERE.md
  Agent Kit/kit/CHANGELOG_v4.0.0.md
  Agent Kit/
    README.md
    START_HERE_AGENT_KIT_PROJECT_OWNER_GUIDE.md
    kit/
  AI-assisted System Design/
    README.md
    AI-assisted System Design.md
```

Earlier 3.x changelogs stay under `Agent Kit/kit/CHANGELOG_v3.*.md` and root `RELEASE_NOTES_v3.*.md`.

---

## Fast start

1. Read `START_HERE.md`.
2. Read `Agent Kit/kit/MOTIVE_AND_ANALOGY.md`, then `Agent Kit/kit/QUESTIONS_THIS_KIT_ANSWERS.md`.
3. Read `AI-assisted System Design/README.md` if you are setting up a project workflow.
4. Read `Agent Kit/README.md` if you are setting up project memory.
5. For an existing project, read `Agent Kit/kit/EXISTING_PROJECT_ADOPTION_GUIDE.md`.
6. For a new empty project, read `Agent Kit/kit/NEW_PROJECT_ADOPTION_GUIDE.md`.
7. Copy the needed templates from `Agent Kit/kit/` into your project's `Project Map/`.
8. Add only a short agent-instruction entrypoint to your coding tool, such as `AGENTS.md` or Cursor rules. Do not paste the whole kit into one always-loaded prompt.

---

## What v4.0.0 published

- Durable-truth role: Project Map is the recommended holder; folders are a recommendation; a checkout and "whatever is in git" are not automatically truth; in a team the map stays truth and only the owner writes it.
- GitHub landing README rewritten for the current instrument.
- Eval case `AMK-DT-001`. Suite id `AMK-EVAL-v4.0.0`.

See `Agent Kit/kit/CHANGELOG_v4.0.0.md`.

The 3.x contour is still in the package: capability management, behavioral oracles, schemes, CN catalog, hooks, execution runtime, verified delivery, orchestration choice. Those were published as `v3.11.3`–`v3.12.1`. This major does not merge the diverged `new_version` branch.

---

## Earlier 3.x (historical)

| Tag | What it added |
|---|---|
| `v3.12.1` | Orchestration as a choice. `ORCHESTRATION_CHOICE.md` |
| `v3.12.0` | Execution Profile Gate, leases, verified delivery, Windows command-launch hygiene |
| `v3.11.3` | FAQ, motive, capability management, oracles, schemes, CN catalog, hook cards |
| `v3.11.2` / `v3.11.1` | GPT-5.6 routing snapshots and label fidelity |
| `v3.11.0` | Executor routing, encoding hygiene, hook recovery, connector policy |
| `v3.10.0` | ChatGPT Project sources manifest workflow |
| `v3.9.x` | Context Advisor, cost-aware routing, Cursor settings |

Read the matching `Agent Kit/kit/CHANGELOG_v3.*.md` or root `RELEASE_NOTES_v3.*.md`. Do not treat those files as the current landing page.

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

Agent Memory Kit is language-agnostic and file-based. Python helper scripts are optional examples only. Replace them with another language if that fits your project better.

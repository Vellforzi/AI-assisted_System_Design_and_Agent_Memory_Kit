# New Project Adoption Guide

Status: practical Core-profile setup guide
Purpose: begin a new project with grounded, owner-controlled agent work without
installing a larger operating system than the work needs.

---

## 1. Start with Core

**Core is the first usable setup.** It is a complete, small operating layer:

1. project-specific claims come from the owner and opened project sources;
2. answers remain answer-only until the owner explicitly authorizes a scoped
   action; and
3. current work and material decisions survive the next session in ordinary
   project documentation.

For a new project, create **only three project-created files** to start. Add at
most three ordinary project documents only when they have real content. The
first usable Core setup therefore has three to six project-created files, not a
prebuilt management structure or a set of empty placeholders.

Core does **not** require a Project Map, pre-created memory registries, task or
handoff directories, raw-source storage, eval directories, a full policy-YAML
set, `.work`, TaskContractV3, Python, hooks, CI, generated projections, or
integrations. Routine work remains at this level unless a later signal warrants
a narrower addition.

---

## 2. The first usable setup: three files

Create this small, project-owned surface:

```text
<Project Root>/
  README.md
  AGENTS.md
  docs/
    CURRENT_WORK.md
```

Use the existing project location and naming conventions if they already exist.
Do not add a separate `Agent Kit/` copy unless the owner has chosen to keep the
portable Kit beside the project.

Put only current, owner-approved information in these files:

| File | Minimum purpose |
|---|---|
| `README.md` | Goal, non-goals, and the project entry point. |
| `AGENTS.md` | Source-authority order; answer-only default; explicit, scoped approval for writes or external actions. |
| `docs/CURRENT_WORK.md` | Current objective, next small step, known unknowns, and what changed in the last session. |

If a topic has real content that would otherwise be lost, add one to three of
these ordinary documents; do not add empty placeholders:

```text
docs/DECISIONS.md       # approved decisions and their reasons
docs/CONSTRAINTS.md     # durable limits, prohibited actions, or safety notes
docs/ARCHITECTURE.md    # only after an actual design choice exists
```

Do not invent architecture, database schema, routes, business rules, or
deployment state merely to fill a file.

---

## 3. What the Core rules should say

Keep the instruction rule short and specific. A usable `AGENTS.md` rule can
state:

```text
Use current owner instructions and opened project files for project-specific
claims. Treat questions, analysis, review, and planning as non-mutating.
Before a write or external action, require explicit intent, exact target scope,
and a stated verification approach. If evidence is missing, say so.
```

The owner may add tool limits, forbidden actions, and the project's normal
review process. Requirements describe intended behavior; they do not prove
current runtime behavior. Describe runtime behavior as `enforced`, `advisory`,
`unknown`, or `absent` only when the available runtime evidence supports that
label. A requirement or policy file alone does not prove current runtime
behavior.

---

## 4. Two concrete adoption paths

### Path A: small single-session project

Use the three Core files above. Record the goal in `README.md`, the action and
grounding rule in `AGENTS.md`, and the one current task in
`docs/CURRENT_WORK.md`. Work directly from those files and the owner request.

Do not create a Project Map, `.work`, TaskContractV3, receipts, evals, task
trees, handoff trees, or automation. At the end of the session, update only
the current-work note if the owner has authorized that write. A short project
can remain at Core indefinitely.

### Path B: growing multi-session project

Start with the same three Core files. On each session, update
`docs/CURRENT_WORK.md` with the current objective, next step, and unresolved
question; add `docs/DECISIONS.md` only when a decision needs durable context.
Add `docs/CONSTRAINTS.md` or `docs/ARCHITECTURE.md` only when its corresponding
content exists. This remains Core and stays within three to six files.

Move to Standard only after an observable context-routing need appears: for
example, repeated sessions or contributors cannot reliably choose the relevant
source set, or a documented context-selection error has occurred. Standard
adds `secondary_memory_governance/` as a secondary-memory overlay; it does not
replace operational docs, code, tests, specs, issues, or current owner
instructions. Project Map is secondary navigation and memory when the
project's authority policy says so, never an automatic replacement source of
truth.

---

## 5. Add mechanisms only when their signal is observable

| Mechanism | Observable signal | Narrow response |
|---|---|---|
| **Standard** | Repeated sessions or contributors need bounded context selection, or a context-selection error is documented. | Adopt the repo-centric `secondary_memory_governance/` baseline as a secondary-memory overlay. |
| **Project Map** | The Standard need specifically requires a compact, maintained navigation layer across operational sources. | Add it under the project's authority policy; operational sources still win on conflict. |
| **`.work`** | Task scale, risk, dependencies, review sensitivity, or `TaskContractV3.workflow_profile` requires a workflow artifact. | Add only the applicable workflow artifact; routine work does not get `.work` or TaskContractV3. |
| **Receipts** | A bounded retrieval decision needs reproducible selection evidence, auditability, or adapter parity. | Add a read-only request/bundle/receipt boundary only for that retrieval use case. |
| **Evals** | A repeated or material agent failure has a concrete behavior that can be checked. | Add a focused manual case first; automate only if its value is demonstrated. |
| **Automation** | A named owner accepts maintenance for a stable, repeated task with a reproducible check or publication need. | Add the smallest maintained script, hook, CI path, or integration. |

No signal means no installation. A signal permits a scoped proposal; it does
not authorize a mutation or make the mechanism permanent. Requirements state
the intended behavior of any adopted mechanism; they do not establish its
current runtime behavior.

---

## 6. First-session prompt

```text
Use the Agent Memory Kit Core profile.
Intent: plan.
Mode: dry-run.
Scope: this new project only.
Goal: propose the three-file Core setup and its initial owner-approved content.
Do not create files unless I explicitly switch to apply mode.
Do not add Project Map, evals, .work, TaskContractV3, registries, or policy YAML
unless I identify an observable trigger and approve that narrower addition.
```

---

## 7. When to allow edits

Before applying an edit, the agent should show the target files, exact scope,
the proposed change, what it will not touch, and the planned verification.
Questions, reviews, analysis, and plans remain non-mutating. A later Standard,
workflow, eval, or automation proposal needs its own explicit scope and owner
approval.

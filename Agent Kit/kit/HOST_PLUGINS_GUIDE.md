# Host plugins guide

Status: canonical portable guide
Purpose: explain Cursor plugins, Codex skills/plugins, and skill packs such as PStack. These are **host add-ons**. They are not Agent Memory Kit, not Project Map truth, and not a substitute for gates, oracles, hooks, or contracts.

If the user asks whether they must install plugins to use the kit, answer from this file first.

---

## 1. What they are

Host add-ons extend what a coding agent can do inside a specific surface (Cursor, Codex, or similar). Examples:

- **Cursor plugins / skills** — optional skill packs the host loads on demand.
- **Codex skills / plugins** — skills from the Codex skills area plus optional MCP connectors the owner chooses.
- **PStack** — a Cursor plugin family for method skills such as `/how` (architecture walkthrough), `/why` (design rationale from evidence sources), and writing-quality skills such as unslop.

They multiply a capable model the same way the kit's proposed specialist functions do. They remain **host capability**, not kit identity.

The kit's proposed hooks, execution-profile gates, and eval cases stay the kit's proposed functions. Host plugins are extra.

---

## 2. What they are not

- not Agent Memory Kit;
- not Project Map or durable project truth;
- not a replacement for action-intent gates, source authority, or behavioral oracles;
- not a license to copy plugin source trees into the published kit;
- not proof that a runtime claim is true until the owner promotes evidence into the map.

Plugin output is advisory until the owner verifies it and records durable facts in Project Map.

---

## 3. PStack specifically

PStack is a Cursor plugin for method skills: `how`, `why`, and optional style modes. Offer it when the question is **how a subsystem is shaped** or **why a design choice was made**, or when published kit prose needs a writing-quality pass.

Do **not** require PStack to adopt or use Agent Memory Kit. Do **not** treat PStack output as project memory. Do **not** vend or mirror PStack source inside this package.

---

## 4. Cursor plugins and skills

Useful when:

- the owner asks for an architecture walkthrough before changing a subsystem (`/how`);
- the owner asks for design rationale backed by evidence sources (`/why`);
- published kit or owner-facing prose needs less sloppy wording (unslop or similar).

Low value when:

- the goal is durable project memory (use Project Map instead);
- the owner has not named a concrete question or task;
- the agent treats plugin transcripts as truth without map promotion.

Install only what the current task needs. Presence of this guide is not a recommendation to install anything.

---

## 5. Codex skills and plugins

Codex can load skills from its skills area and optional MCP tools the owner configures. Same rules:

- host capability, owner-chosen;
- not kit identity;
- connector and side-effect policy still apply (`CODEX_CONNECTOR_POLICY.md`);
- skills do not replace hooks, leases, or verified-delivery oracles.

MCP skills are high value when the owner actually uses that external service for the current task. They are low value as a default garden installed "to make agents smarter."

---

## 6. Usefulness (honest)

| Use case | Value |
|---|---|
| `/how` or `/why` before changing a cross-cutting subsystem | high |
| Writing-quality pass on kit or owner-facing docs | high |
| MCP skill when the owner uses that service for this task | high |
| Installing many plugins with no named trigger | low / none |
| Treating plugin memory or chat as Project Map | harmful |
| Replacing execution-profile gates with a plugin | harmful |

---

## 7. Install discipline

Same discipline as `ORCHESTRATION_CHOICE.md`:

**No trigger = do not install.**

A trigger is a concrete owner question or task: explain this subsystem, justify this design, connect to this external service, or improve this prose. Without that trigger, leave plugins disabled.

After meaningful plugin-assisted work, the agent may propose a Project Map delta. It must not write plugin output into the published kit or into Project Map as verified fact without owner promotion.

---

## 8. Agent must-not list

- Do not describe PStack, Cursor plugins, or Codex skills as Agent Memory Kit.
- Do not copy plugin directories into `Agent Kit/kit/`.
- Do not treat plugin transcripts as durable project truth.
- Do not recommend a plugin garden when gates and map setup are still missing.
- Do not skip execution-profile or action-intent gates because a plugin is installed.

Eval case: `eval_suite/cases/AMK-PL-001.yaml`.

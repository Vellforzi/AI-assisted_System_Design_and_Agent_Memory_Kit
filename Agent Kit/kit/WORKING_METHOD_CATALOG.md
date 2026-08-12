# Working Method Catalog (proposed functions)

Status: portable catalog of working methods extracted from live high-control
use. Not a dump of one project's skills, rules, hooks, or product names.

**Offer schemes.** When a scenario fits a map, it is cheap and accurate.
Read `SCHEMES_AND_COVERAGE_ATLAS.md`. A scheme does not replace this
catalog. Then the rest of the method: how to create the other functions,
and how to limit them.

Specialist cards: `PROPOSED_SPECIALIST_FUNCTIONS.md` and
`cursor/subagents/`.

Copy the **instruction**, then name it in your project. Do not paste a
private roster.

---

## 1. How to read this catalog

Each item is a proposed function:

```text
Job / How to create / How to limit / Must never claim
```

Install only what the project needs. A small project may use hosts only
(Cursor / Codex / GPT). Coupled runtime/UI work needs more of this list.

---

## 2. Coverage schemes (offer this method)

**Job:** keep a visual atlas of what is proven vs open risk.

**How:** INDEX + one scenario per file + Mermaid sequence + closed token
legend + impact-draft before coupled apply.

**Limit:** one mapper writes the tree; workers get a brief, not the whole
atlas; `[OK]` needs evidence; owner can refuse promote after smoke.

**Must never claim:** a child axis closed ⇒ the parent chain is `[OK]`;
a scheme holds the whole working method.

Promote this method because it is cheap, accurate, and readable by both
human and agent. Offer it. Do not use it as a substitute for numbered
constraints, hook bytes, contracts, or smoke. Full guide:
`SCHEMES_AND_COVERAGE_ATLAS.md`.

---

## 3. Fail-closed orchestrator (leader chat)

**Job:** route work, keep scope, pull missing canonical sources when a
gap exists, refuse to self-grade.

**How:** parent chat is the leader. Heavy units go to limited functions
(writer, reviewer, mapper, forensic, builder, deployer). Parallel fan-out
of *different* functions is allowed.

**Limit:**

- answer-only until explicit apply/map-apply;
- on hook/guard block, report the code and stop claiming protection;
- do not silently self-apply if a worker fails;
- do not dump the atlas into every worker;
- do not wait for the owner to re-list every journal, map, or receipt
  when the gap is already named in Project Map or the atlas INDEX.

**Must never claim:** runtime PASS, deploy PASS, or owner acceptance.

---

## 4. Owner-gated live-surface smoke

**Job:** prove runtime/UI behavior on the live surface without letting the
agent drive the GUI.

**How:** write a short skill/runbook: owner starts the product, owner
clicks, owner records wall-clock start/end, agent slices logs and returns
tokens. Agent-safe paths: doctor/scan/tests that do not open the
interactive UI.

**Limit:**

- agent does not launch the interactive product;
- agent does not click the live surface;
- deploy is a separate function and a separate owner allowance;
- forensic verdict is not owner smoke PASS.

**Must never claim:** `SMOKE_PASS` from compile, from writer narrative, or
from a log slice the owner did not window.

A compiled native chart UI with UTF-16LE journals is one specialization.

---

## 5. Contract hygiene (write lock input)

**Job:** make mutation gates machine-checkable.

**How:**

- canonical apply input is a **plain contract file** (YAML) with gates,
  exact output root, one artifact glob, baseline, and owner-bearing write
  authorization;
- a prose+YAML paste / bootstrap is **narrative only** — never pass it as
  the contract;
- if apply points at a hybrid paste, **materialize** a real contract in
  the same open task before taking the write lock;
- do not open a "recovery task" for that.

**Limit:** wrong argv, quoting, encoding, stale receipt, or hybrid-as-
contract is a **harness** failure, not "the model cannot code".

**Must never claim:** a chat paste is a lease.

---

## 6. Mode boundaries

| Mode | Proposed limit |
|---|---|
| `/answer` `/analyze` `/plan` `/review` `/recover` | no mutation |
| `/stage` | write only requested task/bootstrap artifacts |
| `/apply` | exact owner-authorized implementation paths |
| `/map-delta` | candidate under the task root; no Project Map write |
| `/map-apply` | exact owner-approved map/memory paths |

`/stage` does not execute the staged task. `/review` does not repair.
A report or a `next_step` line does not grant the next phase.

---

## 7. Write lock (lease pattern)

**Job:** one writer, one baseline, one scope, compete-fail-closed.

**How:** bind a lock file to contract hash + git baseline + exact paths.
CAS update/release. Competing lock or stale baseline stops mutation.

Local kit v3.12.0 already has the runtime form (execution profile +
lease). A new user may start with a simpler lock. The **limit** is the
method: no second writer on the same scope.

**Must never claim:** a lock authorizes deploy, credentials, or owner
smoke.

---

## 8. Constraint types (numbered CN facts)

Record durable limits as numbered units (`CN-NNN`) in Project Map. Agents
retrieve them by id. They do not invent numbers.

How: `CONSTRAINT_CATALOG.md`. Template:
`constraint_catalog/CONSTRAINT_UNIT.template.yaml`. Method examples:
`constraint_catalog/EXAMPLE_METHOD_CONSTRAINTS.yaml`.

Product CNs (hosts, binaries, vendor trees) stay in the adopting project.

**Must never claim:** a scheme holds these facts; a missing SDK is
`compile_failed`.

---

## 8b. Hook functions (machine stop)

**Job:** fail-closed machine stop when a CN is about to be violated.

**How:** cards + example bytes in `proposed_hooks/`. Existing Cursor/Codex
example scripts remain. Combat-method additions: invoke wrapper (empty
stdout is deny), contract guard, execution profile, finalization,
encoding-safe writes.

**Limit:** unproven hooks are not protection. Crash or empty stdout on a
blocking event is deny.

**Must never claim:** a scheme or a CN text without a hook is enforcement.

---

## 9. Independent review and forensic

Already specified as function cards. Extra limits from live use:

- reviewer cross-checks cited vendor/docs when the behavior is
  platform-defined;
- forensic runs on an owner-windowed log, fail-closed on missing tokens;
- neither writes product.

---

## 10. Builder and deployer

Already specified as function cards. Extra limits:

- builder uses only the **registered** toolchain;
- deployer copies a hashed candidate with backup and readback;
- deployer does not launch the live UI and does not claim smoke PASS.

---

## 11. Architecture rationale vs apply

**Job:** `/how` and `/why` style reads (how a subsystem works, why a
threshold exists) are **read-only** functions.

**Limit:** they do not authorize apply, deploy, or map writes. Findings
that must survive go to Project Map or a scheme via owner-approved
update, not via side-effect from the rationale chat.

---

## 12. Owner-facing language (optional)

If the owner works in a language that is not the kit's English:

- default owner chat in that language;
- keep product/journal tokens in English;
- on first use of an English technical token, add a short gloss;
- paths, SHAs, contract ids stay untranslated.

This is a proposed communication contract, not a required locale.

---

## 13. What this catalog is not

- not your private skill tree;
- not your always-on rules;
- not your live atlas;
- not a claim that every project needs every function.

A stranger should be able to **see the same method** and then create
their own named agents, schemes, smoke skill, and contract lock.

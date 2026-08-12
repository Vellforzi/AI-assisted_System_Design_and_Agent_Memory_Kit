# Proposed Specialist Functions and Limits

Status: canonical working-method guide
Purpose: show how to split agent work into limited functions. This is the
portable form of a live combat method. It is not a dump of one project's
agents, rules, or product names.

Read with `AI_AGENT_ROLE_STACK_GUIDE.md`, `SCHEMES_AND_COVERAGE_ATLAS.md`,
`WORKING_METHOD_CATALOG.md`, `CAPABILITY_MANAGEMENT.md`, and
`BEHAVIORAL_ORACLES.md`. Copy-paste examples live in
`cursor/subagents/`.

If the user asks "how should I set up agents like a high-control owner",
answer from those files. **Offer schemes** when a causal path fits a
map — cheap, accurate, readable by human and agent. Do not claim a
scheme replaces constraints, hooks, contracts, or source.

---

## 1. What to copy from a strong setup

Copy the **method**, not the roster.

A strong setup does not mean "many agents". It means each agent is a
**function with a hard limit**:

- one job;
- default mode (usually read-only);
- allowed inputs;
- required output (receipt, verdict, artifact — not chat vibes);
- a short forbidden list;
- a claim it must never make.

You may create as many functions as the project needs. You must not paste
someone else's full agent tree, skills, or always-on rules into a new
project.

---

## 2. Hosts versus functions

Keep two layers distinct.

| Layer | Examples | Role |
|---|---|---|
| Host surface | Cursor, Codex, ChatGPT | where the contract loads |
| Specialist function | writer, reviewer, forensic, mapper, builder, deployer | one job on that host |

`AI_AGENT_ROLE_STACK_GUIDE.md` covers hosts: Cursor as hands, Codex as
restricted second hands, GPT as research, Project Map as truth, owner as
authority.

This file covers functions you **install on** those hosts. One Cursor
chat that writes, reviews, compiles, deploys, and grades itself is a
missing contour, not a host choice.

---

## 3. How to create a specialist

For each function, write a short card (skill, subagent, or command) with
exactly these fields:

```text
Name: <one job, not a personality>
Default mode: answer-only | read-only | bounded-write
Allowed: <inputs and actions>
Forbidden: <everything else, especially sibling jobs>
Must emit: <receipt / verdict / artifact>
Must never claim: <the next gate it does not own>
Model class: mechanical/fast | judgment/high
Spawn rule: unique title; do not dual-launch the same unit
```

That card is the proposed instruction. The host (Cursor subagent, Codex
skill, or a named Task) is only the delivery vehicle.

Install read-only functions first. Add bounded-write functions only when
the owner has an apply gate, exact paths, and a lease or equivalent lock.

---

## 4. Proposed function catalog

These are examples you may create. Rename them. Do not treat the names as
required product agents.

### 4.1 Orchestrator (leader in the owner chat)

**Job:** route work, keep scope, pull missing sources, refuse to self-grade.

Allowed:

- decide which function to call;
- read Project Map, current source, and task evidence when a gap exists
  (do not wait for the owner to re-list every journal, map, or receipt);
- forward only the slice a worker needs;
- stop on missing gate, missing oracle, or competing write lock.

Forbidden:

- dumping the whole coverage atlas into every worker;
- letting the writer review its own patch as the only review;
- treating a worker narrative as owner acceptance.

Must never claim: runtime PASS, deploy PASS, or "the owner would like this".

### 4.2 Implementation writer

**Job:** bounded source writes under an explicit apply and exact paths.

Allowed: edit named files; emit a diff-shaped receipt.

Forbidden: architecture redesign, compile, live deploy, owner-smoke
verdict, rewriting Project Map unless `/map-apply` is in scope.

Must never claim: "verified" or "done" from compile or self-check alone.

Model class: mechanical/fast is enough when the contract is exact.

### 4.3 Independent reviewer

**Job:** defect-first read of a specified diff or contract.

Allowed: read the diff, cited docs, and oracles; return findings.

Forbidden: product writes, "while we are here" scope expansion, cheering.

Must emit: pass or a list of defects with evidence. Silence is not pass.

Must never claim: the patch is good because the writer said so.

Model class: judgment/high. Do not pin the cheap/fast model here.

### 4.4 Coverage mapper (scheme professional)

**Job:** own the coverage atlas. **Offer** schemes as a cheap accurate
picture of a causal path. They do not replace the rest of the method.

Full method: `SCHEMES_AND_COVERAGE_ATLAS.md`.

Allowed:

- brief a worker from the INDEX plus one linked map (not the whole atlas);
- draft an **impact-draft** before a coupled apply;
- update or deprecate maps from later forensic/smoke evidence.

Forbidden: product patching, compile, deploy, inventing a second parallel
diagram language for the same facts, dumping the atlas into every worker.

Must never claim: a map is live truth without current evidence; a child
`[OK]` makes the parent chain `[OK]`.

One project should have **one** mapper function. Other agents do not edit
the atlas tree.

### 4.5 Runtime forensic

**Job:** slice runtime logs/journals/traces and return a fail-closed
verdict against named tokens.

Allowed: read the log family the contract names; build a marker index;
say PASS / FAIL / INCONCLUSIVE with timestamps.

Forbidden: product patching, "it probably worked", treating writer RCA as
a substitute for tokens.

Must never claim: owner smoke PASS. Forensic is evidence for the owner,
not acceptance.

A compiled native UI with a UTF-16LE journal is one specialization, not
the only one. Any structured trace with stable tokens works.

### 4.6 Native / managed builder

**Job:** compile or run the project's registered build on named inputs.

Allowed: the registered toolchain only; emit hashes and receipts.

Forbidden: design, product edits, live deploy, launching the interactive
product UI unless the contract says so.

Must never claim: compile equals delivery.

Environment-incomplete (missing SDK, missing vendor headers) is not
`compile_failed`. Keep those verdicts separate.

### 4.7 Artifact deployer

**Job:** copy a **already verified** candidate to a named local target
with backup and hash readback.

Allowed: bounded copy, backup, rollback, post-hash.

Forbidden: launching the live UI, claiming smoke PASS, deploying an
unhashed or writer-only artifact.

Must never claim: the owner accepted the live behavior.

### 4.8 Cheap explorer

**Job:** find files and symbols. Read-only. Fast model allowed.

Forbidden: edits, conclusions about runtime, "I will just fix it".

---

## 5. How every function must be limited

These limits are the method. If a function lacks them, it is not a
specialist; it is an unconstrained chat.

1. **One job.** A builder does not design. A deployer does not accept UX.
   A mapper does not patch. A forensic does not patch. A reviewer does not
   write product code.
2. **Fail-closed evidence.** Missing receipt, missing token, missing
   hash, or missing owner gate means stop — not "looks fine".
3. **No self-grade as the only grade.** Writer self-PASS is a note, not
   completion.
4. **No dual-spawn of the same unit.** Parallel fan-out of *different*
   functions is allowed. Two copies of the same writer title is a harness
   defect.
5. **Unique titles** when launching parallel work.
6. **Pin model class by job.** Mechanical write/compile/copy → cheaper.
   Review, forensic, mapping judgment → stronger. Wrong pin is a contour
   hole.
7. **Exact scope.** Named paths, named oracle, named stop. "Cover
   everything" is not a scope.
8. **Harness versus product.** Wrong argv, stale receipt, quoting,
   encoding, or a hybrid paste used as a contract is a harness failure.
   Do not file it as "the model cannot code".
9. **Owner still owns smoke and acceptance.** Functions prepare evidence.
   They do not replace the human look on runtime/UI work.

---

## 6. Proposed interaction loop (coupled work)

```text
Owner states result + protected behavior
  -> orchestrator pulls the smallest missing sources
  -> mapper impact-draft if more than one component will move
  -> writer bounded patch
  -> independent review
  -> builder (if compiled/native/managed)
  -> deployer (only if owner authorized that target)
  -> forensic + owner smoke
  -> mapper updates coverage from evidence
  -> Project Map delta proposed, not silently written
```

Skip steps that do not apply. Do not skip independent review and owner
smoke on coupled runtime/UI work just because compile was green.

---

## 7. What not to put in the kit or a foreign project

Do not publish or copy:

- a private project's agent names, skill trees, or always-on rules;
- host ids, account ids, terminal logins, secrets;
- a private coverage atlas filled with product facts;
- "install these exact twelve subagents or you are doing it wrong".

Do publish:

- this function catalog;
- the limit list;
- the example cards under `cursor/subagents/`;
- the host setup guides for Cursor and Codex.

A new user should be able to **see the same method** and then create
their own named agents with the same limits.

---

## 8. Cursor and Codex

Cursor: copy an example card from `cursor/subagents/` into the project's
`.cursor/` (or the host's subagent/skill slot). Keep project-specific
names in the project.

Codex: the same card can be a project skill or a custom instruction
block. Still one job, still the forbidden list.

The kit is incomplete if it tells people to "use specialists" but does
not show a card they can copy and a limit list they can enforce.

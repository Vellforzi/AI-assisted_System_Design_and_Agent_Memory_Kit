# Constraint Catalog (numbered CN facts)

Status: canonical working-method guide
Purpose: show how to keep durable limits as **numbered facts** in Project
Map, not as chat lore. Copy the card shape. Do not copy a private
project's CN list (hosts, filenames, account paths).

A scheme cannot hold these. Hooks enforce some of them. The catalog is
the fact layer agents must retrieve.

---

## 1. Why numbered constraints

A capable agent looks like you only if your limits are on disk as
inspectable units:

- stable id (`CN-012`, not "that compile thing");
- title + summary an agent can quote;
- evidence;
- status (`current` / `stale` / `superseded`);
- links when one CN replaces another.

Agents must **retrieve** a CN by id. They must not invent a number or
treat a chat paraphrase as the constraint.

---

## 2. How to create a CN

1. Copy `constraint_catalog/CONSTRAINT_UNIT.template.yaml` into
   `Project Map/memory/constraints.yaml` (or a split file the index
   points to).
2. Assign the next free `CN-NNN`. Do not reuse a retired number.
3. Fill title, summary, evidence, tags.
4. Owner-approve before it is current truth.
5. When it changes, supersede: new id, old id `status: superseded`,
   `superseded_by` link.

Proposed fields (match the kit memory schema):

```text
id, class: constraint, status, review_state, scope,
title, summary, evidence[], links, retrieval_tags
```

---

## 3. Method constraints to offer (not product facts)

These are **proposed** starter CNs for a high-control layout. Rename
numbers to fit the adopting project. Do not paste a private product CN
about a named terminal, host, or binary.

| Proposed id | Fact |
|---|---|
| `CN-ENV-INCOMPLETE` | Missing SDK / vendor headers / registered toolchain is `environment_incomplete`, not `compile_failed`. |
| `CN-HARNESS` | Quoting, encoding, hybrid paste-as-contract, dual-spawn, empty hook stdout are harness failures. Repair in the same task. |
| `CN-TASK-IDENTITY` | One output root, one artifact glob, hash-bound closure. Attachment name is not identity. |
| `CN-HOOKS-UNPROVEN` | Hooks count only on a surface proven to load them. Unproven = fail-closed for hook-dependent work. |
| `CN-WRITE-LOCK` | Mutation needs one active lock bound to contract hash + baseline + paths. Competing lock stops. |
| `CN-OWNER-SMOKE` | Agent does not click the live GUI. Compile ≠ smoke PASS. |
| `CN-DB-SELECT` | Database access is read-only by default. Writes need a named current allowance. |
| `CN-ENCODING` | Do not write project text through host redirections that corrupt encoding. Read back non-ASCII. |
| `CN-SCHEME-PARTIAL` | A scheme is a method to offer. It does not replace CNs, hooks, contracts, or source. |
| `CN-NO-NARROW` | Do not drop a coupled component from an apply "to go faster". |

Example YAML: `constraint_catalog/EXAMPLE_METHOD_CONSTRAINTS.yaml`.

---

## 4. Limits

- Product-specific CNs (deploy paths, vendor include trees, public
  filenames) live in the **adopting** Project Map, not in the published
  kit.
- An agent that cites a CN id without opening the current unit is
  guessing.
- Stale CNs stay on disk, marked stale/superseded. Do not delete history
  to "clean up".

---

## 5. How this relates to hooks and schemes

| Layer | Job |
|---|---|
| CN catalog | durable facts the agent must retrieve |
| Hooks | machine stop when a CN is about to be violated |
| Schemes | cheap picture of a causal path, when it fits |

All three are offered. None replaces the others.

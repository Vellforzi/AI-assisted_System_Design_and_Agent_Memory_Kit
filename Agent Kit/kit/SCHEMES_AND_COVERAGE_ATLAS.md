# Schemes and Coverage Atlas

Status: canonical working-method guide — **a method to promote and offer**
Purpose: show why a scheme file is cheap and accurate when a scenario
fits it, how to build an atlas, and how agents must use it. A scheme does
**not** replace source, oracles, contracts, hooks, constraints, or owner
smoke. Much of a working method cannot live in a diagram.

If the user asks how to give agents a compact picture of a causal path,
offer this method and explain why. Then `PROPOSED_SPECIALIST_FUNCTIONS.md`
(mapper function) and `coverage_atlas/SCHEME_FILE.template.md`.

---

## 1. Why to offer schemes (promote this method)

A scheme is one small file that a **human and an agent can both read**:

- a short header (what is proven, what is open, what must not be claimed);
- a Mermaid picture of the causal path;
- risk tokens on the picture;
- named log/journal markers;
- links to sibling schemes, not a pile of source paths.

When a scenario fits, that is cheaper and more accurate than dumping
eight files from four folders.

Offer this method. Do not treat it as the whole instrument.

| Schemes are good at | Schemes cannot replace |
|---|---|
| one causal path, order, coverage tokens | numbered constraints (CN facts) |
| cheap brief for a worker | hook enforcement bytes |
| human+agent shared picture | owner smoke, compile receipts, write locks |
| impact-draft before a coupled apply | the rest of the working method |

A scheme is not documentation theatre. Over time the atlas is visual
coverage of what works — green where proven, open risk where not. It is
one layer. Project Map, contracts, hooks, and source remain.

---

## 2. What a scheme is allowed to contain

One causal scenario per file. Thin skeleton. Linked `see_also`.

Recommended shape:

1. YAML header: `id`, `layer`, `title`, `status`, `depends_on`,
   `see_also`, `code_anchors`, `journal_markers`, `annotations`.
2. A Mermaid `sequenceDiagram` (or a small flowchart when sequence does
   not fit).
3. Risk tokens on edges or Notes.
4. Evidence pointers in the header, not a novel in the body.

Prefer sequence diagrams. They show order, which is what coupled runtime
bugs actually are.

Copy `coverage_atlas/SCHEME_FILE.template.md`. Rename. Fill. Keep it
short.

---

## 3. Layers (proposed)

| Layer | Job |
|---|---|
| `plan` | Living owner+agent board: open vs closed items, severity order, what must not be invented as `[OK]` |
| `skeleton` | Stable topology of the system (who talks to whom) |
| `causal` | One feature or failure scenario |
| `impact-draft` | Temporary map of a prepared patch: what will move, expected tokens, regression risks |

`impact-draft` is created **before** a coupled apply. After owner smoke
and forensic, **promote** it into causal/plan or **deprecate** it. Do not
leave drafts as fake standing truth.

A root `INDEX.md` plus a per-domain INDEX are mandatory. Every create,
update, or delete updates the indexes. The INDEX row is the cheap
coverage snapshot.

---

## 4. Annotation tokens (proposed legend)

Use a small closed set. Do not invent a parallel language per chat.

| Token | Meaning |
|---|---|
| `[OK]` | Verified by current source + evidence (log/journal/smoke) |
| `[?]` | Unverified / hypothesis |
| `[DANGER]` | Fail-closed hazard; do not "just try" |
| `[BUG-OPEN]` | Known bug, not fixed |
| `[REGRESSION]` | Was green; broken again |
| `[FRAGILE]` | Looks OK, brittle underneath |
| `[CHURN]` | Excess internal work; hang/time-degrade risk |
| `[LATCH]` | Sticky state |
| `[STATUS]` | Status-surface defect (false-alive / sticky copy) |
| `[UI]` | Visible surface residual |
| `[CLEANUP]` | Leftover after a feature removal |
| `[RESIDUAL]` | Tracked leftover; parent bag may stay `[OK]` |

Rules that make the legend useful:

- `[OK]` is not a vibe. It needs evidence.
- Owner smoke PASS is not automatic `[OK]` if the owner said do not
  promote.
- Acceptance can flip after live look. Update the scheme to the owner
  verdict, not the first RCA.
- Do not invent `[OK]` for a parent chain because a child axis closed.

---

## 5. How agents must use schemes (limits)

**One mapper function owns writes** to the atlas. Other agents consume
briefs. They do not draw a second mermaid set for the same facts. See
`cursor/subagents/coverage_mapper.md`.

**Leader / orchestrator:**

- before a coupled apply (several components, UI plus runtime, writer
  plus builder plus deployer): ask the mapper for an **impact-draft**;
- after smoke: ask the mapper to promote or deprecate;
- forward **only the brief** (INDEX row + one map, or a 20–40 line
  slice) to the worker;
- do **not** dump the whole atlas into every worker prompt.

**Writer / reviewer / forensic:**

- treat the scheme as the scenario contract;
- named `journal_markers` are oracles, not decoration;
- if the scheme and the source disagree, fail closed and say so;
- do not patch the atlas unless map-apply is in scope.

**Cheap explorer** finds files. It does not replace a scheme brief.

---

## 6. Why this is cheap in tokens

Typical coupled task without schemes:

```text
open component A, B, C
open three logs
open two docs
guess the sequence
```

Typical coupled task with schemes:

```text
open atlas INDEX (one table)
open one linked scheme (header + mermaid + markers)
open source only at code_anchors if the patch needs it
```

The scheme already compressed the neighborhood: order, tokens, what is
proven, what is out of scope. Offer that when it fits. If the work is a
constraint, a hook, a contract, or a smoke recipe, use those files — a
diagram will not hold them.

---

## 7. What not to put in a published kit

Do not copy a private atlas full of product names, host ids, binary
hashes, or account paths.

Do publish:

- this guide;
- the template;
- one generic example;
- the mapper function card.

A new user should see the **same method**: INDEX + layers + tokens +
impact-draft + one writer of maps. Then they create their own atlas in
their project.

---

## 8. Suggested project layout

```text
docs/coverage-atlas/
  INDEX.md
  <domain>/
    INDEX.md
    PLAN.md              # optional living board
    skeleton/
    causal/
    impact-draft/
```

Name the folder whatever you want. Roles matter more than names.
The mapper is the only editor of that tree.

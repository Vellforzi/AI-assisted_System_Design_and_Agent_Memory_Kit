# Capability Management: Model, Contour, and Operator

Status: canonical positioning supplement
Purpose: state the capability claim this kit is built to test without pretending
that constraints can replace model reasoning or human judgment.

Read with `MOTIVE_AND_ANALOGY.md`, `QUESTIONS_THIS_KIT_ANSWERS.md` and `BEHAVIORAL_ORACLES.md`.

The contour is how you lay your method on disk. A capable model operating
that layout looks like you. A foolish model plus folders does not. See
the analogy in `MOTIVE_AND_ANALOGY.md`.

---

## 1. The claim

Agent output quality is a weakest-link system, not a contest between model IQ
and process. Use this qualitative model:

```text
result quality ~= model capability x constraint contour x current evidence x operator judgment
```

A constraint contour is the set of things the agent cannot skip:

- what counts as project truth;
- answer-only default;
- explicit mutation gates;
- exact scope;
- behavioral oracles;
- independent review;
- owner smoke / acceptance;
- eval cases grown from real failures.

A capable model, unconstrained, can produce plausible garbage. Inside a good
contour it can move a messy codebase toward a working product while the owner
avoids reading every generated line. But a contour cannot manufacture reasoning:
a model below the task's capability floor will misunderstand or ignore the
layout. More files then become more unread context.

The operator is the fourth factor. A strong model inside a strong contour can
still build the wrong product when the person provides an ambiguous outcome,
chooses an inadequate model to save money, or accepts a result without judgment.
The kit manages capability; it does not replace the model or the person.

---

## 2. What "managing capability" means here

Managing capability is not "write a longer prompt". It is installing a
system the agent has to pass through:

| Contour piece | Kit surface |
|---|---|
| Grounding | Project Map + `PROJECT_GROUNDING_CONTRACT.md` |
| Intent | `ACTION_INTENT_CONTRACT.md` |
| Scope | task contract, allowed-scope, path zones |
| Routing | `EXECUTOR_ROUTING_GATE.md`, `EXECUTION_PROFILE_GATE.md`, Context Advisor |
| Memory lifecycle | stale/superseded facts, checkpoints, handoffs |
| Delivery evidence | `BEHAVIORAL_ORACLES.md` |
| Regression memory | `eval_suite/` |
| Host actually loads the rules | Cursor pack + Codex pack |

If the host does not load the rules, the contour is theater. Setup guides
are therefore part of the product, not optional docs.

---

## 3. The veteran pattern, abstracted

Some experienced owners stop reading agent-written product source as the
primary quality method. They surround the agent with a chain: tests,
acceptance scenarios, QA procedures, quality metrics, mutation testing,
coverage, and similar gates. Confidence comes from the chain, not from
eyeballing every function.

This kit is the same idea in portable form.

It does **not** require you to copy that exact toolchain. Structural unit
tests are one possible chain. Behavioral oracles, hash pins, independent
review, and owner-gated runtime smoke are another. The kit prefers the
second chain when the product is large, generated, or unpleasant to read
line by line (native UI, compiled plugins, generated bindings).

---

## 4. The common objection

A frequent reply to the veteran pattern:

- you cannot write unit tests without reading the code;
- acceptance tests can be written from the outside; units cannot;
- "cover everything with unit tests" will rot;
- this only works for small personal utilities you could rewrite from
  scratch;
- people who skip reading code are hyping, or they do not ship large
  systems.

### What is true in that objection

Classic **structural** unit tests encode internals: function names, private
helpers, call order, mock graphs. Writing those tests without reading the
implementation is usually theater. A prompt that says "cover everything
with unit tests" is a bad oracle. It rewards volume, not behavior.

Owner acceptance of look-and-feel still requires a human. The kit does not
delete that gate.

### What is false in that objection

Confidence without reading every product line is not limited to throwaway
utilities.

The substitution is not "skip tests". The substitution is:

- **behavioral oracles** instead of structural unit tests as the primary
  chain;
- **independent review** by a role that did not write the patch;
- **fail-closed evidence** (missing receipt = not done);
- **owner smoke** for runtime/UI, not agent self-PASS.

A large coupled system (compiled native UI + host process + settings
surface + logs) can be steered this way. The owner still owns acceptance.
The owner does not have to be the compiler of ten thousand generated
lines.

See `BEHAVIORAL_ORACLES.md` for the practical chain.

---

## 5. What the owner still does

Skipping line-by-line product reading is not "never look at anything".

The owner still:

- states intent and protected behavior;
- grants or withholds apply / deploy / credentials;
- runs or watches runtime smoke when the contract requires it;
- can flip acceptance after seeing the live system (the first RCA is not
  sacred);
- rejects work that passed local checks but feels wrong.

That last point matters. A consistent internal story can still be the
wrong product. Owner smoke outranks agent narrative.

The kit may reduce the owner's clerical work, but it does not remove the
owner's work of thinking. The owner still selects the capability level, defines
meaning, resolves material trade-offs and owns acceptance. See
`HUMAN_MODEL_CAPABILITY_CONTRACT.md`.

---

## 6. Specialist split

One chat where the same model writes, reviews, compiles, deploys, and
grades itself is how people conclude agents cannot ship.

The kit's role stack is the opposite: separate writer, reviewer, and
evidence roles; keep compile/deploy as bounded specialists; keep forensic
or black-box evidence independent of the writer. See
`AI_AGENT_ROLE_STACK_GUIDE.md` for hosts and
`PROPOSED_SPECIALIST_FUNCTIONS.md` for functions you may create, with
limits. Copy the method, not a private project's agent roster.

Using one model for everything without checking task fit is a capability-management
failure. Using a model below the task's capability floor is also a
capability-management failure. Neither folders nor role names erase the model's
actual limits.

**Schemes** are a method to offer: cheap, accurate, human+agent readable
when a causal path fits a map. They do not replace the contour. See
`SCHEMES_AND_COVERAGE_ATLAS.md`.

---

## 7. Label versus pipeline

When a UI string, status line, or banner looks "stuck", classify before
blaming the model:

| Class | Meaning | Typical fix |
|---|---|---|
| A | Cosmetic / copy / projection | Change the label or the status formula |
| B | Weak local feedback / state machine | Hold, debounce, or recompute locally |
| C | Real lifecycle or transport lock | Registration, yield, queue, host busy |

Treating A as C wastes a deploy. Treating C as "the agent is stupid"
wastes a rewrite. The kit requires evidence tokens for C, not vibes.

---

## 8. What would falsify the claim

The claim is empirical. It would be weakened if, with a loaded contour
(gates, oracles, independent review, owner smoke), agents still could not
move a large project toward working behavior over repeated cycles.

It is not falsified by unconstrained chat producing junk. That is the
control condition.

---

## 9. How this kit should be used in an argument

Do not argue "models are better than seniors". Argue:

1. unconstrained agents match the junk people already saw;
2. the missing piece is the contour, which this package installs;
3. confidence comes from oracles and owner smoke, not from pretending
   structural unit tests were written without reading code;
4. Cursor and Codex must actually load the contour, or the demo is fake.

Point people at this file, `BEHAVIORAL_ORACLES.md`, and the Cursor/Codex
setup guides. Do not point them at a private product repository.

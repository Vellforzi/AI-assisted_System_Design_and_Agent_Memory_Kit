# Behavioral Oracles and Owner Smoke

Status: canonical delivery-evidence guide
Purpose: explain how an owner can gain confidence in agent-written work
without reading every generated line, and without pretending that
structural unit tests were authored blind.

This is the practical half of `CAPABILITY_MANAGEMENT.md`.

---

## 1. Compile is not done

A green compiler, a passing local test list written by the same agent, or
an agent saying `PASS` is not completion.

Completion needs an **oracle**: an observable that would fail if the
protected behavior is missing. The oracle must be named before or with the
apply, not invented after the agent wants to stop.

---

## 2. Two kinds of tests (do not mix them)

| Kind | Encodes | Can you write it without reading product source? |
|---|---|---|
| Structural unit tests | internals, helpers, call order, mocks | Usually no. The objection is right here. |
| Behavioral oracles | inputs, outputs, logs, hashes, UI postconditions | Yes, from owner intent and public contracts. |

This kit does not tell you to skip tests. It tells you not to use
structural unit tests as the *primary* confidence chain when you are not
reading the implementation.

"Cover everything with unit tests" is a bad owner prompt. It asks for
volume against internals. Prefer: name the behavior, name the observable,
name the fail-closed evidence.

---

## 3. Oracle catalog (portable)

Use the smallest set that matches risk.

| Oracle | What it proves | Typical evidence |
|---|---|---|
| Contract / schema | the change still speaks the published shape | fixture, golden header, schema check |
| Hash pin | the artifact you deployed is the artifact you built | SHA of binary / bundle, readback after copy |
| Trace token | a named runtime event happened or did not | log/journal line, structured event id |
| Independent review | a second role that did not write the patch found no defect in scope | review receipt, not the writer's self-check |
| Targeted check | a specific command the owner could run | test id, script, expected output |
| Owner smoke | the live system matches intent | screenshot, timestamped log slice, owner verdict |
| Eval case | this failure mode cannot silently return | kit or Project Map eval case |

Missing evidence is fail-closed. Do not substitute a writer narrative for
a missing token.

---

## 4. How to write an oracle without encoding internals

Good oracle (behavioral):

```text
After the owner action A, the status line must show phrase P, and the
runtime log must contain TOKEN_X within N seconds. TOKEN_Y must be absent
after timestamp T.
```

Bad oracle (structural):

```text
Function FooBar must call helper_baz exactly twice and set m_quux to 3.
```

The first can be written from owner intent. The second is a unit test that
requires reading the code — and it will rot when the helper is renamed.

For coupled runtime/UI work, prefer trace tokens plus owner smoke. For
pure functions with a stable public API, structural unit tests are fine
and the owner may still not read every line if the tests were reviewed as
behavior, not as a mock novel.

---

## 5. Owner smoke is a human gate

Runtime and UI work needs a human look. The kit does not automate away
"does this feel right on the live surface".

Rules:

- the agent may prepare the recipe, timestamps, and log slice;
- the owner supplies the acceptance verdict;
- the owner may flip acceptance after seeing the live system;
- when acceptance flips, update the durable docs to the **owner verdict**,
  not to the first agent RCA.

A consistent RCA can still describe the wrong product. Example shape
(abstract): a local hold that made a status line look "ready" can be
technically coherent and still be rejected because sibling surfaces do not
work that way. The contour must follow the owner, not the clever patch.

---

## 6. Label versus pipeline (use with oracles)

Before spending a deploy on a "stuck" UI string:

- **A** — copy / projection / formula. Oracle: the string and the inputs
  to the formula.
- **B** — local feedback machine. Oracle: a hold/debounce token, then the
  later ready token.
- **C** — lifecycle or transport lock. Oracle: registration, busy, queue,
  or host-error tokens. Do not treat a cosmetic string as proof of C.

---

## 7. Independent review

The writer must not be the only grader.

Minimum for coupled work:

- a reviewer role that did not author the patch;
- a written defect-first result (pass is allowed; cheerleading is not);
- no silent scope expansion during review.

See `AI_AGENT_ROLE_STACK_GUIDE.md`. Same-model-all-hats is a contour hole.

---

## 8. What this is not

- not "never look at anything";
- not a license to skip owner smoke;
- not a claim that structural unit tests are useless;
- not a claim that compile receipts equal runtime proof;
- not permission to publish, deploy, or use credentials.

---

## 9. Extraction note for kit maintainers

When a private project invents a strong oracle (a journal token, a pin, a
smoke recipe), copy the **shape** into this file or an eval case. Do not
copy product names, host ids, or account-specific paths into the published
kit.

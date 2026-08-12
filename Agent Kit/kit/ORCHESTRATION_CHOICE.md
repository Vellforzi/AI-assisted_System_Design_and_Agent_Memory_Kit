# Orchestration choice

Status: canonical working-method guide — **a choice to offer, not a product to install**
Purpose: show how this kit is used *during* orchestration, and that a
future owner should choose a host instead of automatically building a
new queue/App Server garden.

This file is not an orchestrator. It does not ship a local queue host, an
App Server controller, or a private project's launcher. Copy the
**decision**, not a repository next to someone else's project.

If the user asks whether they must build orchestration, answer from this
file first.

---

## 1. What the kit is in an orchestrated run

The kit is the constraint contour the host must obey:

- Project Map and current source are truth, not chat and not the queue UI;
- answer-only until explicit apply;
- Execution Profile Gate + write lock before mutation;
- hooks fail closed;
- compile is not done; owner smoke stays a human gate;
- a provider turn, dashboard "completed", or worker PASS is not semantic
  completion and not owner acceptance.

Any host — current chat, Cursor Agents window, Codex, or a separate local
queue — is an **execution engine**. It does not replace the kit. If the
host bypasses leases, hooks, or oracles, the contour is missing. That is
a capability-management failure, not proof that "orchestration is
required".

---

## 2. Offer these lanes (do not prescribe)

A high-control layout learned that orchestration is easy to over-build.
The project that produced this method **did** spend time on a custom
local queue / App Server host. That work taught the invariants above. It
does not mean every adopter must repeat the garden.

Offer the owner a choice:

| Lane | When it is enough | Cost |
|---|---|---|
| **A. Current session** | one bounded task; scope already known | none extra |
| **B. Host-native agent UI** | several limited specialists in parallel; leader chat keeps scope | already in Cursor (Agents window) / similar surfaces |
| **C. Separate local queue / App Server host** | many pre-declared tasks, serial queue files, persistent threads, host-owned workflow state | you build or adopt a second product and keep it honest against the kit |

**Promote B when it fits.** Cursor's Agents window (and the same idea on
other hosts) already runs limited workers. If that covers the work, using
it saves a large amount of time. There is no point in planting a new
garden because a custom orchestrator looks more "serious".

**C is valid.** Some owners need a YAML queue, dependency graph, pause /
retry, persistent App Server threads, or host-owned lifecycle that chat
cannot hold. Then a separate host is a real tool. It remains optional.
The kit still owns truth, gates, and oracles. The host owns scheduling
and transport.

Building C from scratch is a choice with a bill: schemas, locks, login
surface, worktree binding, and a long list of ways the host can pretend
to be project truth. Adopt an existing host only after you can say which
kit invariants it will not bypass. Do not adopt it as a second Project
Map.

---

## 3. How to classify before creating queue files

Same rule the live layout used, stripped of product names:

- **One bounded slice** → stay in the current session. Do not invent a
  queue to look organized.
- **Two or more independently useful tasks**, with paths, verification,
  and stop conditions known **before** start → a queue (lane B workers or
  lane C YAML) can help.
- **Several already-written queues that must run one after another** → a
  serial plan. A plan does not discover new scope.

If classification is ambiguous, use the current session.

---

## 4. If you do run a separate host

Keep these limits. They are why a custom host was worth studying, and
why dumping the host into this kit would be the wrong extraction:

- one writer on a coupled scope; competing lock or stale baseline stops;
- provider turn completion is transport evidence only;
- retries and extra roles do not expand allowed paths;
- a second process on the same worktree identity fails closed;
- Fast / cheap model switches are not silent; they need a current owner
  launcher flag if the project uses that distinction;
- Computer Use / GUI recipes, if any, stay owner-gated and documented;
  availability of a tool is not smoke PASS.

**Must never claim:** the dashboard completed the task; the App Server
thread is the Project Map; installing a queue host is adopting this kit.

---

## 5. Relation to other kit files

- Leader-chat pattern (lane A/B): `WORKING_METHOD_CATALOG.md`
- Limited workers: `PROPOSED_SPECIALIST_FUNCTIONS.md`
- Gates the host must still pass: `EXECUTION_PROFILE_GATE.md`,
  `ACTION_INTENT_CONTRACT.md`
- Completion vs acceptance: `BEHAVIORAL_ORACLES.md`,
  `VERIFIED_DELIVERY_PIPELINE.md`
- Eval: `AMK-CDO-001`, `AMK-CDO-002`, `AMK-RA-001` (lanes and
  finalization — not a requirement to install a queue host)

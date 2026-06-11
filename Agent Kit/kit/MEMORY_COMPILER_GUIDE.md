# Memory Compiler Guide

Status: portable guide
Purpose: define how session notes, owner statements, project evidence, and tool outputs become durable Project Map memory.

---

## 1. Why a compiler is needed

Agents often capture too much, too little, or the wrong thing.

A memory compiler prevents long-term memory from becoming:

- a transcript dump;
- a pile of duplicate facts;
- a mix of old and new truths;
- unverified research claims;
- unsupported assumptions;
- instructions without source authority.

---

## 2. Two-phase memory process

### Phase A: hot-path capture

During the active task, capture only compact notes:

- owner decisions;
- verified facts;
- unresolved questions;
- blockers;
- side-effect receipts;
- candidate memory;
- links to evidence.

Do not try to perfectly consolidate everything while executing the task.

### Phase B: consolidation

After the task or at a session boundary:

1. Review candidate notes.
2. Deduplicate.
3. Resolve conflicts.
4. Check evidence.
5. Promote verified or owner-approved items.
6. Mark stale or superseded items.
7. Update indexes.
8. Update current state and working state.

---

## 3. Promotion rules

Promote to durable memory only when the item is:

- project-specific;
- likely useful later;
- supported by valid evidence or owner approval;
- compact;
- scoped;
- linked to related memory;
- safe to store.

Do not promote:

- unsupported assumptions;
- generic advice;
- raw research as project fact;
- temporary task chatter;
- secrets or credentials;
- model guesses.

---

## 4. Candidate memory format

```yaml
candidates:
  - id: CAND-0001
    captured_at: "2026-06-08T12:00:00Z"
    proposed_class: accepted_decision
    scope: project.memory
    title: "Use Project Map as source of project truth"
    summary: "The owner wants project-specific answers to be grounded in Project Map and project evidence, not model memory."
    source:
      kind: owner_statement
      ref: "current chat"
    evidence:
      - kind: owner_statement
        ref: "current chat"
    proposed_action: promote
    requires_owner_confirmation: false
```

---

## 5. Consolidation output

A consolidation pass should produce:

- promoted memory units;
- updated lifecycle links;
- updated index entries;
- updated current state if needed;
- updated Working State if needed;
- conflict notes;
- owner questions.

---

## 6. Conflict handling

When a candidate conflicts with current memory:

1. Compare authority.
2. Compare recency.
3. Compare evidence quality.
4. If the candidate wins, supersede the old item.
5. If the old item wins, reject or archive the candidate.
6. If unclear, leave both visible and ask the owner.

Never silently overwrite a durable fact.

---

## 7. Research-output handling

Research output can be useful, but it is not automatically project truth.

Possible destinations:

| Research content | Destination |
|---|---|
| General method insight | `knowledge_reusable` or procedure note |
| Suggested project change | candidate decision or task proposal |
| Claim about current project | not valid unless project evidence supports it |
| External source quote | raw source / evidence ref |
| Risk pattern | risk candidate |

---

## 8. Manual consolidation prompt

```text
Mode: dry-run or apply.
Scope: Project Map only.
Task: consolidate session notes into Project Map memory.
Use the Memory Compiler Guide.
Do not promote unsupported assumptions.
For each proposed memory update, show: class, status, evidence, lifecycle effect, and index change.
Do not change files unless mode is apply and scope is explicit.
```


---

## 11. Action-intent boundary during compilation

Do not compile conversation content into durable memory just because the agent discussed it.

Durable memory compilation requires one of:

- explicit owner request to remember/update memory;
- approved task contract that includes memory maintenance;
- owner approval of a proposed memory delta.

If the current interaction was answer-only, the compiler may propose candidate memory but must not apply it.

---

## 12. Claim-ledger integration

When consolidating a complex session, use claim-ledger thinking:

1. extract project-specific claims;
2. identify evidence refs;
3. mark claims as verified, inference, missing evidence, conflict, or rejected;
4. promote only supported claims;
5. keep unsupported claims as candidate/hypothesis/open question;
6. never promote external research directly into project truth.

---

## 13. Significant-work filter

Before compiling memory, apply the significant-work filter from `SIGNIFICANT_WORK_AND_CHECKPOINTS.md`.

Compile only items that changed or clarified future-relevant project state:

- verified facts;
- accepted or rejected decisions;
- constraints;
- risks;
- open questions;
- stale/superseded facts;
- source authority changes;
- permission or retrieval policy changes;
- task checkpoints;
- side-effect receipts;
- repeated failures that should become eval cases.

If the conversation was useful but not durable, do not compile it.

---

## 14. Failure-to-eval output

When compilation sees a repeated or critical agent failure, do not store only a vague note.

Produce a candidate eval case using:

```text
Project Map/eval_suite/failure_to_eval_case_template.yaml
```

This keeps the failure testable in future releases.

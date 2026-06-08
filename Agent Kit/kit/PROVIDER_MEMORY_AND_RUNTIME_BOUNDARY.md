# Provider Memory and Runtime Boundary

Status: portable boundary guide  
Purpose: prevent confusion between owner-controlled Project Map memory, provider-level personalization memory, IDE/repository instruction files, and agent runtime state.

---

## 1. Core rule

Provider memory is not the Project Map.

An AI provider, IDE, coding agent, or chat product may keep personalization notes, repository notes, session state, conversation history, summaries, traces, or tool outputs. These systems can be useful, but they are not the authoritative project memory unless the owner deliberately exports, verifies, and promotes the information into the Project Map.

---

## 2. Memory layers

Use this separation:

| Layer | Owner-controlled? | Use | Project authority? |
|---|---:|---|---:|
| Current user instruction | Yes | immediate intent and scope | Yes |
| Project Map | Yes | durable project memory | Yes |
| Project files/tool outputs opened in current run | Yes, if scoped | current evidence | Yes |
| Repository instruction files | Mostly | behavior and workflow rules | Partial: instructions only |
| Provider memory / chat history | Partly | personalization and reminders | No, unless promoted |
| Runtime session state | Partly | current agent loop state | No durable authority by itself |
| External research | No | general public context | No project truth unless confirmed |

---

## 3. Safe uses of provider memory

Provider memory may safely store or recall:

- high-level owner preferences;
- preferred response style;
- reminders that the owner uses Agent Memory Kit;
- general workflow habits;
- a pointer to where the owner keeps Project Map;
- non-sensitive repeated instructions such as "answer-only is default".

Even then, current user instruction and Project Map take precedence.

---

## 4. Unsafe uses of provider memory

Do not rely on provider memory for:

- credentials, tokens, passwords, access details, or private keys;
- exact project state;
- current file structure;
- current API routes, database tables, or deploy state;
- accepted project decisions unless mirrored in Project Map;
- business rules unless verified;
- side-effect receipts;
- task checkpoints;
- conflict resolution.

If the agent recalls such information from provider memory, it must treat it as a hint to verify, not as evidence.

---

## 5. Recommended storage model

For a solo owner:

```text
Owner-controlled storage:
  Project Map/                 # durable project memory
  AGENTS.md or tool rules       # short always-loaded instruction entrypoint
  git repository                # code and docs
  local encrypted vault         # secrets, never pasted into memory

Provider-controlled or tool-controlled storage:
  chat memory                   # style and personal preferences only
  IDE agent memory              # convenience notes only
  provider traces/sessions      # debugging and continuity, not source of truth
```

The Project Map should remain portable: Markdown and YAML are preferred unless a runtime database is intentionally introduced.

---

## 6. Promotion rule

Provider memory can become Project Map memory only through a promotion step:

1. Agent states what it recalls and labels it as provider-memory hint.
2. Agent checks Project Map or scoped project files if allowed.
3. Owner confirms or provides evidence.
4. Agent creates a candidate memory card.
5. Owner approves durable write.

No automatic promotion.

---

## 7. Runtime-state boundary

Runtime session state is useful for active work, but it is not enough for durable project continuity.

The runtime may store:

- tool calls;
- intermediate observations;
- temporary notes;
- current loop state;
- trace spans;
- interruptions;
- approvals;
- compacted conversation history.

Project Map should store only the durable result:

- verified facts;
- accepted decisions;
- current state;
- working state checkpoints;
- task cursor;
- side-effect receipts;
- handoff packets;
- open questions;
- eval results worth preserving.

---

## 8. Practical instruction for agents

When uncertain whether something came from Project Map or provider memory, say so.

Use this label:

```text
[provider-memory hint; not project evidence]
```

Then either verify against Project Map / project files, ask the owner, or omit the claim.

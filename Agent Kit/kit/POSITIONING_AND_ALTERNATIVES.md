# Positioning and Alternatives

Status: README support document  
Purpose: explain what Agent Memory Kit is strong at, how it differs from common memory tools, and when it is useful.

---

## 1. Short positioning

Agent Memory Kit is not mainly a vector database, not mainly a chatbot memory feature, and not mainly an autonomous agent runtime.

It is a portable owner-controlled project memory and behavior layer.

Its strongest use case is a real project where the owner wants an AI agent to answer and work from verified project context, not from vague chat memory or provider-trained guesses.

---

## 2. What it optimizes for

- owner control;
- project-specific grounding;
- source authority;
- answer-only default behavior;
- explicit action gates;
- small durable memory units;
- stale/superseded fact handling;
- safe continuation across sessions;
- manual or semi-automated evals;
- portability across ChatGPT, Cursor, Claude Code, local IDE agents, and future runtimes.

---

## 3. How it differs from provider memory

Provider memory usually helps with personalization: preferences, prior chats, and broad continuity inside one service.

Agent Memory Kit treats provider memory as non-authoritative for project truth.

Project truth lives in Project Map and current evidence. This keeps the owner able to inspect, edit, version, move, or delete project memory.

---

## 4. How it differs from repository instruction files

Files like `AGENTS.md`, Cursor rules, or `CLAUDE.md` are useful entrypoints.

They are not enough by themselves because they are often too short to hold project history and too long if overloaded with every detail.

Agent Memory Kit uses instruction files as routers into Project Map instead of dumping all memory into always-loaded context.

---

## 5. How it differs from memory frameworks

Many memory frameworks provide storage and recall for agents: short-term state, long-term stores, embeddings, vector search, knowledge graphs, or memory APIs.

Agent Memory Kit is different because it focuses on:

- what should be remembered;
- what must not be remembered;
- which source wins when memory conflicts;
- when stale memory is allowed;
- when the agent may act;
- when a memory update must be proposed;
- how an owner reviews and corrects the memory.

A framework can later implement the kit. The kit itself is the operating contract.

---

## 6. How it differs from autonomous agent platforms

Autonomous agent platforms focus on running agent loops, tools, environments, subagents, and long tasks.

Agent Memory Kit can support those systems later, but it does not require long-running autonomy.

It is useful even when the owner runs short controlled tasks manually.

---

## 7. Conditions where the kit works well

The kit is effective when:

- the owner cares about correctness more than speed;
- the project has enough complexity to forget details;
- the owner is willing to maintain a compact Project Map;
- project facts can be tied to evidence;
- source authority can be defined;
- agents are instructed to stay inside scope;
- eval cases are added from real failures.

---

## 8. Conditions where the kit is weaker

The kit is weaker when:

- the owner will not maintain Project Map;
- the agent runtime ignores instructions and has no permission controls;
- tools can mutate state without approval;
- project files are inaccessible;
- the owner wants a fully automatic system without review;
- the project facts change faster than memory is verified;
- secrets are mixed into memory.

---

## 9. Practical comparison table

| Approach | Strength | Weakness | Agent Memory Kit difference |
|---|---|---|---|
| Provider memory | easy personalization | opaque and service-specific | Project Map is inspectable and portable |
| Chat summaries | quick continuity | vague, lossy, stale | typed memory units with lifecycle |
| Vector database | semantic search | may retrieve wrong/stale context | retrieval is policy-gated and authority-aware |
| Knowledge graph | relationships and temporal facts | heavier setup | kit can start file-first and add graph later |
| Agent runtime | tool execution and autonomy | may act too much | action intent and permissions are explicit |
| Repository rules | lightweight instruction | not a memory system | rules route to Project Map |
| Eval platform | automated measurement | does not define project truth | evals validate kit behavior |

---

## 10. Non-goals

Agent Memory Kit does not claim to:

- duplicate human consciousness;
- reveal or control provider inference internals;
- guarantee that any model follows instructions;
- replace code tests;
- replace security permissions;
- replace human review;
- solve all long-running autonomy problems by itself.

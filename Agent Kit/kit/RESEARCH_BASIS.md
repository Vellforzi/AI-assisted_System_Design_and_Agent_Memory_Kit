# Research Basis for Agent Memory Kit v3.8.0

Status: design rationale  
Purpose: record the external engineering ideas that influenced this release.

---

## 1. Main influences

This release is based on the following engineering patterns:

1. Context is a finite resource. Agents should curate the smallest useful set of high-signal tokens instead of loading everything.
2. Project memory should be external, structured, and inspectable rather than hidden in chat history.
3. State-based memory is often more reliable than loose retrieval over prior conversation when continuity, priorities, and overrides matter.
4. Project-specific claims require grounding, source references, and missing-context handling.
5. Retrieval failures are a first-class failure mode: the agent can receive wrong context, too little context, or too much irrelevant context.
6. Long-running tasks need compact working state, task contracts, checkpoints, handoffs, and replay safety.
7. Tool responses should be concise by default, detailed on demand, paginated when large, and explicit about errors.
8. Stale facts should not be deleted silently; they should be lifecycle-managed and excluded from normal answer context.
9. Permission mode is not action intent. Agents should not mutate state when the user only asked a question.
10. Unsupported claims should be made invalid by process: claim ledger, final-answer gate, and source authority.

---

## 2. Source list

Use the current versions of these sources when maintaining the kit:

- Anthropic, "Effective context engineering for AI agents".
- Anthropic, "Writing effective tools for AI agents".
- Anthropic, "Effective harnesses for long-running agents" and related harness design materials.
- Anthropic, "Building effective agents".
- Anthropic, "Demystifying evals for AI agents".
- OpenAI, "Prompt guidance".
- OpenAI, "Optimizing LLM Accuracy".
- OpenAI Cookbook, "Context Engineering for Personalization — State Management with Long-Term Memory Notes".
- OpenAI developer materials on long-horizon Codex tasks and durable project memory.
- LangChain / LangGraph memory concepts: short-term state, long-term memory, semantic memory, episodic memory, procedural memory, checkpoints, persistence, and interrupts.
- Retrieval-Augmented Generation literature for grounding knowledge-intensive tasks in retrieved external context.

---

## 3. How these ideas are used here

| External idea | Agent Memory Kit design response |
|---|---|
| Context is limited and degrades when overloaded. | Minimal memory intake, indexes, retrieval profiles, concise memory tool responses. |
| Missing context should not be guessed. | Project Grounding Contract and missing-context gating. |
| State-based memory supports continuity and conflict handling. | Current State, Working State, task contracts, lifecycle fields, source authority. |
| Retrieval can fail by returning wrong or noisy context. | Retrieval profile matrix, empty-result recovery, audit/repair modes. |
| Tool descriptions and outputs steer agents. | Memory Tool Interface Contract with natural IDs, concise/detailed modes, pagination, actionable errors. |
| Long tasks need replay support. | Working State, task contracts, handoffs, checkpoints, side-effect receipts, idempotency keys. |
| Research output is not automatically truth. | Memory Compiler promotion rules and research-output handling. |
| Agents can over-act when instruction boundaries are vague. | Action Intent Contract and Permissions Policy. |
| Unsupported claims are difficult to catch in free text. | Claim Ledger and final-answer gate. |

---

## 4. Eval-suite rationale

v3.8.0 adds a portable eval-suite because memory systems fail in recurring, testable ways:

- unsupported project claims;
- stale fact poisoning;
- action without explicit intent;
- external research promoted to project truth;
- over-retrieval of raw logs;
- branch leakage;
- missing side-effect receipt checks;
- memory compiler over-promotion;
- provider memory treated as project authority.

The eval-suite is intentionally lightweight and file-based. It is not an agent benchmark and does not measure general intelligence. It checks whether an agent follows the kit contracts under realistic owner prompts.

Manual owner review remains authoritative. Eval results are regression signals, not correctness guarantees.

---

## 5. Remaining intentional omissions

This release still does not include:

- a runtime memory database;
- a vector index;
- an autonomous long-running agent harness;
- provider-specific API code;
- automatic mutation of project files;
- secret storage.

These are implementation choices for the project owner or future runtime layer.

---

## 6. v3.8.0 Codex integration basis

v3.8.0 adds Codex integration because Codex can operate as a second controlled agent surface over the same Project Map.

The design is based on these practical assumptions:

- Codex configuration can be managed through `config.toml`.
- Codex hooks can be loaded from user-level or project-level hook files.
- Codex permission profiles should start from least privilege, usually read-only.
- Codex compaction is a recoverability boundary, not a memory-authority event.
- Codex Skills and Subagents are useful only when they remain scoped and governed by Project Map, Source Authority, Task Contract, and owner approval.

The kit treats Codex as an execution and review surface, not as durable memory.

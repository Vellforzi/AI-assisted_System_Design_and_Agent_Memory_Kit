# Agent Instruction Files Guide

Status: implementation-facing guide  
Purpose: explain how to connect Agent Memory Kit to repository-aware AI tools without overloading their context windows.

---

## 1. Principle

The agent instruction file is a router, not the memory itself.

It should tell the agent:

- where the Project Map is;
- what to read first;
- what the default intent is;
- what actions are forbidden without explicit owner approval;
- where component-specific rules live;
- how to report missing evidence.

It should not duplicate the whole Agent Kit.

---

## 2. Common files

Different tools use different names, but the pattern is similar:

- `AGENTS.md` for Codex-style and many repository-aware agents;
- `.cursor/rules/*.mdc` or project rules for Cursor;
- `CLAUDE.md` for Claude Code;
- `.cursorrules` for older Cursor setups;
- `GEMINI.md` for Gemini-oriented coding agents;
- `copilot-instructions.md` for GitHub Copilot.

Use one canonical instruction source where possible, then import or mirror it for each tool.

---

## 3. Recommended hierarchy

```text
<Project Root>/
  AGENTS.md
  .cursor/
    rules/
      agent-memory-kit.mdc
  CLAUDE.md                    # optional, can import AGENTS.md where supported
  Project Map/
    README.md
    current_state.md
    working_state.yaml
    source_authority.yaml
    permissions_policy.yaml
    retrieval_policy.yaml
```

---

## 4. Always-loaded instruction budget

Keep always-loaded instructions short.

Target:

- under 150-250 lines for a root file;
- fewer if the client automatically loads many files;
- links or path references for deeper protocols.

Large evergreen protocols should live in `Agent Kit/kit/` and be opened only when needed.

---

## 5. Required root rules

The root instruction file should contain these rules:

1. The Project Map is the source of project memory.
2. Built-in model knowledge is not project truth.
3. Answer-only is the default intent.
4. No file, git, shell, DB, deploy, memory, or external side effect without explicit owner action request.
5. Retrieve the smallest sufficient context.
6. Label missing evidence instead of guessing.
7. External research is allowed only for external facts and does not become project truth without owner approval.
8. For multi-step tasks, use task contracts and handoffs.
9. At the end of significant work, propose Project Map updates, checkpoints, handoffs, or eval triggers; do not apply them unless asked.
10. Eval failures do not grant repair permission; rule/template changes still require explicit owner scope.

---

## 6.1 Significant-work footer

Instruction files should require a short footer after meaningful tasks:

```text
Project Map update: recommended / not needed
Checkpoint or handoff: yes/no
Eval trigger: yes/no
No Project Map changes applied unless explicitly requested.
```

This footer should be omitted for tiny one-off answers unless it adds value.

---

## 6. Technical enforcement

Instruction files shape behavior. They are not a hard security boundary.

Where the AI client supports it, use:

- read-only modes;
- permission prompts;
- denied commands;
- tool hooks;
- sandboxing;
- branch isolation;
- pre-commit review;
- separate local/private instruction files for secrets and preferences.

Never rely only on a natural-language instruction to protect a dangerous system.

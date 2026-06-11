# Model / Surface Routing Snapshot

Status: volatile provider/model/mode snapshot
Captured at: 2026-06-10, Europe/Vienna
Primary source: owner-observed UI controls in Cursor, Codex extension, and ChatGPT Pro web
Secondary sources: Cursor docs/blog/forum and OpenAI Codex/ChatGPT docs checked on 2026-06-10

This file is intentionally dated. It is **not** permanent project truth. Refresh it when Cursor, Codex, ChatGPT, model availability, pricing, context windows, Fast/Max behavior, or UI controls change.

## Core decision

The current owner-observed model set is sufficient with surplus for the Cursor-agent working-horse workflow:

| Surface | Core route | Default use |
|---|---|---|
| Cursor Agent | Composer 2.5 | routine scoped apply, Project Map updates, docs/router edits, mechanical package merge |
| Cursor Agent | Codex 5.3 / GPT-5.3 Codex class | code/test/repair loop, terminal verification, independent code review |
| Cursor Agent | GPT-5.5 | hard reasoning escalation for Agent Kit contracts, eval/router policy, cross-subsystem root cause |
| Cursor Agent | Sonnet 4.6 | balanced review/refactor fallback |
| Cursor Agent | Opus 4.8 | rare premium audit/planning escalation |
| Cursor Agent | Fable 5 | rare long-running autonomous/agentic escalation |
| Codex IDE extension | GPT-5.4-mini / GPT-5.4 / GPT-5.5 / GPT-5.3-Codex-Spark | local code agent, repair loop, independent check, cloud offload when useful |
| ChatGPT Pro web | GPT-5.5 Thinking Heavy / GPT-5.5 Pro Heavy / Deep Research | synthesis, architecture, prompt/package design, external research; not direct repo apply |

Do not add more models to the default router unless a concrete capability gap appears or the owner requests benchmarking.

## Cursor model controls observed by owner on 2026-06-10

| Model | Options | Context controls | Reasoning/effort controls | Default router role |
|---|---|---|---|---|
| Composer 2.5 | fast on/off | not exposed in owner UI | not exposed in owner UI | default working horse |
| Fable 5 | thinking | 300K, 1M | low, medium, high, extra high, max | rare long-running escalation |
| Opus 4.8 | thinking, fast | 300K, 1M | low, medium, high, extra high, max | rare hard audit/planning escalation |
| GPT-5.5 | fast | 272K, 1M | none, low, medium, high, extra high | hard reasoning escalation |
| Sonnet 4.6 | thinking | 200K, 1M | low, medium, high, max | balanced review/refactor fallback |
| Codex 5.3 | fast | not exposed in owner UI | low, medium, high, extra high | code/test/repair specialist |

## Cursor work modes

| Mode | Use | Default route | Cost/scope policy |
|---|---|---|---|
| Ask | questions, tradeoffs, read-only analysis | Composer 2.5 or medium route | no mutation; explicit refs only; no Max |
| Plan | complex apply/debug/audit before changes | Composer 2.5 for normal planning; GPT-5.5/Sonnet/Opus only with trigger | plan first, approval before apply |
| Debug | root-cause with logs/tests/runtime evidence | Codex 5.3 medium/high or GPT-5.5 medium/high depending on code vs reasoning need | include tests/logs/schema; high only with concrete ambiguity |
| Multitask | independent parallel tasks | only with isolated scopes/worktrees and checkpoint/handoff | high fuel; avoid unless tasks are separable |
| Agent/apply | bounded implementation | Composer 2.5 standard first; Codex for code/test loops | no broad scan; apply only accepted scope |

## Auto and Max Mode boundary

Auto is not a model. It is a provider/router mode. For OPTION-PROFIT controlled work, Auto is **not** a default route because the exact provider/model may change and reproducibility is weaker. Use Auto only when the owner explicitly accepts non-deterministic routing for low-risk cheap exploration.

Max Mode is a separate Cursor-level context/capacity toggle for explicit models except Auto. It is not a quality setting and must stay OFF by default. Enable 1M/Max only for context overflow, broad audit, large multimodal context, or explicit owner approval.

## Codex IDE extension controls observed by owner on 2026-06-10

| Control | Owner-observed values | Routing policy |
|---|---|---|
| Model | GPT-5.5, GPT-5.4, GPT-5.4-mini, GPT-5.3-Codex-Spark | start mini/medium for routine code; escalate to GPT-5.5 only for hard reasoning/code repair |
| Reasoning | low, medium, high, extra high | start medium; high/extra high only for root-cause debug, repair, audit, cross-subsystem analysis |
| Speed | standard, fast | standard by default; fast only for low-risk/time-critical/draft work |
| Plan Mode | on/off | on for multi-file debug/audit/repair; off for narrow accepted apply |
| Pursue Goal | on/off | off by default; on only for owner-approved long-running task with clear stop conditions |
| Include IDE Context | on/off | off by default; implicit IDE context is advisory only unless explicitly scoped/approved |

Codex is useful as a controlled code agent, independent checker, sandbox repair loop, and local verification runner. Cursor remains the main working-horse repo agent.

## ChatGPT Pro web routing observed by owner on 2026-06-10

| Mode | Use | Policy |
|---|---|---|
| Thinking Heavy | architecture, synthesis, prompt/package design, hard tradeoffs | use when reasoning quality matters more than speed |
| Pro + Heavy | hardest synthesis / audit / decision support | use sparingly; not for mechanical repo edits |
| Deep Research | external research with citations and dated source review | use for provider/model research, standards, pricing, current docs |

ChatGPT web is for analysis and handoff/task design. It does not apply repo changes; Cursor/Codex execute scoped changes.

## Commands as token-saving route selectors

Use short command vocabulary instead of repeating long instructions:

| Command | Meaning |
|---|---|
| `/context-advisor` | classify intent/scope/model/fuel risk |
| `/settings` | recommend surface/model/reasoning/speed/context with cheaper alternative |
| `/models` | show dated provider/model snapshot and sufficiency |
| `/fuel` | estimate token/fuel risk and checkpoint/new-chat need |
| `/scope` | list mandatory/recommended/optional/forbidden context |
| `/safe-apply` | gate a future mutation; does not mutate |
| `/ask` | read-only answer/analysis mode |
| `/debug` | runtime/root-cause debug preflight |
| `/multitask` | split independent work only when scopes/checkpoints are safe |

## Escalation contract

When recommending GPT-5.5 High/Extra High, Opus, Fable, Max/1M, Fast on expensive models, Auto for controlled work, Codex extra-high, ChatGPT Pro+Heavy, Deep Research, or any optional model, the agent must include:

1. concrete escalation trigger;
2. cheaper sufficient alternative;
3. why cheaper is insufficient;
4. snapshot date/source.

If those are missing, ContextAdvisor should emit an amber warning and downgrade to the lowest sufficient route.

## Source notes captured on 2026-06-10

- Cursor docs show the model catalog, default/max context, capabilities, and notes such as GPT-5.5 requiring Max Mode on request-based plans, Fast mode being available at higher rates, and long context supporting up to 1M with input pricing caveats.
- Cursor Plan Mode docs/blog describe Plan Mode as researching codebase context, creating a reviewable plan, asking clarifying questions, and waiting for approval before building.
- Cursor agent best practices emphasize planning before coding, keeping rules focused, referencing files instead of copying full contents, and starting a new conversation when the current one accumulates noise.
- OpenAI Codex IDE docs confirm support for VS Code forks such as Cursor, editor context, @file references, model switching, reasoning effort, approval modes, slash commands, and extension settings.
- OpenAI reasoning docs state higher reasoning effort is not automatically better and should be increased only when quality gains justify cost/latency.
- OpenAI ChatGPT docs identify GPT-5.5 Instant, Thinking, Pro, Thinking/Pro effort controls, and Deep Research as a report-style research tool.

See machine-readable refs in `context_advisor/provider_surface_routing_snapshot_2026-06-10.yaml` and Cursor-specific routing in `context_advisor/cursor_model_routing_matrix.v1.json`.

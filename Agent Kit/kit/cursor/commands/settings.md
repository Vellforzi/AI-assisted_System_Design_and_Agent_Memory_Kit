# /settings

Purpose: explain which execution surface, model class, reasoning level, speed, and context mode should be used for the current task.

Mode: analyze
Mutations: forbidden

Rules:

- Use current provider capability evidence when model/provider facts matter; exact Cursor model advice must show the snapshot date/ref.
- Show the provider snapshot date when giving concrete Cursor model/settings recommendations.
- Treat provider/model capability facts as volatile snapshots, not durable project truth.
- Prefer the lowest sufficient model/settings class.
- Prefer medium reasoning for owner-provided facts, narrow Project Map updates, version refs, small docs/root-router edits, and bounded local edits.
- Use high reasoning only for concrete escalation triggers: cross-subsystem analysis, audits, repairs, schema/protocol/eval/router changes, production-risk work, side-effect safety, or ambiguous recovery.
- Keep Max Mode and full IDE context off unless the advisor identifies a concrete need.
- If recommending premium/frontier/high/pro, Max/1M, Fast on expensive models, or an optional model, include the escalation trigger, cheaper alternative, why cheaper is insufficient, and snapshot date/ref.
- Do not invent unsupported model controls. In the 2026-06-10 Cursor snapshot, Composer 2.5 has only Fast on/off.

Return:

```text
Recommended route:
- Surface:
- Model/model class:
- Cost class:
- Cheaper sufficient alternative:
- Escalation trigger, if any:
- Why not cheaper, if premium/high/pro is recommended:
- Reasoning:
- Speed:
- Context mode:
- Max Mode:
- Include IDE Context:
- Plan Mode:
Why:
Volatile provider snapshot used: <yes/no/ref/date>
```


## v3.9.3 Auto/Max explicit boundary

Auto is not a specific model. For OPTION-PROFIT controlled work, do not recommend Auto as the default route unless the owner explicitly accepts non-deterministic provider/model routing for low-risk exploration.

Max Mode is a separate Cursor-level capacity toggle for explicit models except Auto. Keep Max OFF by default; recommend 1M/Max only with context-overflow, broad-audit, large multimodal context, or explicit owner approval.

## Surface-specific controls

When the owner asks for settings, distinguish the surface:

- Cursor Agent: Composer/GPT/Sonnet/Opus/Fable/Codex 5.3 routes, Cursor modes Ask/Plan/Debug/Multitask/Agent, Max Mode, Include IDE Context.
- Codex IDE extension: model, reasoning, speed, Plan Mode, Pursue Goal, Include IDE Context.
- ChatGPT Pro web: Thinking Heavy, Pro + Heavy, Deep Research.

Do not mix controls across surfaces. Example: Codex `Pursue Goal` is not a Cursor Agent setting; Cursor Max Mode is not a ChatGPT web setting.

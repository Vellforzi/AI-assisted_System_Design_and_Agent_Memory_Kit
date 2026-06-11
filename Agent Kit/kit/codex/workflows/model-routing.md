# Codex model-routing workflow

Purpose: choose Codex IDE extension settings without over-escalating model/reasoning/fuel.

Snapshot date: 2026-06-10, Europe/Vienna. Refresh if Codex extension controls change.

Owner-observed controls:

- Models: GPT-5.5, GPT-5.4, GPT-5.4-mini, GPT-5.3-Codex-Spark.
- Reasoning: low, medium, high, extra high.
- Speed: standard, fast.
- Toggles/modes: Plan Mode, Pursue Goal, Include IDE Context.

Default:

```text
Reasoning: medium
Speed: standard
Plan Mode: ON for multi-file debug/audit/repair; OFF for narrow accepted apply
Pursue Goal: OFF unless owner approved long-running task + stop conditions
Include IDE Context: OFF unless exact open files/selections are scoped or owner-approved
```

Use Codex when:

- code/test/repair loop is the main work;
- terminal verification matters;
- Cursor's diff needs independent review;
- a sandbox/cloud offload is useful and scope is explicit.

Escalate to high/extra high only when there is a concrete trigger: repeated failing tests, cross-subsystem root cause, ambiguous runtime behavior, or formal audit/repair.

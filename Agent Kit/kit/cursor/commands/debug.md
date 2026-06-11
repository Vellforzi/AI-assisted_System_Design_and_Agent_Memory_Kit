# /debug

Purpose: debug/root-cause preflight before any repair apply.

Mode: debug/analyze first
Mutations: forbidden unless a separate `/apply` task is approved

Required context classes usually include affected files, runtime logs, tests, command output, source authority, and recent diffs.

Routing policy:

- Start with Composer 2.5 or Codex/Cursor medium route when the issue is bounded.
- Use Codex 5.3 medium/high for code/test/repair loops and terminal verification.
- Use GPT-5.5 high or Opus/Sonnet only when root cause is cross-subsystem, ambiguous, or cheaper route failed.
- Plan Mode ON for multi-file or cross-subsystem debugging.
- Max/1M OFF unless logs/docs/context exceed normal context and owner approves.

Return gate, missing evidence, likely root-cause hypotheses, proposed narrow repair scope, verification commands, and route recommendation.

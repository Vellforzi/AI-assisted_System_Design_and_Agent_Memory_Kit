# /debug

Purpose: debug/root-cause preflight before any repair apply.

Mode: debug/analyze first
Mutations: forbidden unless a separate `/apply` task is approved

Required context classes usually include affected files, runtime logs, tests, command output, source authority, and recent diffs.

Routing policy:

- Start with Composer 2.5 for clear scoped implementation or GPT-5.6-Terra with Medium reasoning for bounded analysis.
- Use ChatGPT Codex with GPT-5.6-Terra / High / Standard for difficult code/test repair and terminal verification when it is the best executor for the evidence chain.
- Use model GPT-5.6-Sol with High reasoning only when root cause is cross-system, ambiguous, production-risk, or the cheaper route failed.
- Plan Mode ON for multi-file or cross-subsystem debugging.
- Cursor Max/1M remains a capacity control and stays off unless context exceeds the normal window. Codex Max is separate single-task reasoning and also requires an explicit hardest-problem trigger.

Return gate, missing evidence, likely root-cause hypotheses, proposed narrow repair scope, verification commands, and route recommendation.

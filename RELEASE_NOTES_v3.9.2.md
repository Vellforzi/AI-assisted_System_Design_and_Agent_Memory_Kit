# Release Notes v3.9.2 — Cost-Aware Model Routing Patch

Release date: 2026-06-10

## Purpose

v3.9.2 is a micro-patch on top of v3.9.1. It prevents Context Advisor and router prompts from recommending premium/frontier/high/pro models merely because they are strongest.

The default rule is: **lowest sufficient model/settings class first**.

## What changed

- Added the **Cost-Aware Model Router** rule:
  - low/fast for formatting, extraction, simple cleanup, and grep-like checks;
  - medium/standard for owner-provided facts, narrow Project Map updates, version refs, small docs/root-router edits, and bounded local changes;
  - high/standard only for concrete escalation triggers such as cross-subsystem debugging, schema/protocol/eval/router changes, audit/repair/recovery, production-risk work, or side-effect safety;
  - extra-high/pro only for rare critical synthesis or owner-approved maximum-quality work.
- Premium/frontier/high/pro recommendations must include:
  1. escalation trigger;
  2. cheaper alternative;
  3. why the cheaper alternative is insufficient.
- Added a `project_map_update` advisor intent/profile for narrow Project Map writes based on owner-provided facts.
- Updated `/settings` behavior to show cost class, escalation trigger, and cheaper alternative.
- Updated Context Advisor machine-readable policy with model-cost fields.
- Updated the optional `context_advisor_preflight.py` helper with premium/high routing warning flags.
- Added eval case `AMK-CA-008` for over-escalated model recommendations.

## Compatibility

This patch is backward-compatible with v3.9.1. It does not change the Project Map schema, memory schema, retrieval profiles, or required runtime dependencies.

## Upgrade guidance

For projects that already adopted v3.9.1:

1. Replace the portable `Agent Kit/` files with v3.9.2, or apply only changed files.
2. If root routers such as `AGENTS.md`, `.cursor/rules/*.mdc`, or `PROJECT_AI_BRIEF.md` mention ContextAdvisor/model settings, add a one-line cost-aware routing rule.
3. Do not install TypeScript solely for this patch. The TypeScript file is a contract artifact unless the project edits or compiles kit contracts locally.

## Eval trigger

Yes. The patch changes model/settings routing behavior, Context Advisor profile policy, Cursor/Codex guidance, and eval coverage.

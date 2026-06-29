# Cost And Model Routing Optional Guide

Status: optional integration guide
Last aligned: <YYYY-MM-DD>
Audience: project owners, AI/Codex sessions, maintainers
Runtime impact: none
Authority: advisory model/settings routing; does not override task scope, permissions, or source authority

---

## Purpose

Help the owner and agent choose the lowest sufficient model/settings class for a
task without making model choice part of the core governance baseline.

Use this guide when the owner asks about model choice, cost, reasoning level,
context size, or when a task is expensive, risky, ambiguous, or broad.

## Principle

Do not recommend the strongest or most expensive model as a generic default.
Use the cheapest settings that are sufficient for the task, and escalate only
with a concrete reason.

## Routing Ladder

| Work type | Default class |
|---|---|
| Formatting, extraction, grep-like inspection, simple docs cleanup | low/fast |
| Owner-provided facts, Project Map refs, version updates, small docs/root-router edits | medium/standard |
| Bounded implementation patch with exact scope and verification | medium/standard |
| Cross-subsystem root cause, schema/protocol/eval/router changes, audit/repair/recovery, production-risk work | high/standard |
| Critical ambiguous synthesis or owner-approved maximum-quality run | extra-high/pro only with explicit reason |

## Escalation Triggers

Escalate only when at least one applies:

- cross-subsystem root-cause analysis;
- source-authority conflict or stale-fact repair;
- schema, protocol, retrieval, eval, or agent-behavior contract changes;
- production-risk code, database, deployment, git, or side-effect safety;
- security/privacy-sensitive review;
- long-horizon synthesis where cheaper settings are likely to miss dependencies;
- owner explicitly requests maximum quality after seeing the tradeoff.

## Required Response When Recommending Expensive Settings

Report:

1. escalation trigger;
2. cheaper sufficient alternative;
3. why the cheaper alternative is insufficient;
4. expected verification/checks after the run.

## Provider Volatility Rule

Exact model names, prices, context windows, UI controls, and speed modes are
volatile provider facts. Do not hard-code them as durable project truth.

When exact model advice matters, cite a dated provider snapshot or current
provider documentation. If no current evidence is loaded, give only generic
class-based guidance.

## Boundaries

This guide does not grant mutation permission, expand repository scope, enable
full-context loading, or override `secondary_memory_governance/`.

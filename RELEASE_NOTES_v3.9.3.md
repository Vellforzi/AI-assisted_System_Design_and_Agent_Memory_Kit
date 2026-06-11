# Release Notes v3.9.3

Date: 2026-06-10

## Purpose

v3.9.3 is a mini-patch over v3.9.2. It adds a dated model/surface/mode routing snapshot so ContextAdvisor can recommend Cursor/Codex/ChatGPT settings without over-escalating to expensive models or mixing controls across surfaces.

## Main changes

- Adds `MODEL_SURFACE_ROUTING_SNAPSHOT.md`.
- Adds machine-readable `provider_surface_routing_snapshot_2026-06-10.yaml`.
- Extends Cursor routing matrix with surface modes and command shortcuts.
- Records owner-observed Cursor models and controls: Composer 2.5, Fable 5, Opus 4.8, GPT-5.5, Sonnet 4.6, Codex 5.3.
- Records Auto as non-default for controlled work and Max Mode as separate context/capacity toggle.
- Records Cursor modes: Ask, Plan, Debug, Multitask, Agent/apply.
- Records Codex extension controls: GPT-5.5, GPT-5.4, GPT-5.4-mini, GPT-5.3-Codex-Spark; low/medium/high/extra-high reasoning; standard/fast; Plan Mode; Pursue Goal; Include IDE Context.
- Records ChatGPT Pro web modes: Thinking Heavy, Pro + Heavy, Deep Research.
- Adds `/ask`, `/debug`, `/multitask` command files and expands `/models` and `/settings`.
- Adds Codex `model-routing.md` workflow.
- Adds eval cases AMK-CA-012..014.

## Routing decision

The current model set is sufficient with surplus for Cursor-agent working-horse use. Do not add more default models unless a concrete capability gap, benchmark need, or owner experiment appears.

## Volatility

All model/provider/mode facts are dated snapshots collected on 2026-06-10, Europe/Vienna. Refresh before relying on current availability, pricing, context windows, or UI controls.


## Tooling note

`context_advisor_preflight.py` now accepts surface/mode flags for Cursor Agent, Codex IDE, ChatGPT Pro web, Multitask and Codex pursue-goal style routing.

# Model/Settings Label Fidelity Policy (AMK v3.11.1)

## Core rule

Use exact owner/provider labels from current evidence or an explicitly dated
snapshot. Keep the machine-readable policy state separate from the short tuple
the owner actually selects before submitting a prompt.

The owner-facing tuple includes only:

- surface;
- model display label;
- reasoning effort;
- speed/service tier when that selector exists on the surface.

Config slugs, snapshot refs, approval policy, context policy, delegation state,
shell, terminal profile, and IDE/application configuration remain available in
structured evidence, but are not padded into an owner-facing ChatGPT Codex
recommendation.

Do not invent combined labels, rewrite provider labels, or pair contradictory
controls. A dated snapshot is evidence about its capture date only.

## Current ChatGPT Codex example

```yaml
surface: ChatGPT Codex
model: GPT-5.6-Terra
reasoning: Medium
speed: Standard
```

Evidence: `context_advisor/codex_provider_capability_snapshot_2026-07-10.yaml`,
checked 2026-07-10. Config slug: `gpt-5.6-terra`.

Do not append `Fast off`: `Standard` already expresses the selected speed. Do
not append `Max off` or `Ultra off`: `Medium` or `High` already expresses the
selected reasoning effort. Do not append IDE context, shell, terminal, or app
configuration unless the owner asked for application configuration rather than
prompt-time choices.

Forbidden combined form when reasoning is also a separate field:

```text
Model: GPT-5.6-Terra High
Reasoning: Medium
```

## Max and Ultra fidelity

- Codex Max is single-task reasoning depth.
- Codex Ultra is automatic delegation for independent subproblems.
- Cursor Max Mode is context/capacity and must not be mapped to Codex Max.
- Sol/Terra Ultra requires independent scopes, stop conditions, and fuel
  justification.
- Luna Ultra is unsupported by the owner-local 2026-07-10 capability snapshot.

## Surface and source fidelity

The current official desktop label is `ChatGPT desktop app (Codex mode)`;
`ChatGPT Codex` is the compact owner-facing label and
`chatgpt_desktop_codex` is the structured id. `codex_app` is a compatibility
alias for that desktop mode. `Codex IDE extension`, `Codex CLI`, and `Codex web`
are distinct current clients. Codex evidence does not establish GPT-5.6
availability in the Cursor Agent model picker. The bundled 2026-06-10 Cursor
snapshot remains historical and expired.

## Fast fidelity

Standard is the default. Fast is latency-first and increased-usage, never
cheaper. The owner-local cache exposes GPT-5.6 Fast, while the checked public
Speed page names GPT-5.5 and GPT-5.4. Do not invent a fixed GPT-5.6 Fast credit
multiplier.

## Verification requirement

If label, availability, or control fidelity cannot be verified:

1. report missing/stale evidence;
2. identify the exact surface and control that needs refresh;
3. avoid fabricated substitutions;
4. preserve full structured evidence while keeping the owner prompt tuple
   minimal and surface-specific.

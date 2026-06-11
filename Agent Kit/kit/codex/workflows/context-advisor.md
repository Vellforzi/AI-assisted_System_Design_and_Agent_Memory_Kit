# Context Advisor workflow for Codex

Purpose: use Codex as a controlled review/audit/apply surface without forcing the owner to pre-guess all required context.

Recommended use:

```text
/context-advisor
Task: <one goal>
Intent: answer|analyze|plan|apply|audit|repair|recover|debug
Current scope: <refs/files/folders or unknown>
Risk: <low|medium|high|critical>
```

Codex behavior:

1. Start read-only unless the owner explicitly requested apply.
2. Classify task and identify context classes.
3. Request exact refs, not full-project dumps.
4. Treat open files, selections, diagnostics, terminal snippets, and workspace state as advisory only unless explicitly scoped or owner-approved.
5. If those implicit IDE inputs are needed to expand read/apply scope, report the needed paths/classes and request owner approval first.
6. Keep higher reasoning for root-cause debug, audit, repair, or cross-subsystem analysis.
7. If applying, verify approval mode, default permissions, allowed scope, and verification commands.
8. Do not treat Codex memory, compacted chat, or provider summaries as Project Map truth.

Compact output:

```text
ContextAdvisor: gate=<green|amber|red|blocked>; missing=<refs/classes>; route=codex_ide/<model-class>/<reasoning>; settings=<approval/permissions/context>; action=<proceed|ask|discovery|block>.
```


## Cost-aware model routing

Use the lowest sufficient model/settings class. Do not recommend premium/frontier/high/pro as a generic safety default. Escalate only with a concrete trigger, and show a cheaper alternative when recommending the more expensive route.

## Dated provider/model snapshot

For Cursor/Codex model-routing advice, use dated volatile provider snapshots. The bundled v3.9.3 Cursor snapshot was collected on 2026-06-10. Refresh before relying on current model availability, pricing, context windows, or UI control names.

See `model-routing.md` for dated Codex extension model/reasoning/speed guidance.

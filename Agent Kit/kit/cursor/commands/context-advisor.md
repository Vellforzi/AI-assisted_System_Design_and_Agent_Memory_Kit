# /context-advisor

Purpose: run a compact Context Advisor preflight before expensive, risky, or under-scoped work.

Mode: analyze
Mutations: forbidden

Input:

```text
Task: <one goal>
Intent: answer|analyze|plan|apply|audit|repair|recover|resume|debug|research|prompt_optimize|handoff_package_update
Current scope: <refs/files/folders or unknown>
Risk: low|medium|high|critical
Need: <expected output>
```

Procedure:

1. Classify task and risk conservatively.
2. Identify mandatory/recommended/optional/forbidden context classes.
3. Check whether current scope is insufficient, overbroad, unsafe, secret-bearing, or relying on unscoped implicit IDE context.
4. If open tabs/selections/diagnostics/workspace state are needed for scope expansion, report needed paths/classes and ask owner approval first.
5. Recommend surface/model class/reasoning/speed/context settings.
6. Return compact hint by default. Expand only if the owner asks `why?`.

Output:

```text
ContextAdvisor: gate=<green|amber|red|blocked>; missing=<refs/classes>; route=<surface/model-class/reasoning>; settings=<Max/IDE/Plan/speed>; action=<proceed|ask|discovery|block>.
```

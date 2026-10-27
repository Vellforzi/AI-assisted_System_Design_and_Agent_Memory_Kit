# Evidence and calibration

Sources fetched on 2026-10-22. These establish guidance, not measured performance
for this user's tasks. Refresh when a relevant product constraint changes.

## Official guidance

- [Model selection](https://learn.chatgpt.com/docs/model-selection#how-to-think-about-models-and-reasoning-effort):
  GPT-6.1 Sol / medium is a starting point for technical work that will be
  iterated; Astra / medium for broad, ambitious projects. Extra high is suggested
  for demanding analysis or exacting deliverables. Compare the same inputs and
  keep the lightest setting that meets the quality requirement. This does not
  establish that Astra always needs less effort than Sol.
- [API deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist#set-up-reasoningeffort):
  GPT-6.1 Sol and GPT-6 Astra support low, medium, high, xhigh, and max in the
  documented API guidance; neither supports none there. Extra effort increases
  deliberation and generally latency/usage. Higher settings need evidence of
  worthwhile benefit. Reasoning mode and effort are independent. This page
  does not establish the meaning or API support of ultra.
- [Build skills](https://developers.openai.com/codex/skills):
  a local personal skill is discoverable under `~/.agents/skills`; implicit
  selection depends on its description. `allow_implicit_invocation: true`
  allows selection, but does not guarantee activation for every request.

## Surface-specific evidence

At creation, this desktop session's chat-creation and messaging tool schemas
listed low, medium, high, xhigh, max, and ultra for gpt-6.1-sol and gpt-6-astra on
the calling host. This proves what those tools exposed at that time. It does
not prove the current chat's effective setting, the UI picker's choices, future
availability, or any performance benefit of ultra. Recheck the actual target
surface before recommending a host-specific setting as available.

## Local judgment

The Sol/Astra task-fit criteria, high/medium boundary, phase separation, escalation triggers, and examples in
SKILL.md and this reference are practical selection rules. They have not been established by a
controlled comparison of these models. User choices and observed results can
refine the recommendation; preserve the distinction between a heuristic and
measured evidence. No external model evaluation or API call is required merely
to offer a provisional recommendation.

Use these cases when reviewing revisions. Accept a reasoned nearby setting
where the evidence permits it; the important result is the decision boundary.

| Request/context | Expected decision boundary |
| --- | --- |
| Extract 10,000 already structured entries, preserving exact fields | Low can suffice; volume alone does not demand high |
| Make a bounded edit with known contracts and quick tests | Medium; do not demand maximum effort |
| Plan state ownership and recovery across interacting components | High is justified; independently assess execution |
| Implement an approved plan that still changes concurrent shutdown behavior | Do not lower effort merely because a plan exists |
| Reconcile mutually inconsistent runtime observations | Xhigh can be provisional; collect missing observations |
| User explicitly selects Sol / medium for difficult work | Preserve selection, explain concern; no silent switch |
| Host exposes max but no ultra; user asks for the deepest available effort | Recommend the supported choice; never invent ultra support |
| Database cannot be reached or required product behavior is unspecified | Collect evidence or ask the material question; higher effort is not the remedy |
| A trivial factual follow-up during an active task | Answer directly; no new effort report |
| User asks only for a plan for later execution | Recommend both phases; do not implement or create another chat |

## Detailed effort calibration

Use this table with the selection and pause rules in [SKILL.md](../SKILL.md). These are heuristics, not measured equivalences.

| Reasoning needed in this phase | GPT-6.1 Sol | GPT-6 Astra |
| --- | --- | --- |
| Mechanical extraction, exact edits, or executing a fully specified procedure with little judgment | `low` | `low` |
| Bounded analysis, a straightforward plan, or implementation with clear contracts and prompt feedback | `medium` | `medium` |
| Interacting components, meaningful design trade-offs, subtle failure cleanup, lifecycle/concurrency reasoning, or difficult regression review | `high` | `high`; `medium` only if those interactions have already been resolved and execution is straightforward |
| Deep causal investigation, conflicting evidence, or exacting synthesis whose difficult constraints must be reconciled together | `xhigh`, provisionally | `xhigh`, provisionally |
| Exceptionally difficult reasoning where added deliberation has a concrete purpose, preferably supported by observed shortcomings at lower effort | Consider supported `max` after the checks below | Consider supported `max` after the checks below |
| The target surface exposes `ultra` and there is a specific reason to consider it | Conditional `ultra`; benefit over `max` is unestablished without evidence | Conditional `ultra`; benefit over `max` is unestablished without evidence |

Recommend `max` or `ultra` only when the exact model and target surface expose
that setting and the added deliberation has a concrete purpose. Without
comparative evidence, disclose uncertain benefit and greater expected latency;
do not call it optimal or invent a multiplier. If availability is unknown,
recommend a documented, confirmed available setting and state the gap. If no
current capability evidence exists, label the recommendation conditional.

## Recommendation examples

### Task start

Example: `Для этой задачи рекомендую GPT-6.1 Sol / medium: требования ясны,
изменение ограничено и результат можно проверить локально.` This is a
recommendation, not a claim that the current response uses that setting.

### Investigation and bounded repair

Example: contradictory scraper, database, API and client observations, with
several plausible event sequences, can justify Astra / xhigh provisionally for
investigation. An established missing invalidation of a specific Redis key with
known consumers can instead justify Sol / medium or high for the bounded fix.
Do not execute that example or infer product behavior from it.

### Planning and implementation

Example execution note:

```text
Для подготовки плана: GPT-6 Astra / high — нужно согласовать зависимости и обработку ошибок.
Для реализации плана: GPT-6.1 Sol / medium — решения определены, шаги ограничены и проверяемы.
Пересмотр: high, если реализация выявит неучтённое владение состоянием или конкурентное выполнение.
```

Explain why the implementation model fits the remaining work, not just why the
effort fits. Retain Astra for implementation if the difficult synthesis or
architectural decisions remain unresolved. The example permits different models; it does not mandate switching away from
the user's selected model. At implementation start, reuse the plan's setting
if its assumptions still hold, or briefly explain the revised recommendation.

### Change and pause

Example: `Ранее рекомендовал GPT-6.1 Sol / high. Обнаружены противоречия между
владением очередью и порядком завершения; теперь рекомендую GPT-6 Astra / xhigh
для причинного разбора. Работу приостановил на сопоставлении этих цепочек.`
Then ask whether to switch and confirm the selection, or continue on Sol / high.
This is the user's requested pause boundary, not a claim that the current model
is incapable or that the alternative is proven better.

### Compact phase report

Example: `Для плана рекомендую GPT-6 Astra / high: нужно согласовать владение
состоянием и восстановление после ошибок. Для реализации — GPT-6.1 Sol / high;
пересмотрим режим, если обнаружатся противоречия между контрактами.`

---
name: select-effort
description: Recommend GPT-6.1 Sol or GPT-6 Astra and effort at substantive task start or explicit request; specify implementation separately in plans. Pause for the user's choice when new evidence changes the working recommendation. Routine factual follow-ups need no reassessment.
---

# Select model and reasoning effort

Recommend sufficient capability and correctness first, then avoid unnecessary
latency and usage. Preserve the user's explicit model and effort; explain
concerns and alternatives without overriding them. Use the user's language. This skill recommends settings; it cannot change
inference parameters of an already running response.

## 1. Recommend at task start

In the first progress message, before substantive execution or lengthy
investigation, give one model/effort pair and one concrete reason. Use the
request and available context; if discovery may change the choice, mark it
preliminary and name the uncertainty and revision condition. Do not delay the
recommendation or ask permission merely to offer it.

Identify outcome, acceptance, phase, known dependencies, conflicting evidence,
interacting contracts/states/failures/concurrency, consequences, feedback speed
and the owner's quality/time/usage priority. Do not create an intake questionnaire:
collect missing facts; ask about missing product decisions.

Do not automatically recommend the current model for a different task or list
both models without choosing. Routine factual follow-ups do not restart this
workflow. Keep recommendations to one or two sentences in normal updates;
use a phase table for an explicit comparison or multi-stage plan when clearer.
Do not repeat the assessment every turn.

## 2. Distinguish recommendation from actual settings

Keep selected model, configured default, runtime-reported effective effort,
supported settings and recommendation distinct. Configuration is not proof
of active settings. Never invent the active model or claim an unverified switch.
When reporting actual effort without runtime metadata, say:
"The effective effort for this response is unverified" in the user's language.

Confirm support through current target-host capabilities or its model picker;
API documentation does not prove UI/account availability. Keep exact names
`gpt-6.1-sol` and `gpt-6-astra`; do not substitute `gpt-6-sol`, choose an
unrelated third model or assume `none`/`minimal` support. Treat `ultra`,
`max`, Pro mode and Fast/Ultrafast as distinct controls.

Read [basis](references/basis.md) for platform claims, calibration or highest
settings. Refresh official sources if behavior is uncertain or the surface/model
changes; do not repeat research when relevant current evidence remains valid.

## 3. Select for the actual reasoning burden

These are heuristics, not benchmarks or measured capability boundaries.

- **Sol:** clear outcome/contracts, established cause or bounded investigation,
  concrete verification; coupled engineering can still fit.
- **Astra:** ambiguous causes, conflicting explanations/evidence, difficult
  architectural trade-offs or tightly connected conditions across components.
  Name that burden; Astra does not automatically require xhigh.

Planning versus coding, project/input size, file/component/tool counts, deployment,
missing data or costly consequences alone do not determine model or raise effort.
Risk requires care and verification; scale may require batching; deployment needs
authorized checks; missing evidence requires observation. A small edit can still
involve difficult contracts.

Choose one supported effort for each phase:
- `low`: mechanical extraction, exact edits or fully specified procedures.
- `medium`: ordinary substantive work, bounded analysis/plans or implementation
  with clear contracts and prompt feedback.
- `high`: interacting decisions/components, design trade-offs, subtle cleanup,
  lifecycle/concurrency or difficult regression review.
- `xhigh`: deep causal investigation, conflicting evidence or demanding synthesis.
  Name the expected quality benefit; mark provisional without a representative comparison.
- `max`/`ultra`: only with confirmed support for the exact model/surface and
  a concrete purpose for added deliberation; read basis first. Without comparative
  evidence, disclose uncertain benefit and greater expected latency, not optimality
  or invented multipliers.

Start at medium unless the task warrants otherwise; do not deliberately fail at
lower effort first. Already-resolved interactions may permit medium, including
for Astra. Unknown max/ultra availability means use a confirmed supported setting
and state the gap; if no current capability evidence exists, make the recommendation
conditional. Do not use numeric scoring or equate effort labels, quality or latency
across models. Compare models only when asked or a real trade-off needs explanation.

## 4. Separate planning and implementation

In the existing delivered plan, state planning and implementation pairs separately,
even when identical, with the reasoning that warrants each model and effort.
Identify implementation phases needing different settings; specify review separately
only when its reasoning differs materially, matching the hardest remaining defect
risk without a fixed review premium. Do not create a separate process/task.

Reassess when assumptions fail, cross-component effects emerge or evidence contradicts
the plan. Resolved hard decisions can permit a lighter implementation setting
when the remainder is routine and verifiable; unresolved integration, failures,
synthesis or architecture still require capability.
Retain Astra when that difficult work remains. Different phase pairs do not override
the user's selected model.

At implementation start, reuse the plan's pair if assumptions hold; otherwise explain
the revised recommendation and follow section 5. A plan does not authorize implementation.
A recommendation does not authorize new chats, agents, paid APIs or configuration changes.
Continue authorized work when the working recommendation is unchanged.

## 5. Pause when the working recommendation changes

When new evidence changes the recommended model OR effort, including a decrease,
notify the owner immediately and pause substantive work. A hypothetical alternative
alone is not a changed recommendation.

State the previous agreed/recommended pair (not confirmed active without metadata),
new pair, concrete evidence/reason, exact pause point and remaining work. Offer
switching or explicitly continuing unchanged; add a stop choice when useful.
Use an interactive question tool if supported in the current mode, otherwise ask
in plain text. Delivery or a preselected answer is not consent. End the turn awaiting
the user's choice; do not continue investigation, edits or execution. Only necessary
safe completion of an in-flight operation and a compact continuity note are allowed.

For switching, ask the user to select settings in the interface for the next turn
and confirm before resuming, unless an authorized supported control applies them
with verified effective-setting readback. A recommendation or selected answer
does not prove a switch. Never simulate switching by changing a global default,
creating a chat or resending the task.

If the user chooses continuing unchanged, resume with the identified uncertainty.
Honor decisions already given for the same change; do not repeat the question without
new evidence or a newly relevant phase boundary.

Raise recommendations for reasoning failures such as repeatedly lost qualifiers,
unresolved contradictions or missed interactions. Do not escalate unchanged retries
for missing tools, inaccessible data, permissions or product decisions. Effort never
replaces dependency tracing, verification or owner acceptance.

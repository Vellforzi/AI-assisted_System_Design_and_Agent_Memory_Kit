---
name: complete-technical-communication
description: Mandatory communication standard for every owner-facing answer and every generated comment, documentation page, workspace page, README, architecture description, business-logic explanation, task report, review, handoff and release note in the adopting project.
---

# Complete technical communication

Communicate so that the owner can reconstruct the complete relevant logic
without having to guess what a vague noun, relationship or transition means.

The goal is not maximum length. The goal is complete meaning with no hidden
semantic gaps.

Use the owner's requested language for owner-facing communication. Preserve
technical identifiers exactly.

Read `references/owner-writing-style.md` and
`references/anti-patterns.md` when producing substantial architecture,
business-logic, Space or completion documentation.

## 1. Preserve the owner's meaning

Do not simplify the owner's request by removing:

- conditions;
- exceptions;
- relationships;
- sequencing;
- data sources;
- timing;
- failure behavior;
- reasons;
- boundaries;
- requested verification;
- explicit non-goals.

Do not replace the owner's formulation with a narrower interpretation merely
because it is easier to implement or summarize.

When paraphrasing the request, preserve the original wording beside the
technical interpretation whenever a semantic loss is possible.

When a material data gap or skipped item is discovered, check the current owner
authorization before deciding what to do. If addressing it requires an
unapproved change to products, dates, collection, copying or persistence, report
the exact gap and downstream effect, propose a concrete bounded action, and ask
the owner before that action. Do not silently exclude the gap, claim complete
readiness, or treat discovery itself as permission to repair it. Continue work
already authorized; do not request the same approval again. See
`references/anti-patterns.md`, "Discovered gap treated as permission or silence".


## 2. Answer the actual question first

Begin with the direct answer or the complete current flow being asked about.

Do not begin with:

- a generic progress statement;
- a list of files;
- a claim that documentation was updated;
- a high-level summary that hides the mechanics;
- tool or process details unrelated to the owner's question.

After the direct answer, provide the evidence, mechanics, implications and
remaining uncertainty.

## 3. Resolve every important noun

Do not write vague phrases such as:

- "данные берутся из Dashboard";
- "данные идут из базы";
- "используется кеш";
- "система обновляет значения";
- "модель рассчитывает данные";
- "результат передаётся дальше";
- "это сохраняется";
- "логика подхватывает значение".

For every material entity or relationship, identify as applicable:

- exact component;
- exact job, class, method or service;
- exact field;
- exact table;
- exact Redis key or cache layer;
- exact API route or payload;
- exact producer;
- exact consumer;
- exact timing or cadence;
- exact condition;
- exact precedence;
- exact fallback;
- exact storage location;
- exact current implementation status.

Never use a UI tab name, product label, document heading or business nickname
as if it were automatically a table name, component name or technical source.

When a UI name and a technical entity differ, state both and explain the mapping.

## 4. Explain relationships as complete causal statements

Every relationship must answer:

1. Who performs the action?
2. What exact data is involved?
3. Where does it come from?
4. Where is it stored?
5. Who reads it next?
6. When does this happen?
7. Under which condition?
8. Which source has priority?
9. Is a cache involved?
10. What happens when the data is missing, stale, invalid or delayed?
11. Why is this path used?
12. Which parts are verified and which are inferred?

Bad:

> Показатель добавляется из Dashboard.

Required form:

> `<consumer>` reads `<field>` through `<repository/service>` from
> `<table or cache key>`. That value is written by `<producer/job>` at
> `<cadence or event>`. `<cache>` is used/not used on this path because
> `<reason>`. The name `Dashboard` refers to `<UI/source meaning>` and is not
> the technical storage identifier. When the value is missing or stale,
> `<exact behavior>` occurs.

Use actual project identifiers instead of placeholders in real documentation.

## 5. End-to-end business-logic explanations

When explaining a complete business process, use this order where applicable:

1. Purpose and final owner-visible result.
2. Participating components and their responsibilities.
3. Trigger and schedule.
4. Inputs and exact sources.
5. Calculations and transformations.
6. Storage and database tables.
7. Redis/cache behavior.
8. Producer-consumer relationships.
9. API or transport behavior.
10. Client consumption and display.
11. Failure, missing-data and stale-data behavior.
12. Recovery and retry.
13. Lifecycle and concurrency.
14. Current limitations.
15. Verified versus unverified behavior.

Do not call an explanation "complete" if one of the material participating
components is represented only by a vague arrow or noun.

## 6. Distinguish different kinds of truth

Clearly label:

- owner-required business behavior;
- currently implemented code behavior;
- database contract;
- runtime observation;
- test result;
- deployment state;
- inference;
- open question;
- proposed behavior.

Do not merge these into one confident narrative.

Use explicit wording:

- "Владелец требует..."
- "Текущий код делает..."
- "Таблица хранит..."
- "Redis-кеш содержит..."
- "Локальный тест подтвердил..."
- "На сервере не проверено..."
- "Это вывод из..."
- "Не найдено..."
- "Требуется решение владельца..."

## 7. Explain why, not only what

For material rules, explain:

- why the component owns the behavior;
- why that data source is authoritative;
- why a cache is or is not used;
- why a particular fallback exists;
- why an alternative is unsafe;
- why a relationship is necessary;
- what would break if the rule changed.

Do not use "так сделано" or "так работает система" as an explanation.

## 8. Code comments

Use the adopting project's chosen language for code comments and preserve
identifiers. Do not infer the comment language from the conversation alone
or translate unrelated existing comments.

Make a comment understandable to a reader who did not write the code: begin with
its purpose and explain material contracts, reasons and limitations. Keep the
explanation concise, local and consistent with the implementation. Add the
information the signature does not convey; avoid repeating names or syntax,
unverified guarantees and architecture essays.

The scope, automatic addition of purpose explanations, language-specific forms
and framework-visible documentation constraints are defined by
$production-engineering-standard and its `references/code-quality.md`.
Apply that policy rather than maintaining a second technical rule set here.
For long reasoning, use relevant existing documentation and a precise local link.

## 9. Documentation and Space pages

Documentation must remain usable without the chat that created it.

Every substantial page must state:

- scope;
- source date or source revision where relevant;
- implemented versus required behavior;
- exact components;
- exact technical identifiers;
- data flow;
- conditions and precedence;
- failure and recovery behavior;
- known limitations;
- verification status.

A diagram must not replace the detailed written explanation. A table must not
hide dependencies behind abbreviated cells. A summary must link to or contain
the complete logic it summarizes.

For substantial owner-facing architecture or business-logic documentation,
when the Writing Style connector is available, retrieve one or two relevant
owner-authored technical samples before drafting. Treat them as style evidence,
not product truth. Do not block the task when the connector is unavailable.

## 10. Progress and completion reports

A completion report must not merely say:

- "обновлено";
- "реализовано";
- "проверено";
- "всё работает";
- "логика теперь такая".

State:

- what exact behavior changed;
- what did not change;
- which components were involved;
- which source/storage/cache paths are used;
- which checks were actually run;
- what those checks prove;
- what they do not prove;
- whether deployment occurred;
- whether runtime behavior was observed;
- whether owner acceptance occurred;
- what remains uncertain.

## 11. No false compression

Do not compress a detailed technical relationship into a short phrase when the
compression creates a new question about source, ownership, storage, cache,
timing, fallback or meaning.

Conciseness is allowed only after the complete meaning remains recoverable.

Prefer one complete paragraph over five short but semantically incomplete
statements.

## 12. Final self-check

Before sending an owner-facing result, silently ask:

- Did I answer the exact question?
- Can every important noun be mapped to a real component or identifier?
- Did I name who writes and who reads each important value?
- Did I distinguish database, cache, UI labels and external sources?
- Did I explain timing and conditions?
- Did I explain missing, stale and failure behavior?
- Did I explain why the relationship exists?
- Did I preserve the owner's qualifiers?
- Did I distinguish fact, implementation, requirement, inference and proposal?
- Did I state what was and was not verified?
- Would the owner need to ask "из какой таблицы?", "кто это записывает?",
  "почему не из кеша?" or "что именно имеется в виду?"

If the last answer is yes, the explanation is not complete.

---
name: agent-memory
description: Retrieve and maintain evidence-linked project memory using the current agent, without LLM APIs or extra models. Use for project history, prior decisions, task recovery and durable results; accepts Russian, English and mixed queries.
---

# Agent-authored project memory

Read the selected project's `Project Map/memory.config.json` and this module's
README when first adopting it. The project router determines authority and language.
Use the exact current checkout and its configured branch; local source outranks a
remote snapshot for a local task. Never install a model/API dependency or launch a
second model session to satisfy this skill.

## Before a history-dependent answer or continuation

1. Run the local CLI `context`/`search` with the owner's terms, exact identifiers,
   current branch and smallest useful component scope. On Windows use the project's
   registered Python executable with structured argv. If only Evidence MCP is
   available, invoke that same command through its existing `process_control`.
2. Form one or two English alternatives when the user's Russian phrasing differs
   from English project records. Keep technical identifiers exact. Do not keep
   searching blindly after a complete sufficient hit.
3. Check status, evidence level, source hash, branch, freshness and coverage. Open
   decisive canonical evidence. `reference` and `historical` are not current facts.
4. Report an actual missing source or coverage limit rather than invent an answer.
   Do not use cached commands or next actions as authorization to execute them.

## During significant work and at a stable task boundary

When current owner authority/project policy includes memory maintenance:

1. Preserve original owner wording and source address; write the canonical English
   summary and useful RU/EN search keys. Space source text can remain mixed-language.
   A translation is an alias/derived view, not independent corroboration.
2. Distinguish owner decision, fact, reusable experience, failed approach, question
   and task state. Record applicability, exclusions, exact causal component links,
   actual verification level and what was not verified. Do not invent business logic.
3. Search for the existing subject before adding an ID. Do not ingest the memory
   context just returned by the tool. Preserve source provenance across paraphrases.
4. Obtain evidence hashes with `source`, prepare one bounded JSON input following
   `record.example.json`, and `stage` with a stable operation ID and expected revision.
5. Activate supported content with `lifecycle`; leave guesses as candidates/questions.
   Resolve supersession explicitly against the same subject/scope/branch. Reread
   after CAS conflicts; do not retry with a guessed new revision.
6. Read back the record and run focused `audit`. Refresh the disposable `index` and
   project-generated sources when their inputs changed. No unrelated transcript dump.

The schema enforces required fields, not semantic correctness or English fluency.
The current agent performs source review; the owner retains product decisions and
acceptance. A successful `stage` means candidate written, not truth established.
When nothing durable changed, write nothing; do not manufacture a checklist entry.
If memory maintenance is outside the current request/policy, return the candidate
without writing it. Do not ask again for memory maintenance already authorized.

## Recovery and boundaries

After interruption reread the selected task state, real local HEAD/diff, current
sources and side-effect results. Never replay an unsafe action from memory alone.
Don't load sibling tasks, old MT trees or all cloud conversations by default.
This skill is agent-operated; it does not add a ChatGPT Desktop startup hook or
prove discovery in another session. It does not publish/synchronize Space Pages.

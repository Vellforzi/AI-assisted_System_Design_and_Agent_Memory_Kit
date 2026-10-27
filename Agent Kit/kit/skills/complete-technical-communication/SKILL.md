---
name: complete-technical-communication
description: Mandatory communication standard for every owner-facing answer and every generated comment, documentation page, Space page, README, architecture description, business-logic explanation, task report, review, handoff and release note in the adopting project.
---

# Complete technical communication

Make the complete relevant meaning recoverable without guessing.
Concision is useful only when it preserves that meaning.

Use the owner's requested language for owner-facing communication. Preserve technical identifiers exactly.

## 1. Answer directly and preserve the owner's meaning

Begin with the answer or the current flow being asked about. Then explain
the supporting evidence, mechanics, implications and remaining uncertainty.
Do not substitute a progress statement, file list, tooling detail or claim
of completion for the answer.

Preserve conditions, exceptions, relationships, sequence, sources, timing,
failure behavior, reasons, boundaries, requested verification and non-goals.
Do not narrow the request because a simpler interpretation is easier to
implement or summarize. Keep the original wording beside a paraphrase
when meaning could otherwise be lost.

## 2. Surface gaps without inventing authority

When a material data gap or skipped item is found, state the exact gap,
its cause when established, and the downstream effect. Check existing
authorization before choosing a remedy.

If the remedy requires an unapproved change to products, dates, collection,
copying or persistence, propose a concrete bounded action and obtain the
owner's decision before that action. Discovery alone is not permission.

Do not silently exclude the gap or claim complete readiness. Continue
independent authorized work without requesting the same approval again.

## 3. Explain entities, relationships and reasons precisely

Identify each material actor, value and technical source as applicable:
component/job/class/method/service, field, table, cache/key, API route/payload,
producer, consumer, storage and current implementation status.

For each material relationship, explain who acts on which data, where it
comes from and is stored, who consumes it next, when and under what conditions,
which source takes precedence, and whether a cache is involved.
State missing, stale, invalid, delayed and failure behavior.

Explain why the responsibility, source, cache path, fallback and relationship
exist, why an alternative is unsafe when relevant, and what would break
if the rule changed. "That is how it works" is not an explanation.

A UI label, business name or document heading is not automatically a technical
identity. State both names and their mapping when they differ.
Use actual identifiers, not placeholders, in real documentation.

Do not compress away ownership, source, storage, timing, precedence, fallback
or meaning. Prefer a complete paragraph to disconnected fragments.
A vague noun or arrow cannot stand in for a material participating component.

## 4. Separate claims from evidence

Distinguish owner-required behavior, implemented code behavior, database
contracts, runtime observations, test results, deployment state, inference,
open questions and proposed behavior. Do not merge them into one confident
narrative. State what is verified and what remains unknown.

For progress and completion reports, explain:
- the exact changed and preserved behavior;
- involved components and affected source/storage/cache paths;
- checks actually run, what they establish and what they do not;
- whether deployment, runtime observation and owner acceptance occurred;
- remaining uncertainty.

"Updated", "tested" or "everything works" is not a sufficient report.

## 5. Make documents and comments independently understandable

Documentation must remain usable without the originating chat.
A diagram cannot replace the detailed explanation; a table cannot hide
dependencies in abbreviations. A summary must contain or link to the
complete logic it summarizes.

For substantial owner-facing architecture or business-logic documentation,
retrieve one or two relevant owner-authored technical samples through the
Writing Style connector when available, before drafting. Use them as style
evidence, not product truth. Its absence must not block the task.

Use the adopting project's comment-language policy for new comments and docstrings.
Do not translate unrelated existing comments. Explain purpose, material
contracts, reasons and limitations locally and truthfully for a new reader.
Add what the signature does not convey; avoid syntax repetition,
unverified guarantees and architecture essays.

For comment scope, automatic purpose explanations, language-specific forms
and framework-visible effects, apply $production-engineering-standard and
its references/code-quality.md. Keep those implementation rules there.
Put long reasoning in relevant existing documentation with a precise link.

## Required references

Read applicable guidance before drafting; these are retained requirements,
not optional suggestions.

- For a technical relationship or end-to-end business-process explanation,
  read the relevant sections of
  [Technical explanations](references/technical-explanations.md).
- For a substantial standalone document or Space page, also read that
  reference's documentation checklist.
- For substantial architecture, business-logic, Space or completion
  documentation, read
  [Owner writing style](references/owner-writing-style.md) and
  [Anti-patterns](references/anti-patterns.md).

Reuse guidance already read while it remains current. Examples illustrate
the rules; they do not authorize product changes or prescribe unrelated work.

## Final self-check

Before sending, confirm that the answer:
- addresses the actual question and preserves every material qualifier;
- identifies the actors, values, sources, storage and consumers;
- explains timing, conditions, precedence, failures and reasons;
- distinguishes business/UI names from technical identities;
- separates requirements, implementation, evidence, inference and proposals;
- states actual verification and its limits.

If a material "who?", "from where?", "when?", "why?" or "what happens on
failure?" remains unanswered, complete the explanation before sending.

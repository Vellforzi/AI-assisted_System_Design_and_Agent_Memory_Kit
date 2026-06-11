# README Authoring Guide

Status: publishing guide
Purpose: keep public README files useful, concise, and aligned with Agent Memory Kit.

---

## 1. README hierarchy

Use three README levels:

1. root package README — what the whole toolkit is;
2. tool-level README — what each major tool does;
3. implementation-level README — how to use files inside a folder.

Do not put the full protocol in every README.

---

## 2. Root README should contain

- one-sentence purpose;
- who it is for;
- what problems it solves;
- repository layout;
- quick start;
- core safety rules;
- what is included;
- what is not included;
- version and status.

---

## 3. Tool README should contain

For each tool:

- purpose;
- start file;
- key concepts;
- common workflows;
- non-goals;
- relation to the other tool.

---

## 4. Folder README should contain

- exact files in the folder;
- how to copy/adapt templates;
- recommended order;
- warnings about secrets and project truth.

---

## 5. Keep it laconic

A README should route the reader. It should not become the full memory operating protocol.

If a README exceeds practical scanning length, move detail into a guide and link to it.

---

## 6. Public positioning section

For public publishing, include a short "How this differs" section.

Recommended points:

- not a hidden provider-memory feature;
- not a vector database by itself;
- not an autonomous-agent runtime;
- not a chat-summary archive;
- owner-controlled, file-first, inspectable Project Map;
- source authority and grounding before project claims;
- answer-only default and explicit action gates;
- eval cases based on real failures.

Link to `POSITIONING_AND_ALTERNATIVES.md` instead of copying the whole comparison.

---

## 7. When the kit is effective

State the conditions clearly:

- project has enough complexity to benefit from durable memory;
- owner is willing to maintain Project Map;
- source authority can be defined;
- agents have at least basic permission controls;
- repeated failures are converted into eval cases;
- the owner keeps high-risk actions gated.

---

## 8. Avoid overclaiming

Do not claim that the kit guarantees model compliance, replaces security controls, fully automates evals, or solves long-running autonomy by itself.

The honest claim is narrower and stronger: the kit gives the owner a portable operating contract for project truth, memory lifecycle, action permission, checkpoints, and behavioral regression checks.

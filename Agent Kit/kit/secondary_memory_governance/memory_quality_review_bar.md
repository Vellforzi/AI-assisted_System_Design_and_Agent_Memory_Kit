# Memory-Quality Review Bar

Status: reusable review checklist
Last aligned: <YYYY-MM-DD>
Audience: owner, reviewers, AI/Codex sessions
Runtime impact: none
Authority: secondary governance review checklist; operational docs and current owner instructions win
Purpose: block memory, retrieval, permission, and governance changes that weaken owner control or source authority.

Do not approve a memory, rule, schema, retrieval, or permission change if it:

- weakens source authority;
- allows stale memory to become current truth in normal answer, plan, or resume profiles;
- stores external research as a project fact without evidence and promotion;
- broadens apply or mutation permission through vague wording;
- adds a memory class without lifecycle or status rules;
- increases always-loaded context instead of using index, search, or hydration;
- duplicates operational docs into Project Map as competing truth;
- adds silent durable auto-capture;
- omits evidence refs for material claims;
- stores secrets, raw private data, raw external-system payloads, or tokens;
- treats embeddings, similarity score, or entity links as source of truth.

Expected review output:

```text
Findings:
- Critical:
- High:
- Medium:
Source authority impact:
Retrieval impact:
Lifecycle/staleness impact:
Permission/action-intent impact:
Evidence/claim-check impact:
Eval trigger:
Required repair:
Approval decision:
```

---
id: domain.layer.short-name
layer: causal
title: One sentence
status: coverage claim, not a novel
depends_on: []
see_also: []
code_anchors: []
journal_markers: []
annotations:
  - token: "[OK]"
    where: what was proven
    evidence_ref: receipt / smoke window / log slice
  - token: "[?]"
    where: what is still a hypothesis
    evidence_ref: missing
---

# Title

Copy this file into the adopting project's atlas. One causal scenario per
file. Keep it short. See `../SCHEMES_AND_COVERAGE_ATLAS.md`.

Replace the placeholder header fields. Keep the legend tokens closed.

## Sequence

```mermaid
sequenceDiagram
    participant Owner
    participant Surface
    participant Runtime
    Owner->>Surface: named action
    Surface->>Runtime: request
    Runtime-->>Surface: TOKEN_X
    Note over Surface: [OK] or [BUG-OPEN]
```

## Must not claim

- Parent chain is `[OK]` just because this axis closed.
- Compile equals live behavior.

# Eval Case Builder Skill

Use this skill when an agent repeats a failure or violates an Agent Memory Kit contract.

## Required fields

```yaml
id:
title:
failure_mode:
input_prompt:
required_behavior:
forbidden_behavior:
trusted_sources:
grader:
severity:
```

The goal is to prevent regressions in behavior such as unauthorized edits, stale fact use, provider-memory contamination, or Project Map writes without approval.

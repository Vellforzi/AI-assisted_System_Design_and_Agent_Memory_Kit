# Source Authority Audit Skill

Use this skill to verify which files are authoritative for a project area.

## Rules

- Prefer code and database schema over stale docs for API/DB contracts.
- Mark legacy documents as legacy until verified.
- Do not promote external research into project truth.
- Report missing evidence explicitly.

## Output

```text
Area:
Authoritative sources:
Secondary sources:
Legacy/stale sources:
Conflicts:
Missing evidence:
Recommended source_authority.yaml delta:
```

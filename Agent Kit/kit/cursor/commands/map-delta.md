# /map-delta

Purpose: propose Project Map changes without applying them.

Mode: plan
Mutations: forbidden

Use this when the current session discovered durable project information but the owner has not explicitly authorized Project Map writes.

Output format:

```yaml
project_map_delta:
  proposed_updates:
    - target_file:
      change_type: add | update | mark_stale | supersede | remove_candidate
      summary:
      evidence:
      confidence:
      owner_review_needed: true
  not_updated:
    - reason:
```

Rules:

- Do not write files.
- Do not promote research output to project fact without project evidence.
- Do not use compressed chat summary as evidence.

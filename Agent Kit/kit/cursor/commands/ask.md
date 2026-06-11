# /ask

Purpose: read-only question/analysis mode.

Mode: answer or analyze
Mutations: forbidden

Rules:

- Answer from allowed evidence only.
- Do not edit files, run mutating commands, write Project Map, push, deploy, or touch DB/secrets.
- Use explicit refs first. Implicit IDE context is advisory only unless scoped/approved.
- If model/settings advice is requested, use `/settings` and show the provider snapshot date.

Return a direct answer, missing evidence, and at most one next-step suggestion.

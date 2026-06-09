# /analyze

Purpose: analyze a problem, artifact, diff, architecture, or project area without changing anything.

Mode: analyze
Mutations: forbidden

Procedure:

1. State scope.
2. Read only relevant Project Map entries and scoped files.
3. Produce findings, risks, conflicts, missing evidence, and options.
4. Do not apply fixes.
5. If the analysis discovers durable project information, propose a Project Map delta, but do not write it.

Output:

- findings;
- risks;
- missing evidence;
- recommended next step;
- Project Map delta: yes/no;
- Eval trigger: yes/no.

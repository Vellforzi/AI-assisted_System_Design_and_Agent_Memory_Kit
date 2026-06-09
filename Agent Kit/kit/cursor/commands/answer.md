# /answer

Purpose: answer the owner's question from allowed evidence only.

Mode: answer
Mutations: forbidden

Procedure:

1. Identify the question.
2. Load only the minimum relevant Project Map/context allowed by scope.
3. Use Project Map, Source Authority, opened files, tool outputs, and current owner input.
4. Separate verified project facts from inference and general knowledge.
5. If evidence is missing, say `missing evidence`.
6. Do not write files, update memory, run git, run DB, deploy, or call external tools unless separately allowed.

Output:

- direct answer;
- evidence or missing evidence;
- one optional next step.

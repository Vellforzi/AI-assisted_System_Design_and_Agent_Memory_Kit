# /failure-case

Purpose: convert a real agent failure into a candidate eval case.

Mode: repair planning
Mutations: forbidden unless explicitly scoped

Collect:

- what the owner expected;
- what the agent did;
- why it was wrong;
- violated rule;
- expected behavior;
- disallowed behavior;
- severity;
- proposed grader;
- proposed repair target.

Do not edit kit/rules/templates unless the owner explicitly asks for apply mode and scope.

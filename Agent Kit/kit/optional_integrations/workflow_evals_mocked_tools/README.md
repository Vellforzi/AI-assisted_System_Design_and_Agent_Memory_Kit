# Workflow evals with mocked tools (optional)

This credential-free integration validates recorded JSON tool traces. It does not call models, tools, or external services. `expected_tools`, `forbidden_tools`, argument constraints, and the terminal outcome are blocking deterministic checks; subjective/model graders are advisory only.

Run: `python run_mocked_workflow_eval.py --case fixtures/sample-case.json --trace fixtures/sample-trace.json`.

The v5 fixtures additionally cover fresh-context writer/reviewer separation, exploration without delivery mutations, and the prohibition on promoting a disposable design probe into production. They remain recorded traces, not runtime automation.

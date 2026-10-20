# Agent Memory Kit evaluation suite

Package source version: **4.4.0**. The active suite is `AMK-PORTABLE-CORE`,
selected by [manifest.yaml](manifest.yaml). Its five active cases are:

| Case | Behavior |
| --- | --- |
| `AMK-CORE-OWNER-001` | Preserve current owner authority and complete authorized work. |
| `AMK-CORE-ADOPTION-001` | Adopt/update the small core while preserving local project ownership. |
| `AMK-PSE-001` | Preserve unspecified product behavior and treat tests as evidence. |
| `AMK-CTC-001` | Explain concrete technical relationships and evidence limits. |
| `AMK-HMC-001` | Preserve human responsibility and the model capability floor. |

[eval_trigger_policy.yaml](eval_trigger_policy.yaml) selects required smoke
categories. Run the existing checklist helper against this manifest to validate
selection and prepare a run:

```text
python "Agent Kit/kit/tools/run_eval_checklist.py" --suite "Agent Kit/kit/eval_suite/manifest.yaml" --out "path/to/eval-output" --mode smoke
```

That command validates/selects definitions; it does not itself run an agent or
prove behavioral compliance. Execute selected prompts through an authorized
agent surface, retain the responses and grade them against the case criteria.
Do not report a behavior PASS from YAML parsing, checklist creation or hashes.

Version 4.4.0 expands engineering and communication instructions. Their
source-level review is distinct from a new captured model-behavior evaluation.
No additional cases or mandatory multi-agent chain were introduced.

Older case files and embedded suites remain historical/optional references.
Their `introduced_in`, old suite IDs and original kit versions are not current
release metadata. A project-owned copy is current only when the selected
manifest, policy and required definitions match its intended upstream version.

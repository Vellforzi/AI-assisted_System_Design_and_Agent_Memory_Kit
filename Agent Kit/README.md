# Agent Memory Kit

Candidate version: 4.2.0-dev. Published base: 4.1.0.

Use [the short workflow](portable/core/WORKFLOW.md) and
[portable adoption](portable/README.md). This is the current default entry.

`portable/package.json` lists the distributable core and binds its bytes.
`INSTALLATION.json` in an adopting project records baseline and local overrides.
Project-specific policies and private history are not part of the core package.

The `kit/` directory is a reference library for optional capabilities. Read only
what the current task needs: recovery, evidence, evals, hooks or stronger delivery
proof. A reference guide does not add permission or activate its own mechanism.

Kit quality is assessed through reproducible adoption/update checks and actual
agent traces. File count and a passing YAML schema do not measure agent quality.

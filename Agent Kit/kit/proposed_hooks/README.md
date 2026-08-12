# Proposed hook functions

Status: canonical working-method cards plus copyable example bytes
Purpose: show which hooks to create, how to limit them, and give portable
scripts. Copy the **function**. Do not paste a private project's paths,
hosts, or product names into the examples.

Existing kit examples remain valid:

- Cursor: `cursor/hooks/scripts/` (secrets, db, git, scope, Project Map)
- Codex: `codex/hooks/scripts/` (dangerous command, compaction, Project Map)

This folder adds the **combat-method** hooks that a high-control layout
uses and that were not yet offered as cards: contract guard, execution
profile, finalization, encoding-safe writes, fail-closed invoke wrapper.

Recovery payload shape: `../HOOK_RECOVERY_PLAYBOOK.md`.
Request workflow: `../HOOK_REQUEST_WORKFLOW.md`.

A scheme cannot enforce these. A CN states the fact. The hook is the
machine stop.

---

## Cards

### H1. Fail-closed invoke wrapper

**Job:** every hook event goes through one wrapper. Empty stdout is a
deny, not a pass.

**Limit:** never exit 0 with no JSON on a blocking event. Crash = deny
payload + playbook.

**Bytes:** `scripts/invoke_wrapper.example.py`

### H2. Task contract guard

**Job:** mutating apply/stage/map-apply requires a plain contract file
(gates, output root, one artifact glob, baseline, owner write
authorization). Hybrid prose+YAML paste is narrative only.

**Limit:** do not accept a bootstrap paste as `--contract`. Materialize
YAML in the same task. Do not open a recovery task for that.

**Bytes:** `scripts/task_contract_guard.example.py`

### H3. Execution profile gate

**Job:** R1–R4 work resolves exactly one route from mode + task class +
path zone, with toolchain and write lock named.

**Limit:** zero or multiple equal-priority matches = deny. Unregistered
launcher = deny.

**Bytes:** `scripts/execution_profile_gate.example.py`

### H4. Task finalization guard

**Job:** stop/complete cannot claim verified delivery without the
receipts the contract named.

**Limit:** compile is not done. Writer self-PASS is not done. Missing
oracle = deny finalization.

**Bytes:** `scripts/task_finalization_guard.example.py`

### H5. Encoding / host-write guard

**Job:** block project file writes through host redirections that corrupt
text (PowerShell Set-Content/Out-File, file-association script launch).

**Limit:** this is harness, not product. Deny and tell the agent to use
the structured editor / registered interpreter.

**Bytes:** `scripts/text_file_write_guard.example.py`

---

## Install

Copy into the adopting project's `.cursor/hooks/` or `.codex/hooks/`.
Wire `hooks.json` with `failClosed: true` on mutating events
(`beforeShellExecution`, apply/stop as the host allows).

Unproven hooks: report unproven and enforce the same checks manually.
See proposed CN `CN-HOOKS-UNPROVEN`.

Do not claim these example scripts are a drop-in for a private combat
tree. They are the **offered functions** with runnable shape.

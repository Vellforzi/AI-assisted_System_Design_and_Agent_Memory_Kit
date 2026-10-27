---
name: create-hook
description: Create or update native Codex or Cursor hooks, hook configuration and scripts for agent events.
---

# Create native hooks

Identify the actual client, execution host and target configuration from current
evidence, not this skill's legacy title. Codex and Cursor have different events,
schemas and path rules; a .cursor path does not configure Codex.

Honor analysis-only requests. When implementation is requested, create or update
the required files rather than stopping at format advice. Preserve unrelated
hooks and change only the entries needed for the owner's outcome.

## 1. Establish the contract

Determine project/user scope, trigger, audit/permission/rewrite/context/continuation
behavior, supported handler type, filtering and intended fail-open/fail-closed
behavior. Infer available answers; ask only for material missing requirements.
Choose the narrowest event that implements the requested behavior.

Prefer project scope for repository-shared behavior. This preference does not
authorize committing or publishing it.

## 2. Load the target client's guidance

- **Codex:** use $openai-docs, installed native configuration/schema and current
  official documentation as needed. Project hooks use .codex/hooks.json;
  common hooks use the actual CODEX_HOME. Inspect existing active configuration
  before adding another source. Verify session cwd, exact session identity,
  event-specific output, enabled state and trust separately. Never silently
  enable a disabled hook or treat a present definition as trusted/active.
- **Cursor:** read [Cursor hooks](references/cursor-hooks.md) before choosing
  paths, events, matchers, fields, exit behavior or examples. Verify applicable
  semantics against current official Cursor documentation and the target host.

Use only the selected client's supported handler and event contract. Command
hooks are the default choice for deterministic, auditable logic. Use prompt
hooks for lightweight policy decisions only where the target supports them.

## 3. Implement and filter safely

Create the script in the directory appropriate to its configuration source.
Verify the actual launcher, interpreter, dependencies, working directory and
path resolution in the hook environment. Do not assume jq, Python, Node or
repo-local commands exist because they work elsewhere. Use command -v or the
platform equivalent; give directly executed scripts the required permissions
and a valid interpreter/shebang where applicable.

Read the event input through its documented channel and return only supported
event-specific fields. Verify how intentional denial, crash, timeout, malformed
output and nonzero exit are interpreted. A configured failure policy cannot
protect a script that catches a failure and returns successful allow output.

Use a matcher when appropriate, with the event's actual match target and regex
dialect. Start with no matcher or the simplest safe one; for a narrow risky
command family, prefer script-side filtering before adding a complex matcher.
Confirm loading and firing before tightening it. When diagnosing parsing or
matcher failures, simplify in a safe test context without disabling a live guard.

## 4. Verify the delivered hook

Through the configured launcher, verify ordinary allow and genuine-boundary
deny from both repository root and nested cwd. Exercise the selected failure
policy and confirm dependencies are reachable from the hook process.

Trigger the relevant native event within current authority and inspect the
actual client's hook diagnostics. Helper success alone does not prove native
attachment. If native execution is unavailable or unauthorized, finish safe
local verification and report that exact gap.

Troubleshoot source/path/schema/matcher parsing and executable availability;
use only the target client's verified reload/restart behavior. Preserve disabled
state and trust decisions. Do not restart a client or exercise external side
effects outside current authority.

Report changed files, event/filter and allowed/denied behavior, actual checks,
and remaining activation/trust/runtime limits. Keep helper, launcher and native
event evidence distinct. Follow applicable engineering and communication rules
without recreating their general workflow here.

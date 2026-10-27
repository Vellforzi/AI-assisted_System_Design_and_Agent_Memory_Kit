# Temporal verification

Read before selecting or interpreting checks for an affected MQL event
lifecycle. These requirements supplement the engineering standard and do not
authorize terminal control.

## Sequence coverage

Select sequences that challenge the changed boundary and preserved invariants:

- cold start before dependencies exist, then their arrival;
- repeated ordinary timers/probes while a continuation is pending;
- view changes during a partial operation and delivery of an obsolete ticket;
- enqueue refusal, consumer early return and execution failure;
- cancellation, disposal/reinitialization and another instance where relevant.

Include a normal sequence that must finish. Check forbidden effects and eventual
progress under explicitly bounded/stable input. Establish expected outcomes
from owner requirements and verified platform contracts before testing.
Prefer existing source-linked checks. When an old failing version is available,
use the same targeted check to reject it and accept the corrected version.

## Diagnostic evidence

Distinguish enqueue, receipt, rejection, consumption and completion.
Record instance/ticket/revision, relevant flags, cursor and API result with
immediate error where applicable. Use existing diagnostics first; add only
bounded necessary observations. Repeated logs or successful API returns alone
do not prove progress.

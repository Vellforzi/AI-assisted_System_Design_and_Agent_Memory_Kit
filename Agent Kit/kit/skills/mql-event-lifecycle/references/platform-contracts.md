# Platform contracts for event lifecycle work

Official references checked 2026-10-20. These are narrow lookup anchors, not a
claim about every terminal build or every function. Reopen the material source
when a task depends on a detail, and inspect wrappers that may change behavior.
Do not generalize a queue rule for one event class to every other class.

## Program events and timers

| Boundary | Contract that changes reasoning | Primary sources |
| --- | --- | --- |
| Program callbacks | Event handlers execute sequentially in a program. A handler cannot wait for another callback of that same program to complete while retaining control. Other programs and terminal work are separate contexts. | [MQL5 program execution](https://www.mql5.com/en/docs/runtime/running), [MQL4 program execution](https://docs.mql4.com/runtime/running) |
| Timer delivery | At most one timer per program. When Timer is already queued or being processed, another Timer event is not added. Requested cadence does not promise one callback for every elapsed interval. | [MQL5 EventSetTimer](https://www.mql5.com/en/docs/eventfunctions/eventsettimer), [MQL4 EventSetTimer](https://docs.mql4.com/eventfunctions/eventsettimer) |
| Custom event | EventChartCustom returns true for successful placement in the receiving chart's event queue. This is not proof that the intended consumer accepted or completed the work. custom_event_id becomes CHARTEVENT_CUSTOM + that ID in the handler. | [MQL5 EventChartCustom](https://www.mql5.com/en/docs/eventfunctions/eventchartcustom), [MQL4 EventChartCustom](https://docs.mql4.com/eventfunctions/eventchartcustom) |
| Event payload | EventChartCustom truncates sparam longer than 63 characters. A prefix or ownership token transported there must survive the actual serialization; sender-side equality is insufficient. | Same EventChartCustom references |
| Initialization/shutdown | Init/Deinit are lifecycle events; relevant causes include period/symbol changes. Inspect actual program kind, deinitialization reason and storage lifetime. Do not equate a successful OnInit with readiness of independently arriving data. | [MQL5 terminal events](https://www.mql5.com/en/docs/runtime/event_fire), [MQL4 terminal events](https://docs.mql4.com/runtime/event_fire) |
| MQL4 EA period change | The documented symbol/timeframe change calls Deinit/Init without unloading the EA or resetting global/static variables. A retained ready flag can outlive the resource released by Deinit. Do not transfer this rule to a different program kind or platform without checking. | [MQL4 program execution](https://docs.mql4.com/runtime/running) |

Separate an external prerequisite that has not arrived from a dependency cycle
inside the program. Document the real source of the future notification; never
presume another timer will fix an orphaned pending state.

## Chart commands, reads and visible completion

| Operation | MQL5 | MQL4 |
| --- | --- | --- |
| ObjectCreate | Always asynchronous: true means the command was queued, execution result remains unknown. | On the current chart, direct access and true means successful creation. On another chart, asynchronous enqueue. |
| Checking an object after creation | ObjectFind/ObjectGet calls can establish the requested object/property result; synchronous reads may wait behind queued chart work. | Check the specific current/other-chart API contract rather than importing MQL5 behavior. |
| Visible rendering | A creation result or verified property is not by itself proof that the user saw the intended completed presentation. | Same evidence distinction; execution details still require the platform's own contract. |

Sources: [MQL5 ObjectCreate](https://www.mql5.com/en/docs/objects/objectcreate),
[MQL4 ObjectCreate](https://docs.mql4.com/objects/objectcreate),
[MQL5 ObjectFind](https://www.mql5.com/en/docs/objects/objectfind),
[MQL4 ObjectFind](https://docs.mql4.com/objects/objectfind).

Do not read every property on every timer as a generic completion strategy.
Identify the required completion boundary, existing checks, batch size and cost.
Do not treat ChartRedraw as an acknowledgement that arbitrary custom events or
bridge work have completed.

## Program kind, bridge and shared state

MQL5 EAs have separate execution threads; indicators on one symbol share a
thread. This matters for blocking work and resource contention; it does not
justify adding concurrency machinery to ordinary serialized callback state.
Source: [MQL5 program execution](https://www.mql5.com/en/docs/runtime/running).

For a bridge, inspect the exact exported function and completion consumer.
Record which state belongs to MQL, the DLL, a worker, a chart or persistent
storage. A function named Async/Poll/Ready is not evidence of its contract.
Keep platform-specific evidence separate from a Python/C# model of that route.

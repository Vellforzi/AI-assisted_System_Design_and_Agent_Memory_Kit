# Router fragment — model escalation trigger wording, v3.9.4

Insert this fragment into root routers or routing instructions that decide
model/provider escalation.

The user is not expected to predict model insufficiency. Start with the lowest
sufficient route for the current task. Escalate only after reporting a concrete
trigger: validation failure, schema/router conflict, insufficient context window,
missing model control, repeated scoped failure, or task reclassification to
audit/repair/protocol design.

Provider/model capability data is volatile. Keep it dated (`observed_at`) and do
not treat current model data as permanent project truth.

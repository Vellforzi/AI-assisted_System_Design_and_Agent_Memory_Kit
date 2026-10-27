# Technical explanations

Read the applicable sections before drafting technical relationships, complete
business processes or substantial standalone documents, as routed by SKILL.md.
These checklists remain mandatory; they do not authorize product changes.

## Causal relationship checklist

Every relationship must answer:

1. Who performs the action?
2. What exact data is involved?
3. Where does it come from?
4. Where is it stored?
5. Who reads it next?
6. When does this happen?
7. Under which condition?
8. Which source has priority?
9. Is a cache involved?
10. What happens when the data is missing, stale, invalid or delayed?
11. Why is this path used?
12. Which parts are verified and which are inferred?

Required form:

> `<consumer>` reads `<field>` through `<repository/service>` from
> `<table or cache key>`. That value is written by `<producer/job>` at
> `<cadence or event>`. `<cache>` is used/not used on this path because
> `<reason>`. The name `Heatmap` refers to `<UI/source meaning>` and is not
> the technical storage identifier. When the value is missing or stale,
> `<exact behavior>` occurs.

Use actual project identifiers instead of placeholders in real documentation.

## End-to-end process order

When explaining a complete business process, use this order where applicable:

1. Purpose and final owner-visible result.
2. Participating components and their responsibilities.
3. Trigger and schedule.
4. Inputs and exact sources.
5. Calculations and transformations.
6. Storage and database tables.
7. Redis/cache behavior.
8. Producer-consumer relationships.
9. API or transport behavior.
10. Client consumption and display.
11. Failure, missing-data and stale-data behavior.
12. Recovery and retry.
13. Lifecycle and concurrency.
14. Current limitations.
15. Verified versus unverified behavior.

Do not call an explanation "complete" if one of the material participating
components is represented only by a vague arrow or noun.

## Reasons and consequences

For material rules, explain:

- why the component owns the behavior;
- why that data source is authoritative;
- why a cache is or is not used;
- why a particular fallback exists;
- why an alternative is unsafe;
- why a relationship is necessary;
- what would break if the rule changed.

Do not use "так сделано" or "так работает система" as an explanation.

## Standalone documentation checklist

Every substantial page must state:

- scope;
- source date or source revision where relevant;
- implemented versus required behavior;
- exact components;
- exact technical identifiers;
- data flow;
- conditions and precedence;
- failure and recovery behavior;
- known limitations;
- verification status.

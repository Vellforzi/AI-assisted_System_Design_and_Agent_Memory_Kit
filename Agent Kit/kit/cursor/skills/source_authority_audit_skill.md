# Source Authority Audit Skill

Purpose: identify which files are authoritative for different project topics.

Procedure:

1. Inventory relevant files only.
2. Group by topic: routes, services, database schema, scraper jobs, cache, deployment, business rules, client code.
3. Propose authority order.
4. Mark conflicts and stale docs.
5. Do not update source_authority.yaml unless explicitly authorized.

Output:

- topic;
- candidate authoritative files;
- weaker sources;
- conflicts;
- missing evidence;
- proposed source_authority.yaml delta.

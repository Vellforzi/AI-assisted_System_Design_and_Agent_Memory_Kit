# OPTION_PROFIT toolchain boundaries

Read for implementation in the named component. These are verified starting
points from 2026-10-20, not replacements for current manifests/build settings.

| Component | Supported starting point | Verification boundary |
| --- | --- | --- |
| Options_api / Options_scraper | Python 3.13; Pipfile/Pipfile.lock | Run the component's `pipenv run typecheck` after Python changes; follow its `docs/TYPECHECK.md` for setup, baseline and import coverage. |
| OP_Bridge and PremiaOP.Tests | .NET Framework 4.7.2; C# 7.3 in relevant configurations | Resolve the exact build configuration before syntax/nullability changes; use registered build helpers. |
| PremiaRuntime | .NET 10; C# 14; nullable enabled; warnings as errors | Preserve the current Directory.Build.props contract and project checks. |
| MQL4 / MQL5 | Native platform compiler and current ABI | Verify type widths, serialization, event/lifecycle API and native compile separately. |
| PostgreSQL | Current schema and server/extension versions | Preserve NULL, precision, row grain and existing producers/consumers. |

New explanatory code comments are English. Owner-facing explanations remain
Russian. Do not translate unrelated existing comments or annotate entire modules
merely because one function changed.

Python type-check baseline represents existing diagnostic debt. A successful
baseline-aware check does not establish full typing correctness. Check the
affected contracts manually and keep runtime tests distinct. The local checker
does not authorize imports that start services, production probes or changes to
FastAPI/Pydantic runtime contracts.

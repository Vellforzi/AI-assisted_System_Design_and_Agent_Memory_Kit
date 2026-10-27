# Project toolchain boundaries

Before selecting syntax, types, static analysis or a build command, establish the
adopting project's supported language/compiler/runtime versions from its current
configuration and registered checks. Preserve framework, ABI, serialization and
consumer compatibility. A newer installed compiler does not authorize migration.

Use existing project launchers and environments. Do not install a checker,
dependency, framework or interpreter merely to satisfy a generic recommendation.
Treat pre-existing diagnostics separately from regressions; do not weaken checks
or silently expand into unrelated cleanup. Record unavailable checks precisely.

Follow the project's comment-language policy and the owner's requested language.
Do not translate unrelated existing comments or annotate entire modules as a side
effect. OPTION_PROFIT's concrete version and check routing is retained separately
in `skill-profiles/option-profit/references/option-profit-toolchains.md` in the
source library; it is not a default for other projects.

# Context Contract V1

## Objective

Оформить принадлежащий Kit языково-независимый контракт V1 для `ContextRequestV1`, `ContextBundleV1` и `ContextReceiptV1`: versioned JSON Schemas, переносимый corpus valid/invalid payloads и smoke fixtures, а также краткое руководство для Python и TypeScript adapters. Kit остаётся библиотекой артефактов и правил, а не отдельным runtime-сервисом.

## Original Request

Подготовить цель `context-contract-v1`: переиспользовать `context_governance_helper.py`, `context_index.yaml`, `retrieval_policy.yaml`, `retrieval_scoring_policy.yaml` и существующие context-selection smoke cases; создать versioned JSON schemas, valid/invalid examples, smoke fixtures для over-retrieval, under-retrieval, forbidden paths и stale authority, плюс краткое руководство для TypeScript и Python adapters. Не создавать скрытую agent memory и не дублировать существующие правила. Oracle: одни и те же fixtures проверяются в Python и будущей TypeScript-реализации.

## Intake Summary

- Input shape: `specific`
- Audience: maintainers Kit и авторы Python/TypeScript adapters
- Authority: `requested`
- Proof type: `test`
- Completion proof: все три versioned schema и требуемые примеры/fixtures существуют; Python-проверка проходит; независимый от языка manifest фиксирует те же ожидаемые результаты для будущего TypeScript validator.
- Goal oracle: один canonical fixture corpus даёт одинаковые нормализованные результаты в Python и в будущей TypeScript-реализации, без привязки к validator-specific error strings.
- Likely misfire: создать новый runtime, скрытое хранилище памяти или второй источник governance/retrieval правил внутри schemas/fixtures.
- Blind spots considered: диалект JSON Schema и правила URI/reference resolution; стабильные cross-language error codes; граница между структурной schema validation и policy evaluation; provenance/freshness authority; совместимость существующих smoke cases.
- Existing plan facts: названные helper/index/policy/smoke artifacts обязательны к переиспользованию; Kit владеет schemas, правилами и fixtures; runtime-сервис, hidden agent memory и дублирование правил запрещены.

## Goal Oracle

The oracle for this goal is:

`Один versioned, language-neutral fixture manifest можно прогнать Python adapter-ом сейчас и будущим TypeScript adapter-ом без изменения payloads или expected outcomes; оба дают одинаковые case ids, pass/fail и стабильные reason codes.`

PM должен после каждого Worker package сопоставлять receipt с этим oracle. Наличие файлов, успешная проверка только schema shape или один Python-only smoke не закрывают цель. Завершение допустимо только после финального Judge/PM-аудита с `full_outcome_complete: true`.

## Goal Kind

`specific`

## Current Tranche

Непрерывно пройти от карты существующих источников истины к одному согласованному implementation package: определить границы contract/policy, реализовать versioned schemas и canonical fixtures, подключить Python validation/oracle, описать TypeScript parity adapter, прогнать проверки и устранить локальные расхождения до полного доказательства исходного результата.

## Non-Negotiable Constraints

- Kit владеет schemas, правилами, fixtures и adapter guidance, но не становится отдельным runtime-сервисом.
- Не создавать hidden agent memory, background persistence, implicit user/profile store или новый memory subsystem.
- Не переносить и не копировать существующие governance/retrieval правила в schemas или fixtures; использовать ссылки, identifiers, expected reason codes и существующие policy sources.
- Переиспользовать `context_governance_helper.py`, `context_index.yaml`, `retrieval_policy.yaml`, `retrieval_scoring_policy.yaml` и context-selection smoke cases после подтверждения их точных путей Scout-ом.
- Зафиксировать versioning и JSON Schema dialect явно.
- Cross-language oracle сравнивает стабильные результаты, а не текст исключений конкретной библиотеки.
- Сохранить совместимость существующих smoke cases либо документировать и проверить намеренную миграцию без параллельного источника истины.
- Не вводить обязательный Node/TypeScript runtime в Kit только ради текущей проверки: TypeScript guide и parity contract должны позволять будущую реализацию на том же corpus.

## Stop Rule

Stop only when a final audit proves the full original outcome is complete.

Не останавливаться после discovery, design decision, создания одних schemas или успешного Python-only happy path. Если обязательная TypeScript реализация ещё не существует по исходному запросу, oracle закрывается доказательством того, что corpus и expected result format полностью language-neutral и реально прогоняются Python validator-ом; guide должен давать точную будущую TypeScript parity procedure.

Не создавать отдельную Worker/Judge пару для каждой schema или smoke category: schemas, examples, fixtures, validation и adapter guidance составляют один связный пакет, если Scout/Judge не обнаружат риск, требующий безопасного разделения.

## Slice Sizing

Safe means bounded, explicit, verified, and reversible. It does not mean tiny.

Основной Worker должен закончить цельный contract package, а не оставить набор несвязанных заготовок. Judge разделяет работу только при доказанной несовместимости write scopes, неоднозначном владении правилами или отсутствии надёжной проверки.

## Board Health

Machine truth находится в `docs/goals/context-contract-v1/state.yaml`. При расхождении charter и board выигрывает `state.yaml`.

Проверка доски:

```powershell
node "C:/Users/Alexander Lozovoy/.codex/plugins/cache/goalbuddy/goalbuddy/0.4.1/skills/goal-prep/scripts/check-goal-state.mjs" docs/goals/context-contract-v1
```

## Canonical Board

`docs/goals/context-contract-v1/state.yaml`

## Run Command

```text
/goal Follow docs/goals/context-contract-v1/goal.md.
```

## PM Loop

На каждом `/goal` continuation прочитать charter и `state.yaml`, выполнить только active task, сохранить receipt, обновить board и без паузы активировать следующий крупнейший безопасный пакет. Завершать только через финальный audit, который связывает receipts и свежие проверки с oracle и фиксирует `full_outcome_complete: true`.

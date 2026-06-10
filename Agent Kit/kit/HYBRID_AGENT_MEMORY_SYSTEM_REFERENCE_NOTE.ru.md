# Проект гибридной системы памяти агента

Status: reference note  
Language: Russian  
Purpose: зафиксировать конкретную Markdown-first / SQLite-accelerated архитектуру памяти агента как проектную reference-note без подмены базового контракта Agent Memory Kit.

---

## 1. Назначение заметки

Этот документ фиксирует проектную концепцию локальной гибридной системы памяти для AI-агентов.

Его роль в репозитории:

- сохранить архитектурную идею в reviewable виде;
- сделать её доступной как reference-note внутри `Agent Kit`;
- не объявлять её обязательным layout по умолчанию для всех пользователей пакета.

Если эта схема будет внедряться в конкретный проект, её нужно явно связать с:

- источниками истины проекта;
- retrieval policy;
- lifecycle durable/runtime памяти;
- правилами owner approval и mutation safety.

---

## 2. Цель проекта

Цель проекта — создать локальную, бесплатную и переносимую систему памяти для AI-агентов, которая помогает агенту работать с проектом не "с нуля" каждый раз, а с учётом накопленных правил, решений, ошибок, текущего контекста и повторяемых рабочих процессов.

Система не должна зависеть от платных сервисов или закрытых инструментов. Hermes рассматривается только как референс подхода, но не как обязательная зависимость.

Главная идея:

```text
Markdown = источник истины и ревью
SQLite = быстрый runtime-index и recall
Agent hooks / CLI / MCP = интерфейс работы агента с памятью
```

---

## 3. Зачем нужна система

Обычная проблема AI-агентов в разработке:

- агент забывает прошлые решения;
- агенту приходится каждый раз заново объяснять правила проекта;
- длинные Markdown-документы раздувают контекст;
- временные договорённости смешиваются с постоянными правилами;
- полезные повторяемые процессы не превращаются в устойчивые skills;
- память агента может стать мусорной, если сохранять всё подряд.

Гибридная система памяти решает это через разделение ролей:

- стабильные правила живут в `AGENTS.md`;
- архитектура и продуктовые решения живут в `docs/`;
- повторяемые процессы живут в `skills/`;
- рабочая память агента живёт в `memory/`;
- быстрый поиск и выбор релевантных фрагментов выполняет локальный SQLite/FTS5 index.

---

## 4. Базовый принцип

Система не должна заставлять агента читать всё подряд.

Вместо этого перед задачей агент получает короткий context pack:

```text
2-5 релевантных memory units
до 900 токенов
с ссылками на исходные Markdown-источники
```

Экономия токенов появляется не из-за SQLite как формата, а из-за селективного recall:

```text
плохо:
прочитай все docs/ и memory/

лучше:
найди 3-5 релевантных правил, решений и workflow
```

---

## 5. Общая архитектура

```text
AGENTS.md
  стабильные обязательные правила проекта

docs/
  архитектура, ADR, продуктовые решения, ограничения

skills/
  оформленные повторяемые workflow

issues/
  задачи, контракты задач, acceptance criteria

prompts/
  переиспользуемые промпты и task templates

memory/
  наблюдаемая память агента в Markdown

.agent-memory/
  локальный runtime index на SQLite + FTS5
```

Система состоит из двух основных слоёв.

### Durable layer

Человеко-читаемый слой. Он хранится в Git, проходит review и является источником истины.

Сюда входят:

```text
AGENTS.md
docs/
skills/
issues/
prompts/
memory/rules/
memory/decisions/
memory/mistakes/
memory/workflows/
memory/retired/
```

### Runtime layer

Локальный производный слой. Он не является источником истины и может быть пересобран.

Сюда входят:

```text
.agent-memory/runtime.sqlite
.agent-memory/cache/
memory/active.md
memory/pinned.md
memory/inbox/
memory/summaries/
memory/log/
memory/.state/
memory/.snapshots/
```

---

## 6. Роль `memory/`

Каталог `memory/` нужен не для замены `docs/` или `skills/`, а для хранения знаний, которые появляются в процессе работы агента.

Рекомендуемая структура:

```text
memory/
  _MEMORY.md
  _memory.yaml

  active.md
  pinned.md

  inbox/
    processed/

  rules/
  decisions/
  mistakes/
  workflows/
  summaries/
  handoffs/
  retired/

  log/
  templates/

  .state/
  .snapshots/
```

---

## 7. Назначение ключевых файлов

### `memory/_MEMORY.md`

Инструкция для агента о том, как пользоваться памятью:

- что можно сохранять;
- что нельзя сохранять;
- какие типы записей существуют;
- как работает promotion;
- когда писать signal;
- когда создавать rule;
- когда выносить workflow в skill.

### `memory/_memory.yaml`

Конфигурация системы памяти.

Пример:

```yaml
version: 1
project_key: agent-memory-kit
mode: repo-local

runtime:
  engine: sqlite
  search: fts5
  semantic_search: false

retrieval:
  max_entries: 5
  max_entry_tokens: 120
  total_budget_tokens: 900

lifecycle:
  candidate_threshold: 3
  unconfirmed_ttl_days: 14
  stale_evidence_days: 90

active:
  max_chars: 5000

retention:
  inbox_days: 45
  summaries_days: 60
  snapshots_keep: 20
```

### `memory/active.md`

Автоматически собираемый digest актуальной памяти.

Он не редактируется вручную.

Содержит:

- подтверждённые правила;
- важные решения;
- частые ошибки;
- активные workflow;
- недавно retired правила;
- самые часто вспоминаемые entries.

Назначение:

```text
быстро дать агенту актуальную карту проекта на старте сессии
```

### `memory/pinned.md`

Временная память текущей задачи.

Сюда попадает то, что важно прямо сейчас, но не должно становиться постоянным правилом.

Пример:

```md
# Pinned context

## Current task

Добавить runtime-memory слой без зависимости от Hermes.

## Constraints

- не использовать платные сервисы
- не делать SQLite источником истины
- оставить Markdown reviewable
- MVP должен работать без MCP

## Open questions

- нужен ли shared-vault режим в первой версии
```

### `memory/inbox/`

Сырые сигналы.

Сюда попадают замечания, исправления и наблюдения:

```text
"Не сохраняй временный контекст как постоянное правило"
"Это уже было решено в docs/architecture.md"
"Такой workflow повторился третий раз"
```

Сигнал ещё не является правилом.

### `memory/rules/`

Подтверждённые правила, родившиеся из работы агента.

Пример:

```md
---
id: amk:rule:markdown-source-of-truth
kind: rule
state: confirmed
topic: memory.architecture
scope: repo
confidence: medium
source_refs:
  - memory/inbox/2026-06-10.md
tags: [memory, architecture]
---

Markdown remains the source of truth. SQLite is only a rebuildable runtime index.
```

### `memory/decisions/`

Решения, которые важно помнить агенту.

Пример:

```md
---
id: amk:decision:no-hermes-dependency
kind: decision
state: confirmed
topic: memory.runtime
scope: repo
confidence: high
tags: [runtime, sqlite, hermes]
---

Hermes is not used as a dependency. The project implements its own local runtime-memory layer inspired by Hermes-like recall.
```

### `memory/mistakes/`

Повторяющиеся ошибки агента.

Пример:

```md
---
id: amk:mistake:reading-too-much-context
kind: mistake
state: confirmed
topic: memory.retrieval
scope: repo
confidence: medium
tags: [context, retrieval]
---

Do not load all project documents for every task. Use selective recall and return only the most relevant memory units.
```

### `memory/workflows/`

Процессы, которые ещё не стали полноценными skills.

Если workflow повторяется и стабилен, его можно повысить до `skills/`.

### `memory/retired/`

Устаревшие правила и решения.

Удалять их полностью не нужно: важно сохранять историю, почему правило больше не действует.

---

## 8. Runtime SQLite layer

SQLite не является главным хранилищем памяти.

Он нужен для:

- быстрого поиска;
- FTS5 recall;
- ранжирования;
- дедупликации;
- подсчёта применений;
- сбора статистики;
- генерации context pack;
- пересборки `active.md`.

Файл:

```text
.agent-memory/runtime.sqlite
```

Он должен быть gitignored и полностью пересобираемым из Markdown-источников.

Минимальные таблицы MVP:

```text
documents
chunks
memory_entries
entry_fts
signals
evidence
retrievals
```

### `documents`

Индексирует все источники:

```text
AGENTS.md
docs/**
skills/**
issues/**
prompts/**
memory/**
```

### `chunks`

Хранит разбитые на части Markdown-документы.

### `memory_entries`

Нормализованное представление rules, decisions, mistakes, workflows, summaries.

### `entry_fts`

FTS5-поиск по memory entries.

### `signals`

Сырые сигналы до превращения в правила.

### `evidence`

Факты применения или нарушения правил.

### `retrievals`

Лог того, какие memory entries были выбраны для задачи.

---

## 9. Жизненный цикл памяти

Система не должна превращать каждое замечание в вечное правило.

Правильный lifecycle:

```text
signal
  ->
unconfirmed entry
  ->
confirmed rule / decision / mistake / workflow
  ->
promotion candidate
  ->
skill или retained memory
  ->
retired при устаревании
```

### Signal

Сырой сигнал.

Примеры:

- пользователь поправил агента;
- агент заметил повторяющуюся ошибку;
- задача повторила старый workflow;
- правило всплыло в review;
- решение оказалось важным для будущих задач.

### Unconfirmed

Кандидат в правило.

Создаётся, если похожий signal повторился несколько раз или был явно отмечен пользователем.

### Confirmed

Подтверждённое правило, решение, ошибка или workflow.

Подтверждается через:

- ручное review;
- повторное применение;
- evidence из задачи;
- ссылку на `docs/`, `AGENTS.md`, `issues/` или `skills/`.

### Promotion candidate

Если workflow или правило часто применяется, система предлагает повысить его:

```text
memory/workflows/*
  -> skills/*/SKILL.md
```

### Retired

Если правило устарело, конфликтует с `AGENTS.md` или было заменено новым решением, оно переносится в `memory/retired/`.

---

## 10. Правила приоритетов

Если источники конфликтуют, порядок такой:

```text
1. Явный запрос пользователя в текущей задаче
2. AGENTS.md
3. docs/
4. skills/
5. issue / task contract
6. memory/rules и memory/decisions
7. pinned.md
8. summaries
9. raw signals
```

SQLite-memory никогда не может переопределить `AGENTS.md`.

Если memory entry конфликтует с `AGENTS.md`, она должна быть:

```text
- понижена в recall
- помечена hygiene finding
- перенесена в retired или quarantine
```

---

## 11. CLI-интерфейс

Первая версия должна работать через CLI, без обязательного MCP.

Рекомендуемое имя CLI:

```bash
ams
```

`ams` = Agent Memory System.

### Базовые команды MVP

```bash
ams init
ams reindex
ams search "query"
ams context "task description"
ams remember "memory text"
ams pin "temporary task context"
ams clear-pin
ams stats
```

### Расширенные команды

```bash
ams dream
ams promote <entry-id> --to rule
ams promote <entry-id> --to workflow
ams write-skill <entry-id> --slug <slug>
ams retire <entry-id> --reason "<reason>"
ams hygiene
ams snapshot
ams rollback <snapshot-id>
```

---

## 12. Команда `ams context`

Это ключевая команда системы.

Пример:

```bash
ams context "Добавить Telegram уведомления"
```

Ответ:

```text
Relevant memory:

1. Telegram is only a delivery transport, not a domain actor.
   Source: memory/decisions/telegram-transport-boundary.md

2. Domain events must not depend on notification transport.
   Source: docs/architecture.md#domain-events

3. Do not load all project docs for small implementation tasks.
   Source: memory/rules/selective-recall.md
```

Именно эта команда заменяет необходимость каждый раз вручную перечитывать все Markdown-файлы.

---

## 13. MCP-интерфейс

MCP нужен не в первой версии, а как следующий слой.

Минимальный MCP writer subset:

```text
memory_context
memory_feedback
memory_apply_evidence
memory_note
memory_pinned_context
```

Полный MCP surface:

```text
memory_search
memory_context_pack
memory_pre_compact_pack
memory_stats
memory_hygiene_scan
memory_promote
memory_retire
```

Разделение важно, чтобы не раздувать context window схемами всех инструментов.

---

## 14. Hooks

Hooks подключаются после CLI MVP.

Целевые события:

```text
SessionStart
UserPromptSubmit
PreCompact
PostResponse
```

### SessionStart

На старте сессии агент получает:

- `AGENTS.md` pointer;
- `memory/active.md`;
- `memory/pinned.md`, если есть;
- короткий context pack.

### UserPromptSubmit

Перед обработкой задачи система решает, нужен ли recall.

Если нужен, вызывается:

```bash
ams context "<user task>"
```

### PreCompact

Перед сжатием контекста система сохраняет:

- открытые решения;
- важные ограничения;
- что уже сделано;
- что осталось;
- текущий pinned context.

### PostResponse

После завершения задачи система может:

- добавить summary;
- записать evidence;
- предложить signal;
- предложить promotion в skill.

---

## 15. Правила гигиены памяти

Система должна защищаться от мусора.

Нельзя сохранять:

- секреты;
- API-ключи;
- токены;
- приватные данные;
- временную мысль как постоянное правило;
- догадки как confirmed rule;
- длинные пересказы всего чата;
- правила без источника или причины.

Каждая durable memory entry должна иметь:

```text
id
kind
state
topic
scope
confidence
source_refs
created_at
updated_at
```

---

## 16. Promotion в skills

Одна из главных функций системы — превращать повторяемые workflow в skills.

Пример:

```text
1. Агент несколько раз получает correction:
   "Перед задачей сначала проверь AGENTS.md, docs и related issues."

2. Система сохраняет signals.

3. После нескольких повторений создаётся workflow:
   memory/workflows/task-preparation.md

4. После подтверждения workflow повышается:
   skills/task-preparation/SKILL.md
```

Так система постепенно улучшает не только память, но и процесс работы агента.

---

## 17. Что входит в MVP

MVP должен быть простым.

В первую версию входят:

```text
memory/ layout
_memory.yaml
_MEMORY.md
active.md
pinned.md
inbox/
rules/
decisions/
mistakes/
workflows/
retired/

.agent-memory/runtime.sqlite

ams init
ams reindex
ams search
ams context
ams remember
ams pin
ams clear-pin
ams stats
```

MCP, hooks, dream-pass и automatic skill promotion можно добавить позже.

---

## 18. Что не входит в MVP

Не нужно делать в первой версии:

- полноценный MCP-server;
- semantic embeddings;
- vector database;
- web dashboard;
- multi-agent shared vault;
- автоматический rewrite всех правил;
- сложный confidence engine;
- автогенерацию skills без review;
- зависимость от Hermes;
- зависимость от платных сервисов.

---

## 19. Главная формула проекта

```text
Agent Memory Kit = методология и структура
Markdown memory = наблюдаемая долговременная память
SQLite runtime = быстрый recall и экономия контекста
CLI/MCP/hooks = интерфейс агента
skills = закреплённые повторяемые процессы
```

Итоговая архитектурная позиция:

```text
Не Hermes.
Не скрытая база знаний.
Не огромный Markdown, который агент читает целиком.

А локальная гибридная система:

Markdown-first.
SQLite-accelerated.
Review-safe.
Agent-friendly.
Free by default.
```

# Communication anti-patterns

## Vague source

Bad:

> Открытый интерес добавляется из Heatmap.

Why it fails:

- writer is unknown;
- reader is unknown;
- table is unknown;
- cache behavior is unknown;
- cadence is unknown;
- "Heatmap" may be a UI label rather than storage;
- missing-data behavior is unknown;
- source precedence is unknown.

Required correction:

Name the producer, technical storage, field, reader, cadence, cache path,
precedence, fallback and relation between the UI name and technical identifier.

## False completeness

Bad:

> Данные сохраняются, кеши обновляются, API формирует график.

Why it fails:

- which data;
- which tables;
- which caches;
- which keys;
- which process updates them;
- when;
- which API route;
- which transformation;
- which client;
- what happens on partial failure.

## Test-only confidence

Bad:

> Всё проверено, тесты проходят.

Required correction:

List the checks, exact behavior exercised, evidence layer, missing runtime
coverage and whether production/deployment/owner acceptance occurred.

## Tool-centric answer

Bad:

> Обновил 17 разделов и проверил страницу.

Why it fails:

It reports the work process but may not answer how the business logic actually
works.

Required correction:

Explain the resulting logic first, then state what artifact was updated and how
it was checked.

## Business label used as technical identity

Bad:

> Данные берутся из Price Sheet / Heatmap / QuikEDU.

Why it fails:

A UI tab, business label or external product name does not identify the actual
producer class, table, field, cache key, API path or ownership boundary.

Required correction:

State the UI/business name and then map it to the exact technical producer,
storage, field and consumer. If the mapping was not verified, say so.

## Compressed transition

Bad:

> После этого система обновляет всё необходимое.

Why it fails:

The action, trigger, affected state, order, failure behavior and downstream
consumer are hidden.

Required correction:

Name each material transition, its owner, condition, written state and next
consumer. Separate successful, missing-data and failure paths.


## Discovered gap treated as permission or silence

Bad:

> Я должен был самостоятельно устранить пробел по JPY и WTI.

Also bad:

> Эти продукты не попали в локальный сбор, поэтому отсутствие данных на
> следующий день находится вне задачи. Работа завершена.

Why it fails:

A collector's selection filter is an implementation detail, not an owner
decision about scope. A discovered gap may require a decision about recollection,
copying or leaving data absent. Neither its technical importance nor the agent's
desire to finish authorizes that decision. Silently ignoring the gap also denies
the owner the information needed to decide.

Required correction:

State which products and dates are missing, why they were skipped, and what
downstream work will wait. Check whether an existing instruction already covers
the proposed action. If it does not, present the smallest concrete action and
ask the owner before changing data or expanding collection. Keep independent,
already authorized work moving; do not invent an approval gate for that work.
Report completed work and the pending owner decision separately.

Example for this incident:

> У JPY и WTI есть календарь за 1 октября, поэтому локальный запуск пропустил
> их. На 2 октября строк нет; после смены торгового дня PS будет ждать календарь.
> Для остальных 11 продуктов копии проверены. Копировать также имеющиеся
> актуальные строки JPY и WTI на 2 октября по штатным правилам Calendar?

In a retrospective, say "I should have surfaced the gap and asked for the
decision", not "I should have repaired it" when that repair was not authorized.


## Connection reuse described as bypassing an intermediary

Bad:

> При заполненном PgBouncer используем исправное соединение.

Why it fails:

The connection endpoints and the exhausted limit are unnamed. The owner can
reasonably read this as a direct PostgreSQL fallback that bypasses PgBouncer,
although the implementation only reuses an accepted client connection to it.
This ambiguity can turn approval of connection reuse into apparent approval of
a different network path or bypass of resource limits.

Required correction:

Name both ends of the reused connection, the intermediary that still handles
the request, and the specific limit involved. Distinguish client connections
from server connections and transactions. State whether routing, admission,
queueing or resource limits change; verify those claims in code/configuration.
Do not equate reuse with bypass, or claim that an existing connection guarantees
success when the backend is unavailable or busy.

Example for this incident:

> API повторно использует уже открытое соединение с PgBouncer. Путь остаётся
> API → PgBouncer → PostgreSQL; прямого запасного подключения к PostgreSQL нет.
> Заполнен лимит новых клиентских подключений к PgBouncer. Существующее
> исправное подключение может продолжать работу через него; серверный пул,
> ожидание свободного соединения и ошибки PostgreSQL по-прежнему действуют.

This is a communication rule, not permission to add pooling, a fallback or new
overload behavior. Those changes still require the current owner's authority.


## Vague phrasing examples

The existing Heatmap example above covers ambiguous UI/source identity.

Do not write vague phrases such as:

- "данные идут из базы";
- "используется кеш";
- "система обновляет значения";
- "модель рассчитывает данные";
- "результат передаётся дальше";
- "это сохраняется";
- "логика подхватывает значение".

## Explicit claim and evidence wording

Use explicit wording:

- "Владелец требует..."
- "Текущий код делает..."
- "Таблица хранит..."
- "Redis-кеш содержит..."
- "Локальный тест подтвердил..."
- "На сервере не проверено..."
- "Это вывод из..."
- "Не найдено..."
- "Требуется решение владельца..."

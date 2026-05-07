# test-task2

Простое приложение на FastAPI для управления кошельками.

## Что делает проект
- создаёт кошелёк
- показывает баланс кошелька
- выполняет операции пополнения и снятия
- работает с PostgreSQL через Alembic миграции
- запускается через Docker Compose

## Как запустить через Docker
1. Убедитесь, что Docker Desktop запущен.
2. Выполните в корне проекта:

```bash
docker compose up --build
```

3. Перейдите в браузере:

```text
http://localhost:8000/docs
```

> При старте контейнера приложение автоматически ждёт PostgreSQL и применяет миграции.

## Endpoints
- `POST /api/v1/wallets` — создать новый кошелёк
- `GET /api/v1/wallets/{wallet_id}/balance` — получить баланс кошелька
- `POST /api/v1/wallets/{wallet_id}/operation` — выполнить операцию на кошельке

### Пример запроса на операцию
```json
{
  "operation_type": "DEPOSIT",
  "amount": 100
}
```

## Настройки базы данных
Файл `.env` содержит параметры подключения к PostgreSQL:
- `DB_NAME`
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASS`

## Тесты
Запустить тесты можно командой:

```bash
pytest
```

## Дополнительно
Если Docker не используется, проект можно запускать локально через Python и uvicorn, но тогда нужна рабочая PostgreSQL и выполненные миграции.

#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
python - <<'PY'
import asyncio
import sys

import asyncpg
from src.config import settings

async def check():
    try:
        dsn = (
            f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
        conn = await asyncpg.connect(dsn)
        await conn.close()
        return True
    except Exception:
        return False

async def main():
    for _ in range(60):
        if await check():
            print("PostgreSQL is available")
            return
        print("PostgreSQL unavailable, retrying in 1 second...")
        await asyncio.sleep(1)
    raise RuntimeError("PostgreSQL is unavailable after 60 seconds")

try:
    asyncio.run(main())
except Exception as exc:
    print(exc, file=sys.stderr)
    sys.exit(1)
PY

echo "Running alembic migrations..."
alembic upgrade head

echo "Starting server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000

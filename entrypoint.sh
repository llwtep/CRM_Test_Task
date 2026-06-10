#!/bin/sh
set -e

echo "Running migrations..."
uv run alembic upgrade head

echo "Running seeder..."
uv run python seeder.py

echo "Starting application..."
exec uv run uvicorn main:app --host 0.0.0.0 --port 8000

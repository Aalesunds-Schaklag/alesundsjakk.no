#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Ensure .env exists
if [ ! -f .env ]; then
  echo "Creating .env from ../.env.example"
  cp ../.env.example .env
fi

# Run migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start FastAPI with hot reload
echo "Starting FastAPI on :8000..."
exec uvicorn app.main:app --reload --port 8000

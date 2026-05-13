#!/bin/bash
set -e

echo "=== Smart Guardian Backend Starting ==="

# Wait for PostgreSQL
echo "Waiting for database..."
until pg_isready -h db -U ${POSTGRES_USER:-sgadmin} -d ${POSTGRES_DB:-smartguardian} >/dev/null 2>&1; do
  echo "  Database not ready yet - retrying..."
  sleep 2
done
echo "  Database is ready!"

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head || echo "  Warning: Migration failed (may already be up to date)"

# Create logs directory
mkdir -p /app/logs

# Start the application
echo "Starting FastAPI server on port 8001..."
exec "$@"

#!/bin/bash
set -e

echo "Waiting for database..."
python -c "
import time, os
from urllib.parse import urlparse
db = os.environ.get('DATABASE_URL', '')
if db.startswith('postgresql'):
    import psycopg2
    p = urlparse(db.replace('+asyncpg', ''))
    for i in range(30):
        try:
            psycopg2.connect(dbname=p.path[1:], user=p.username, password=p.password, host=p.hostname, port=p.port or 5432)
            break
        except psycopg2.OperationalError:
            time.sleep(1)
    else:
        raise RuntimeError('Database not ready after 30s')
"
echo "Database ready."

echo "Running migrations..."
python manage.py makemigrations home --noinput 2>/dev/null || true
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true
echo "Ready."

exec "$@"

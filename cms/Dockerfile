FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DATABASE_URL=sqlite:///tmp/build.db python manage.py collectstatic --noinput

EXPOSE 8001

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "cms.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2"]

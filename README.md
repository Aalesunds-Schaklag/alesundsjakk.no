# alesundsjakk.no

Website for Aalesunds Schaklag -- the chess club of Alesund, Norway.

## Prerequisites

- Docker & Docker Compose
- Node.js 20+
- Python 3.12+

## Setup

```bash
# 1. Start PostgreSQL and Wagtail CMS
docker compose -f docker-compose.dev.yml up -d --build

# 2. Seed CMS with demo pages and create an admin user
docker compose -f docker-compose.dev.yml exec cms python manage.py setup_site
docker compose -f docker-compose.dev.yml exec cms python manage.py createsuperuser

# 3. Set up backend
cp .env.example backend/.env
cd backend && alembic upgrade head

# 4. Start backend (port 8000)
cd backend && uvicorn app.main:app --reload --port 8000

# 5. Start frontend (port 5173)
cd frontend && npm install && npm run dev
```

Open http://localhost:5173 for the site, http://localhost:5173/cms/ for the Wagtail page editor.

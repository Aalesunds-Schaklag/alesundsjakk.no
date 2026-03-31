# alesundsjakk.no — Project Context

## What is this?

Website for **Aalesunds Schaklag** (chess club, est. 1913, Ålesund, Norway). Replaces the old WordPress club site and the separate Wix festival site (aalesundsjakkfestival.no). Domain: alesundsjakk.no.

## Tech Stack

- **Frontend:** Vue 3 + Vuetify 3 + TypeScript + Vite + vue-i18n (NO/EN)
- **Backend:** Python 3.12 + FastAPI + SQLAlchemy async + asyncpg
- **CMS:** Wagtail (Django) — manages static pages, served via API v2
- **Database:** PostgreSQL 16 (shared by FastAPI and Wagtail)
- **Infra:** Docker Compose, nginx, Let's Encrypt (certbot)
- **CI/CD:** GitHub Actions → GHCR → webhook deploy to Hetzner
- **Org:** [Aalesunds-Schaklag](https://github.com/Aalesunds-Schaklag)

## Local Development

```bash
# 1. Start database + Wagtail CMS (port 5433 for DB, 8001 for CMS)
docker compose -f docker-compose.dev.yml up -d

# 2. Seed Wagtail with demo pages + create admin user
docker compose -f docker-compose.dev.yml exec cms python manage.py setup_site
docker compose -f docker-compose.dev.yml exec cms python manage.py createsuperuser

# 3. Copy .env.example to backend/.env and adjust if needed
cp .env.example backend/.env

# 4. Run backend migrations
cd backend && alembic upgrade head

# 5. Start backend (in terminal, with hot reload)
cd backend && uvicorn app.main:app --reload --port 8000

# 6. Start frontend (Vite on :5173, proxies /api to :8000, /api/v2 and /cms to :8001)
cd frontend && npm install && npm run dev
```

Wagtail admin: http://localhost:8001/cms/  (or via Vite proxy at http://localhost:5173/cms/)

## Project Structure

```
frontend/           Vue 3 SPA
  src/views/        Page views (Home, Join, Schedule, Results, Festival, Rental, About, Contact, News, Puzzle, Login + admin views)
  src/components/   Reusable components (Hero, NextEvents, NewsTimeline, LichessPuzzle, SponsorBar, LanguageSwitcher, AppFooter)
  src/locales/      Norwegian (no.ts) and English (en.ts)
  src/stores/       Pinia stores (auth, app)
  src/composables/  useApi.ts (FastAPI), useWagtail.ts (Wagtail pages)

backend/            FastAPI application
  app/main.py       Entry point, CORS, router mounting
  app/models.py     SQLAlchemy models: User, MagicToken, Post, Event, Sponsor, MediaFile
  app/routers/      API routes: auth, content, events, pages (sponsors), media, admin
  app/services/     External integrations: Lichess puzzle, email
  alembic/          Database migrations

cms/                Wagtail CMS (Django)
  cms/settings.py   Django settings (parses DATABASE_URL, whitenoise for static)
  cms/urls.py       Routes: /cms/ (admin), /api/v2/ (API)
  home/models.py    Page models: HomePage, ContentPage (bilingual)
  home/management/  setup_site command (seeds demo content)
  Dockerfile        Production image with gunicorn
  entrypoint.sh     Runs migrations + collectstatic on boot

nginx/              Reverse proxy config + Dockerfile
.github/workflows/  CI (lint + build) and Deploy (GHCR + webhook)
```

## Key Design Decisions

- **Wagtail CMS** — manages static pages (om-oss, festival, lokaler). Admin at /cms/. API at /api/v2/pages/.
- **FastAPI** — handles dynamic content: posts, events, sponsors, auth, media
- **Auth:** Magic link (email → token → JWT) for FastAPI admin. Separate Django superuser for Wagtail.
- **Posts:** Two types — "article" (full blog) and "message" (short timeline message)
- **Events = Terminliste** — categories: turnering, klubbkveld, ungdom, festival, annet
- **Festival** is just an event type at /festival, adaptable for any tournament
- **Sponsors:** Can be global or per-event
- **i18n:** Norwegian default, English available. Wagtail pages use dual fields (body_no/body_en). FastAPI content uses `_no`/`_en` fields.
- **Colors:** Navy #1B2A4A, Gold #C9A84C, Accent #2196F3, Background #F5F5F0
- **Logo:** Black/white knight+rook crest, 1913 — at `assets/logo_original.jpg` and `frontend/public/logo.jpg`

## URL Routing

| Path | Handler | Purpose |
|---|---|---|
| `/cms/` | Wagtail (nginx → cms:8001) | CMS admin UI |
| `/api/v2/` | Wagtail (nginx → cms:8001) | Wagtail API (pages, images, documents) |
| `/api/` | FastAPI (nginx → backend:8000) | Backend API (posts, events, auth, etc.) |
| `/uploads/` | nginx static | User uploads |
| `/*` | Vue SPA (nginx → index.html) | Frontend app |

## External Services

- **Lichess API:** Daily puzzle at `https://lichess.org/api/puzzle/daily`
- **Spond:** Club uses it for registrations. We just link to it, no API.
- **Social:** Facebook (facebook.com/aalesundsschaklag), YouTube channel

## Navigation

Main: Hjem, Bli med, Terminliste, Resultater, Festival, Lei lokaler, Om oss, Kontakt
Secondary: Nyheter, Daglig oppgave
Admin: /admin (Vue admin for posts/events/sponsors), /cms/ (Wagtail admin for pages)

## Content Sources

| Content | Source | Update method |
|---|---|---|
| Static pages | Wagtail CMS | Wagtail admin at /cms/ |
| News/posts | FastAPI (PostgreSQL) | Vue admin panel |
| Events/terminliste | FastAPI (PostgreSQL) | Vue admin panel (Google Calendar sync planned) |
| Daily puzzle | Lichess API | Auto-fetched, cached 1 hour |
| Sponsors | FastAPI (PostgreSQL) | Vue admin panel |

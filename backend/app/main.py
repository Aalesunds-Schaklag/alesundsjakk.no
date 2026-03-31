from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import admin, auth, content, events, media, pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Aalesunds Schaklag API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(content.router, prefix="/api", tags=["content"])
app.include_router(events.router, prefix="/api", tags=["events"])
app.include_router(pages.router, prefix="/api", tags=["pages"])
app.include_router(media.router, prefix="/api", tags=["media"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

Path(settings.upload_dir).mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


@app.get("/api/health")
async def health():
    return {"status": "ok"}

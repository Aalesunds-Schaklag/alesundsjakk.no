import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Event, Post, Sponsor

router = APIRouter()

# NOTE: In production, add JWT auth dependency to all admin routes.
# For now, these are open for development.


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[æ]", "ae", text)
    text = re.sub(r"[ø]", "o", text)
    text = re.sub(r"[å]", "a", text)
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


# === Posts ===

class PostCreate(BaseModel):
    title_no: str
    title_en: str | None = None
    content_no: str
    content_en: str | None = None
    excerpt_no: str | None = None
    excerpt_en: str | None = None
    post_type: str = "article"
    category: str | None = None
    image_url: str | None = None
    published: bool = False


class PostUpdate(PostCreate):
    pass


@router.get("/posts")
async def admin_list_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()
    return [
        {
            "id": str(p.id),
            "slug": p.slug,
            "title_no": p.title_no,
            "post_type": p.post_type,
            "category": p.category,
            "published": p.published,
            "published_at": p.published_at.isoformat() if p.published_at else None,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in posts
    ]


@router.post("/posts")
async def admin_create_post(body: PostCreate, db: AsyncSession = Depends(get_db)):
    slug = _slugify(body.title_no)
    post = Post(
        slug=slug,
        post_type=body.post_type,
        category=body.category,
        title_no=body.title_no,
        title_en=body.title_en,
        content_no=body.content_no,
        content_en=body.content_en,
        excerpt_no=body.excerpt_no,
        excerpt_en=body.excerpt_en,
        image_url=body.image_url,
        published=body.published,
        published_at=datetime.now(timezone.utc) if body.published else None,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return {"id": str(post.id), "slug": post.slug}


@router.put("/posts/{post_id}")
async def admin_update_post(post_id: str, body: PostUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    if body.published and not post.published_at:
        post.published_at = datetime.now(timezone.utc)

    await db.commit()
    return {"id": str(post.id), "slug": post.slug}


@router.delete("/posts/{post_id}")
async def admin_delete_post(post_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(post)
    await db.commit()
    return {"ok": True}


# === Events ===

class EventCreate(BaseModel):
    title_no: str
    title_en: str | None = None
    description_no: str | None = None
    description_en: str | None = None
    category: str = "annet"
    location: str | None = None
    start_date: datetime
    end_date: datetime | None = None
    spond_link: str | None = None
    published: bool = True


@router.get("/events")
async def admin_list_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).order_by(Event.start_date.desc()))
    events = result.scalars().all()
    return [
        {
            "id": str(e.id),
            "title_no": e.title_no,
            "category": e.category,
            "start_date": e.start_date.isoformat() if e.start_date else None,
            "location": e.location,
            "published": e.published,
        }
        for e in events
    ]


@router.post("/events")
async def admin_create_event(body: EventCreate, db: AsyncSession = Depends(get_db)):
    event = Event(**body.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return {"id": str(event.id)}


@router.put("/events/{event_id}")
async def admin_update_event(event_id: str, body: EventCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    await db.commit()
    return {"id": str(event.id)}


@router.delete("/events/{event_id}")
async def admin_delete_event(event_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(event)
    await db.commit()
    return {"ok": True}


# === Sponsors ===

class SponsorCreate(BaseModel):
    name: str
    logo_url: str | None = None
    website_url: str | None = None
    tier: str = "sponsor"
    scope: str = "global"
    event_id: str | None = None
    sort_order: int = 0


@router.get("/sponsors")
async def admin_list_sponsors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sponsor).order_by(Sponsor.sort_order.asc()))
    sponsors = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "name": s.name,
            "tier": s.tier,
            "scope": s.scope,
            "is_active": s.is_active,
        }
        for s in sponsors
    ]


@router.post("/sponsors")
async def admin_create_sponsor(body: SponsorCreate, db: AsyncSession = Depends(get_db)):
    sponsor = Sponsor(**body.model_dump())
    db.add(sponsor)
    await db.commit()
    await db.refresh(sponsor)
    return {"id": str(sponsor.id)}


@router.put("/sponsors/{sponsor_id}")
async def admin_update_sponsor(sponsor_id: str, body: SponsorCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sponsor).where(Sponsor.id == sponsor_id))
    sponsor = result.scalar_one_or_none()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(sponsor, field, value)
    await db.commit()
    return {"id": str(sponsor.id)}

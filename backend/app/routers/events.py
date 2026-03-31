from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Event

router = APIRouter()


@router.get("/events")
async def list_events(
    category: str | None = None,
    upcoming: bool = True,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    query = select(Event).where(Event.published.is_(True))

    if upcoming:
        query = query.where(Event.start_date >= datetime.now(timezone.utc)).order_by(Event.start_date.asc())
    else:
        query = query.order_by(Event.start_date.desc())

    if category:
        query = query.where(Event.category == category)

    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    events = result.scalars().all()

    return {
        "items": [_event_to_dict(e) for e in events],
        "page": page,
        "limit": limit,
    }


@router.get("/events/next")
async def next_events(
    count: int = Query(3, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Event)
        .where(Event.published.is_(True), Event.start_date >= datetime.now(timezone.utc))
        .order_by(Event.start_date.asc())
        .limit(count)
    )
    events = result.scalars().all()
    return [_event_to_dict(e) for e in events]


@router.get("/events/{event_id}")
async def get_event(event_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        return {"error": "Not found"}, 404
    return _event_to_dict(event)


def _event_to_dict(event: Event) -> dict:
    return {
        "id": str(event.id),
        "title_no": event.title_no,
        "title_en": event.title_en,
        "description_no": event.description_no,
        "description_en": event.description_en,
        "category": event.category,
        "location": event.location,
        "start_date": event.start_date.isoformat() if event.start_date else None,
        "end_date": event.end_date.isoformat() if event.end_date else None,
        "spond_link": event.spond_link,
    }

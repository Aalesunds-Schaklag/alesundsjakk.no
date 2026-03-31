from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Sponsor

router = APIRouter()


@router.get("/sponsors")
async def list_sponsors(scope: str | None = None, db: AsyncSession = Depends(get_db)):
    query = select(Sponsor).where(Sponsor.is_active.is_(True)).order_by(Sponsor.sort_order.asc())
    if scope:
        query = query.where(Sponsor.scope == scope)
    result = await db.execute(query)
    sponsors = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "name": s.name,
            "logo_url": s.logo_url,
            "website_url": s.website_url,
            "tier": s.tier,
            "scope": s.scope,
        }
        for s in sponsors
    ]

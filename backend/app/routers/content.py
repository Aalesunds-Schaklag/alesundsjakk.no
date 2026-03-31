from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Post
from app.services.lichess import get_daily_puzzle

router = APIRouter()


class PostOut(BaseModel):
    id: str
    slug: str
    post_type: str
    category: str | None
    title_no: str
    title_en: str | None
    content_no: str
    content_en: str | None
    excerpt_no: str | None
    excerpt_en: str | None
    image_url: str | None
    published_at: str | None
    created_at: str

    model_config = {"from_attributes": True}


@router.get("/posts")
async def list_posts(
    category: str | None = None,
    post_type: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Post).where(Post.published.is_(True)).order_by(Post.published_at.desc().nullslast(), Post.created_at.desc())

    if category:
        query = query.where(Post.category == category)
    if post_type:
        query = query.where(Post.post_type == post_type)

    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    posts = result.scalars().all()

    return {
        "items": [_post_to_dict(p) for p in posts],
        "page": page,
        "limit": limit,
    }


@router.get("/posts/{slug}")
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.slug == slug, Post.published.is_(True)))
    post = result.scalar_one_or_none()
    if not post:
        return {"error": "Not found"}, 404
    return _post_to_dict(post)


@router.get("/news-timeline")
async def news_timeline(
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Mixed timeline of articles and short messages."""
    result = await db.execute(
        select(Post)
        .where(Post.published.is_(True))
        .order_by(Post.published_at.desc().nullslast(), Post.created_at.desc())
        .limit(limit)
    )
    posts = result.scalars().all()
    return [_post_to_dict(p) for p in posts]


@router.get("/puzzle")
async def daily_puzzle():
    return await get_daily_puzzle()


def _post_to_dict(post: Post) -> dict:
    return {
        "id": str(post.id),
        "slug": post.slug,
        "post_type": post.post_type,
        "category": post.category,
        "title_no": post.title_no,
        "title_en": post.title_en,
        "content_no": post.content_no,
        "content_en": post.content_en,
        "excerpt_no": post.excerpt_no,
        "excerpt_en": post.excerpt_en,
        "image_url": post.image_url,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "created_at": post.created_at.isoformat() if post.created_at else None,
    }

import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import MediaFile

router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/media/upload")
async def upload_media(file: UploadFile, db: AsyncSession = Depends(get_db)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Filtypen støttes ikke")

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="Filen er for stor (maks 10MB)")

    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(settings.upload_dir, filename)

    os.makedirs(settings.upload_dir, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(content)

    # Resize if very large
    try:
        img = Image.open(filepath)
        if max(img.size) > 2000:
            img.thumbnail((2000, 2000), Image.LANCZOS)
            img.save(filepath, quality=85)
    except Exception:
        pass

    media = MediaFile(
        filename=filename,
        original_name=file.filename,
        content_type=file.content_type,
        size=len(content),
        url=f"/uploads/{filename}",
    )
    db.add(media)
    await db.commit()
    await db.refresh(media)

    return {"id": str(media.id), "url": media.url, "filename": media.original_name}


@router.get("/media")
async def list_media(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MediaFile).order_by(MediaFile.uploaded_at.desc()).limit(100))
    files = result.scalars().all()
    return [
        {
            "id": str(f.id),
            "url": f.url,
            "filename": f.original_name,
            "content_type": f.content_type,
            "size": f.size,
            "uploaded_at": f.uploaded_at.isoformat() if f.uploaded_at else None,
        }
        for f in files
    ]

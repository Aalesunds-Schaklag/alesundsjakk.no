import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import MagicToken, User
from app.services.email import send_magic_link, EmailNotConfiguredError

router = APIRouter()


class RequestLinkBody(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str

    model_config = {"from_attributes": True}


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": expire},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = None,
) -> User:
    """Dependency: extract user from Authorization header."""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == user_id, User.is_active.is_(True)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/request-link")
async def request_magic_link(body: RequestLinkBody, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email, User.is_active.is_(True)))
    user = result.scalar_one_or_none()
    if not user:
        # Don't reveal whether user exists
        return {"message": "Hvis e-posten er registrert, vil du motta en innloggingslenke."}

    token = secrets.token_urlsafe(48)
    magic = MagicToken(
        email=body.email,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.magic_link_expire_minutes),
    )
    db.add(magic)
    await db.commit()

    try:
        await send_magic_link(body.email, token)
    except EmailNotConfiguredError:
        link = f"{settings.base_url}/auth/verify?token={token}"
        return {
            "message": "E-post er ikke konfigurert ennå. Bruk lenken under for å logge inn.",
            "email_not_configured": True,
            "magic_link": link,
        }
    return {"message": "Hvis e-posten er registrert, vil du motta en innloggingslenke."}


@router.get("/verify", response_model=TokenResponse)
async def verify_magic_link(token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MagicToken).where(
            MagicToken.token == token,
            MagicToken.used.is_(False),
            MagicToken.expires_at > datetime.now(timezone.utc),
        )
    )
    magic = result.scalar_one_or_none()
    if not magic:
        raise HTTPException(status_code=400, detail="Ugyldig eller utløpt lenke")

    magic.used = True
    await db.commit()

    user_result = await db.execute(select(User).where(User.email == magic.email, User.is_active.is_(True)))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Bruker ikke funnet")

    access_token = create_access_token(str(user.id), user.role)
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(db: AsyncSession = Depends(get_db)):
    # In practice, extract token from header via middleware
    # This is a placeholder showing the pattern
    raise HTTPException(status_code=401, detail="Not implemented - use JWT middleware")

import datetime
import uuid

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(Enum("admin", "editor", name="user_role"), default="editor")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MagicToken(Base):
    __tablename__ = "magic_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), index=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    post_type: Mapped[str] = mapped_column(Enum("article", "message", name="post_type"), default="article")
    category: Mapped[str | None] = mapped_column(String(100))
    title_no: Mapped[str] = mapped_column(String(500))
    title_en: Mapped[str | None] = mapped_column(String(500))
    content_no: Mapped[str] = mapped_column(Text)
    content_en: Mapped[str | None] = mapped_column(Text)
    excerpt_no: Mapped[str | None] = mapped_column(String(500))
    excerpt_en: Mapped[str | None] = mapped_column(String(500))
    image_url: Mapped[str | None] = mapped_column(String(500))
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    author_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_no: Mapped[str] = mapped_column(String(500))
    title_en: Mapped[str | None] = mapped_column(String(500))
    description_no: Mapped[str | None] = mapped_column(Text)
    description_en: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100))  # turnering, klubbkveld, ungdom, festival, annet
    location: Mapped[str | None] = mapped_column(String(500))
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))
    recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence_rule: Mapped[str | None] = mapped_column(String(255))  # e.g. "WEEKLY:THU"
    spond_link: Mapped[str | None] = mapped_column(String(500))
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Sponsor(Base):
    __tablename__ = "sponsors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    logo_url: Mapped[str | None] = mapped_column(String(500))
    website_url: Mapped[str | None] = mapped_column(String(500))
    tier: Mapped[str] = mapped_column(String(50))  # hovedsponsor, sponsor, stotter
    scope: Mapped[str] = mapped_column(String(50), default="global")  # global, festival, event-specific
    event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("events.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MediaFile(Base):
    __tablename__ = "media_files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(255))
    original_name: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100))
    size: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(String(500))
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))

"""Initial migration

Revision ID: 001
Revises:
Create Date: 2026-03-29
"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("admin", "editor", name="user_role"), nullable=False, server_default="editor"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "magic_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("email", sa.String(255), nullable=False, index=True),
        sa.Column("token", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("used", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "posts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("slug", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("post_type", sa.Enum("article", "message", name="post_type"), nullable=False, server_default="article"),
        sa.Column("category", sa.String(100)),
        sa.Column("title_no", sa.String(500), nullable=False),
        sa.Column("title_en", sa.String(500)),
        sa.Column("content_no", sa.Text(), nullable=False),
        sa.Column("content_en", sa.Text()),
        sa.Column("excerpt_no", sa.String(500)),
        sa.Column("excerpt_en", sa.String(500)),
        sa.Column("image_url", sa.String(500)),
        sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
    )

    op.create_table(
        "events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("title_no", sa.String(500), nullable=False),
        sa.Column("title_en", sa.String(500)),
        sa.Column("description_no", sa.Text()),
        sa.Column("description_en", sa.Text()),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("location", sa.String(500)),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True)),
        sa.Column("recurring", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("recurrence_rule", sa.String(255)),
        sa.Column("spond_link", sa.String(500)),
        sa.Column("tournament_id", sa.String(255)),
        sa.Column("published", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "pages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("slug", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("title_no", sa.String(500), nullable=False),
        sa.Column("title_en", sa.String(500)),
        sa.Column("content_no", sa.Text(), nullable=False),
        sa.Column("content_en", sa.Text()),
        sa.Column("published", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("sort_order", sa.Integer(), server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sponsors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("logo_url", sa.String(500)),
        sa.Column("website_url", sa.String(500)),
        sa.Column("tier", sa.String(50), nullable=False),
        sa.Column("scope", sa.String(50), nullable=False, server_default="global"),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("events.id")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("sort_order", sa.Integer(), server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "media_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("original_name", sa.String(255), nullable=False),
        sa.Column("content_type", sa.String(100), nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(500), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
    )


def downgrade() -> None:
    op.drop_table("media_files")
    op.drop_table("sponsors")
    op.drop_table("pages")
    op.drop_table("events")
    op.drop_table("posts")
    op.drop_table("magic_tokens")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS user_role")
    op.execute("DROP TYPE IF EXISTS post_type")

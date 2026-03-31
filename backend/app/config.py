from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://alesundsjakk:devpassword@localhost:5432/alesundsjakk"
    secret_key: str = "change-me-to-random-string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 1 week
    magic_link_expire_minutes: int = 15

    club_email: str = "post@alesundsjakk.no"

    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    base_url: str = "http://localhost:5173"

    upload_dir: str = "uploads"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

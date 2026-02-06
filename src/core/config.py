"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str

    # Authentication
    BETTER_AUTH_SECRET: str

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # App
    DEBUG: bool = False
    APP_NAME: str = "Todo API"
    APP_VERSION: str = "1.0.0"

    @property
    def async_database_url(self) -> str:
        """Convert standard PostgreSQL URL to async version."""
        url = self.DATABASE_URL
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        # Remove sslmode parameter - will be handled via connect_args
        if "?sslmode=" in url:
            url = url.split("?sslmode=")[0]
        elif "&sslmode=" in url:
            url = url.replace("&sslmode=require", "").replace("&sslmode=prefer", "").replace("&sslmode=disable", "")
        return url

    @property
    def requires_ssl(self) -> bool:
        """Check if database requires SSL."""
        return "sslmode=require" in self.DATABASE_URL or "neon.tech" in self.DATABASE_URL


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

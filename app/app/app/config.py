from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AMF_")

    app_name: str = "agentic-migration-factory"
    app_version: str = "1.1.0"
    store_backend: str = Field(default="memory", description="memory or sqlite")
    sqlite_path: str = Field(default="/tmp/amf.db", description="SQLite DB path")


settings = Settings()

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-Native Microservice Platform"
    app_version: str = "0.1.0"
    environment: str = Field(default="local", validation_alias="ENVIRONMENT")
    api_prefix: str = "/api/v1"
    max_upload_mb: int = 25
    default_provider: str = "balanced"
    daily_request_target: int = 4_000
    service_level_latency_ms: int = 500
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

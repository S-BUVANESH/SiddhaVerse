import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_prefix: str = "/api/v1"
    db_path: str = r"d:\Siddha_Wisdom\siddhaverse.db"
    db_type: str = "sqlite"  # "sqlite" or "postgres"
    postgres_dsn: str = "postgresql://user:pass@localhost:5432/siddhaverse"
    log_level: str = "INFO"
    environment: str = "development"  # "development" | "staging" | "production"
    max_context_tokens: int = 4000

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 60     # requests per window
    rate_limit_window_seconds: int = 60

    # Security
    api_key_required: bool = False    # Set True in production
    allowed_origins: str = "*"        # Comma-separated list or "*"

    # Observability
    request_id_header: str = "X-Request-ID"
    structured_logging: bool = False  # JSON logging when True

settings = Settings()

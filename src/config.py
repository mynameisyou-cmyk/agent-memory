"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/agent_memory"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # OpenAI
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-ada-002"
    embedding_dimensions: int = 1536

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "info"

    # Working memory
    working_memory_ttl: int = 3600  # seconds

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    # Plan limits
    seed_memory_limit: int = 10_000
    seed_agent_limit: int = 5
    grow_memory_limit: int = 100_000
    grow_agent_limit: int = 25

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

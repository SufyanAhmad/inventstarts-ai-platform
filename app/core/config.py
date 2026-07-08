from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "InventStarts AI Platform"
    app_version: str = "1.0.0"

    database_url: str = "sqlite+aiosqlite:///./app.db"

    ai_provider: str = "gemini"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    openai_api_key: str | None = None
    openai_model: str = "gpt-5.5"

    ai_request_timeout_seconds: float = 30
    ai_max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def validate_settings(self) -> None:
        supported_providers = {"gemini", "openai"}

        if self.ai_provider.lower() not in supported_providers:
            raise ValueError(
                f"Unsupported AI provider: {self.ai_provider}"
            )

        if self.ai_provider.lower() == "gemini" and not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from environment variables."
            )

        if self.ai_provider.lower() == "openai" and not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing from environment variables."
            )

        if self.ai_request_timeout_seconds <= 0:
            raise ValueError(
                "AI_REQUEST_TIMEOUT_SECONDS must be greater than zero."
            )

        if self.ai_max_retries < 1:
            raise ValueError(
                "AI_MAX_RETRIES must be at least 1."
            )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_settings()
    return settings


settings = get_settings()
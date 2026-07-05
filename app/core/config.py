import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = os.getenv(
        "PROJECT_NAME",
        "InventStarts AI Platform"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./app.db"
    )
    AI_PROVIDER = os.getenv(
        "AI_PROVIDER",
        "gemini"
    ).lower()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    AI_REQUEST_TIMEOUT_SECONDS = float(
        os.getenv("AI_REQUEST_TIMEOUT_SECONDS", "30")
    )

    AI_MAX_RETRIES = int(
        os.getenv("AI_MAX_RETRIES", "3")
    )

    def validate(self) -> None:
        supported_providers = {"gemini"}

        if self.AI_PROVIDER not in supported_providers:
            raise ValueError(
                f"Unsupported AI provider: {self.AI_PROVIDER}"
            )

        if self.AI_PROVIDER == "gemini" and not self.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing from environment variables."
            )

        if self.AI_REQUEST_TIMEOUT_SECONDS <= 0:
            raise ValueError(
                "AI_REQUEST_TIMEOUT_SECONDS must be greater than zero."
            )

        if self.AI_MAX_RETRIES < 1:
            raise ValueError(
                "AI_MAX_RETRIES must be at least 1."
            )


settings = Settings()
settings.validate()
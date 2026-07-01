from app.providers.base import BaseLLMProvider
from app.providers.gemini import GeminiProvider


class ProviderFactory:

    @staticmethod
    def create(provider_name: str) -> BaseLLMProvider:
        provider_name = provider_name.lower().strip()

        if provider_name == "gemini":
            return GeminiProvider()

        raise ValueError(
            f"Unsupported AI provider: {provider_name}"
        )
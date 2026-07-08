from app.providers.base import BaseLLMProvider
from app.providers.gemini import GeminiProvider
from app.providers.openai import OpenAIProvider


class ProviderFactory:

    @staticmethod
    def create(provider_name: str) -> BaseLLMProvider:
        provider_name = provider_name.lower().strip()

        if provider_name == "gemini":
            return GeminiProvider()

        if provider_name == "openai":
            return OpenAIProvider()

        raise ValueError(
            f"Unsupported AI provider: {provider_name}"
        )

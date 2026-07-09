from app.providers.gemini import GeminiProvider
from app.providers.openai import OpenAIProvider


class ProviderFactory:
    _providers = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
    }

    @classmethod
    def create(cls, provider_name: str):
        provider = provider_name.lower()

        provider_class = cls._providers.get(provider)

        if provider_class is None:
            raise ValueError(
                f"Unsupported AI provider: {provider}"
            )

        return provider_class()
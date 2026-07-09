from app.core.config import settings
from app.prompts.prompt_manager import PromptManager
from app.providers.base import BaseLLMProvider
from app.providers.factory import ProviderFactory
from app.schemas.ai import AIResponse


class AIService:

    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    async def chat(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 300,
    ) -> AIResponse:
        prompt = PromptManager.build_chat_prompt(message)

        provider_response = await self.provider.generate_response(
            message=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return AIResponse(
            content=provider_response.content,
            provider=provider_response.provider,
            model=provider_response.model,
            temperature=temperature,
            max_tokens=max_tokens,
            latency_ms=provider_response.latency_ms,
        )

    async def generate_conversation_title(
        self,
        message: str,
    ) -> str:
        prompt = PromptManager.build_conversation_title_prompt(message)

        title_response = await self.provider.generate_response(
            message=prompt,
            temperature=0.3,
            max_tokens=30,
        )

        return title_response.content.strip().replace('"', "")


provider = ProviderFactory.create(settings.ai_provider)
ai_service = AIService(provider)

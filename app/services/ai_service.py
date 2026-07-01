from app.core.config import settings
from app.prompts.prompt_manager import PromptManager
from app.providers.base import BaseLLMProvider
from app.providers.factory import ProviderFactory


class AIService:

    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    async def chat(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> str:
        prompt = PromptManager.build_chat_prompt(message)

        return await self.provider.generate_response(
            message=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )


provider = ProviderFactory.create(settings.AI_PROVIDER)
ai_service = AIService(provider)
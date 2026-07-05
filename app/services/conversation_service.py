from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.conversation_exceptions import (
    ConversationNotFoundException,
)
from app.repositories.conversation_repository import (
    ConversationRepository,
    conversation_repository,
)
from app.schemas.conversation import (
    ConversationData,
    ConversationMessage,
)
from app.services.ai_service import AIService, ai_service


class ConversationService:

    def __init__(
        self,
        repository: ConversationRepository,
        ai_service: AIService,
    ):
        self.repository = repository
        self.ai_service = ai_service

    async def create_conversation(
        self,
        session: AsyncSession,
    ) -> str:
        conversation = await self.repository.create(session)
        return conversation.id

    async def send_message(
        self,
        session: AsyncSession,
        conversation_id: str,
        message: str,
        temperature: float,
        max_tokens: int,
    ) -> ConversationData:
        await self._ensure_exists(
            session=session,
            conversation_id=conversation_id,
        )

        user_message = ConversationMessage(
            role="user",
            content=message,
        )

        await self.repository.add_message(
            session=session,
            conversation_id=conversation_id,
            message=user_message,
        )

        ai_response = await self.ai_service.chat(
            message=message,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        assistant_message = ConversationMessage(
            role="assistant",
            content=ai_response,
        )

        await self.repository.add_message(
            session=session,
            conversation_id=conversation_id,
            message=assistant_message,
        )

        return await self.get_conversation(
            session=session,
            conversation_id=conversation_id,
        )

    async def get_conversation(
        self,
        session: AsyncSession,
        conversation_id: str,
    ) -> ConversationData:
        await self._ensure_exists(
            session=session,
            conversation_id=conversation_id,
        )

        messages = await self.repository.get_messages(
            session=session,
            conversation_id=conversation_id,
        )

        return ConversationData(
            conversation_id=conversation_id,
            messages=messages,
        )

    async def _ensure_exists(
        self,
        session: AsyncSession,
        conversation_id: str,
    ) -> None:
        exists = await self.repository.exists(
            session=session,
            conversation_id=conversation_id,
        )

        if not exists:
            raise ConversationNotFoundException(
                conversation_id
            )


conversation_service = ConversationService(
    repository=conversation_repository,
    ai_service=ai_service,
)
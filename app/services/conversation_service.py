from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.conversation_exceptions import (
    ConversationNotFoundException,
)
from app.models.conversation import (
    ConversationMessage as ConversationMessageModel,
)
from app.repositories.conversation_repository import (
    ConversationRepository
)
from app.schemas.conversation import (
    ConversationData,
    ConversationListData,
    ConversationMessage,
    ConversationSummary,
)
from app.services.ai_service import AIService


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

    async def get_conversations(
        self,
        session: AsyncSession,
    ) -> ConversationListData:
        conversations = await self.repository.get_conversations(
            session=session,
        )

        return ConversationListData(
            conversations=[
                ConversationSummary(
                    conversation_id=conversation.id,
                    title=conversation.title,
                )
                for conversation in conversations
            ],
        )

    async def send_message(
        self,
        session: AsyncSession,
        conversation_id: str,
        message: str,
        temperature: float,
        max_tokens: int,
    ) -> ConversationData:
        conversation = await self.repository.get_conversation(
            session=session,
            conversation_id=conversation_id,
        )

        if conversation is None:
            raise ConversationNotFoundException(conversation_id)

        await self.repository.add_message(
            session=session,
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

        ai_response = await self.ai_service.chat(
            message=message,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        await self.repository.add_message(
            session=session,
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response.content,
            provider=ai_response.provider,
            model=ai_response.model,
            temperature=ai_response.temperature,
            max_tokens=ai_response.max_tokens,
            latency_ms=ai_response.latency_ms,
        )

        if conversation.title is None:
            title = await self.ai_service.generate_conversation_title(
                message
            )

            await self.repository.update_title(
                session=session,
                conversation_id=conversation_id,
                title=title,
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
            messages=[
                self._map_message_to_schema(message)
                for message in messages
            ],
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
            raise ConversationNotFoundException(conversation_id)

    @staticmethod
    def _map_message_to_schema(
        message: ConversationMessageModel,
    ) -> ConversationMessage:
        return ConversationMessage(
            role=message.role,
            content=message.content,
            provider=message.provider,
            model=message.model,
            temperature=message.temperature,
            max_tokens=message.max_tokens,
            latency_ms=message.latency_ms,
        )

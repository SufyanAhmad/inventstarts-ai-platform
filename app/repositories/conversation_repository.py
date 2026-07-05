from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import (
    Conversation,
    ConversationMessage as ConversationMessageModel,
)
from app.schemas.conversation import ConversationMessage


class ConversationRepository:

    async def create(
        self,
        session: AsyncSession,
    ) -> Conversation:
        conversation = Conversation()

        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        return conversation

    async def exists(
        self,
        session: AsyncSession,
        conversation_id: str,
    ) -> bool:
        result = await session.execute(
            select(Conversation.id).where(
                Conversation.id == conversation_id
            )
        )

        return result.scalar_one_or_none() is not None

    async def add_message(
        self,
        session: AsyncSession,
        conversation_id: str,
        message: ConversationMessage,
    ) -> None:
        db_message = ConversationMessageModel(
            conversation_id=conversation_id,
            role=message.role,
            content=message.content,
        )

        session.add(db_message)
        await session.commit()

    async def get_messages(
        self,
        session: AsyncSession,
        conversation_id: str,
    ) -> list[ConversationMessage]:
        result = await session.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))
        )

        conversation = result.scalar_one_or_none()

        if conversation is None:
            return []

        sorted_messages = sorted(
            conversation.messages,
            key=lambda message: message.created_at,
        )

        return [
            ConversationMessage(
                role=message.role,
                content=message.content,
            )
            for message in sorted_messages
        ]


conversation_repository = ConversationRepository()
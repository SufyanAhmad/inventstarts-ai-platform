from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation
from app.models.conversation import ConversationMessage as ConversationMessageModel


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

    async def get_conversation(
        self,
        session: AsyncSession,
        conversation_id: str,
    ) -> Conversation | None:
        result = await session.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))
        )

        return result.scalar_one_or_none()

    async def add_message(
        self,
        session: AsyncSession,
        conversation_id: str,
        role: str,
        content: str,
    ) -> ConversationMessageModel:
        db_message = ConversationMessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        session.add(db_message)
        await session.commit()
        await session.refresh(db_message)

        return db_message

    async def get_messages(
        self,
        session: AsyncSession,
        conversation_id: str,
    ) -> list[ConversationMessageModel]:
        result = await session.execute(
            select(ConversationMessageModel)
            .where(
                ConversationMessageModel.conversation_id == conversation_id
            )
            .order_by(ConversationMessageModel.created_at)
        )

        return list(result.scalars().all())

    async def update_title(
        self,
        session: AsyncSession,
        conversation_id: str,
        title: str,
    ) -> Conversation | None:
        conversation = await session.get(
            Conversation,
            conversation_id,
        )

        if conversation is None:
            return None

        conversation.title = title

        await session.commit()
        await session.refresh(conversation)

        return conversation


conversation_repository = ConversationRepository()
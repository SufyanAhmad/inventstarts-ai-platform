import uuid

from app.exceptions.conversation_exceptions import (
    ConversationNotFoundException,
)
from app.repositories.conversation_repository import (
    ConversationRepository,
)
from app.schemas.conversation import (
    ConversationData,
    ConversationMessage,
)
from app.services.ai_service import AIService


class ConversationService:

    def __init__(
        self,
        repository: ConversationRepository,
        ai_service: AIService
    ):
        self.repository = repository
        self.ai_service = ai_service

    def create_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        self.repository.create(conversation_id)

        return conversation_id

    async def send_message(
        self,
        conversation_id: str,
        message: str,
        temperature: float,
        max_tokens: int
    ) -> ConversationData:
        self._ensure_exists(conversation_id)

        user_message = ConversationMessage(
            role="user",
            content=message
        )

        self.repository.add_message(
            conversation_id,
            user_message
        )

        ai_response = await self.ai_service.chat(
            message=message,
            temperature=temperature,
            max_tokens=max_tokens
        )

        assistant_message = ConversationMessage(
            role="assistant",
            content=ai_response
        )

        self.repository.add_message(
            conversation_id,
            assistant_message
        )

        return self.get_conversation(conversation_id)

    def get_conversation(
        self,
        conversation_id: str
    ) -> ConversationData:
        self._ensure_exists(conversation_id)

        return ConversationData(
            conversation_id=conversation_id,
            messages=self.repository.get_messages(
                conversation_id
            )
        )

    def _ensure_exists(self, conversation_id: str) -> None:
        if not self.repository.exists(conversation_id):
            raise ConversationNotFoundException(
                conversation_id
            )
        
from app.repositories.conversation_repository import (
    conversation_repository,
)
from app.services.ai_service import ai_service


conversation_service = ConversationService(
    repository=conversation_repository,
    ai_service=ai_service
)
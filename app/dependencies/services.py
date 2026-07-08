from fastapi import Depends

from app.dependencies.ai import get_ai_service
from app.dependencies.repositories import get_conversation_repository
from app.repositories.conversation_repository import ConversationRepository
from app.services.ai_service import AIService
from app.services.conversation_service import ConversationService


def get_conversation_service(
    repository: ConversationRepository = Depends(
        get_conversation_repository
    ),
    ai: AIService = Depends(get_ai_service),
) -> ConversationService:
    return ConversationService(
        repository=repository,
        ai_service=ai,
    )
from app.repositories.conversation_repository import ConversationRepository


def get_conversation_repository() -> ConversationRepository:
    return ConversationRepository()
from app.schemas.conversation import ConversationMessage


class ConversationRepository:

    def __init__(self):
        self._conversations: dict[str, list[ConversationMessage]] = {}

    def create(self, conversation_id: str) -> None:
        self._conversations[conversation_id] = []

    def exists(self, conversation_id: str) -> bool:
        return conversation_id in self._conversations

    def add_message(
        self,
        conversation_id: str,
        message: ConversationMessage
    ) -> None:
        self._conversations[conversation_id].append(message)

    def get_messages(
        self,
        conversation_id: str
    ) -> list[ConversationMessage]:
        return self._conversations[conversation_id]


conversation_repository = ConversationRepository()
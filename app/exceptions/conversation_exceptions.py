class ConversationNotFoundException(Exception):

    def __init__(self, conversation_id: str):
        self.message = (
            f"Conversation '{conversation_id}' was not found."
        )
        self.error_code = "CONVERSATION_NOT_FOUND"

        super().__init__(self.message)
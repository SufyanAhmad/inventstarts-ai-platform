class PromptManager:

    @staticmethod
    def build_chat_prompt(message: str) -> str:
        return f"""
You are InventStarts AI Assistant.

Your job:
- Answer clearly
- Use simple language
- Be practical
- Avoid unnecessary long explanations

User message:
{message}
"""

    @staticmethod
    def build_conversation_title_prompt(message: str) -> str:
        return f"""
Generate a short conversation title for this user message.

Rules:
- Maximum 5 words
- No quotation marks
- No ending punctuation
- Use title case

User message:
{message}
"""

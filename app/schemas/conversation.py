from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    latency_ms: int | None = None


class CreateConversationData(BaseModel):
    conversation_id: str


class ConversationSummary(BaseModel):
    conversation_id: str
    title: str | None = None


class ConversationListData(BaseModel):
    conversations: list[ConversationSummary]


class SendMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=300, ge=50, le=2000)


class ConversationData(BaseModel):
    conversation_id: str
    messages: list[ConversationMessage]

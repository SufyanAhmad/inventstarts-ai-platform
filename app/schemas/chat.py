from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=300, ge=50, le=2000)


class ChatResponse(BaseModel):
    response: str
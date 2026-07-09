from pydantic import BaseModel


class AIResponse(BaseModel):
    content: str
    provider: str
    model: str
    temperature: float
    max_tokens: int
    latency_ms: int
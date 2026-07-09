from typing import Any

from pydantic import BaseModel


class ProviderResponse(BaseModel):
    content: str

    provider: str
    model: str

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    finish_reason: str | None = None
    latency_ms: int

    raw_response: Any | None = None

    class Config:
        arbitrary_types_allowed = True

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error_code: Optional[str] = None
    request_id: Optional[str] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    data: Optional[dict] = None
    error_code: str
    request_id: Optional[str] = None
from fastapi import APIRouter

from app.middleware.request_context import get_request_id
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.common import APIResponse, ErrorResponse
from app.services.ai_service import ai_service


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/",
    response_model=APIResponse[ChatResponse],
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid AI provider request",
        },
        422: {
            "model": ErrorResponse,
            "description": "Request validation failed",
        },
        500: {
            "model": ErrorResponse,
            "description": "Unexpected internal server error",
        },
        502: {
            "model": ErrorResponse,
            "description": "Invalid or empty AI provider response",
        },
        503: {
            "model": ErrorResponse,
            "description": "AI provider temporarily unavailable",
        },
        504: {
            "model": ErrorResponse,
            "description": "AI provider request timed out",
        },
    },
)
async def chat(request: ChatRequest):
    ai_response = await ai_service.chat(
        message=request.message,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return APIResponse[ChatResponse](
        success=True,
        message="AI response generated successfully.",
        data=ChatResponse(response=ai_response),
        request_id=get_request_id(),
    )
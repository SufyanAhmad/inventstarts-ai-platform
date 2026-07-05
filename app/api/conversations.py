from fastapi import APIRouter

from app.middleware.request_context import get_request_id
from app.schemas.common import APIResponse, ErrorResponse
from app.schemas.conversation import (
    ConversationData,
    CreateConversationData,
    SendMessageRequest,
)
from app.services.conversation_service import (
    conversation_service,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post(
    "/",
    response_model=APIResponse[CreateConversationData]
)
def create_conversation():
    conversation_id = (
        conversation_service.create_conversation()
    )

    return APIResponse[CreateConversationData](
        success=True,
        message="Conversation created successfully.",
        data=CreateConversationData(
            conversation_id=conversation_id
        ),
        request_id=get_request_id()
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=APIResponse[ConversationData],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Conversation not found"
        }
    }
)
async def send_message(
    conversation_id: str,
    request: SendMessageRequest
):
    conversation = await conversation_service.send_message(
        conversation_id=conversation_id,
        message=request.message,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

    return APIResponse[ConversationData](
        success=True,
        message="Message processed successfully.",
        data=conversation,
        request_id=get_request_id()
    )


@router.get(
    "/{conversation_id}",
    response_model=APIResponse[ConversationData],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Conversation not found"
        }
    }
)
def get_conversation(conversation_id: str):
    conversation = (
        conversation_service.get_conversation(
            conversation_id
        )
    )

    return APIResponse[ConversationData](
        success=True,
        message="Conversation retrieved successfully.",
        data=conversation,
        request_id=get_request_id()
    )
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.middleware.request_context import get_request_id
from app.schemas.common import APIResponse, ErrorResponse
from app.schemas.conversation import (
    ConversationData,
    CreateConversationData,
    SendMessageRequest,
)
from fastapi import Depends

from app.dependencies.services import get_conversation_service
from app.services.conversation_service import ConversationService


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "/",
    response_model=APIResponse[CreateConversationData],
)
async def create_conversation(
    session: AsyncSession = Depends(get_db_session),
    service: ConversationService = Depends(get_conversation_service),
):
    conversation_id = await service.create_conversation(session)

    return APIResponse[CreateConversationData](
        success=True,
        message="Conversation created successfully.",
        data=CreateConversationData(
            conversation_id=conversation_id,
        ),
        request_id=get_request_id(),
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=APIResponse[ConversationData],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Conversation not found",
        }
    },
)
async def send_message(
    conversation_id: str,
    request: SendMessageRequest,
    session: AsyncSession = Depends(get_db_session),
    service: ConversationService = Depends(get_conversation_service),

):
    conversation = await service.send_message(
        session=session,
        conversation_id=conversation_id,
        message=request.message,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return APIResponse[ConversationData](
        success=True,
        message="Message processed successfully.",
        data=conversation,
        request_id=get_request_id(),
    )


@router.get(
    "/{conversation_id}",
    response_model=APIResponse[ConversationData],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Conversation not found",
        }
    },
)
async def get_conversation(
    conversation_id: str,
    session: AsyncSession = Depends(get_db_session),
    service: ConversationService = Depends(get_conversation_service),
):
    conversation = await service.get_conversation(
        session=session,
        conversation_id=conversation_id,
    )

    return APIResponse[ConversationData](
        success=True,
        message="Conversation retrieved successfully.",
        data=conversation,
        request_id=get_request_id(),
    )
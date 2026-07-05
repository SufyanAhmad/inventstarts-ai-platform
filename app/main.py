from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.chat import router as chat_router
from app.core.config import settings
from app.exceptions.ai_exceptions import AIProviderException
from app.exceptions.handlers import (
    global_exception_handler,
    validation_exception_handler,
)
from app.middleware.logging_middleware import logging_middleware
from app.middleware.request_context import get_request_id
from app.api.conversations import (
    router as conversation_router,
)
from app.exceptions.conversation_exceptions import (
    ConversationNotFoundException,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="AI-powered services and automation platform by InventStarts."
)


# Request logging and correlation-ID middleware
app.middleware("http")(logging_middleware)


# Handle Pydantic/FastAPI request validation errors
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)


# Handle all unexpected application errors
app.add_exception_handler(
    Exception,
    global_exception_handler
)

@app.exception_handler(ConversationNotFoundException)
async def conversation_not_found_handler(
    request: Request,
    exc: ConversationNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
            "data": None,
            "error_code": exc.error_code,
            "request_id": get_request_id(),
        }
    )
# Handle known AI provider errors
@app.exception_handler(AIProviderException)
async def ai_provider_exception_handler(
    request: Request,
    exc: AIProviderException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "data": None,
            "error_code": exc.error_code,
            "request_id": get_request_id(),
        }
    )


# Register API routers
app.include_router(chat_router)

app.include_router(conversation_router)
@app.get("/", tags=["System"])
def home():
    return {
        "success": True,
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "data": {
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": "/health",
        },
        "error_code": None,
        "request_id": get_request_id(),
    }


@app.get("/health", tags=["System"])
def health():
    return {
        "success": True,
        "message": "Application is healthy.",
        "data": {
            "service": settings.PROJECT_NAME,
            "version": settings.APP_VERSION,
            "provider": settings.AI_PROVIDER,
            "model": settings.GEMINI_MODEL,
        },
        "error_code": None,
        "request_id": get_request_id(),
    }
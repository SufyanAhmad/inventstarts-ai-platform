from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import logger
from app.middleware.request_context import get_request_id


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    request_id = get_request_id()

    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(
                str(item) for item in error.get("loc", [])
            ),
            "message": error.get("msg"),
            "type": error.get("type"),
        })

    logger.warning(
        "Validation failed | request_id=%s | errors=%s",
        request_id,
        errors,
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Request validation failed.",
            "data": {
                "errors": errors
            },
            "error_code": "VALIDATION_ERROR",
            "request_id": request_id,
        }
    )


async def global_exception_handler(
    request: Request,
    exc: Exception
):
    request_id = get_request_id()

    logger.exception(
        "Unhandled exception | request_id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred.",
            "data": None,
            "error_code": "INTERNAL_SERVER_ERROR",
            "request_id": request_id,
        }
    )
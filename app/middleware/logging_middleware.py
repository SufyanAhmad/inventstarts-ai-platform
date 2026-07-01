import time

from fastapi import Request

from app.core.logger import logger
from app.middleware.request_context import (
    generate_request_id,
    request_id_context,
)


async def logging_middleware(request: Request, call_next):
    request_id = request.headers.get(
        "X-Request-ID",
        generate_request_id()
    )

    token = request_id_context.set(request_id)
    start_time = time.perf_counter()

    logger.info(
        "Request started | request_id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

        duration = round(
            time.perf_counter() - start_time,
            3
        )

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed | request_id=%s | method=%s | "
            "path=%s | status=%s | duration=%ss",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    finally:
        request_id_context.reset(token)
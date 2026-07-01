import asyncio
import time

from google import genai
from google.genai import errors, types
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import settings
from app.core.logger import logger
from app.exceptions.ai_exceptions import AIProviderException
from app.middleware.request_context import get_request_id
from app.providers.base import BaseLLMProvider


class TemporaryGeminiError(Exception):
    """Internal exception used only for retryable Gemini failures."""


class GeminiProvider(BaseLLMProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    @retry(
        retry=retry_if_exception_type(TemporaryGeminiError),
        stop=stop_after_attempt(settings.AI_MAX_RETRIES),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=8
        ),
        reraise=True,
    )
    async def _generate_with_retry(
        self,
        message: str,
        temperature: float,
        max_tokens: int
    ):
        try:
            return await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=message,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                ),
                timeout=settings.AI_REQUEST_TIMEOUT_SECONDS,
            )

        except asyncio.TimeoutError as exc:
            raise AIProviderException(
                message="The AI provider request timed out.",
                error_code="AI_PROVIDER_TIMEOUT",
                status_code=504,
            ) from exc

        except errors.ServerError as exc:
            if exc.code in {429, 500, 502, 503, 504}:
                raise TemporaryGeminiError(str(exc)) from exc

            raise AIProviderException(
                message="Gemini returned a server error.",
                error_code="GEMINI_SERVER_ERROR",
                status_code=503,
            ) from exc

        except errors.ClientError as exc:
            raise AIProviderException(
                message="The Gemini request configuration is invalid.",
                error_code="GEMINI_CLIENT_ERROR",
                status_code=400,
            ) from exc

    async def generate_response(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> str:
        request_id = get_request_id()
        start_time = time.perf_counter()

        logger.info(
            "Gemini call started | request_id=%s | "
            "model=%s | temperature=%s | max_tokens=%s",
            request_id,
            settings.GEMINI_MODEL,
            temperature,
            max_tokens,
        )

        try:
            response = await self._generate_with_retry(
                message=message,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response_text = response.text

            if not response_text:
                raise AIProviderException(
                    message="AI provider returned an empty response.",
                    error_code="EMPTY_AI_RESPONSE",
                    status_code=502,
                )

            duration = round(
                time.perf_counter() - start_time,
                3
            )

            logger.info(
                "Gemini call completed | request_id=%s | duration=%ss",
                request_id,
                duration,
            )

            return response_text

        except AIProviderException:
            raise

        except TemporaryGeminiError as exc:
            logger.exception(
                "Gemini unavailable after retries | request_id=%s",
                request_id,
            )

            raise AIProviderException(
                message=(
                    "Gemini is temporarily busy. "
                    "Please try again shortly."
                ),
                error_code="GEMINI_TEMPORARILY_UNAVAILABLE",
                status_code=503,
            ) from exc

        except Exception as exc:
            logger.exception(
                "Unexpected Gemini provider failure | request_id=%s",
                request_id,
            )

            raise AIProviderException(
                message="Gemini service is currently unavailable.",
                error_code="GEMINI_PROVIDER_ERROR",
                status_code=503,
            ) from exc
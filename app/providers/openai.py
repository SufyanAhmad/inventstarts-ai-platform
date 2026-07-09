import asyncio
import time
from typing import Any

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
from app.providers.response import ProviderResponse


class TemporaryOpenAIError(Exception):
    """Internal exception used only for retryable OpenAI failures."""


class OpenAIProvider(BaseLLMProvider):

    def __init__(self):
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise AIProviderException(
                message="OpenAI SDK is not installed.",
                error_code="OPENAI_SDK_MISSING",
                status_code=500,
            ) from exc

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key
        )

    @property
    def model_name(self) -> str:
        return settings.openai_model

    @retry(
        retry=retry_if_exception_type(TemporaryOpenAIError),
        stop=stop_after_attempt(settings.ai_max_retries),
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
    ) -> Any:
        try:
            return await asyncio.wait_for(
                self.client.responses.create(
                    model=settings.openai_model,
                    input=message,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
                timeout=settings.ai_request_timeout_seconds,
            )

        except asyncio.TimeoutError as exc:
            raise AIProviderException(
                message="The AI provider request timed out.",
                error_code="AI_PROVIDER_TIMEOUT",
                status_code=504,
            ) from exc

        except Exception as exc:
            status_code = getattr(exc, "status_code", None)

            if status_code in {429, 500, 502, 503, 504}:
                raise TemporaryOpenAIError(str(exc)) from exc

            if status_code is not None and 400 <= status_code < 500:
                raise AIProviderException(
                    message="The OpenAI request configuration is invalid.",
                    error_code="OPENAI_CLIENT_ERROR",
                    status_code=400,
                ) from exc

            raise

    async def generate_response(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> ProviderResponse:
        request_id = get_request_id()
        start_time = time.perf_counter()

        logger.info(
            "OpenAI call started | request_id=%s | "
            "model=%s | temperature=%s | max_tokens=%s",
            request_id,
            settings.openai_model,
            temperature,
            max_tokens,
        )

        try:
            response = await self._generate_with_retry(
                message=message,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response_text = self._extract_response_text(response)

            if not response_text:
                raise AIProviderException(
                    message="AI provider returned an empty response.",
                    error_code="EMPTY_AI_RESPONSE",
                    status_code=502,
                )

            latency_ms = int(
                (time.perf_counter() - start_time) * 1000
            )

            logger.info(
                "OpenAI call completed | request_id=%s | duration=%ss",
                request_id,
                round(latency_ms / 1000, 3),
            )

            return ProviderResponse(
                content=response_text,
                provider="openai",
                model=self.model_name,
                latency_ms=latency_ms,
                raw_response=response,
            )

        except AIProviderException:
            raise

        except TemporaryOpenAIError as exc:
            logger.exception(
                "OpenAI unavailable after retries | request_id=%s",
                request_id,
            )

            raise AIProviderException(
                message=(
                    "OpenAI is temporarily busy. "
                    "Please try again shortly."
                ),
                error_code="OPENAI_TEMPORARILY_UNAVAILABLE",
                status_code=503,
            ) from exc

        except Exception as exc:
            logger.exception(
                "Unexpected OpenAI provider failure | request_id=%s",
                request_id,
            )

            raise AIProviderException(
                message="OpenAI service is currently unavailable.",
                error_code="OPENAI_PROVIDER_ERROR",
                status_code=503,
            ) from exc

    def _extract_response_text(self, response: Any) -> str:
        response_text = getattr(response, "output_text", None)

        if response_text:
            return response_text

        output = getattr(response, "output", None) or []
        text_parts = []

        for output_item in output:
            content = getattr(output_item, "content", None) or []

            for content_item in content:
                text = getattr(content_item, "text", None)

                if text:
                    text_parts.append(text)

        return "".join(text_parts)

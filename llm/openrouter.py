"""Single OpenRouter client: chat (text) + vision, retry, fallback, cost accounting.

Framework-agnostic — no FastAPI import — so the CLI runner and the future
HTTP API both call this directly.
"""

from __future__ import annotations

import base64
import logging
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

_API_URL = "https://openrouter.ai/api/v1/chat/completions"
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}
_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


class OpenRouterError(Exception):
    """Raised when a model call fails after retries and (if configured) fallback."""


@dataclass
class LLMUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float


@dataclass
class LLMResponse:
    content: str
    model: str
    usage: LLMUsage


def image_content_block(image_path: Path, *, detail: str = "auto") -> dict[str, Any]:
    """Build an OpenAI/OpenRouter-style image content block from a local file."""
    suffix = image_path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{mime};base64,{encoded}", "detail": detail},
    }


def extract_json(text: str) -> str:
    """Strip a markdown code fence around JSON, if the model added one."""
    match = _FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


class OpenRouterClient:
    def __init__(self, *, timeout_s: float = 180.0) -> None:
        self._settings = get_settings()
        self._timeout_s = timeout_s

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.4,
        max_tokens: int = 4096,
        max_retries: int = 3,
    ) -> LLMResponse:
        """Call `model` (default `settings.openrouter_model`); on failure after
        retries, fall back once to `settings.openrouter_fallback_model`."""
        if not self._settings.openrouter_api_key:
            raise OpenRouterError("OPENROUTER_API_KEY is not set")

        primary = model or self._settings.openrouter_model
        if not primary:
            raise OpenRouterError("no model specified and OPENROUTER_MODEL is not set")

        try:
            return self._call_with_retries(primary, messages, temperature, max_tokens, max_retries)
        except OpenRouterError as primary_exc:
            fallback = self._settings.openrouter_fallback_model
            if not fallback or fallback == primary:
                raise
            logger.warning(
                "primary model %s failed (%s); falling back to %s", primary, primary_exc, fallback
            )
            try:
                return self._call_with_retries(
                    fallback, messages, temperature, max_tokens, max_retries
                )
            except OpenRouterError as fallback_exc:
                raise OpenRouterError(
                    f"both primary model {primary!r} and fallback model {fallback!r} failed. "
                    f"primary: {primary_exc}; fallback: {fallback_exc}"
                ) from fallback_exc

    def _call_with_retries(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float,
        max_tokens: int,
        max_retries: int,
    ) -> LLMResponse:
        last_error: str = "unknown error"
        for attempt in range(1, max_retries + 1):
            try:
                response = httpx.post(
                    _API_URL,
                    headers={
                        "Authorization": f"Bearer {self._settings.openrouter_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "usage": {"include": True},
                    },
                    timeout=self._timeout_s,
                )
            except httpx.HTTPError as exc:
                last_error = f"transport error: {exc}"
                logger.warning(
                    "OpenRouter call to %s failed (attempt %d/%d): %s",
                    model,
                    attempt,
                    max_retries,
                    last_error,
                )
                self._sleep_backoff(attempt)
                continue

            if response.status_code in _RETRYABLE_STATUS:
                last_error = f"HTTP {response.status_code}: {response.text[:300]}"
                logger.warning(
                    "OpenRouter call to %s got %s (attempt %d/%d), retrying",
                    model,
                    response.status_code,
                    attempt,
                    max_retries,
                )
                self._sleep_backoff(attempt)
                continue

            if response.status_code >= 400:
                raise OpenRouterError(
                    f"model {model!r} returned HTTP {response.status_code}: "
                    f"{response.text[:500]}"
                )

            data = response.json()
            if "error" in data:
                raise OpenRouterError(f"model {model!r} returned an error: {data['error']}")

            choice = data["choices"][0]
            content = choice["message"]["content"]
            usage_raw = data.get("usage") or {}
            usage = LLMUsage(
                prompt_tokens=usage_raw.get("prompt_tokens", 0),
                completion_tokens=usage_raw.get("completion_tokens", 0),
                total_tokens=usage_raw.get("total_tokens", 0),
                cost_usd=usage_raw.get("cost", 0.0),
            )
            return LLMResponse(content=content, model=data.get("model", model), usage=usage)

        raise OpenRouterError(
            f"model {model!r} failed after {max_retries} attempts: {last_error}"
        )

    @staticmethod
    def _sleep_backoff(attempt: int) -> None:
        time.sleep(min(2**attempt, 20))

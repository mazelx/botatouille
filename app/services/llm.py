"""OpenRouter LLM service for conversational AI."""

import logging

import httpx

from app.core.config import settings
from app.core.constants import (
    DEFAULT_LLM_MAX_TOKENS,
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_TEMPERATURE,
    MEAL_PLANNING_SYSTEM_PROMPT,
    OPENROUTER_API_BASE_URL,
)

logger = logging.getLogger(__name__)


class OpenRouterService:
    """Service to interact with OpenRouter API."""

    def __init__(self) -> None:
        """Initialize OpenRouter service."""
        self.api_key = settings.openrouter_api_key
        self.base_url = OPENROUTER_API_BASE_URL
        self.app_name = settings.openrouter_app_name
        self.site_url = settings.openrouter_site_url

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = DEFAULT_LLM_MODEL,
        max_tokens: int = DEFAULT_LLM_MAX_TOKENS,
        temperature: float = DEFAULT_LLM_TEMPERATURE,
    ) -> str:
        """
        Send chat completion request to OpenRouter.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model identifier on OpenRouter
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)

        Returns:
            Response text from the model
        """
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url or "https://github.com/botatouille",
            "X-Title": self.app_name,
        }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                logger.info(f"Sending chat completion request to {model}")
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()

                data = response.json()
                content = data["choices"][0]["message"]["content"]

                logger.info(f"Received response: {content[:100]}...")
                return content

            except httpx.HTTPError as e:
                logger.error(f"OpenRouter API error: {e}", exc_info=True)
                if hasattr(e, "response") and e.response is not None:
                    logger.error(f"Response body: {e.response.text}")
                raise
            except (KeyError, IndexError) as e:
                logger.error(f"Failed to parse OpenRouter response: {e}", exc_info=True)
                raise

    async def generate_meal_plan_response(self, user_message: str) -> str:
        """
        Generate a meal planning response based on user message.

        Args:
            user_message: User's text message

        Returns:
            AI-generated response
        """
        messages = [
            {"role": "system", "content": MEAL_PLANNING_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        return await self.chat_completion(messages)


# Global instance
llm_service = OpenRouterService()

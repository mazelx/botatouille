"""OpenRouter LLM service for conversational AI."""

import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenRouterService:
    """Service to interact with OpenRouter API."""

    def __init__(self) -> None:
        """Initialize OpenRouter service."""
        self.api_key = settings.openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.app_name = settings.openrouter_app_name
        self.site_url = settings.openrouter_site_url

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "anthropic/claude-3.5-sonnet",
        max_tokens: int = 1024,
        temperature: float = 0.7,
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
        system_prompt = """You are Botatouille, a friendly meal planning assistant on WhatsApp.

Your role is to help users:
- Plan weekly menus
- Generate shopping lists
- Save and organize recipes
- Manage dietary preferences and restrictions

Keep responses concise and friendly (WhatsApp style).
Use emojis sparingly and appropriately.
When suggesting meal plans, format them clearly with days and meal types.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        return await self.chat_completion(messages)


# Global instance
llm_service = OpenRouterService()

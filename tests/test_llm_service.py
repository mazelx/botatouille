"""Unit tests for LLM service."""

import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx

from app.core.constants import (
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_TEMPERATURE,
    DEFAULT_LLM_MAX_TOKENS,
    MEAL_PLANNING_SYSTEM_PROMPT,
)


@pytest.mark.unit
class TestOpenRouterService:
    """Test suite for OpenRouterService."""

    async def test_chat_completion_success(self, llm_service, mock_httpx_client):
        """Test successful chat completion."""
        messages = [{"role": "user", "content": "Hello"}]
        response = await llm_service.chat_completion(messages)

        assert response == "Test response"
        mock_httpx_client.post.assert_called_once()
        call_kwargs = mock_httpx_client.post.call_args.kwargs
        assert call_kwargs["json"]["model"] == DEFAULT_LLM_MODEL
        assert call_kwargs["json"]["temperature"] == DEFAULT_LLM_TEMPERATURE
        assert call_kwargs["json"]["max_tokens"] == DEFAULT_LLM_MAX_TOKENS

    async def test_chat_completion_custom_params(self, llm_service, mocker):
        """Test chat completion with custom parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Custom response"}}]
        }
        mock_response.raise_for_status = MagicMock()

        mock_post = AsyncMock(return_value=mock_response)

        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        messages = [{"role": "user", "content": "Test"}]
        response = await llm_service.chat_completion(
            messages, model="custom/model", temperature=0.5, max_tokens=512
        )

        assert response == "Custom response"
        call_kwargs = mock_post.call_args.kwargs
        assert call_kwargs["json"]["model"] == "custom/model"
        assert call_kwargs["json"]["temperature"] == 0.5
        assert call_kwargs["json"]["max_tokens"] == 512

    async def test_http_error_handling(self, llm_service, mocker):
        """Test handling of HTTP errors."""
        async def mock_post(*args, **kwargs):
            raise httpx.HTTPError("API Error")

        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        messages = [{"role": "user", "content": "Test"}]
        with pytest.raises(httpx.HTTPError):
            await llm_service.chat_completion(messages)

    async def test_invalid_response_handling(self, llm_service, mocker):
        """Test handling of invalid API response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"invalid": "structure"}
        mock_response.raise_for_status = MagicMock()

        async def mock_post(*args, **kwargs):
            return mock_response

        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        messages = [{"role": "user", "content": "Test"}]
        with pytest.raises(KeyError):
            await llm_service.chat_completion(messages)

    async def test_meal_plan_generation(self, llm_service, mocker):
        """Test meal plan response generation."""
        expected = "Here's your meal plan!"
        mock_chat = AsyncMock(return_value=expected)
        mocker.patch.object(llm_service, "chat_completion", mock_chat)

        response = await llm_service.generate_meal_plan_response("Plan for 3 days")

        assert response == expected
        call_args = mock_chat.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[0]["role"] == "system"
        assert call_args[0]["content"] == MEAL_PLANNING_SYSTEM_PROMPT
        assert call_args[1]["role"] == "user"

    async def test_reasoning_parameter(self, llm_service, mocker):
        """Test reasoning parameter is passed correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Response"}}]
        }
        mock_response.raise_for_status = MagicMock()

        mock_post = AsyncMock(return_value=mock_response)

        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        messages = [{"role": "user", "content": "Test"}]
        await llm_service.chat_completion(messages, reasoning=False)

        call_kwargs = mock_post.call_args.kwargs
        assert call_kwargs["json"]["reasoning"]["enabled"] is False

"""Unit tests for LLM service."""

import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx

from app.services.llm import OpenRouterService
from app.core.constants import (
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_TEMPERATURE,
    DEFAULT_LLM_MAX_TOKENS,
    MEAL_PLANNING_SYSTEM_PROMPT,
)


@pytest.fixture
def llm_service():
    """Create an LLM service instance for testing."""
    return OpenRouterService()


@pytest.mark.unit
class TestOpenRouterService:
    """Test suite for OpenRouterService."""

    async def test_chat_completion_success(self, llm_service, mocker):
        """Test successful chat completion."""
        # Mock the httpx client
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response from AI"}}]
        }
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()

        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        # Call the method
        messages = [{"role": "user", "content": "Hello"}]
        response = await llm_service.chat_completion(messages)

        # Assertions
        assert response == "Test response from AI"
        mock_client.post.assert_called_once()
        call_kwargs = mock_client.post.call_args.kwargs
        assert call_kwargs["json"]["model"] == DEFAULT_LLM_MODEL
        assert call_kwargs["json"]["temperature"] == DEFAULT_LLM_TEMPERATURE
        assert call_kwargs["json"]["max_tokens"] == DEFAULT_LLM_MAX_TOKENS

    async def test_chat_completion_with_custom_params(self, llm_service, mocker):
        """Test chat completion with custom parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Custom response"}}]
        }
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()

        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        # Call with custom params
        messages = [{"role": "user", "content": "Test"}]
        custom_model = "custom/model"
        custom_temp = 0.5
        custom_tokens = 512

        response = await llm_service.chat_completion(
            messages, model=custom_model, temperature=custom_temp, max_tokens=custom_tokens
        )

        # Assertions
        assert response == "Custom response"
        call_kwargs = mock_client.post.call_args.kwargs
        assert call_kwargs["json"]["model"] == custom_model
        assert call_kwargs["json"]["temperature"] == custom_temp
        assert call_kwargs["json"]["max_tokens"] == custom_tokens

    async def test_chat_completion_http_error(self, llm_service, mocker):
        """Test handling of HTTP errors."""
        async def mock_post(*args, **kwargs):
            raise httpx.HTTPError("API Error")

        mock_client = MagicMock()
        mock_client.post = mock_post
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        # Should raise HTTPError
        messages = [{"role": "user", "content": "Test"}]
        with pytest.raises(httpx.HTTPError):
            await llm_service.chat_completion(messages)

    async def test_chat_completion_invalid_response(self, llm_service, mocker):
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

        # Should raise KeyError
        messages = [{"role": "user", "content": "Test"}]
        with pytest.raises(KeyError):
            await llm_service.chat_completion(messages)

    async def test_generate_meal_plan_response(self, llm_service, mocker):
        """Test meal plan response generation."""
        expected_response = "Here's your meal plan for the week!"

        # Mock the chat_completion method
        mock_chat = AsyncMock(return_value=expected_response)
        mocker.patch.object(llm_service, "chat_completion", mock_chat)

        # Call the method
        user_message = "I need a meal plan for 3 days"
        response = await llm_service.generate_meal_plan_response(user_message)

        # Assertions
        assert response == expected_response
        mock_chat.assert_called_once()

        # Verify the messages structure
        call_args = mock_chat.call_args[0][0]
        assert len(call_args) == 2
        assert call_args[0]["role"] == "system"
        assert call_args[0]["content"] == MEAL_PLANNING_SYSTEM_PROMPT
        assert call_args[1]["role"] == "user"
        assert call_args[1]["content"] == user_message

    async def test_reasoning_parameter(self, llm_service, mocker):
        """Test that reasoning parameter is passed correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Reasoning response"}}]
        }
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()

        mocker.patch("httpx.AsyncClient", return_value=mock_client)

        # Call with reasoning disabled
        messages = [{"role": "user", "content": "Test"}]
        await llm_service.chat_completion(messages, reasoning=False)

        # Check that reasoning was passed correctly
        call_kwargs = mock_client.post.call_args.kwargs
        assert call_kwargs["json"]["reasoning"]["enabled"] is False

"""Shared pytest fixtures and configuration."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.services.llm import OpenRouterService


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def llm_service():
    """LLM service instance."""
    return OpenRouterService()


@pytest.fixture
def mock_httpx_client(mocker):
    """Mock httpx AsyncClient with success response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test response"}}]
    }
    mock_response.raise_for_status = MagicMock()

    mock_post = AsyncMock(return_value=mock_response)

    mock_client = MagicMock()
    mock_client.post = mock_post
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    return mock_client


@pytest.fixture
def sample_whatsapp_text_message():
    """Sample WhatsApp text message payload."""
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": "33612345678",
                                    "id": "msg_123",
                                    "type": "text",
                                    "text": {"body": "Test message"},
                                }
                            ]
                        }
                    }
                ]
            }
        ],
    }


@pytest.fixture
def sample_whatsapp_image_message():
    """Sample WhatsApp image message payload."""
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": "33612345678",
                                    "id": "msg_456",
                                    "type": "image",
                                    "image": {"id": "image_123"},
                                }
                            ]
                        }
                    }
                ]
            }
        ],
    }

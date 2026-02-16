"""Integration tests for webhook API."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.core.config import settings


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.mark.integration
class TestWebhookVerification:
    """Test suite for webhook verification endpoint."""

    def test_webhook_verification_success(self, client):
        """Test successful webhook verification."""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": settings.whatsapp_verify_token,
                "hub.challenge": "test_challenge_123",
            },
        )

        assert response.status_code == 200
        assert response.text == "test_challenge_123"

    def test_webhook_verification_wrong_token(self, client):
        """Test webhook verification with wrong token."""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong_token",
                "hub.challenge": "test_challenge_123",
            },
        )

        assert response.status_code == 403
        assert response.json()["detail"] == "Verification failed"

    def test_webhook_verification_wrong_mode(self, client):
        """Test webhook verification with wrong mode."""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "unsubscribe",
                "hub.verify_token": settings.whatsapp_verify_token,
                "hub.challenge": "test_challenge_123",
            },
        )

        assert response.status_code == 403


@pytest.mark.integration
class TestWebhookMessages:
    """Test suite for webhook message handling."""

    def test_receive_text_message(self, client, mocker):
        """Test receiving and processing a text message."""
        # Mock the LLM service
        mock_llm_response = "AI response to user message"
        mock_generate = AsyncMock(return_value=mock_llm_response)
        mocker.patch(
            "app.api.webhook.llm_service.generate_meal_plan_response",
            mock_generate,
        )

        # Mock the WhatsApp send function
        mock_send = AsyncMock()
        mocker.patch("app.api.webhook.send_text_message", mock_send)

        # Send webhook payload
        payload = {
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
                                        "text": {"body": "Hello bot!"},
                                    }
                                ]
                            }
                        }
                    ]
                }
            ],
        }

        response = client.post("/webhook", json=payload)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        mock_generate.assert_called_once_with("Hello bot!")
        mock_send.assert_called_once_with("33612345678", mock_llm_response)

    def test_receive_image_message(self, client, mocker):
        """Test receiving an image message."""
        # Mock the WhatsApp send function
        mock_send = AsyncMock()
        mocker.patch("app.api.webhook.send_text_message", mock_send)

        payload = {
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

        response = client.post("/webhook", json=payload)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        mock_send.assert_called_once()
        assert "Vision processing not yet implemented" in mock_send.call_args[0][1]

    def test_receive_status_update(self, client):
        """Test receiving a status update."""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "statuses": [
                                    {
                                        "id": "msg_789",
                                        "status": "delivered",
                                        "timestamp": "1234567890",
                                    }
                                ]
                            }
                        }
                    ]
                }
            ],
        }

        response = client.post("/webhook", json=payload)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_llm_error_handling(self, client, mocker):
        """Test error handling when LLM fails."""
        # Mock the LLM service to raise an error
        mock_generate = AsyncMock(side_effect=Exception("LLM error"))
        mocker.patch(
            "app.api.webhook.llm_service.generate_meal_plan_response",
            mock_generate,
        )

        # Mock the WhatsApp send function
        mock_send = AsyncMock()
        mocker.patch("app.api.webhook.send_text_message", mock_send)

        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "from": "33612345678",
                                        "id": "msg_error",
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

        response = client.post("/webhook", json=payload)

        # Should still return 200 but send error message
        assert response.status_code == 200
        mock_send.assert_called_once()
        error_message = mock_send.call_args[0][1]
        assert "trouble responding" in error_message

    def test_invalid_webhook_payload(self, client):
        """Test handling of invalid webhook payload."""
        payload = {"invalid": "payload"}

        response = client.post("/webhook", json=payload)

        # Should still return ok (just ignore invalid payloads)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_empty_messages_array(self, client):
        """Test handling of empty messages array."""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{"changes": [{"value": {"messages": []}}]}],
        }

        response = client.post("/webhook", json=payload)

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

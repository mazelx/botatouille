"""Integration tests for webhook API."""

import pytest
from unittest.mock import AsyncMock

from app.core.config import settings


@pytest.mark.integration
class TestWebhookVerification:
    """Test webhook verification endpoint."""

    def test_successful_verification(self, client):
        """Test successful webhook verification."""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": settings.whatsapp_verify_token,
                "hub.challenge": "test_challenge",
            },
        )
        assert response.status_code == 200
        assert response.text == "test_challenge"

    def test_wrong_token(self, client):
        """Test verification with wrong token."""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong",
                "hub.challenge": "test",
            },
        )
        assert response.status_code == 403

    def test_wrong_mode(self, client):
        """Test verification with wrong mode."""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "unsubscribe",
                "hub.verify_token": settings.whatsapp_verify_token,
                "hub.challenge": "test",
            },
        )
        assert response.status_code == 403


@pytest.mark.integration
class TestWebhookMessages:
    """Test webhook message handling."""

    def test_text_message(self, client, sample_whatsapp_text_message, mocker):
        """Test receiving and processing text message."""
        mock_llm = AsyncMock(return_value="AI response")
        mocker.patch("app.api.webhook.llm_service.generate_meal_plan_response", mock_llm)

        mock_send = AsyncMock()
        mocker.patch("app.api.webhook.send_text_message", mock_send)

        response = client.post("/webhook", json=sample_whatsapp_text_message)

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        mock_llm.assert_called_once_with("Test message")
        mock_send.assert_called_once_with("33612345678", "AI response")

    def test_image_message(self, client, sample_whatsapp_image_message, mocker):
        """Test receiving image message."""
        mock_send = AsyncMock()
        mocker.patch("app.api.webhook.send_text_message", mock_send)

        response = client.post("/webhook", json=sample_whatsapp_image_message)

        assert response.status_code == 200
        mock_send.assert_called_once()
        assert "Vision processing not yet implemented" in mock_send.call_args[0][1]

    def test_status_update(self, client):
        """Test receiving status update."""
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
                                    }
                                ]
                            }
                        }
                    ]
                }
            ],
        }

        response = client.post("/webhook", json=payload)
        assert response.status_code == 200

    def test_llm_error_handling(self, client, sample_whatsapp_text_message, mocker):
        """Test error handling when LLM fails."""
        mock_llm = AsyncMock(side_effect=Exception("LLM error"))
        mocker.patch("app.api.webhook.llm_service.generate_meal_plan_response", mock_llm)

        mock_send = AsyncMock()
        mocker.patch("app.api.webhook.send_text_message", mock_send)

        response = client.post("/webhook", json=sample_whatsapp_text_message)

        assert response.status_code == 200
        mock_send.assert_called_once()
        assert "trouble responding" in mock_send.call_args[0][1]

    def test_invalid_payload(self, client):
        """Test handling of invalid payload."""
        response = client.post("/webhook", json={"invalid": "payload"})
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

"""WhatsApp webhook payload models."""

from typing import Any
from pydantic import BaseModel


class WhatsAppMessage(BaseModel):
    """WhatsApp incoming message model."""

    from_number: str
    message_id: str
    timestamp: str
    text: str | None = None
    type: str  # text, image, video, etc.
    media_id: str | None = None


class WhatsAppWebhookEntry(BaseModel):
    """WhatsApp webhook entry model."""

    id: str
    changes: list[dict[str, Any]]


class WhatsAppWebhook(BaseModel):
    """WhatsApp webhook payload model."""

    object: str
    entry: list[WhatsAppWebhookEntry]

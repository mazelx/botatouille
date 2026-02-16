"""WhatsApp webhook endpoints."""

import logging
from fastapi import APIRouter, Request, Response, Query, HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge"),
) -> Response:
    """
    Verify WhatsApp webhook.

    Meta sends a GET request to verify the webhook URL.
    We must respond with the challenge if the verify token matches.
    """
    logger.info(f"Webhook verification request: mode={mode}, token={token}")

    if mode == "subscribe" and token == settings.whatsapp_verify_token:
        logger.info("Webhook verified successfully")
        return Response(content=challenge, media_type="text/plain")

    logger.warning("Webhook verification failed")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def receive_webhook(request: Request) -> dict[str, str]:
    """
    Receive WhatsApp webhook messages.

    Meta sends incoming messages and status updates to this endpoint.
    """
    try:
        body = await request.json()
        logger.info(f"Received webhook: {body}")

        # Extract message data
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})

                    # Handle incoming messages
                    if "messages" in value:
                        for message in value["messages"]:
                            await handle_incoming_message(message, value)

                    # Handle status updates (delivered, read, etc.)
                    if "statuses" in value:
                        logger.info(f"Status update: {value['statuses']}")

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


async def handle_incoming_message(message: dict, value: dict) -> None:
    """
    Process incoming WhatsApp message.

    Args:
        message: Message data from webhook
        value: Full value object containing metadata
    """
    message_type = message.get("type")
    from_number = message.get("from")
    message_id = message.get("id")

    logger.info(f"Processing message {message_id} from {from_number}, type: {message_type}")

    # Handle text messages
    if message_type == "text":
        text_body = message.get("text", {}).get("body", "")
        logger.info(f"Text message: {text_body}")

        # TODO: Send to LLM for processing
        # For now, just log it
        await send_text_message(from_number, f"Echo: {text_body}")

    # Handle image messages
    elif message_type == "image":
        image_id = message.get("image", {}).get("id")
        logger.info(f"Image message: {image_id}")

        # TODO: Download and process image
        await send_text_message(from_number, "Image received! (Vision processing not yet implemented)")

    else:
        logger.info(f"Unsupported message type: {message_type}")


async def send_text_message(to_number: str, text: str) -> None:
    """
    Send a text message via WhatsApp Cloud API.

    Args:
        to_number: Recipient phone number
        text: Message text
    """
    import httpx

    url = f"https://graph.facebook.com/v21.0/{settings.whatsapp_phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text},
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Message sent to {to_number}: {text[:50]}...")
        except httpx.HTTPError as e:
            logger.error(f"Failed to send message: {e}", exc_info=True)

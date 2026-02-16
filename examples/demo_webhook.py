"""Script to test WhatsApp webhook locally."""

import httpx
import asyncio


async def test_text_message():
    """Test sending a text message webhook."""
    url = "http://localhost:8000/webhook"

    # Sample WhatsApp webhook payload for text message
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15551234567",
                                "phone_number_id": "1006855875841566",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Test User"},
                                    "wa_id": "33612345678",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "33612345678",
                                    "id": "wamid.test123",
                                    "timestamp": "1234567890",
                                    "text": {"body": "Hello Botatouille!"},
                                    "type": "text",
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10.0)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Testing WhatsApp webhook with text message...")
    asyncio.run(test_text_message())

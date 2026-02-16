"""Test webhook locally without WhatsApp."""

import httpx
import asyncio


async def test_webhook_message(message: str):
    """
    Send a test message to the local webhook.

    Args:
        message: Text message to send
    """
    url = "http://localhost:8000/webhook"

    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "33612345678",
                        "id": "test_msg_123",
                        "type": "text",
                        "text": {
                            "body": message
                        }
                    }]
                }
            }]
        }]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            print(f"✅ Message sent: {message}")
            print(f"📨 Response: {response.json()}")
            print("\n⚠️  Check your server logs for the AI response!")
        except httpx.HTTPError as e:
            print(f"❌ Error: {e}")


async def main():
    """Run multiple test messages."""
    test_messages = [
        "Salut! Propose moi un menu pour 2 jours",
        "Je suis végétarien",
        "Donne moi une recette rapide pour ce soir",
    ]

    print("🧪 Testing webhook locally...\n")
    print("Make sure your server is running: uv run python main.py\n")

    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}/{len(test_messages)}")
        print(f"{'='*60}")
        await test_webhook_message(message)
        await asyncio.sleep(2)  # Wait between messages


if __name__ == "__main__":
    asyncio.run(main())

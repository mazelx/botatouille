"""Test script for LLM service."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.llm import llm_service


async def test_basic_conversation():
    """Test basic conversation with LLM."""
    print("Testing LLM service...")

    test_messages = [
        "Hello! Can you help me plan meals?",
        "I need a meal plan for 3 days, vegetarian only",
        "Can you suggest a quick dinner recipe?",
    ]

    for message in test_messages:
        print(f"\n{'='*60}")
        print(f"User: {message}")
        print(f"{'='*60}")

        try:
            response = await llm_service.generate_meal_plan_response(message)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("Starting LLM test...")
    asyncio.run(test_basic_conversation())

# Testing Guide

## LLM Service Testing

### Test LLM service directly

```bash
uv run python tests/test_llm.py
```

This tests the OpenRouter integration without WhatsApp dependency.

Expected output:
- Bot responds to greetings
- Bot generates meal plans based on preferences
- Bot suggests recipes

### Test complete webhook flow

1. Start the server:
```bash
uv run python main.py
```

2. In another terminal, send test webhook:
```bash
uv run python tests/test_webhook.py
```

3. Check logs for LLM response:
```bash
tail -f /tmp/botatouille.log
```

## What Works Now

✅ **LLM Integration**
- OpenRouter API connected
- Claude 3.5 Sonnet model responding
- Context-aware meal planning assistant
- Friendly conversational tone

✅ **Message Processing**
- Receives text messages via webhook
- Sends to LLM for processing
- Generates intelligent responses

⚠️ **WhatsApp Sending**
- Will fail in local testing (expected)
- Requires ngrok + Meta webhook setup for real testing
- 400 error is normal without live WhatsApp connection

## Next Steps for Real WhatsApp Testing

1. **Start server**:
   ```bash
   uv run python main.py
   ```

2. **Start ngrok tunnel**:
   ```bash
   ngrok http 8000
   ```

3. **Configure Meta Webhook**:
   - URL: `https://YOUR-NGROK-URL/webhook`
   - Verify token: from `.env`
   - Subscribe to: `messages`

4. **Send WhatsApp message**:
   - Send to your test number
   - Should receive intelligent AI response

## Example LLM Responses

**User**: "Hello! Can you help me plan meals?"

**Bot**: "Hi there! 👋 I'd love to help you plan your meals!..."

**User**: "I need a meal plan for 3 days, vegetarian only"

**Bot**: "I'll help you create a 3-day vegetarian meal plan! 🌱..."

## Troubleshooting

### LLM test fails
- Check `OPENROUTER_API_KEY` in `.env`
- Verify API key is valid
- Check internet connection

### Webhook test fails
- Ensure server is running on port 8000
- Check if port is already in use: `lsof -i :8000`

### Server won't start
- Check `.env` file exists
- Verify all required variables are set
- Check Python version: `python --version` (should be 3.12+)

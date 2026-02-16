# Setup Guide - Week 1 Foundation

## What's Been Done

### ✅ Completed Tasks

1. **Project Structure**
   - Created FastAPI application with modular structure
   - Set up `uv` for dependency management
   - Organized code into: `api/`, `core/`, `models/`, `services/`

2. **Configuration**
   - Environment variable management with `pydantic-settings`
   - `.env` file for local secrets
   - `.env.example` as template

3. **WhatsApp Webhook**
   - GET endpoint for webhook verification
   - POST endpoint for receiving messages
   - Basic message parsing (text, image)
   - Echo functionality for testing

4. **Dependencies Installed**
   - `fastapi`: Web framework
   - `uvicorn`: ASGI server
   - `python-dotenv`: Environment variables
   - `httpx`: HTTP client for API calls
   - `pydantic-settings`: Settings management

## Next Steps

### 1. Test Locally (Right Now!)

Start the server:
```bash
uv run python main.py
```

In another terminal, test the webhook:
```bash
uv run python test_webhook.py
```

### 2. Setup ngrok for WhatsApp Testing

Install ngrok:
```bash
brew install ngrok  # macOS
```

Start ngrok tunnel:
```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 3. Configure Meta WhatsApp Webhook

Go to: https://developers.facebook.com/apps/

1. Select your app
2. Go to WhatsApp > Configuration
3. Edit webhook URL:
   - Callback URL: `https://YOUR-NGROK-URL.ngrok.io/webhook`
   - Verify token: `your_random_verification_token_here` (from your `.env`)
   - Click "Verify and Save"
4. Subscribe to webhook fields:
   - ✅ messages

### 4. Send a Test Message

From your phone, send a WhatsApp message to your test number.

You should see:
- Logs in your FastAPI console
- An echo response from the bot

## Environment Variables Checklist

Make sure your `.env` file has:

```bash
# ✅ Must have
OPENROUTER_API_KEY=sk-or-v1-...
WHATSAPP_VERIFY_TOKEN=your_random_verification_token_here
WHATSAPP_ACCESS_TOKEN=EAAVCCSmc7ZAgBQld7...
WHATSAPP_PHONE_NUMBER_ID=1006855875841566

# ⚠️ Can wait for later
DATABASE_URL=postgresql://...  # Week 3
```

## Common Issues

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Webhook verification fails
- Check that `WHATSAPP_VERIFY_TOKEN` in `.env` matches what you entered in Meta dashboard
- Make sure ngrok is running and URL is correct

### Message not received
- Check ngrok is still running (tunnels expire after 2h on free tier)
- Check Meta webhook logs: WhatsApp > Configuration > Webhook fields
- Check FastAPI logs for errors

## What's Working

Current functionality:
- ✅ Webhook verification (GET)
- ✅ Receive text messages
- ✅ Receive image messages (ID logged, not processed yet)
- ✅ Send text responses (echo)

## What's Next - Week 1 Remaining

- [ ] Integrate OpenRouter API for LLM conversation
- [ ] Handle basic meal planning requests
- [ ] Deploy to Railway
- [ ] Test with your phone number

## Useful Commands

```bash
# Start server
uv run python main.py

# Test webhook locally
uv run python test_webhook.py

# Check logs
tail -f /tmp/botatouille.log  # if we add file logging

# Start ngrok
ngrok http 8000

# Check running processes
lsof -i :8000
```

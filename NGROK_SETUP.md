# Testing with ngrok + WhatsApp

## Step-by-Step Guide

### 1. Install ngrok

```bash
brew install ngrok
```

Or download from: https://ngrok.com/download

### 2. Setup ngrok account

1. Create free account: https://dashboard.ngrok.com/signup
2. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
3. Configure ngrok:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

### 3. Start the FastAPI server

**Terminal 1** - Run the server:
```bash
./start.sh
# Or: uv run python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 4. Start ngrok tunnel

**Terminal 2** - Run ngrok:
```bash
ngrok http 8000
```

You'll see output like:
```
Forwarding   https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

### 5. Configure Meta WhatsApp Webhook

1. Go to: https://developers.facebook.com/apps/
2. Select your app (or create one if needed)
3. Go to **WhatsApp** > **Configuration**
4. Click **Edit** next to Webhook

**Webhook Configuration:**
- **Callback URL**: `https://YOUR-NGROK-URL.ngrok.io/webhook`
  - Example: `https://abc123.ngrok.io/webhook`
- **Verify Token**: `your_random_verification_token_here`
  - (This is from your `.env` file: `WHATSAPP_VERIFY_TOKEN`)
- Click **Verify and Save**

5. **Subscribe to webhook fields**:
   - ✅ Check `messages`
   - Click **Save**

### 6. Test with WhatsApp

1. From your phone, send a WhatsApp message to your test number
2. Watch the logs in Terminal 1 for:
   ```
   INFO - Received webhook: ...
   INFO - Processing message ...
   INFO - Text message: Hello Botatouille!
   INFO - Sending chat completion request to anthropic/claude-3.5-sonnet
   INFO - Received response: ...
   INFO - Message sent to ...
   ```

3. You should receive an AI response on WhatsApp! 🎉

## Troubleshooting

### Webhook verification fails
- ✅ Check that ngrok is running and URL is correct
- ✅ Verify token in Meta matches `.env` exactly
- ✅ Use HTTPS URL from ngrok (not HTTP)
- ✅ Check FastAPI server is running

### Message not received by bot
- Check ngrok is still running (free tier times out after 2 hours)
- Check Meta webhook logs: WhatsApp > Configuration > Webhook fields
- Look at FastAPI logs for errors

### Bot doesn't respond
- Check OpenRouter API key in `.env`
- Look for LLM errors in logs
- Verify WhatsApp access token is valid

### ngrok URL expired
- Restart ngrok to get new URL
- Update webhook URL in Meta dashboard
- Free tier: URL changes each restart
- Paid tier: Get static URL

## Watch logs in real-time

```bash
# Terminal 1
uv run python main.py

# Terminal 3 (optional)
tail -f /tmp/botatouille.log
```

## Example Conversation Flow

**You**: "Hi!"
**Bot**: "Hi there! 👋 I'm Botatouille, your friendly meal planning buddy!..."

**You**: "I need a meal plan for 3 days, vegetarian"
**Bot**: "I'll help you create a 3-day vegetarian meal plan! 🌱..."

**You**: "Generate shopping list"
**Bot**: "[Shopping list generation]"

## Notes

- ⏱️ Free ngrok tunnels expire after 2 hours
- 🔄 URL changes each time you restart ngrok (unless paid plan)
- 📱 Test number has limits on free Meta tier
- 💬 You can add your personal number for testing in Meta dashboard

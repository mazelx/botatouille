# Quick Start - Test with WhatsApp

## 🚀 Fast Track (5 minutes)

### Step 1: Install ngrok
```bash
brew install ngrok
```

### Step 2: Configure ngrok
```bash
# Get token from: https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_TOKEN
```

### Step 3: Start everything

**Terminal 1** - Server:
```bash
uv run python main.py
```

**Terminal 2** - Ngrok:
```bash
ngrok http 8000
```

Copy the HTTPS URL shown (e.g., `https://abc123.ngrok.io`)

### Step 4: Configure Meta WhatsApp

1. Go to: https://developers.facebook.com/apps/
2. Your App > WhatsApp > Configuration
3. Edit Webhook:
   - URL: `https://YOUR-NGROK-URL.ngrok.io/webhook`
   - Token: `your_random_verification_token_here` (from `.env`)
   - Click "Verify and Save"
4. Subscribe to: `messages`

### Step 5: Test!

Send a WhatsApp message to your test number and get an AI response! 🎉

---

## 📊 Current Status

### ✅ What's Working
- FastAPI server with webhook endpoints
- OpenRouter LLM integration (Claude 3.5 Sonnet)
- Intelligent meal planning conversations
- WhatsApp message handling

### ⏳ Ready to Test
- ngrok tunnel setup
- Meta webhook configuration
- Real WhatsApp messages

### 📝 To Do Later
- Deploy to Railway (permanent URL)
- Add conversation history
- Implement vision features (recipe photos)
- Add database persistence

---

## 🆘 Need Help?

See detailed guides:
- [NGROK_SETUP.md](NGROK_SETUP.md) - Complete ngrok setup guide
- [TESTING.md](TESTING.md) - Testing without WhatsApp
- [SETUP.md](SETUP.md) - Full setup documentation

# Botatouille

WhatsApp conversational agent for meal planning and grocery shopping.

## Setup

### Prerequisites
- Python 3.12+
- `uv` package manager
- Meta WhatsApp Business Account
- OpenRouter API key

### Installation

1. Clone the repository
```bash
git clone <repo-url>
cd botatouille
```

2. Copy environment variables
```bash
cp .env.example .env
```

3. Fill in your `.env` file with your actual credentials:
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `WHATSAPP_VERIFY_TOKEN`: A random token you create for webhook verification
- `WHATSAPP_ACCESS_TOKEN`: Your Meta WhatsApp access token
- `WHATSAPP_PHONE_NUMBER_ID`: Your WhatsApp phone number ID

4. Install dependencies
```bash
uv sync
```

## Running Locally

### Start the FastAPI server

```bash
uv run python main.py
```

The server will start on `http://localhost:8000`

### Test endpoints

- Health check: `http://localhost:8000/health`
- Root: `http://localhost:8000/`
- Webhook (for verification): `http://localhost:8000/webhook`

## Testing with ngrok

To test WhatsApp webhook locally, you need to expose your local server to the internet:

1. Install ngrok: https://ngrok.com/download

2. Start ngrok tunnel:
```bash
ngrok http 8000
```

3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

4. Configure Meta WhatsApp webhook:
   - Go to your Meta App > WhatsApp > Configuration
   - Webhook URL: `https://abc123.ngrok.io/webhook`
   - Verify token: Use the value from `WHATSAPP_VERIFY_TOKEN` in your `.env`
   - Subscribe to webhook fields: `messages`

## Project Structure

```
botatouille/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   └── webhook.py       # WhatsApp webhook endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Settings and configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── whatsapp.py      # WhatsApp data models
│   └── services/
│       └── __init__.py      # Business logic (LLM, etc.)
├── tests/
│   ├── __init__.py
│   └── test_webhook.py      # Test scripts
├── main.py                  # Entry point
├── .env                     # Environment variables (not committed)
├── .env.example             # Template for environment variables
├── pyproject.toml           # uv/Python dependencies
└── README.md
```

## Development

### Week 1 MVP Checklist
- [x] FastAPI project structure with uv
- [x] Environment setup (.env, python-dotenv)
- [x] WhatsApp webhook endpoint (verify + message receive)
- [ ] OpenRouter API integration for basic conversation
- [ ] Handle text messages and simple responses
- [ ] Deploy to Railway
- [ ] Test with single user

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

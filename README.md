# 🤖 Botatouille

WhatsApp AI bot for meal planning and grocery shopping powered by Claude 3.5 Sonnet.

[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-blueviolet)](https://botatouille-production.up.railway.app)
[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129+-green)](https://fastapi.tiangolo.com/)

## ✨ Features

- 🍽️ Generate weekly meal plans
- 🛒 Create shopping lists from meal plans
- 📸 Import recipes from photos (coming soon)
- 💬 Natural language conversations via WhatsApp
- 🧠 Powered by Claude 3.5 Sonnet via OpenRouter

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/mazelx/botatouille.git
cd botatouille

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run locally
uv run python main.py
```

Server runs on `http://localhost:8000`

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide (Railway, ngrok)
- **[TESTING.md](TESTING.md)** - Testing locally without WhatsApp
- **[docs/](docs/)** - Additional documentation and guides
- **[CLAUDE.md](CLAUDE.md)** - Project context and roadmap

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python 3.13
- **LLM**: Claude 3.5 Sonnet (via OpenRouter)
- **Messaging**: Meta WhatsApp Cloud API
- **Deployment**: Railway
- **Package Manager**: uv

## 📦 Project Structure

```
botatouille/
├── app/
│   ├── api/          # API routes (webhook)
│   ├── core/         # Config and constants
│   ├── models/       # Data models
│   └── services/     # Business logic (LLM)
├── tests/            # Test scripts
├── docs/             # Documentation
└── main.py           # Entry point
```

## 🔧 Configuration

Required environment variables:

```bash
OPENROUTER_API_KEY=       # Your OpenRouter API key
WHATSAPP_VERIFY_TOKEN=    # Random token for webhook verification
WHATSAPP_ACCESS_TOKEN=    # Meta WhatsApp access token
WHATSAPP_PHONE_NUMBER_ID= # Your WhatsApp phone number ID
```

See [.env.example](.env.example) for all options.

## 🌐 Live Deployment

The bot is live at: **https://botatouille-production.up.railway.app**

- Status: ✅ Running
- Hosting: Railway
- Auto-deploy: Enabled (on push to main)

## 📝 Development Status

### ✅ Week 1 - MVP Complete
- [x] FastAPI backend
- [x] WhatsApp webhook integration
- [x] LLM conversations (OpenRouter + Claude)
- [x] Deployed to Railway
- [x] Tested with real WhatsApp messages

### 🔮 Roadmap
- [ ] **Week 2**: Vision features (recipe photos, shopping tickets)
- [ ] **Week 3**: Database persistence (PostgreSQL)
- [ ] **Week 4**: Advanced features (shopping lists, tool use)

## 🧪 Testing

```bash
# Test LLM service
uv run python tests/test_llm.py

# Test webhook locally
uv run python tests/test_webhook.py
```

See [TESTING.md](TESTING.md) for details.

## 📊 API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /webhook` - WhatsApp webhook verification
- `POST /webhook` - Receive WhatsApp messages

API docs: `http://localhost:8000/docs`

## 🤝 Contributing

This is a personal project but contributions are welcome!

## 📄 License

MIT

## 🔗 Links

- **GitHub**: https://github.com/mazelx/botatouille
- **Railway**: https://railway.app/project/5f6538c3-0e39-4497-8bcd-71bae59c9a82
- **Meta Dashboard**: https://developers.facebook.com/apps/

---

Made with ❤️ using FastAPI, Claude, and WhatsApp

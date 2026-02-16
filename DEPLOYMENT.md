# Deployment Guide

## Prerequisites

- Python 3.12+
- `uv` package manager
- Meta WhatsApp Business Account
- OpenRouter API key
- Railway account (or ngrok for local testing)

## Local Development

### 1. Setup

```bash
# Clone and setup
git clone https://github.com/mazelx/botatouille.git
cd botatouille

# Copy environment variables
cp .env.example .env

# Edit .env with your credentials
# Add: OPENROUTER_API_KEY, WHATSAPP_*, etc.

# Install dependencies
uv sync
```

### 2. Run Locally

```bash
# Start server
uv run python main.py

# Server runs on http://localhost:8000
```

### 3. Test with ngrok (Optional)

```bash
# Install ngrok
brew install ngrok

# Configure with your token
ngrok config add-authtoken YOUR_TOKEN

# Start tunnel
ngrok http 8000

# Copy HTTPS URL and configure in Meta Dashboard
```

## Production Deployment (Railway)

### 1. Install Railway CLI

```bash
curl -fsSL https://railway.app/install.sh | sh
```

### 2. Login and Initialize

```bash
railway login
railway init
```

### 3. Configure Environment Variables

Via Railway Dashboard (recommended):
1. Go to https://railway.app/dashboard
2. Select your project
3. Click "Variables"
4. Add all variables from `.env`
5. Make sure they are "shared" to your service

Required variables:
- `OPENROUTER_API_KEY`
- `WHATSAPP_VERIFY_TOKEN`
- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `ENVIRONMENT=production`
- `LOG_LEVEL=INFO`

### 4. Deploy

```bash
# Connect to GitHub (automatic deploys on push)
# Or deploy directly:
railway up

# Get your URL
railway domain
```

Your bot will be live at: `https://your-app.railway.app`

### 5. Configure Meta WhatsApp Webhook

1. Go to https://developers.facebook.com/apps/
2. Your App > WhatsApp > Configuration
3. Edit Webhook:
   - **URL**: `https://your-app.railway.app/webhook`
   - **Verify Token**: Value from `WHATSAPP_VERIFY_TOKEN`
   - Click "Verify and Save"
4. Subscribe to webhook field: `messages`

## Updating Your Deployment

### Railway Auto-Deploy (Recommended)

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Railway auto-deploys from GitHub
```

### Manual Deploy

```bash
railway up
```

## Monitoring

### View Logs

```bash
# Real-time logs
railway logs --tail

# Or in Railway Dashboard
railway open
```

### Check Status

```bash
railway status
```

### Health Check

```bash
curl https://your-app.railway.app/health
```

## Troubleshooting

### Deployment Fails
- Check Railway logs: `railway logs`
- Verify all environment variables are set
- Check Railway dashboard for build errors

### Webhook Verification Fails
- Ensure `WHATSAPP_VERIFY_TOKEN` matches in both Railway and Meta
- Check URL ends with `/webhook`
- Verify Railway service is running

### Bot Doesn't Respond
- Check Railway logs for errors
- Verify `WHATSAPP_ACCESS_TOKEN` is valid (regenerate if expired)
- Test OpenRouter API key
- Ensure webhook subscription includes `messages`

### 401 Unauthorized
- WhatsApp access token expired
- Regenerate token in Meta Dashboard
- Update `WHATSAPP_ACCESS_TOKEN` in Railway variables

## Cost Estimation

### Railway
- **Free tier**: $5 credits/month
- **Estimated usage**: $2-3/month
- Monitor usage in Railway dashboard

### OpenRouter
- Pay-as-you-go per API call
- Claude 3.5 Sonnet: ~$3 per 1M input tokens
- Estimated: $1-5/month depending on usage

## Production Checklist

- [ ] All environment variables configured
- [ ] Railway deployment successful
- [ ] Meta webhook verified
- [ ] Test message sent and received
- [ ] Logs monitored for errors
- [ ] GitHub auto-deploy configured

## Links

- **Live Bot**: https://botatouille-production.up.railway.app
- **GitHub**: https://github.com/mazelx/botatouille
- **Railway Dashboard**: https://railway.app/dashboard
- **Meta Dashboard**: https://developers.facebook.com/apps/

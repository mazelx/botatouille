# Railway Deployment Guide

## Prerequisites

1. **Railway Account** (free)
   - Sign up at: https://railway.app/
   - Login with GitHub (recommended)

2. **Railway CLI**
   ```bash
   # Install via curl
   curl -fsSL https://railway.app/install.sh | sh

   # Or via npm
   npm i -g @railway/cli
   ```

## Deployment Steps

### 1. Login to Railway

```bash
railway login
```

This will open your browser to authenticate.

### 2. Initialize Railway Project

```bash
railway init
```

- Choose: "Create a new project"
- Name: `botatouille` (or your choice)
- Choose: "Empty project"

### 3. Link to Railway Project

```bash
railway link
```

Select your newly created project.

### 4. Add Environment Variables

You can add them via CLI or Web Dashboard (easier):

**Option A: Web Dashboard** (Recommended)
1. Go to: https://railway.app/dashboard
2. Select your project
3. Click "Variables"
4. Add all variables from your `.env`:

```
OPENROUTER_API_KEY=sk-or-v1-...
WHATSAPP_VERIFY_TOKEN=vNm-YjD7EmJgOGFayg0hZcJfctgyTJIEH9yN4kvLcLU
WHATSAPP_ACCESS_TOKEN=EAAVCCSmc7ZAgBQld7...
WHATSAPP_PHONE_NUMBER_ID=1006855875841566
DATABASE_URL=postgresql://...
ENVIRONMENT=production
LOG_LEVEL=INFO
OPENROUTER_APP_NAME=Botatouille
OPENROUTER_SITE_URL=https://botatouille.railway.app
```

**Option B: CLI**
```bash
railway variables set OPENROUTER_API_KEY=sk-or-v1-...
railway variables set WHATSAPP_VERIFY_TOKEN=vNm-YjD7EmJgOGFayg0hZcJfctgyTJIEH9yN4kvLcLU
# ... etc
```

### 5. Deploy!

```bash
railway up
```

This will:
- Build your app
- Deploy to Railway
- Give you a public URL

### 6. Get Your Railway URL

```bash
railway domain
```

Or in the Railway dashboard, you'll see your deployment URL (e.g., `botatouille.railway.app`)

### 7. Update Meta WhatsApp Webhook

1. Go to: https://developers.facebook.com/apps/
2. Your App > WhatsApp > Configuration
3. Edit Webhook:
   - URL: `https://YOUR-APP.railway.app/webhook`
   - Token: `vNm-YjD7EmJgOGFayg0hZcJfctgyTJIEH9yN4kvLcLU`
   - Click "Verify and Save"

### 8. Test!

Send a WhatsApp message to your bot - it should work! 🎉

## Monitoring

### View Logs
```bash
railway logs
```

### Check Deployment Status
```bash
railway status
```

### Open in Browser
```bash
railway open
```

## Troubleshooting

### Deployment fails
- Check logs: `railway logs`
- Verify all environment variables are set
- Check Railway dashboard for build errors

### Webhook verification fails
- Ensure `WHATSAPP_VERIFY_TOKEN` matches in both Railway and Meta
- Check logs for verification attempts

### Bot doesn't respond
- Check Railway logs for errors
- Verify OpenRouter API key is valid
- Test health endpoint: `https://YOUR-APP.railway.app/health`

## Updating Your Bot

After making changes to your code:

```bash
git add .
git commit -m "Update bot features"
git push

# Railway auto-deploys from GitHub
# Or manually deploy:
railway up
```

## Cost Estimation

- **Estimated cost**: $2-3/month
- **$5 free credits** included in trial
- Monitor usage in Railway dashboard

## Useful Commands

```bash
railway login          # Login to Railway
railway init           # Create new project
railway link           # Link to existing project
railway up             # Deploy current directory
railway logs           # View application logs
railway logs --tail    # Stream logs in real-time
railway status         # Check deployment status
railway variables      # List environment variables
railway open           # Open project in browser
railway domain         # Get your app URL
```

## Files Added for Railway

- `railway.json` - Railway configuration
- `Procfile` - Process definition
- `runtime.txt` - Python version
- `pyproject.toml` - Already exists (uv dependencies)

## Next Steps After Deployment

1. ✅ Bot is live 24/7
2. ✅ No more ngrok needed
3. ✅ Permanent URL
4. 🎯 Move to Week 2 features!

# 🚀 Inkel AI Tourism Assistant - Deployment Guide

## Quick Deploy Options

### Option 1: Render.com (Recommended - Free)

1. **Go to**: https://render.com
2. **Sign up** with GitHub account
3. **New Web Service** → Connect GitHub → Select `Inkel_AI_Project`
4. **Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python api/main.py`
   - Environment: `Python 3`
   - Plan: `Free`
5. **Deploy** → Get live URL like: `https://inkel-tourism-api.onrender.com`

### Option 2: Railway.app (Alternative - Free)

1. **Go to**: https://railway.app
2. **Deploy from GitHub** → Connect repository
3. **Auto-detects** Python and deploys automatically
4. **Get URL**: `https://your-app.railway.app`

### Option 3: Vercel (Frontend Only)

1. **Go to**: https://vercel.com
2. **Import** from GitHub → Select repository
3. **Framework Preset**: Other
4. **Build Command**: Leave empty (static files)
5. **Get URL**: `https://your-app.vercel.app`

## Environment Configuration

The app is configured to work with these environment variables:
- `PORT`: Server port (auto-set by hosting platforms)
- `HOST`: Server host (defaults to 0.0.0.0)

## Live Demo URLs (After Deployment)

- **Backend API**: `https://your-app.onrender.com`
- **API Documentation**: `https://your-app.onrender.com/docs`
- **Health Check**: `https://your-app.onrender.com/health`

## Testing Your Deployment

Once deployed, test with:
```bash
# Health check
curl https://your-deployed-url.com/health

# Sample query
curl -X POST https://your-deployed-url.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Mumbai tourist places"}'
```

## Quick Deploy Commands

```bash
# Commit deployment files
git add .
git commit -m "Add deployment configuration"
git push origin main

# Then deploy via web interface on chosen platform
```

## Cost: FREE ✅

All recommended platforms offer free tiers perfect for this assignment:
- **Render**: 750 hours/month free
- **Railway**: $5 free credit monthly
- **Vercel**: Unlimited for personal projects
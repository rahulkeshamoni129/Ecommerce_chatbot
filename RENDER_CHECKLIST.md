# 🚀 Render Deployment Checklist

## ✅ Pre-Deployment (All Done!)

- [x] **Procfile** - Configured with `gunicorn app:app`
- [x] **requirements.txt** - All dependencies listed
- [x] **runtime.txt** - Python 3.12.0 specified
- [x] **build.sh** - Build script created
- [x] **render.yaml** - Infrastructure as code config
- [x] **.gitignore** - Excludes unnecessary files
- [x] **app.py** - Uses environment variables for PORT and HOST
- [x] **README.md** - Updated with deployment instructions
- [x] **MongoDB removed** - No database dependencies
- [x] **Model files included** - sklearn_pipeline.pkl ready

## 📋 Deployment Steps

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Render deployment - 81.05% accuracy chatbot"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-chatbot.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render

#### Option A: Blueprint (Recommended)
1. Go to https://dashboard.render.com/
2. Click **"New"** → **"Blueprint"**
3. Connect GitHub repository
4. Render detects `render.yaml` automatically
5. Click **"Apply"**
6. Wait 2-5 minutes for deployment

#### Option B: Manual
1. Go to https://dashboard.render.com/
2. Click **"New"** → **"Web Service"**
3. Connect GitHub repository
4. Settings:
   - **Name**: ecommerce-chatbot
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
5. Click **"Create Web Service"**

### 3. Verify Deployment

Once deployed:
- URL: `https://your-app-name.onrender.com`
- Test homepage: Visit URL in browser
- Test API:
  ```bash
  curl -X POST https://your-app-name.onrender.com/chat \
    -H "Content-Type: application/json" \
    -d '{"message":"hello"}'
  ```

## 🎯 What Gets Deployed

✅ **Full-featured chatbot with:**
- 81.05% accuracy Linear SVM model
- 948 training patterns across 21 intents
- Chat UI at homepage
- Order tracking (5 mock orders)
- All intents working (greetings, products, shipping, etc.)

## 📊 Expected Performance

- **Build Time**: 1-3 minutes
- **Cold Start**: 10-15 seconds (free tier)
- **Warm Response**: 100-500ms
- **Memory Usage**: 200-300MB
- **Free Tier**: 750 hours/month

## 🔧 Post-Deployment

### Monitor Logs
```
Render Dashboard → Your Service → Logs
```

### Update Deployment
```bash
git add .
git commit -m "Updated chatbot"
git push
# Render auto-deploys!
```

### Custom Domain (Optional)
```
Render Dashboard → Your Service → Settings → Custom Domains
```

## 🐛 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Verify all files committed: `git status`
- Check `build.sh` permissions

### App Won't Start
- Check start command: `gunicorn app:app`
- Verify `gunicorn` in requirements.txt
- Check Python version in runtime.txt

### Slow First Request
- Normal on free tier (spins down after 15min)
- Consider upgrading to paid tier

## 📝 Environment Variables (Optional)

If needed, add in Render dashboard:
- `FLASK_DEBUG` = False (for production)
- Custom variables for your app

## ✨ You're Ready!

Your chatbot is **100% ready** for Render deployment!

Just push to GitHub and deploy! 🚀

---

**Need help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide.

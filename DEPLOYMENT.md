# Deployment Guide for Render

## 🚀 Quick Deploy to Render

### Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)

### Step 1: Push to GitHub

1. **Initialize Git (if not already done)**
   ```bash
   git init
   git add .
   git commit -m "Ready for Render deployment"
   ```

2. **Create GitHub repository and push**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ecommerce-chatbot.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

#### Option A: Using render.yaml (Recommended - Infrastructure as Code)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"** to deploy

#### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ecommerce-chatbot`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

5. **Environment Variables** (Optional):
   - Add any custom variables if needed
   - Render auto-sets `PORT` variable

6. Click **"Create Web Service"**

### Step 3: Access Your Chatbot

After deployment (takes 2-5 minutes):
- Your chatbot will be live at: `https://your-app-name.onrender.com`
- Test it: `https://your-app-name.onrender.com`

## 📁 Files Required for Deployment

✅ All files are already configured in your project:

| File | Purpose | Status |
|------|---------|--------|
| `Procfile` | Tells Render how to run the app | ✅ Ready |
| `requirements.txt` | Python dependencies | ✅ Ready |
| `runtime.txt` | Python version | ✅ Ready |
| `build.sh` | Build script | ✅ Ready |
| `render.yaml` | Infrastructure config (optional) | ✅ Ready |
| `app.py` | Main application | ✅ Ready |

## 🔧 Configuration Details

### Procfile
```
web: gunicorn app:app
```
Uses Gunicorn (production WSGI server) instead of Flask dev server.

### requirements.txt
```
Flask>=2.0
flask-cors
numpy
scikit-learn
gunicorn
python-dotenv
```

### runtime.txt
```
python-3.12.0
```

### build.sh
```bash
#!/usr/bin/env bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🎯 Features Deployed

Your deployed chatbot includes:
- ✅ **81.05% accuracy** Linear SVM model
- ✅ **948 training patterns** across 21 intents
- ✅ **Mock order tracking** (ORD100-ORD104)
- ✅ **No database required** (uses mock data)
- ✅ **Fast startup** (no MongoDB connection)
- ✅ **Production-ready** with Gunicorn

## 📊 Performance on Render Free Tier

- **Cold Start**: ~10-15 seconds (first request after inactivity)
- **Warm Response**: ~100-500ms per request
- **Memory Usage**: ~200-300MB
- **Free Tier Limits**: 
  - 750 hours/month
  - Spins down after 15 min inactivity
  - Automatic spin-up on request

## 🔍 Monitoring & Logs

1. **View Logs**: Render Dashboard → Your Service → Logs
2. **Check Health**: Visit `https://your-app.onrender.com/`
3. **Test Chat**: Visit `https://your-app.onrender.com/` (web UI)

## 🐛 Troubleshooting

### Build Fails
- Check logs in Render dashboard
- Verify all files are committed to Git
- Ensure `build.sh` has correct permissions

### App Won't Start
- Check that `Procfile` is present
- Verify `gunicorn` is in `requirements.txt`
- Check logs for Python errors

### Slow Response
- Free tier spins down after inactivity (normal)
- Upgrade to paid tier for always-on service
- First request may take 10-15 seconds

## 🎨 Custom Domain (Optional)

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Configure DNS (CNAME or A record)

## 💡 Tips for Production

1. **Monitor Usage**: Check Render dashboard for metrics
2. **Update Model**: Push to GitHub, Render auto-deploys
3. **Scale Up**: Upgrade instance for better performance
4. **Add Caching**: Implement Redis for faster responses
5. **Error Tracking**: Add Sentry or similar service

## 🔄 Update Deployment

To update your chatbot:
```bash
git add .
git commit -m "Updated chatbot"
git push
```
Render will automatically redeploy! 🚀

## 📱 Test Your Deployment

Once deployed, test with curl:
```bash
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```

Or visit the web UI directly in your browser!

## ✨ You're Ready!

Your e-commerce chatbot is production-ready and can be deployed to Render in minutes!

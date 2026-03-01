# Deployment Guide for GitHub Webhook System

## Overview
This guide walks you through deploying your webhook receiver to a cloud platform so it can receive GitHub webhooks.

## Why Deploy?
GitHub webhooks require a **publicly accessible URL** (https). Local development with `localhost` won't work unless you use a tunneling service like ngrok.

---

## Option 1: Railway (Recommended - Easiest)

### Why Railway?
- ✅ Free MongoDB included
- ✅ Automatic HTTPS
- ✅ GitHub integration
- ✅ Easy environment variables
- ✅ Auto-deploys on git push

### Steps:

1. **Sign up at Railway**
   - Go to https://railway.app
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `webhook-repo` repository

3. **Add MongoDB Database**
   - In your project, click "New"
   - Select "Database" → "Add MongoDB"
   - Railway will automatically create a MongoDB instance

4. **Configure Environment Variables**
   - Click on your web service
   - Go to "Variables" tab
   - Add these variables:
     ```
     MONGODB_URI=${{MongoDB.MONGO_URL}}
     DATABASE_NAME=github_events_db
     SECRET_KEY=your-random-secret-key-here
     DEBUG=False
     ```
   - Railway automatically injects MongoDB connection string

5. **Deploy**
   - Railway will automatically deploy
   - Click on "Settings" to find your public URL
   - Copy the URL (e.g., `https://your-app.railway.app`)

6. **Test Your Deployment**
   - Visit `https://your-app.railway.app`
   - You should see the UI!

---

## Option 2: Render

### Why Render?
- ✅ Free tier available
- ✅ Easy setup
- ✅ Good documentation

### Steps:

1. **Sign up at Render**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your `webhook-repo` repository
   - Configure:
     - **Name**: webhook-receiver
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

3. **Add MongoDB**
   - Sign up for MongoDB Atlas (free): https://www.mongodb.com/cloud/atlas
   - Create a free cluster
   - Get connection string
   - Add to Render environment variables

4. **Set Environment Variables**
   In Render dashboard, add:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=github_events_db
   SECRET_KEY=your-secret-key
   DEBUG=False
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Copy your app URL

---

## Option 3: Heroku

### Why Heroku?
- ✅ Well-documented
- ✅ CLI tools
- ✅ Many addons

**Note**: Heroku ended free tier in November 2022. You'll need a paid plan.

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Mac
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-webhook-receiver
   ```

3. **Add MongoDB Addon**
   ```bash
   heroku addons:create mongolab:sandbox
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **View Your App**
   ```bash
   heroku open
   ```

---

## Option 4: Local Testing with ngrok (Development Only)

### Why ngrok?
- ✅ Perfect for testing
- ✅ No deployment needed
- ✅ Quick setup

### Steps:

1. **Install ngrok**
   - Go to https://ngrok.com
   - Sign up and download
   - Unzip and place in PATH

2. **Start Your Flask App**
   ```bash
   python app.py
   ```

3. **Start ngrok**
   ```bash
   ngrok http 5000
   ```

4. **Copy Public URL**
   - ngrok will show a URL like `https://abc123.ngrok.io`
   - Use this as your webhook URL
   - **Note**: URL changes every time you restart ngrok (unless you have paid plan)

---

## After Deployment: Configure GitHub Webhook

### For action-repo:

1. **Go to Repository Settings**
   - Navigate to your `action-repo` on GitHub
   - Click "Settings" → "Webhooks" → "Add webhook"

2. **Configure Webhook**
   - **Payload URL**: `https://your-deployed-url.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: (optional)
   - **SSL verification**: Enable
   - **Events to trigger**:
     - ✅ Pushes
     - ✅ Pull requests
   - Click "Add webhook"

3. **Test Webhook**
   - Make a commit to action-repo:
     ```bash
     echo "test" > test.txt
     git add test.txt
     git commit -m "Test webhook"
     git push origin main
     ```
   - Check your webhook receiver UI
   - Should see the push event!

4. **Verify in GitHub**
   - Go back to webhook settings
   - Click on the webhook
   - Check "Recent Deliveries"
   - Should see green checkmarks ✅

---

## Troubleshooting Deployments

### Deployment Failed

**Check build logs:**
- Railway: Click on deployment → View logs
- Render: Check "Events" tab
- Heroku: `heroku logs --tail`

**Common issues:**
- Missing dependencies in requirements.txt
- Wrong Python version
- MongoDB connection issues

### Webhook Not Receiving Events

1. **Check webhook delivery status in GitHub**
   - Go to webhook settings
   - Click "Recent Deliveries"
   - Look for error messages

2. **Test webhook endpoint manually**
   ```bash
   curl -X POST https://your-app.com/webhook \
     -H "Content-Type: application/json" \
     -H "X-GitHub-Event: push" \
     -d '{"pusher":{"name":"Test"},"ref":"refs/heads/main"}'
   ```

3. **Check application logs**
   - Railway: Deployment → Logs
   - Render: Logs tab
   - Heroku: `heroku logs --tail`

### MongoDB Connection Issues

**Error: "Cannot connect to MongoDB"**

Solutions:
1. Check MONGODB_URI is correctly set
2. For MongoDB Atlas:
   - Whitelist IP addresses (0.0.0.0/0 for all)
   - Check username/password
   - Ensure database user has read/write permissions

3. Test connection:
   ```python
   from pymongo import MongoClient
   client = MongoClient(your_uri)
   client.list_database_names()
   ```

### App Running But UI Not Loading

1. Check if root route is working: `https://your-app.com/health`
2. Check static files are being served correctly
3. Look for JavaScript errors in browser console (F12)

---

## Performance Tips

1. **Add database indexes** (already done in app.py):
   ```python
   events_collection.create_index([('timestamp', DESCENDING)])
   ```

2. **Limit query results**:
   - Already limited to 10 events
   - Adjust in app.py if needed

3. **Enable caching** for static files:
   - Most platforms do this automatically

4. **Monitor your app**:
   - Railway: Built-in metrics
   - Heroku: Use monitoring addons
   - Render: Check metrics tab

---

## Security Best Practices

1. **Use webhook secrets**:
   - Add secret in GitHub webhook settings
   - Verify signature in Flask app

2. **Environment variables**:
   - Never commit .env file
   - Use platform's secret management

3. **HTTPS only**:
   - All platforms provide HTTPS by default
   - Never use HTTP for webhooks

4. **Rate limiting**:
   - Consider adding rate limiting for webhook endpoint
   - Use Flask-Limiter if needed

---

## Cost Estimates

| Platform | Free Tier | Pro Tier |
|----------|-----------|----------|
| Railway | $5 credit/month | Pay as you go (~$5-10/month) |
| Render | 750 hours/month | $7/month |
| Heroku | No free tier | $7/month eco dyno |
| ngrok | 8 hours/session | $8/month for persistent URL |

**Recommendation**: Start with Railway's free tier for testing and development.

---

## Submission Checklist

Before submitting your assignment, ensure:

- [ ] webhook-repo is deployed and accessible via HTTPS
- [ ] action-repo exists with webhook configured
- [ ] Push events are being captured and displayed
- [ ] Pull request events work correctly
- [ ] Merge events work correctly
- [ ] UI updates every 15 seconds
- [ ] Both repositories have good README files
- [ ] .env file is NOT committed to Git
- [ ] All sensitive data is in environment variables

---

## Support Resources

- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **MongoDB Atlas**: https://www.mongodb.com/docs/atlas/
- **GitHub Webhooks**: https://docs.github.com/webhooks
- **Flask Documentation**: https://flask.palletsprojects.com/

---

Good luck with your deployment! 🚀

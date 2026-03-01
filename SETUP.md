# Quick Setup Guide

## For Windows Users

### 1. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Install MongoDB
Download from: https://www.mongodb.com/try/download/community

Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

### 3. Configure Environment
```powershell
Copy-Item .env.example .env
# Edit .env with your settings
```

### 4. Run the Application
```powershell
python app.py
```

### 5. Test the Application
Open another terminal and run:
```powershell
python test_webhook.py
```

### 6. View the UI
Open your browser and go to: http://localhost:5000

## For Mac/Linux Users

### 1. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Install MongoDB
```bash
# Mac (using Homebrew)
brew tap mongodb/brew
brew install mongodb-community

# Ubuntu/Debian
sudo apt-get install mongodb

# Start MongoDB
brew services start mongodb-community  # Mac
sudo systemctl start mongod            # Linux
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

### 4. Run the Application
```bash
python3 app.py
```

### 5. Test the Application
```bash
python3 test_webhook.py
```

### 6. View the UI
Open your browser: http://localhost:5000

## Quick Testing with ngrok

To test with actual GitHub webhooks locally:

1. Install ngrok: https://ngrok.com/download
2. Start your Flask app: `python app.py`
3. In another terminal: `ngrok http 5000`
4. Copy the ngrok URL (https://xxxxx.ngrok.io)
5. Use this URL in GitHub webhook settings

## Deployment Options

### Heroku (Free Tier Available)
```bash
heroku login
heroku create your-app-name
heroku addons:create mongolab:sandbox
git push heroku main
```

### Railway (Recommended)
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select webhook-repo
5. Add MongoDB plugin
6. Deploy!

## Common Issues

### Port Already in Use
Change PORT in .env file to a different number (e.g., 8000)

### MongoDB Connection Error
- Make sure MongoDB is running
- Check your MONGODB_URI in .env file
- Test connection: `mongosh` or `mongo`

### Webhook Not Receiving Events
- Use ngrok or deploy to a public server
- GitHub webhooks need a public URL
- Check webhook logs in GitHub Settings

## Need Help?

Check the full README.md for detailed instructions!

# GitHub Webhook Receiver (webhook-repo)

A Flask-based webhook receiver that captures GitHub events (Push, Pull Request, Merge) and displays them in a real-time UI with MongoDB storage.

## 🎯 Features

- **Webhook Integration**: Receives GitHub webhook events automatically
- **Event Tracking**: Monitors Push, Pull Request, and Merge actions
- **Real-time UI**: Auto-refreshes every 15 seconds to display latest events
- **MongoDB Storage**: Persists all events with proper schema
- **Clean Interface**: Minimal, modern UI with color-coded event types

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- MongoDB (local or cloud instance like MongoDB Atlas)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-webhook-repo-url>
cd webhook-repo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=github_events_db
SECRET_KEY=your-secret-key-here
DEBUG=True
PORT=5000
```

**For MongoDB Atlas:**
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
```

### 4. Start MongoDB (if running locally)

```bash
# For Windows
mongod

# For Linux/Mac
sudo systemctl start mongod
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🌐 Deployment

### Deploy to Cloud (Recommended for GitHub Webhooks)

Since GitHub webhooks require a public URL, you need to deploy to a cloud platform:

#### Option 1: Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Deploy
git push heroku main
```

#### Option 2: Railway

1. Visit [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your webhook-repo
4. Add MongoDB plugin
5. Set environment variables in Railway dashboard

#### Option 3: Render

1. Visit [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Add MongoDB connection string in environment variables

### For Local Testing (using ngrok)

```bash
# Install ngrok
# Visit https://ngrok.com and sign up

# Start your Flask app
python app.py

# In another terminal, expose local server
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) for webhook configuration.

## 🔧 GitHub Webhook Configuration

### 1. Create the action-repo Repository

1. Go to GitHub and create a new repository named `action-repo`
2. Push some initial content (README, code files, etc.)

### 2. Configure Webhook

1. Go to your `action-repo` repository on GitHub
2. Click **Settings** → **Webhooks** → **Add webhook**
3. Configure webhook:
   - **Payload URL**: `https://your-deployment-url.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: (optional, but recommended)
   - **Events**: Select individual events:
     - ✅ Pushes
     - ✅ Pull requests
4. Click **Add webhook**

### 3. Test the Integration

1. Make a commit and push to `action-repo`:
   ```bash
   git add .
   git commit -m "Test webhook"
   git push origin main
   ```

2. Check your webhook-repo UI at `https://your-deployment-url.com`
3. You should see the push event displayed!

## 📊 MongoDB Schema

Events are stored in MongoDB with the following schema:

```javascript
{
  "author": "string",          // GitHub username
  "action": "string",          // PUSH, PULL_REQUEST, or MERGE
  "to_branch": "string",       // Target branch
  "from_branch": "string",     // Source branch (null for PUSH)
  "timestamp": "ISODate"       // UTC timestamp
}
```

## 🎨 UI Display Formats

The UI displays events in the following formats:

**PUSH:**
```
Travis pushed to staging on 1st April 2021 - 9:30 PM UTC
```

**PULL_REQUEST:**
```
Travis submitted a pull request from staging to master on 1st April 2021 - 9:00 AM UTC
```

**MERGE:**
```
Travis merged branch dev to master on 2nd April 2021 - 12:00 PM UTC
```

## 📁 Project Structure

```
webhook-repo/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── README.md             # This file
├── static/
│   └── css/
│       └── style.css     # UI styling
└── templates/
    └── index.html        # Main UI template
```

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main UI page |
| `/webhook` | POST | GitHub webhook receiver |
| `/api/events` | GET | Fetch latest events (JSON) |
| `/health` | GET | Health check endpoint |

## 🧪 Testing

### Test Webhook Locally

You can test the webhook endpoint using curl:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d '{
    "pusher": {"name": "TestUser"},
    "ref": "refs/heads/main"
  }'
```

### Test Pull Request Event

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -d '{
    "action": "opened",
    "pull_request": {
      "user": {"login": "TestUser"},
      "head": {"ref": "feature-branch"},
      "base": {"ref": "main"}
    }
  }'
```

### Test Merge Event

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: pull_request" \
  -d '{
    "action": "closed",
    "pull_request": {
      "merged": true,
      "user": {"login": "TestUser"},
      "head": {"ref": "feature-branch"},
      "base": {"ref": "main"}
    }
  }'
```

## 🐛 Troubleshooting

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
mongosh

# Or for older versions
mongo
```

### Port Already in Use

```bash
# Change PORT in .env file
PORT=8000
```

### Webhook Not Receiving Events

1. Check webhook URL is publicly accessible
2. Verify webhook configuration in GitHub
3. Check Recent Deliveries in GitHub webhook settings
4. Review application logs for errors

## 📝 Additional Notes

- The UI polls the database every 15 seconds for new events
- Events are displayed in reverse chronological order (newest first)
- The application stores the last 10 events by default (configurable)
- All timestamps are stored and displayed in UTC

## 🤝 Submission

For assignment submission, provide:
1. Link to `action-repo` (repository being monitored)
2. Link to `webhook-repo` (this repository)
3. Deployed application URL (if applicable)

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created as part of the GitHub Webhook Integration Assessment Task.

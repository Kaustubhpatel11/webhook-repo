# Sample action-repo Structure
# This is a reference for what to create in your action-repo

## Directory Structure

```
action-repo/
├── README.md
├── .gitignore
├── src/
│   ├── index.js
│   ├── app.py
│   └── utils.js
├── tests/
│   └── test_sample.js
└── docs/
    └── setup.md
```

## File: README.md

```markdown
# action-repo

This repository is monitored by GitHub webhooks. All pushes, pull requests, and merges trigger events that are captured by the webhook receiver.

## Purpose
Demonstration repository for GitHub webhook integration assignment.

## Webhook Events Tracked
- Push events
- Pull request events  
- Merge events

## Setup
See the webhook-repo for complete system documentation.
```

## File: .gitignore

```
node_modules/
*.pyc
__pycache__/
.env
.DS_Store
```

## File: src/index.js

```javascript
// Simple Node.js application
console.log('Hello from action-repo!');

function greet(name) {
    return `Hello, ${name}!`;
}

function calculate(a, b) {
    return a + b;
}

module.exports = { greet, calculate };
```

## File: src/app.py

```python
# Simple Python application
def main():
    print("Hello from action-repo!")

def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    main()
```

## Creating the Repository

### Step 1: Create on GitHub
1. Go to GitHub
2. Click "New repository"
3. Name: `action-repo`
4. Make it public
5. Do NOT initialize with README (we'll add it)
6. Click "Create repository"

### Step 2: Clone and Setup Locally

```bash
git clone https://github.com/yourusername/action-repo.git
cd action-repo
```

### Step 3: Add Files

```bash
# Create directory structure
mkdir src tests docs

# Create README
cat > README.md << 'EOF'
# action-repo

This repository is monitored by GitHub webhooks.

## Events Tracked
- Push
- Pull Request
- Merge
EOF

# Create sample code
cat > src/index.js << 'EOF'
console.log('Hello from action-repo!');

function greet(name) {
    return `Hello, ${name}!`;
}

module.exports = { greet };
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules/
*.pyc
__pycache__/
.env
EOF

# Commit and push
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 4: Configure Webhook

1. Go to repository Settings
2. Click "Webhooks" → "Add webhook"
3. Configure:
   - **Payload URL**: Your deployed webhook-repo URL + `/webhook`
     - Example: `https://your-app.railway.app/webhook`
   - **Content type**: `application/json`
   - **Events**: Select "Let me select individual events"
     - ✅ Pushes
     - ✅ Pull requests
4. Click "Add webhook"

### Step 5: Test Push Event

```bash
echo "# Test change" >> README.md
git add README.md
git commit -m "Test push event"
git push origin main
```

Check your webhook-repo UI - you should see the push event!

### Step 6: Test Pull Request

```bash
# Create feature branch
git checkout -b feature-test

# Make changes
echo "console.log('New feature');" > src/feature.js
git add src/feature.js
git commit -m "Add new feature"

# Push branch
git push origin feature-test
```

Go to GitHub and create a pull request.

### Step 7: Test Merge

1. On GitHub, go to the pull request
2. Click "Merge pull request"
3. Confirm merge
4. Check webhook-repo UI for merge event!

## Alternative: Quick Setup Script

### For Bash/Mac/Linux:

```bash
#!/bin/bash
# setup-action-repo.sh

REPO_NAME="action-repo"

# Create directory structure
mkdir -p src tests docs

# Create README
echo "# $REPO_NAME" > README.md
echo "" >> README.md
echo "Monitored by GitHub webhooks." >> README.md

# Create sample code
cat > src/index.js << 'EOF'
console.log('Hello from action-repo!');
EOF

cat > src/app.py << 'EOF'
def main():
    print("Hello from action-repo!")

if __name__ == "__main__":
    main()
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules/
*.pyc
__pycache__/
.env
.DS_Store
EOF

# Initialize git
git init
git add .
git commit -m "Initial commit"

echo ""
echo "Repository initialized!"
echo "Next steps:"
echo "1. Create repository on GitHub: $REPO_NAME"
echo "2. Add remote: git remote add origin https://github.com/yourusername/$REPO_NAME.git"
echo "3. Push: git push -u origin main"
echo "4. Configure webhook in repository settings"
```

### For PowerShell/Windows:

```powershell
# setup-action-repo.ps1

$repoName = "action-repo"

# Create directory structure
New-Item -ItemType Directory -Force -Path src, tests, docs

# Create README
@"
# $repoName

Monitored by GitHub webhooks.
"@ | Out-File README.md

# Create sample code
@"
console.log('Hello from action-repo!');
"@ | Out-File src/index.js

@"
def main():
    print("Hello from action-repo!")

if __name__ == "__main__":
    main()
"@ | Out-File src/app.py

# Create .gitignore
@"
node_modules/
*.pyc
__pycache__/
.env
.DS_Store
"@ | Out-File .gitignore

# Initialize git
git init
git add .
git commit -m "Initial commit"

Write-Host ""
Write-Host "Repository initialized!"
Write-Host "Next steps:"
Write-Host "1. Create repository on GitHub: $repoName"
Write-Host "2. Add remote: git remote add origin https://github.com/yourusername/$repoName.git"
Write-Host "3. Push: git push -u origin main"
Write-Host "4. Configure webhook in repository settings"
```

## Webhook Configuration Details

### Payload URL Format
```
https://your-deployment.com/webhook
```

**Examples:**
- Railway: `https://your-app.railway.app/webhook`
- Render: `https://your-app.onrender.com/webhook`
- ngrok: `https://abc123.ngrok.io/webhook`

### Required Settings
- **Content type**: `application/json` (Required)
- **SSL verification**: Enabled (Recommended)
- **Events**:
  - Pushes ✅
  - Pull requests ✅

### Optional Settings
- **Secret**: Add for additional security
- **Active**: Must be checked

## Testing Your Setup

### 1. Verify Webhook Added
- Go to Settings → Webhooks
- Should see your webhook listed
- Check that it has a green checkmark

### 2. Test Push
```bash
git commit --allow-empty -m "Test webhook"
git push
```

### 3. View Delivery
- Click on webhook in settings
- Click "Recent Deliveries"
- Should see delivery with Response code 200

### 4. Check UI
- Go to your webhook-repo app URL
- Should see the event displayed!

## Troubleshooting

### Webhook Shows Red X
- Check webhook URL is correct
- Verify app is deployed and running
- Test webhook endpoint: `curl https://your-app.com/webhook`

### No Events in UI
- Check MongoDB is connected
- Verify webhook is active
- Check app logs for errors
- Test /api/events endpoint

### Webhook Timing Out
- Check app is responding quickly
- Verify MongoDB connection is fast
- Check app isn't sleeping (some free tiers sleep)

## What to Include in action-repo

At minimum:
- ✅ README.md with description
- ✅ .gitignore file
- ✅ Some code files (any language)
- ✅ At least one commit
- ✅ Webhook configured

Optional extras:
- Multiple branches
- Real application code
- Tests
- Documentation
- CI/CD configuration

## Sample Commits for Testing

```bash
# Test push
echo "test" >> README.md
git commit -am "docs: update README"
git push

# Test feature branch
git checkout -b feature/new-ui
echo "// New UI code" > src/ui.js
git add src/ui.js
git commit -m "feat: add new UI component"
git push origin feature/new-ui

# Create PR on GitHub

# Merge PR on GitHub
```

## Expected Results

After setup, your webhook-repo UI should show:
1. Initial push commit
2. Feature branch push (if tracked)
3. Pull request opened event
4. Pull request merged event

All with proper formatting:
- "username pushed to main on 1st March 2026..."
- "username submitted a pull request from feature/new-ui to main..."
- "username merged branch feature/new-ui to main..."

---

**You're all set!** Your action-repo is ready to generate webhook events.

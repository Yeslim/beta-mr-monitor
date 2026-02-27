# Beta.mr Procurement Monitor 🔔

Automatically monitors [beta.mr](https://www.beta.mr) for new public procurement announcements and sends WhatsApp notifications every hour.

## Features ✨

- 🕐 **Automated hourly checks** using GitHub Actions
- 📱 **WhatsApp notifications** for new announcements
- 💰 **100% Free** - no paid services required
- 🚀 **Zero maintenance** - runs automatically in the cloud
- 🔒 **Private** - your data stays in your GitHub repo

## How It Works

1. GitHub Actions runs the monitoring script every hour
2. Script fetches the latest announcements from beta.mr
3. Compares with previous state (stored in `last_state.json`)
4. If new announcements are found, sends you a WhatsApp message
5. Updates the state file for next check

## Setup Instructions 📋

### Step 1: Get Your WhatsApp API Credentials (5 minutes)

We'll use **CallMeBot** - a free WhatsApp notification service.

1. **Add CallMeBot to your WhatsApp contacts:**
   - Save this number: **+34 644 40 81 67**
   - Name it: "CallMeBot"

2. **Get your API key:**
   - Send this message to CallMeBot: `I allow callmebot to send me messages`
   - You'll receive your **API key** in response
   - **Save this key** - you'll need it in Step 3

3. **Note your phone number:**
   - Write down your phone number in international format
   - Example: `+22212345678` (Mauritania)
   - Format: `+[country code][number without zeros or spaces]`

### Step 2: Create GitHub Repository (3 minutes)

1. **Create a new repository:**
   - Go to https://github.com/new
   - Repository name: `beta-mr-monitor` (or any name you like)
   - Select: ✅ Public (required for free GitHub Actions)
   - Click "Create repository"

2. **Upload the project files:**
   
   You have two options:

   **Option A - Using GitHub Web Interface (Easier):**
   - Click "uploading an existing file"
   - Drag and drop these 4 files:
     - `monitor_beta.py`
     - `requirements.txt`
     - `last_state.json`
     - `.gitignore`
   - Commit the files
   - Create a folder `.github/workflows/` and upload `monitor.yml` there

   **Option B - Using Git Command Line:**
   ```bash
   # In the folder with the downloaded files
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/beta-mr-monitor.git
   git push -u origin main
   ```

### Step 3: Configure Secrets (2 minutes)

1. In your GitHub repository, go to **Settings** → **Secrets and variables** → **Actions**

2. Click **"New repository secret"** and add:

   **Secret 1:**
   - Name: `WHATSAPP_PHONE`
   - Value: Your phone number (e.g., `+22212345678`)
   - Click "Add secret"

   **Secret 2:**
   - Name: `WHATSAPP_API_KEY`
   - Value: The API key you received from CallMeBot
   - Click "Add secret"

### Step 4: Enable GitHub Actions (1 minute)

1. Go to **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. The workflow is now active! ✅

### Step 5: Test It! (2 minutes)

1. Go to **Actions** tab
2. Click on "Monitor Beta.mr" workflow on the left
3. Click **"Run workflow"** button → **"Run workflow"**
4. Wait 30-60 seconds
5. Click on the workflow run to see logs
6. Check your WhatsApp - you should receive a message with current announcements!

## How to Use 📱

### Normal Operation

Once set up, the system runs automatically:
- ✅ Checks beta.mr **every hour** (at minute 0)
- ✅ Sends WhatsApp notifications only when **new announcements** appear
- ✅ No action needed from you!

### Manual Check

Want to check immediately?
1. Go to **Actions** → **Monitor Beta.mr**
2. Click **"Run workflow"**

### View Logs

To see what the monitor is doing:
1. Go to **Actions** tab
2. Click on any workflow run
3. Click "monitor" to expand logs

## Customization 🔧

### Change Check Frequency

Edit `.github/workflows/monitor.yml`:

```yaml
schedule:
  - cron: '0 * * * *'    # Every hour
  # - cron: '0 */2 * * *'  # Every 2 hours
  # - cron: '0 9-17 * * 1-5'  # Every hour, 9am-5pm, weekdays only
  # - cron: '*/30 * * * *'  # Every 30 minutes
```

### Disable Notifications Temporarily

1. Go to **Actions** tab
2. Click "Monitor Beta.mr" workflow
3. Click "..." → **"Disable workflow"**
4. Re-enable when ready

## Troubleshooting 🔧

### ❌ Not receiving WhatsApp messages?

**Check 1:** Verify your phone number format
- Must include country code: `+222...`
- No spaces, dashes, or extra characters
- Test by sending yourself a message manually

**Check 2:** Verify API key
- Make sure you copied it exactly from CallMeBot
- No extra spaces before/after

**Check 3:** Check CallMeBot status
- Send "ping" to CallMeBot to verify it's working
- Wait a few minutes and try again

### ❌ Workflow failing?

1. Go to **Actions** → click on failed run
2. Check the error message
3. Common fixes:
   - Make sure secrets are set correctly
   - Verify the repository is public
   - Check if GitHub Actions is enabled

### ❌ Getting too many notifications?

The script only notifies you of **NEW** announcements. If you're getting many messages:
- It means many new announcements were posted since last check
- This is expected behavior
- Wait for the next check - you'll only get notified of truly new items

### ❌ Missing some announcements?

- The script checks every hour
- If an announcement is posted AND removed within 1 hour, it might be missed
- To check more frequently, see "Customization" section above

## Files Explanation 📁

- `monitor_beta.py` - Main Python script that does the monitoring
- `.github/workflows/monitor.yml` - GitHub Actions configuration
- `last_state.json` - Stores seen announcements (auto-updated)
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

## Cost 💰

**Completely FREE!**
- ✅ GitHub Actions: Free for public repositories (2,000 minutes/month)
- ✅ CallMeBot: Free WhatsApp API (300 messages/day limit)
- ✅ This monitor uses ~1 minute per check = ~720 minutes/month
- ✅ Well within free limits!

## Security & Privacy 🔒

- Your WhatsApp credentials are stored as **encrypted secrets** in GitHub
- Only your workflow can access them
- The state file is public but contains no sensitive data (just announcement IDs)
- No data is sent to any third party except CallMeBot for notifications

## Support 💬

Having issues? Check:
1. This README's Troubleshooting section
2. GitHub Actions logs for error messages
3. Verify all secrets are set correctly

## License

MIT License - Free to use and modify

---

**Happy monitoring! 🎉**

You'll now receive WhatsApp notifications whenever new procurement announcements are posted on beta.mr.

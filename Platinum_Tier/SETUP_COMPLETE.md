# LinkedIn & Gmail Automation Setup - Complete!

## What's Been Set Up

Your project now has real browser automation for:
- **LinkedIn**: Monitors your feed for new posts
- **Gmail**: Monitors your inbox for new emails

## Files Created

1. `.env` - Your credentials (secure, not committed to git)
2. `Platinum_Tier/RUN_WATCHERS.bat` - Easy launcher for Windows
3. `Platinum_Tier/setup_credentials.py` - Credential setup tool
4. `Platinum_Tier/test_setup.py` - Verification script

## How to Run

### Option 1: Interactive Menu (Easiest)
```bash
cd Platinum_Tier
RUN_WATCHERS.bat
```
Then select which watcher to run.

### Option 2: Run Individually
```bash
cd Platinum_Tier
python linkedin_watcher_playwright.py
# OR
python gmail_watcher_playwright.py
```

### Option 3: Run Both Simultaneously
```bash
cd Platinum_Tier
# In terminal 1:
python linkedin_watcher_playwright.py

# In terminal 2:
python gmail_watcher_playwright.py
```

## What Happens When You Run

1. **Browser Opens**: A Chrome browser window will open (not headless)
2. **Auto-Login**: The script will automatically log into your account
3. **Monitoring Starts**: Every 2-3 minutes, it checks for new content
4. **Files Created**: New posts/emails are saved to `Inbox/` folder
5. **Logs**: Activity is logged to `Gold_Tier/Logs/`

## Important Notes

### LinkedIn
- May require verification code on first login (check email/phone)
- If verification needed, you have 60 seconds to enter it manually
- Monitors your feed for new posts from connections

### Gmail
- If you have 2FA enabled, you MUST use an App Password
- Generate App Password: https://myaccount.google.com/apppasswords
- Monitors inbox for new emails

## File Output Format

### LinkedIn Posts
```
Inbox/LINKEDIN_20260217_123456_AuthorName.txt
```

### Gmail Emails
```
Inbox/GMAIL_20260217_123456_EmailSubject.txt
```

## Troubleshooting

**Login Fails:**
- Check credentials in .env file
- For Gmail: Use App Password if 2FA is enabled
- LinkedIn may require manual verification first time

**Browser Crashes:**
- Script will auto-restart after 5 retries
- Check logs in Gold_Tier/Logs/

**No New Content Detected:**
- Normal if no new posts/emails
- Check interval: LinkedIn (2 min), Gmail (3 min)

## Security Reminders

1. Never commit .env file to git (already in .gitignore)
2. Keep credentials secure
3. Use App Passwords for Gmail, not main password
4. This violates LinkedIn/Gmail ToS - use at your own risk

## Next Steps

Run the watchers and watch the magic happen!

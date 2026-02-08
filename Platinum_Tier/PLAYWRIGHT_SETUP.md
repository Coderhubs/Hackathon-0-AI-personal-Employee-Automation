# Real Gmail & LinkedIn Watchers - Setup Guide

## Overview
You now have **real Playwright-based watchers** that automate a browser to fetch actual emails and LinkedIn posts.

## Files Created
1. `gmail_watcher_playwright.py` - Real Gmail watcher
2. `linkedin_watcher_playwright.py` - Real LinkedIn watcher

## Current Status
⚠️ **CRITICAL ISSUE**: Your C: drive has **only 22MB free space**. This is blocking:
- Playwright installation (failed with "No space left on device")
- Docker Desktop (crashed)
- System stability

## Setup Instructions

### Step 1: Free Up Disk Space (REQUIRED)
You need at least **2-3 GB free** to install Playwright and its browser binaries.

**Quick wins to free space:**
```bash
# Clean Windows temp files
cleanmgr

# Delete old Windows updates
Dism.exe /online /Cleanup-Image /StartComponentCleanup

# Check largest folders
powershell "Get-ChildItem C:\ -Directory | ForEach-Object { $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum; [PSCustomObject]@{Folder=$_.Name; SizeGB=[math]::Round($size/1GB,2)} } | Sort-Object SizeGB -Descending | Select-Object -First 10"
```

### Step 2: Install Playwright
Once you have free space:

```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"

# Install Playwright
pip install playwright python-dotenv

# Install browser binaries (requires ~500MB)
playwright install chromium
```

### Step 3: Configure Credentials
Edit the `.env` file and add your credentials:

```bash
# Gmail Playwright
GMAIL_EMAIL=your_actual_email@gmail.com
GMAIL_PASSWORD=your_actual_password

# LinkedIn Playwright
LINKEDIN_EMAIL=your_actual_email@example.com
LINKEDIN_PASSWORD=your_actual_password
```

**Security Notes:**
- Never commit `.env` to git (it's in .gitignore)
- For Gmail, consider using an App Password instead of your main password
- LinkedIn may require 2FA verification on first login

### Step 4: Run the Watchers

**Test Gmail Watcher:**
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
python gmail_watcher_playwright.py
```

**Test LinkedIn Watcher:**
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
python linkedin_watcher_playwright.py
```

## How They Work

### Gmail Watcher
- Opens Chrome browser (visible, not headless)
- Logs into Gmail with your credentials
- Checks inbox every 3 minutes
- Saves new emails to `Inbox/GMAIL_*.txt`
- Tracks seen emails to avoid duplicates

### LinkedIn Watcher
- Opens Chrome browser (visible, not headless)
- Logs into LinkedIn with your credentials
- Checks feed every 2 minutes
- Saves new posts to `Inbox/LINKEDIN_*.txt`
- Tracks seen posts to avoid duplicates

## Features

✅ **Real browser automation** - Uses actual Chrome browser
✅ **Error recovery** - Exponential backoff on failures
✅ **Duplicate detection** - Won't save the same email/post twice
✅ **Logging** - All activity logged to `Gold_Tier/Logs/`
✅ **Graceful shutdown** - Press Ctrl+C to stop

## Troubleshooting

### "No space left on device"
- Free up at least 2-3 GB on C: drive
- See Step 1 above

### Gmail login fails
- Use App Password instead of regular password
- Go to: https://myaccount.google.com/apppasswords
- Generate new app password for "Mail"

### LinkedIn requires verification
- The script will wait 60 seconds for you to enter the code
- Check your email/phone for LinkedIn verification code
- Enter it in the browser window

### Browser doesn't open
- Make sure Playwright browsers are installed: `playwright install chromium`
- Check if Chrome/Chromium is blocked by antivirus

### Posts/Emails not being detected
- LinkedIn/Gmail may change their HTML structure
- Check logs in `Gold_Tier/Logs/` for errors
- The selectors may need updating

## Comparison: Mock vs Real

| Feature | Mock (Current) | Real (Playwright) |
|---------|---------------|-------------------|
| Data Source | Random fake data | Real Gmail/LinkedIn |
| Authentication | None | Your credentials |
| Browser | None | Chrome/Chromium |
| Reliability | 100% | ~90% (depends on site changes) |
| Setup | None | Requires credentials |
| Disk Space | Minimal | ~500MB for browsers |

## Next Steps

1. **Free up disk space** (most important!)
2. Install Playwright
3. Configure credentials in `.env`
4. Test the watchers
5. Run them in background or with PM2

## Running in Background

Once working, you can run them in background:

```bash
# Using Python background
nohup python gmail_watcher_playwright.py &
nohup python linkedin_watcher_playwright.py &

# Or using PM2 (if installed)
pm2 start gmail_watcher_playwright.py --name gmail-watcher
pm2 start linkedin_watcher_playwright.py --name linkedin-watcher
```

## Security Warnings

⚠️ **Important:**
- Your credentials are stored in plain text in `.env`
- Never share or commit the `.env` file
- Consider using App Passwords for Gmail
- LinkedIn may flag automated access as suspicious
- Use at your own risk - automation may violate ToS

## Support

If you encounter issues:
1. Check logs in `Gold_Tier/Logs/`
2. Run with visible browser (headless=False) to see what's happening
3. Update selectors if LinkedIn/Gmail changes their layout

# Agentic AI Watchers - Quick Reference

## 🚀 Quick Start

```bash
# 1. Setup credentials
python Platinum_Tier/setup_credentials.py

# 2. Test configuration
python Platinum_Tier/test_agentic_watchers.py

# 3. Run watchers
Platinum_Tier\RUN_WATCHERS.bat
```

## 📋 What It Does

### Gmail Watcher
- ✅ Monitors inbox every 3 minutes
- ✅ Filters for Agentic AI keywords
- ✅ Saves matching emails to `Inbox/GMAIL_AGENTIC_*.txt`
- ✅ Can send emails about Agentic AI (optional)

### LinkedIn Watcher
- ✅ Monitors feed every 2 minutes
- ✅ Filters for Agentic AI keywords
- ✅ Saves matching posts to `Inbox/LINKEDIN_AGENTIC_*.txt`
- ✅ Can create posts about Agentic AI (optional)

## 🔑 Keywords Monitored

- agentic
- ai agent
- autonomous ai
- llm
- claude
- gpt
- artificial intelligence
- machine learning

## 📁 Files Created

```
Inbox/
├── GMAIL_AGENTIC_20260217_120000_Subject.txt
└── LINKEDIN_AGENTIC_20260217_120000_Author.txt

Gold_Tier/Logs/
├── gmail_watcher_playwright.log
└── linkedin_watcher_playwright.log
```

## ⚙️ Enable Sending/Posting

### Gmail - Send Demo Email
Edit `gmail_watcher_playwright.py` line 197:
```python
asyncio.run(watcher.run(send_demo_email=True))
```

### LinkedIn - Create Demo Post
Edit `linkedin_watcher_playwright.py` line 218:
```python
asyncio.run(watcher.run(create_demo_post=True))
```

## 🔧 Configuration

### Change Check Intervals
```python
# Gmail (line 195)
check_interval=180  # seconds

# LinkedIn (line 215)
check_interval=120  # seconds
```

### Add/Remove Keywords
Edit `__init__` method in both watchers:
```python
self.agentic_keywords = [
    'agentic',
    'ai agent',
    # Add more keywords here
]
```

## 🐛 Troubleshooting

### Gmail Issues
- **2FA Error**: Use App Password from https://myaccount.google.com/apppasswords
- **Login Blocked**: Google may require manual verification on first login

### LinkedIn Issues
- **Verification Required**: Enter code in browser (60 second wait time)
- **Can't Create Post**: LinkedIn may have rate limits, wait and retry

### General Issues
- **No Content Found**: Keywords may be too specific, add more keywords
- **Browser Crashes**: Auto-restarts after 5 retries, check logs

## 📊 Logs

```bash
# View logs
type Gold_Tier\Logs\gmail_watcher_playwright.log
type Gold_Tier\Logs\linkedin_watcher_playwright.log
```

## 🛑 Stop Watchers

- Close the browser windows
- Press Ctrl+C in the terminal
- Close the command prompt windows

## 📖 Full Documentation

See `AGENTIC_AI_WATCHERS_GUIDE.md` for complete documentation.

## 🔒 Security

- Never commit `.env` file
- Use App Passwords for Gmail
- Keep credentials secure
- Monitor activity regularly

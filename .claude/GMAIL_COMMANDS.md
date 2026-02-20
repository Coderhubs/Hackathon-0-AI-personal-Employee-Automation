# Gmail Automation Commands - Send & Receive

## 📧 SENDING EMAILS

### Test Gmail Sending (Recommended)
```cmd
python test_gmail_manual.py
```

This will:
- Connect to Gmail SMTP
- Authenticate with app password
- Send test email to yourself
- Show success/failure message

### Alternative Send Commands

**Simple Gmail Test:**
```cmd
python test_gmail_simple.py
```

**Direct SMTP Sender:**
```cmd
python Platinum_Tier\gmail_sender_smtp.py
```

**Send Custom Email:**
```cmd
python -c "import sys; sys.path.insert(0, 'Platinum_Tier'); from gmail_sender_smtp import GmailSender; import os; from dotenv import load_dotenv; load_dotenv(); sender = GmailSender(os.getenv('GMAIL_ADDRESS'), os.getenv('GMAIL_APP_PASSWORD')); sender.send_email(to_email='recipient@example.com', subject='Your Subject', body='Your message here')"
```

---

## 📥 RECEIVING EMAILS (Monitoring Inbox)

### Start Gmail Watcher - IMAP (Fully Automated)
```cmd
cd Platinum_Tier
python gmail_watcher_imap.py
```

**Features:**
- ✅ Fully automated (NO browser, NO manual login)
- ✅ Uses Gmail App Password (NO 2FA issues)
- ✅ Monitors inbox every 3 minutes
- ✅ Detects emails with "Agentic AI" keywords
- ✅ Saves to AI_Employee_Vault/Needs_Action/
- ✅ Runs 24/7 autonomously

**Keywords Detected:**
- agentic, ai agent, autonomous ai
- llm, claude, gpt
- artificial intelligence, machine learning
- automation

### Alternative: Gmail Watcher - Playwright (Browser-based)
```cmd
python Platinum_Tier\gmail_watcher_playwright.py
```

**Note:** Requires manual login first time, then uses persistent session.

### Stop Gmail Watcher
Press `Ctrl+C` in the command window

---

## 📊 Check Status

### View Received Emails
```cmd
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

### View Latest Received Email
```cmd
type AI_Employee_Vault\Needs_Action\EMAIL_*.md | more
```

### View Gmail Watcher Logs
```cmd
type AI_Employee_Vault\Logs\gmail_watcher_imap.log
```

### View Sent Emails Log
```cmd
type AI_Employee_Vault\Logs\gmail_sender.log
```

### Verify Credentials
```cmd
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Gmail Address:', os.getenv('GMAIL_ADDRESS')); print('App Password:', 'Set' if os.getenv('GMAIL_APP_PASSWORD') else 'Not Set')"
```

---

## 🔧 Setup Commands (First Time Only)

### Setup Gmail Credentials
```cmd
python setup_gmail_login.py
```

This will:
- Guide you through app password setup
- Save credentials to .env file

**How to Get Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Google Account
3. Select "Mail" and your device
4. Click "Generate"
5. Copy the 16-character password
6. Add to .env file as GMAIL_APP_PASSWORD

---

## 🚀 Complete Workflow Example

### Send and Receive Workflow
```cmd
REM Step 1: Test sending
python test_gmail_manual.py

REM Step 2: Start monitoring inbox
cd Platinum_Tier
python gmail_watcher_imap.py

REM Step 3: In another terminal, check received emails
dir ..\AI_Employee_Vault\Needs_Action\EMAIL_*.md

REM Step 4: View a received email
type ..\AI_Employee_Vault\Needs_Action\EMAIL_*.md

REM Step 5: View logs
type ..\AI_Employee_Vault\Logs\gmail_watcher_imap.log
```

---

## 🛡️ Troubleshooting

### If Sending Fails

**Check credentials:**
```cmd
type .env | findstr GMAIL
```

Should show:
```
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-password
```

**Test connection:**
```cmd
ping smtp.gmail.com
```

**Re-setup if needed:**
```cmd
python setup_gmail_login.py
```

### If Receiving/Watcher Fails

**Check IMAP credentials:**
```cmd
type .env | findstr GMAIL
```

**Test IMAP connection:**
```cmd
ping imap.gmail.com
```

**Check watcher logs:**
```cmd
type AI_Employee_Vault\Logs\gmail_watcher_imap.log
```

**Common Issues:**
- Using regular password instead of App Password
- 2FA not enabled (required for App Passwords)
- IMAP not enabled in Gmail settings

**Enable IMAP in Gmail:**
1. Go to Gmail Settings → See all settings
2. Click "Forwarding and POP/IMAP"
3. Enable IMAP
4. Save changes

### If Email Not Received

1. Check spam folder
2. Verify email address in .env
3. Check if watcher is running: `tasklist | findstr python`
4. Check watcher logs for errors

---

## 📋 Current Status

**Gmail Watcher:** ✅ Running
**Emails Detected:** 5 emails saved to Needs_Action
**Monitoring Interval:** Every 180 seconds (3 minutes)
**Status:** Fully operational

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python test_gmail_manual.py` | Test Gmail sending (recommended) |
| `python setup_gmail_login.py` | Setup Gmail credentials |
| `python Platinum_Tier\gmail_watcher_playwright.py` | Start Gmail monitoring |
| `type AI_Employee_Vault\Logs\gmail_sender.log` | View Gmail logs |

---

## Required .env Variables

```
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

**Note:** Use Gmail App Password, NOT your regular password.

**How to get App Password:**
1. Go to Google Account settings
2. Security → 2-Step Verification
3. App passwords → Generate new
4. Copy 16-character password
5. Add to .env file

---

**Last Updated:** 2026-02-20

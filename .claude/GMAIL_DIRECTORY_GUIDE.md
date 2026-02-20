# Gmail Commands - Directory Context Guide

## 🚨 IMPORTANT: Commands depend on your current directory!

---

## FROM ROOT DIRECTORY (AI_personal_Employee/)

### Send Email
```cmd
python Platinum_Tier\gmail_sender_smtp.py
```

### Start IMAP Watcher
```cmd
cd Platinum_Tier
python gmail_watcher_imap.py
```

### Start Playwright Watcher
```cmd
python Platinum_Tier\gmail_watcher_playwright.py
```

### Test Gmail
```cmd
python test_gmail_manual.py
```

---

## FROM PLATINUM_TIER DIRECTORY (Already inside Platinum_Tier/)

### Send Email
```cmd
python gmail_sender_smtp.py
```

### Start IMAP Watcher
```cmd
python gmail_watcher_imap.py
```

### Start Playwright Watcher
```cmd
python gmail_watcher_playwright.py
```

### Test Gmail (go back to root first)
```cmd
cd ..
python test_gmail_manual.py
```

---

## 🎯 QUICK REFERENCE

### Check Your Current Directory
```cmd
cd
```

### If you see: `...\AI_personal_Employee>`
You're in ROOT directory. Use:
```cmd
python Platinum_Tier\gmail_sender_smtp.py
cd Platinum_Tier
python gmail_watcher_imap.py
```

### If you see: `...\AI_personal_Employee\Platinum_Tier>`
You're in PLATINUM_TIER directory. Use:
```cmd
python gmail_sender_smtp.py
python gmail_watcher_imap.py
```

---

## 📋 ALL GMAIL SCRIPTS (with correct paths)

### From ROOT directory:
```cmd
# Sending
python test_gmail_manual.py
python Platinum_Tier\gmail_sender_smtp.py

# Receiving (IMAP - Recommended)
cd Platinum_Tier
python gmail_watcher_imap.py

# Receiving (Playwright)
python Platinum_Tier\gmail_watcher_playwright.py

# Receiving (Other options)
python Platinum_Tier\gmail_watcher_session.py
python Platinum_Tier\gmail_watcher_manual.py
python Platinum_Tier\gmail_watcher_hackathon.py
```

### From PLATINUM_TIER directory:
```cmd
# Sending
python gmail_sender_smtp.py

# Receiving (IMAP - Recommended)
python gmail_watcher_imap.py

# Receiving (Playwright)
python gmail_watcher_playwright.py

# Receiving (Other options)
python gmail_watcher_session.py
python gmail_watcher_manual.py
python gmail_watcher_hackathon.py
```

---

## 🔧 TROUBLESHOOTING

### Error: "can't open file"
**Problem:** Wrong directory or wrong path

**Solution:**
1. Check current directory: `cd`
2. If in root, use: `python Platinum_Tier\gmail_sender_smtp.py`
3. If in Platinum_Tier, use: `python gmail_sender_smtp.py`

### Error: "No such file or directory"
**Problem:** Filename typo or wrong directory

**Solution:**
1. List files: `dir *.py` (Windows) or `ls *.py` (Git Bash)
2. Check filename: `gmail_sender_smtp.py` (underscores, not hyphens)
3. Verify you're in correct directory

---

## ✅ RECOMMENDED WORKFLOW

### Option 1: Stay in ROOT directory
```cmd
REM Check you're in root
cd

REM Test sending
python test_gmail_manual.py

REM Start watcher (opens new window in Platinum_Tier)
START_GMAIL_WATCHER.bat
```

### Option 2: Work from PLATINUM_TIER directory
```cmd
REM Go to Platinum_Tier
cd Platinum_Tier

REM Check you're in Platinum_Tier
cd

REM Start IMAP watcher
python gmail_watcher_imap.py

REM In another terminal, send email
cd ..
python test_gmail_manual.py
```

---

## 🎯 YOUR CURRENT SITUATION

You were in: `C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier>`

You tried: `python Platinum_Tier\gmail_sender_smtp.py`

This looked for: `Platinum_Tier\Platinum_Tier\gmail_sender_smtp.py` ❌

**Correct command (since you're already in Platinum_Tier):**
```cmd
python gmail_sender_smtp.py
```

---

## 📖 BATCH FILES (Always work from ROOT)

These batch files automatically handle directory changes:

```cmd
REM From any directory, go to root first
cd C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee

REM Then run batch files
TEST_GMAIL.bat
START_GMAIL_WATCHER.bat
TEST_GMAIL_SEND_RECEIVE.bat
VIEW_RECEIVED_EMAILS.bat
```

---

**Last Updated:** 2026-02-20
**Tip:** Always check your current directory with `cd` before running commands!

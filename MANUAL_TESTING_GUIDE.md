# Manual Testing Guide - AI Personal Employee
## Test LinkedIn, Gmail, and WhatsApp with Python Commands

This guide shows you how to manually test each automation component using Python commands.

---

## 🔧 Prerequisites

Make sure you have:
- Python 3.x installed
- All dependencies: `pip install -r requirements.txt`
- `.env` file configured with credentials
- ngrok installed (for WhatsApp)

---

## 📱 WHATSAPP AUTOMATION TESTING

### Test 1: Send a WhatsApp Message

**Command:**
```bash
python whatsapp_send.py "+923173851441" "Test message from AI Employee!"
```

**What it does:**
- Sends a WhatsApp message via Twilio API
- Saves sent message to `WhatsApp_Vault/Sent/`
- Logs activity to `AI_Employee_Vault/Logs/whatsapp_sender.log`

**Expected Output:**
```
[OK] Message sent successfully!
SID: SMxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### Test 2: Start WhatsApp Auto-Reply Server

**Step 1: Start ngrok (Terminal 1)**
```bash
ngrok http 5000
```

**Step 2: Start Flask Auto-Reply Server (Terminal 2)**
```bash
python whatsapp_autoreply.py
```

**Step 3: Configure Twilio Webhook**
1. Copy ngrok URL (e.g., `https://xxxx.ngrok-free.dev`)
2. Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
3. Set "When a message comes in" to: `https://xxxx.ngrok-free.dev/whatsapp`
4. Click Save

**Step 4: Test Auto-Reply**
Send a WhatsApp message to `+14155238886` with:
- "hello" → Gets auto-reply: "Hello! 👋 I am an AI assistant..."
- "price" → Gets auto-reply: "Please contact us at business@email.com..."
- "help" → Gets auto-reply: "I can help you with..."

**Check Results:**
```bash
# View received messages
ls -lt WhatsApp_Vault/Conversations/

# View sent auto-replies
ls -lt WhatsApp_Vault/Sent/

# View logs
tail -20 AI_Employee_Vault/Logs/whatsapp_autoreply.log
```

---

## 📧 GMAIL AUTOMATION TESTING

### Test 1: Send Email via SMTP

**Command:**
```bash
python -c "
from Platinum_Tier.gmail_sender_smtp import GmailSender
import os
from dotenv import load_dotenv

load_dotenv()

sender = GmailSender(
    email_address=os.getenv('GMAIL_ADDRESS'),
    app_password=os.getenv('GMAIL_APP_PASSWORD')
)

result = sender.send_email(
    to_email='recipient@example.com',
    subject='Test Email from AI Employee',
    body='This is a test email sent via Python command.'
)

print('Email sent!' if result else 'Failed to send email')
"
```

**What it does:**
- Sends email using Gmail SMTP
- Uses App Password for authentication
- Logs activity

**Expected Output:**
```
Email sent successfully!
```

---

### Test 2: Monitor Gmail for New Emails (IMAP)

**Command:**
```bash
python Platinum_Tier/gmail_watcher_imap.py
```

**What it does:**
- Connects to Gmail via IMAP
- Monitors for new emails with "Agentic AI" keywords
- Saves urgent emails to `AI_Employee_Vault/Needs_Action/`
- Runs continuously (press Ctrl+C to stop)

**Expected Output:**
```
[INFO] Connected to Gmail IMAP
[INFO] Monitoring inbox for new emails...
[INFO] Checking for new emails... (every 60 seconds)
```

**Check Results:**
```bash
# View detected emails
ls -lt AI_Employee_Vault/Needs_Action/

# View logs
tail -20 AI_Employee_Vault/Logs/gmail_watcher.log
```

---

## 💼 LINKEDIN AUTOMATION TESTING

### Test 1: Setup LinkedIn Session (First Time Only)

**Command:**
```bash
python setup_linkedin_login.py
```

**What it does:**
- Opens browser for manual LinkedIn login
- Saves session cookies to `browser_data/linkedin/`
- Session persists for future automated posts

**Expected Output:**
```
[INFO] Browser opened - Please login to LinkedIn manually
[INFO] Waiting for login...
[SUCCESS] LinkedIn session saved!
```

---

### Test 2: Post to LinkedIn (Simple)

**Command:**
```bash
python linkedin_post_simple.py "This is a test post from my AI Employee automation! 🤖 #AI #Automation"
```

**What it does:**
- Uses saved LinkedIn session
- Posts content to your LinkedIn feed
- Takes screenshot of posted content
- Logs activity

**Expected Output:**
```
[INFO] Using saved session
[INFO] Launching browser...
[INFO] Navigating to LinkedIn...
[INFO] Posting content...
[SUCCESS] Post published successfully!
```

**Check Results:**
1. Check your LinkedIn profile for the new post
2. View screenshot: `AI_Employee_Vault/Generated_Images/linkedin_post_*.png`
3. View logs: `tail -20 AI_Employee_Vault/Logs/linkedin_automation.log`

---

### Test 3: LinkedIn Content Generator + Auto-Post

**Command:**
```bash
python linkedin_content_generator.py
```

**What it does:**
- Generates AI-powered LinkedIn post content
- Automatically posts to LinkedIn
- Saves content to vault

**Expected Output:**
```
[INFO] Generating LinkedIn content...
[INFO] Content generated successfully
[INFO] Posting to LinkedIn...
[SUCCESS] Posted to LinkedIn!
```

---

### Test 4: Monitor LinkedIn for Messages/Posts

**Command:**
```bash
python Platinum_Tier/linkedin_watcher_playwright.py
```

**What it does:**
- Monitors LinkedIn for new messages
- Detects posts with AI-related keywords
- Saves detected items to `AI_Employee_Vault/Needs_Action/`
- Runs continuously (press Ctrl+C to stop)

**Expected Output:**
```
[INFO] LinkedIn Watcher started
[INFO] Monitoring for new messages and posts...
[INFO] Checking LinkedIn... (every 5 minutes)
```

**Check Results:**
```bash
# View detected LinkedIn items
ls -lt AI_Employee_Vault/Needs_Action/

# View logs
tail -20 AI_Employee_Vault/Logs/linkedin_watcher.log
```

---

## 🔄 COMPLETE SYSTEM TESTING

### Test All Watchers Together

**Terminal 1: WhatsApp**
```bash
# Start ngrok
ngrok http 5000
```

**Terminal 2: WhatsApp Auto-Reply**
```bash
python whatsapp_autoreply.py
```

**Terminal 3: Gmail Watcher**
```bash
python Platinum_Tier/gmail_watcher_imap.py
```

**Terminal 4: LinkedIn Watcher**
```bash
python Platinum_Tier/linkedin_watcher_playwright.py
```

**Terminal 5: Send Test Messages**
```bash
# Test WhatsApp
python whatsapp_send.py "+923173851441" "System test message"

# Test Gmail (using Python)
python -c "from Platinum_Tier.gmail_sender_smtp import GmailSender; import os; from dotenv import load_dotenv; load_dotenv(); sender = GmailSender(os.getenv('GMAIL_ADDRESS'), os.getenv('GMAIL_APP_PASSWORD')); sender.send_email('test@example.com', 'Test', 'Test message')"

# Test LinkedIn
python linkedin_post_simple.py "System test post 🤖"
```

---

## 📊 MONITORING & VERIFICATION

### Check System Status

**View All Logs:**
```bash
# WhatsApp logs
tail -20 AI_Employee_Vault/Logs/whatsapp_sender.log
tail -20 AI_Employee_Vault/Logs/whatsapp_autoreply.log

# Gmail logs
tail -20 AI_Employee_Vault/Logs/gmail_sender.log
tail -20 AI_Employee_Vault/Logs/gmail_watcher.log

# LinkedIn logs
tail -20 AI_Employee_Vault/Logs/linkedin_automation.log
tail -20 AI_Employee_Vault/Logs/linkedin_watcher.log
```

**View Vault Activity:**
```bash
# Items needing action
ls -lt AI_Employee_Vault/Needs_Action/

# Pending approvals
ls -lt AI_Employee_Vault/Pending_Approval/

# Completed tasks
ls -lt AI_Employee_Vault/Done/

# WhatsApp activity
ls -lt WhatsApp_Vault/Sent/
ls -lt WhatsApp_Vault/Conversations/
```

---

## 🐛 TROUBLESHOOTING

### WhatsApp Issues

**Problem: "Authentication failed"**
```bash
# Check Twilio credentials
cat .whatsapp_config
```

**Problem: "No auto-reply received"**
```bash
# Check if webhook is configured in Twilio
curl http://localhost:4040/api/tunnels

# Check Flask server is running
curl http://localhost:5000/health
```

---

### Gmail Issues

**Problem: "Authentication failed"**
```bash
# Verify Gmail credentials in .env
grep GMAIL .env

# Test SMTP connection
python -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com',587); s.starttls(); print('SMTP connection OK')"
```

**Problem: "App Password not working"**
- Go to: https://myaccount.google.com/apppasswords
- Generate new App Password
- Update `.env` file with new password

---

### LinkedIn Issues

**Problem: "Session not found"**
```bash
# Re-run LinkedIn login setup
python setup_linkedin_login.py
```

**Problem: "Post failed"**
```bash
# Check if session is still valid
ls -la browser_data/linkedin/

# View detailed logs
tail -50 AI_Employee_Vault/Logs/linkedin_automation.log
```

---

## ✅ QUICK TEST CHECKLIST

- [ ] WhatsApp: Send message → `python whatsapp_send.py "+92XXX" "Test"`
- [ ] WhatsApp: Auto-reply working → Send message to Twilio number
- [ ] Gmail: Send email → Use Python command above
- [ ] Gmail: Watcher running → `python Platinum_Tier/gmail_watcher_imap.py`
- [ ] LinkedIn: Session saved → `python setup_linkedin_login.py`
- [ ] LinkedIn: Post working → `python linkedin_post_simple.py "Test"`
- [ ] LinkedIn: Watcher running → `python Platinum_Tier/linkedin_watcher_playwright.py`
- [ ] All logs being created → Check `AI_Employee_Vault/Logs/`
- [ ] Vault structure working → Check all vault folders

---

## 📝 NOTES

1. **WhatsApp requires ngrok** to be running for receiving messages
2. **Gmail App Password** must be generated from Google Account settings
3. **LinkedIn session** must be created once before automated posting
4. **All watchers** run continuously - use Ctrl+C to stop
5. **Logs are your friend** - always check logs when troubleshooting

---

## 🚀 NEXT STEPS

After manual testing works:
1. Use batch files for automated startup: `START_ALL_AUTOMATION.bat`
2. Set up Windows Task Scheduler for 24/7 operation
3. Configure approval workflow for sensitive actions
4. Monitor `AI_Employee_Vault/Dashboard.md` for system status

---

**Last Updated:** 2026-02-20
**Project:** AI Personal Employee Hackathon

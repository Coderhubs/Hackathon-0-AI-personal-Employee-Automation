# All Automation Commands - Quick Reference

**Last Updated:** 2026-02-20

---

## 🚀 Quick Start - Test All Systems

```cmd
python quick_test.py
```

This tests:
- ✅ Vault structure
- ✅ WhatsApp sending
- ✅ Gmail sending
- ✅ LinkedIn session

---

## 📧 Gmail Commands (Send & Receive)

### Send Email - Test
```cmd
python test_gmail_manual.py
```

### Receive Emails - Start Watcher (Fully Automated)
```cmd
cd Platinum_Tier
python gmail_watcher_imap.py
```

**Features:**
- ✅ Monitors inbox every 3 minutes
- ✅ Detects "Agentic AI" keywords
- ✅ Saves to Needs_Action folder
- ✅ NO browser, NO manual login
- ✅ Runs 24/7 autonomously

### Check Received Emails
```cmd
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

### View Gmail Logs
```cmd
type AI_Employee_Vault\Logs\gmail_watcher_imap.log
type AI_Employee_Vault\Logs\gmail_sender.log
```

**Full Guide:** See `GMAIL_COMMANDS.md`

---

## 💼 LinkedIn Commands

### Check Safety Status (ALWAYS FIRST)
```cmd
python linkedin_safety_check.py
```

### Post Safely (Only When GREEN)
```cmd
python linkedin_safe_post.py
```

### Setup LinkedIn Session
```cmd
python setup_linkedin_login.py
```

**Full Guide:** See `LINKEDIN_COMMANDS.md`

**⚠️ CRITICAL:** Never bypass LinkedIn safety checks!

---

## 💬 WhatsApp Commands

### Test WhatsApp
```cmd
python test_whatsapp_send.py
```

### Start WhatsApp Watcher
```cmd
python Platinum_Tier\whatsapp_watcher_hackathon.py
```

### View Sent Messages
```cmd
dir WhatsApp_Vault\Sent\
```

**Full Guide:** See `WHATSAPP_COMMANDS.md`

---

## 🤖 Complete System Commands

### Start All Watchers
```cmd
START_ALL_WATCHERS.bat
```

### Start Full Automation
```cmd
START_FULLY_AUTOMATED.bat
```

### Run Orchestrator
```cmd
python orchestrator.py
```

---

## 📊 Status & Monitoring

### Check System Status
```cmd
python quick_test.py
```

### View All Logs
```cmd
dir AI_Employee_Vault\Logs\
```

### Check Pending Actions
```cmd
dir AI_Employee_Vault\Needs_Action\
```

### Check Pending Approvals
```cmd
dir AI_Employee_Vault\Pending_Approval\
```

### Check Completed Tasks
```cmd
dir AI_Employee_Vault\Done\
```

---

## 🔧 Setup Commands (First Time)

### Setup Gmail
```cmd
python setup_gmail_login.py
```

### Setup LinkedIn
```cmd
python setup_linkedin_login.py
```

### Setup WhatsApp (Twilio)
Add to .env file:
```
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TEST_PHONE_NUMBER=whatsapp:+your-number
```

---

## 📝 Testing Workflow

### 1. Test Individual Platforms
```cmd
REM Test Gmail
python test_gmail_manual.py

REM Check LinkedIn safety
python linkedin_safety_check.py

REM Test WhatsApp
python test_whatsapp_send.py
```

### 2. Test Complete System
```cmd
REM Run all tests
python quick_test.py

REM Start watchers
START_ALL_WATCHERS.bat

REM Monitor logs
type AI_Employee_Vault\Logs\orchestrator.log
```

### 3. Test Approval Workflow
```cmd
REM Create test action
echo Test action > AI_Employee_Vault\Needs_Action\TEST.md

REM Process with Claude (in Claude Code)
/process-inbox

REM Check pending approval
dir AI_Employee_Vault\Pending_Approval\

REM Approve action
move AI_Employee_Vault\Pending_Approval\DRAFT_* AI_Employee_Vault\Approved\

REM Check completion
dir AI_Employee_Vault\Done\
```

---

## 🛡️ Safety Checklist

Before running automation:

- [ ] Gmail credentials in .env
- [ ] LinkedIn safety status is GREEN
- [ ] WhatsApp credentials in .env
- [ ] Network connection stable
- [ ] Vault directories exist
- [ ] Logs directory monitored

---

## 📚 Detailed Guides

- **Gmail:** `.claude\GMAIL_COMMANDS.md`
- **LinkedIn:** `.claude\LINKEDIN_COMMANDS.md`
- **WhatsApp:** `.claude\WHATSAPP_COMMANDS.md`
- **Manual Testing:** `.claude\MANUAL_TESTING_GUIDE.md`

---

## 🚨 Important Notes

1. **LinkedIn Safety:** ALWAYS check safety status before posting
2. **Network:** WhatsApp requires stable internet connection
3. **Credentials:** Keep .env file secure, never commit to git
4. **Logs:** Monitor logs for errors and issues
5. **Approval:** Human approval required for sensitive actions

---

## 🔍 Troubleshooting Quick Commands

### Check Credentials
```cmd
type .env | findstr /i "GMAIL LINKEDIN TWILIO"
```

### Check Network
```cmd
ping smtp.gmail.com
ping api.twilio.com
```

### Check Vault Structure
```cmd
dir AI_Employee_Vault\
```

### View Recent Logs
```cmd
type AI_Employee_Vault\Logs\orchestrator.log
```

---

## 📞 Support

For issues:
1. Check detailed guides in `.claude\` folder
2. Review logs in `AI_Employee_Vault\Logs\`
3. Check `HACKATHON_COMPLIANCE_REPORT.md`
4. Review `FULLY_AUTOMATED_GUIDE.md`

---

**Quick Access:**
- All commands: This file
- Gmail: `GMAIL_COMMANDS.md`
- LinkedIn: `LINKEDIN_COMMANDS.md`
- WhatsApp: `WHATSAPP_COMMANDS.md`
- Testing: `MANUAL_TESTING_GUIDE.md`

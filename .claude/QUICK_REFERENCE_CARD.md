# Quick Reference Card - AI Personal Employee

**Keep this handy for daily testing!**

---

## 🚀 Daily Testing Commands

### Test All Systems
```cmd
python quick_test.py
```

### Gmail - Send Email
```cmd
python test_gmail_manual.py
```

### Gmail - Receive Emails (Start Watcher)
```cmd
cd Platinum_Tier
python gmail_watcher_imap.py
```

### Gmail - Check Received Emails
```cmd
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

### Check LinkedIn Safety (ALWAYS FIRST)
```cmd
python linkedin_safety_check.py
```

### Post to LinkedIn (Only When GREEN)
```cmd
python linkedin_safe_post.py
```

### WhatsApp - Send Message
```cmd
python test_whatsapp_send.py
```

### WhatsApp - Receive Messages (Start Watcher)
```cmd
python Platinum_Tier\whatsapp_watcher_hackathon.py
```

---

## 📊 Check Status

### View Logs
```cmd
type AI_Employee_Vault\Logs\orchestrator.log
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

## 🛡️ LinkedIn Safety Rules

**ALWAYS check before posting:**
```cmd
python linkedin_safety_check.py
```

**Traffic Light System:**
- 🟢 GREEN = Safe to post NOW
- 🟡 YELLOW = Caution (needs confirmation)
- 🔴 RED = DO NOT POST (blocked)

**Rules:**
- Max 2 posts/day
- Min 4 hours between posts
- Max 10 posts/week
- Hours: 9 AM - 6 PM only

---

## 🔧 Setup (First Time Only)

### Gmail Setup
```cmd
python setup_gmail_login.py
```

### LinkedIn Setup
```cmd
python setup_linkedin_login.py
```

### WhatsApp Setup
Add to .env:
```
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TEST_PHONE_NUMBER=whatsapp:+your-number
```

---

## 🚨 Troubleshooting

### Gmail Not Working
```cmd
python setup_gmail_login.py
type .env | findstr GMAIL
```

### LinkedIn Session Expired
```cmd
python setup_linkedin_login.py
```

### WhatsApp Network Error
```cmd
ping api.twilio.com
```

### Check Credentials
```cmd
type .env
```

---

## 📚 Full Documentation

- **All Commands:** `.claude\ALL_COMMANDS.md`
- **Gmail Guide:** `.claude\GMAIL_COMMANDS.md`
- **LinkedIn Guide:** `.claude\LINKEDIN_COMMANDS.md`
- **WhatsApp Guide:** `.claude\WHATSAPP_COMMANDS.md`
- **Testing Guide:** `.claude\MANUAL_TESTING_GUIDE.md`

---

## ⚡ Emergency Commands

### Stop All Watchers
```cmd
Ctrl+C
```

### View Latest Error
```cmd
type AI_Employee_Vault\Logs\orchestrator.log
```

### Clear Pending Actions
```cmd
del AI_Employee_Vault\Needs_Action\*.md
```

---

**Last Updated:** 2026-02-20
**Status:** Gmail ✅ | LinkedIn 🔴 | WhatsApp ⚠️

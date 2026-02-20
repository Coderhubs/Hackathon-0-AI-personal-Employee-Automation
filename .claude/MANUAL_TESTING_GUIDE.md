# Manual Testing Guide - AI Personal Employee

**Last Updated:** 2026-02-20 22:35:00

## Current System Status

### ✅ Gmail Automation - FULLY WORKING (Send & Receive)
- SMTP sending: Working
- IMAP receiving: Working
- Watcher Status: **RUNNING** (monitoring inbox)
- Emails Detected: 5 emails saved to Needs_Action
- Test email sent: ✓
- Status: **READY FOR TESTING**

**Send Command:**
```bash
python test_gmail_manual.py
```

**Receive Command (Start Watcher):**
```bash
cd Platinum_Tier
python gmail_watcher_imap.py
```

**Check Received Emails:**
```bash
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

### 🔴 LinkedIn Automation - SAFETY BLOCKED
- Safety Status: **RED - DO NOT POST**
- Reason: Posted 4 times in last 24 hours (COOLDOWN)
- Posts Today: 4/2 (exceeded daily limit)
- Next Safe Window: **2026-02-21 09:00:00** (10.4 hours)
- Status: **BLOCKED UNTIL GREEN**

### ⚠️ WhatsApp Automation - NETWORK ISSUE
- Code Status: Working
- Network: DNS resolution error (api.twilio.com)
- Status: **WAIT FOR NETWORK**

### ✅ Vault Structure - COMPLETE
All directories present and ready.

---

## CRITICAL: LinkedIn Safety Rules

### 🚨 MANDATORY SAFETY ENFORCEMENT

**LinkedIn posting MUST ALWAYS follow the safety script, even if explicitly asked to post.**

**Safety Rules:**
- Maximum 2 posts per day
- Minimum 4 hours between posts
- Maximum 10 posts per week
- Posting hours: 9 AM - 6 PM only
- 48-hour cooldown after exceeding limits

**Traffic Light System:**
- 🟢 **GREEN**: Safe to post immediately
- 🟡 **YELLOW**: Caution - can post with confirmation
- 🔴 **RED**: DO NOT POST - blocked

**Before ANY LinkedIn post:**
```bash
python linkedin_safety_check.py
```

**Only post when GREEN:**
```bash
python linkedin_safe_post.py
```

**NEVER bypass the safety check. NEVER post when RED or YELLOW (without confirmation).**

---

## Manual Testing Commands

### 1. Test Gmail Automation (Available Now)

**Send Email:**
```bash
python test_gmail_manual.py
```

**Expected Result:**
- Connects to smtp.gmail.com:587
- Authenticates with app password
- Sends test email to your inbox
- Logs success message

**Receive Emails (Start Watcher):**
```bash
cd Platinum_Tier
python gmail_watcher_imap.py
```

**Expected Result:**
- Connects to imap.gmail.com
- Monitors inbox every 3 minutes
- Detects emails with "Agentic AI" keywords
- Saves to AI_Employee_Vault/Needs_Action/
- Runs continuously (press Ctrl+C to stop)

**Check Received Emails:**
```bash
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md
type AI_Employee_Vault\Needs_Action\EMAIL_20260220_*.md
```

**Check Result:**
- Open your Gmail inbox
- Look for email: "✅ Manual Test - AI Personal Employee"
- Verify email was received
- Check Needs_Action folder for detected emails

---

### 2. Test LinkedIn Automation (When GREEN)

**Step 1: Check Safety Status**
```bash
python linkedin_safety_check.py
```

**Step 2: If GREEN, Post Safely**
```bash
python linkedin_safe_post.py
```

**Step 3: Verify Post**
- Open LinkedIn in browser
- Check your profile feed
- Verify post appears

**Current Status:**
- 🔴 RED - BLOCKED
- Wait until: 2026-02-21 09:00:00
- Do NOT attempt to post until GREEN

---

### 3. Test WhatsApp Automation (When Network Available)

**Test Send:**
```bash
python test_whatsapp_send.py
```

**Expected Result:**
- Connects to Twilio API
- Sends test message
- Returns message SID
- Logs to WhatsApp_Vault/Sent/

**Current Issue:**
- Network DNS error
- Check internet connection
- Retry when network is stable

---

### 4. Test Complete System Workflow

**Step 1: Create Test Email in Needs_Action**
```bash
# Create a test email file
echo "---
type: email
from: test@example.com
subject: Test Email
priority: normal
---

This is a test email for the AI Employee system.
" > AI_Employee_Vault/Needs_Action/TEST_email_$(date +%Y%m%d_%H%M%S).md
```

**Step 2: Process with Claude**
```bash
# Use /process-inbox skill in Claude Code
/process-inbox
```

**Step 3: Review Pending Approval**
```bash
ls AI_Employee_Vault/Pending_Approval/
```

**Step 4: Approve Action**
```bash
# Move approved item to Approved folder
mv AI_Employee_Vault/Pending_Approval/DRAFT_* AI_Employee_Vault/Approved/
```

**Step 5: Execute (if safe)**
- Gmail: Executes immediately
- LinkedIn: Only if safety check is GREEN
- WhatsApp: Only if network available

**Step 6: Verify Completion**
```bash
ls AI_Employee_Vault/Done/
cat AI_Employee_Vault/Logs/orchestrator.log
```

---

## Test Scripts Reference

### Gmail Tests
- `test_gmail_manual.py` - Manual Gmail test (recommended)
- `test_gmail_simple.py` - Simple Gmail test
- `Platinum_Tier/gmail_sender_smtp.py` - Direct SMTP sender

### LinkedIn Tests
- `linkedin_safety_check.py` - Check safety status (ALWAYS run first)
- `linkedin_safe_post.py` - Safe posting with checks (recommended)
- `linkedin_post_simple.py` - Direct posting (NOT recommended - bypasses safety)

### WhatsApp Tests
- `test_whatsapp_send.py` - Send test message
- `whatsapp_send.py` - Direct WhatsApp sender

### System Tests
- `quick_test.py` - Test all platforms quickly
- `test_complete_system.py` - Test complete workflow
- `test_integration.py` - Integration tests

---

## Troubleshooting

### Gmail Issues
**Problem:** Authentication failed
**Solution:**
1. Check GMAIL_ADDRESS in .env
2. Check GMAIL_APP_PASSWORD in .env
3. Verify app password is correct (not regular password)
4. Run: `python setup_gmail_login.py`

### LinkedIn Issues
**Problem:** Safety check shows RED
**Solution:**
1. Wait for next safe window (shown in safety check)
2. Do NOT attempt to bypass
3. Check again with: `python linkedin_safety_check.py`

**Problem:** Session expired
**Solution:**
1. Run: `python setup_linkedin_login.py`
2. Login manually in browser
3. Session will be saved for future use

### WhatsApp Issues
**Problem:** Network error
**Solution:**
1. Check internet connection
2. Verify Twilio credentials in .env
3. Test DNS: `ping api.twilio.com`

---

## Safety Checklist

Before running any automation:

- [ ] Gmail credentials configured in .env
- [ ] LinkedIn safety status checked (must be GREEN)
- [ ] WhatsApp network connection verified
- [ ] Vault directories exist
- [ ] Test files created in Needs_Action
- [ ] Approval workflow understood
- [ ] Logs directory monitored

**CRITICAL:** Never bypass LinkedIn safety checks. Always run `linkedin_safety_check.py` before posting.

---

## Quick Reference

**Check System Status:**
```bash
python quick_test.py
```

**Check LinkedIn Safety:**
```bash
python linkedin_safety_check.py
```

**Test Gmail:**
```bash
python test_gmail_manual.py
```

**Start Full System:**
```bash
START_FULLY_AUTOMATED.bat
```

**Process Inbox:**
```bash
# In Claude Code
/process-inbox
```

---

## Expected Test Results

### Successful Gmail Test
```
✅ SUCCESS - Gmail Test Passed
Check your inbox: your-email@gmail.com
Gmail automation is working perfectly!
```

### LinkedIn Safety Check (GREEN)
```
🟢 GREEN - SAFE TO POST
Safe to post. Last post: 6.5h ago. Posts today: 1/2
```

### LinkedIn Safety Check (RED)
```
🔴 RED - DO NOT POST
COOLDOWN: Posted 4 times in 24h. Wait 33.0 more hours.
```

### WhatsApp Success
```
✓ WhatsApp: PASSED
Message SID: SM...
```

---

## Notes

1. **LinkedIn Safety is MANDATORY** - Never bypass, even if asked
2. **Test in order** - Gmail first, then LinkedIn (when GREEN), then WhatsApp
3. **Monitor logs** - Check AI_Employee_Vault/Logs/ for details
4. **Human approval required** - For all sensitive actions
5. **Network dependent** - WhatsApp requires stable internet

---

**For issues or questions, check:**
- `HACKATHON_COMPLIANCE_REPORT.md` - System status
- `FULLY_AUTOMATED_GUIDE.md` - Usage instructions
- `AI_Employee_Vault/Logs/` - Error logs

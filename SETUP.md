# Setup Guide - AI Personal Employee

Complete setup instructions for getting the AI Personal Employee system running.

---

## 📋 Prerequisites

### Required Software
- **Python 3.10 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### Required Accounts
- **Gmail Account** - For email automation
- **LinkedIn Account** - For LinkedIn automation
- **Twilio Account** (Free tier works) - For WhatsApp automation

---

## 🚀 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI_personal_Employee.git
cd AI_personal_Employee
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install chromium
```

### 4. Install MCP Server Dependencies

```bash
cd mcp_servers/email-mcp
npm install
cd ../..
```

### 5. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
# Use your favorite text editor (notepad, vim, nano, etc.)
notepad .env
```

---

## 🔑 Getting Credentials

### Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Sign in to your Google Account
3. If you don't see "App passwords", enable 2-Step Verification first
4. Select "Mail" and your device
5. Click "Generate"
6. Copy the 16-character password (no spaces)
7. Add to `.env` file:
   ```
   GMAIL_ADDRESS=your-email@gmail.com
   GMAIL_APP_PASSWORD=your-16-char-password
   ```

### LinkedIn Credentials

1. Use your regular LinkedIn login credentials
2. Add to `.env` file:
   ```
   LINKEDIN_EMAIL=your-linkedin-email@gmail.com
   LINKEDIN_PASSWORD=your-linkedin-password
   ```

### Twilio (WhatsApp)

1. Sign up at https://www.twilio.com (free trial available)
2. Get your Account SID and Auth Token from the console
3. Join WhatsApp sandbox:
   - Go to https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Send "join <your-sandbox-name>" to +1 415 523 8886 from your WhatsApp
4. Add to `.env` file:
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your-auth-token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   TEST_PHONE_NUMBER=whatsapp:+your-phone-number
   ```

---

## ✅ Verify Installation

### Test All Systems

```bash
python quick_test.py
```

Expected output:
- ✅ Vault Structure: PASS
- ✅ WhatsApp: PASS (if network available)
- ✅ Gmail: PASS
- ✅ LinkedIn: Session check

---

## 🎮 First Run

### Option 1: Test Individual Components

**Test Gmail:**
```bash
python test_gmail_manual.py
```

**Check LinkedIn Safety:**
```bash
python linkedin_safety_check.py
```

**Test WhatsApp:**
```bash
python test_whatsapp_send.py
```

### Option 2: Use Batch Files (Windows)

```bash
# Test Gmail
TEST_GMAIL.bat

# Check LinkedIn safety
TEST_LINKEDIN_SAFETY.bat

# Test WhatsApp
TEST_WHATSAPP.bat

# Test all platforms
TEST_ALL_PLATFORMS.bat
```

---

## 📧 Gmail Setup

### Start Gmail Monitoring

**Option 1: IMAP Watcher (Recommended - Fully Automated)**
```bash
cd Platinum_Tier
python gmail_watcher_imap.py
```

**Option 2: Playwright Watcher (Browser-based)**
```bash
python Platinum_Tier\gmail_watcher_playwright.py
```

**Option 3: Use Batch File**
```bash
START_GMAIL_WATCHER.bat
```

### Check Received Emails

```bash
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

---

## 💼 LinkedIn Setup

### Important: LinkedIn Safety System

LinkedIn posting is protected by a traffic light safety system:
- 🟢 GREEN = Safe to post
- 🟡 YELLOW = Caution (requires confirmation)
- 🔴 RED = DO NOT POST (blocked)

**Always check safety before posting:**
```bash
python linkedin_safety_check.py
```

### Setup LinkedIn Session

```bash
python setup_linkedin_login.py
```

This will:
1. Open a browser
2. Ask you to login to LinkedIn
3. Save your session for future use

### Post to LinkedIn (When Safe)

```bash
python linkedin_safe_post.py
```

---

## 💬 WhatsApp Setup

### Join Twilio Sandbox

1. Send "join <your-sandbox-name>" to +1 415 523 8886 from WhatsApp
2. Wait for confirmation message
3. Test sending:
   ```bash
   python test_whatsapp_send.py
   ```

### Start WhatsApp Monitoring

```bash
python Platinum_Tier\whatsapp_watcher_hackathon.py
```

---

## 📁 Directory Structure

After setup, your directory should look like this:

```
AI_personal_Employee/
├── .env                          # Your credentials (DO NOT COMMIT)
├── AI_Employee_Vault/
│   ├── Needs_Action/             # Detected items
│   ├── Pending_Approval/         # Awaiting approval
│   ├── Approved/                 # Ready to execute
│   ├── Done/                     # Completed tasks
│   ├── Logs/                     # Activity logs
│   └── Plans/                    # Action plans
├── WhatsApp_Vault/
│   ├── Sent/                     # Sent messages
│   └── Conversations/            # Message history
└── Platinum_Tier/
    └── browser_data/             # Saved browser sessions
        ├── gmail/
        └── linkedin/
```

---

## 🔧 Troubleshooting

### Gmail Issues

**Problem:** Authentication failed
```bash
# Solution: Check credentials
type .env | findstr GMAIL

# Re-setup if needed
python setup_gmail_login.py
```

**Problem:** IMAP watcher not connecting
```bash
# Solution: Test connection
ping imap.gmail.com

# Check if IMAP is enabled in Gmail settings
# Gmail → Settings → Forwarding and POP/IMAP → Enable IMAP
```

### LinkedIn Issues

**Problem:** Safety check shows RED
```bash
# Solution: Wait for next safe window
python linkedin_safety_check.py
# Check the "Next Safe Window" time shown
```

**Problem:** Session expired
```bash
# Solution: Re-login
python setup_linkedin_login.py
```

### WhatsApp Issues

**Problem:** Network error
```bash
# Solution: Test connection
ping api.twilio.com

# Check credentials
type .env | findstr TWILIO
```

**Problem:** Message not received
```bash
# Solution: Verify sandbox setup
# 1. Check if you joined sandbox
# 2. Verify phone number format: whatsapp:+1234567890
# 3. Check Twilio console for logs
```

### Directory Issues

**Problem:** "can't open file" error
```bash
# Solution: Check current directory
cd

# If in root, use: python Platinum_Tier\script.py
# If in Platinum_Tier, use: python script.py
```

See `.claude\GMAIL_DIRECTORY_GUIDE.md` for detailed directory guidance.

---

## 📖 Documentation

All documentation is in the `.claude` directory:

| File | Description |
|------|-------------|
| `ALL_COMMANDS.md` | Master command reference |
| `GMAIL_COMMANDS.md` | Gmail send/receive guide |
| `GMAIL_DIRECTORY_GUIDE.md` | Directory-specific commands |
| `LINKEDIN_COMMANDS.md` | LinkedIn with safety rules |
| `WHATSAPP_COMMANDS.md` | WhatsApp send/receive guide |
| `MANUAL_TESTING_GUIDE.md` | Complete testing workflow |
| `QUICK_REFERENCE_CARD.md` | Daily quick reference |
| `COMPLETE_TESTING_SUMMARY.md` | Current system status |

**View any guide:**
```bash
type .claude\ALL_COMMANDS.md
```

---

## 🎯 Next Steps

After successful setup:

1. **Test all platforms:**
   ```bash
   python quick_test.py
   ```

2. **Start Gmail monitoring:**
   ```bash
   START_GMAIL_WATCHER.bat
   ```

3. **Check LinkedIn safety:**
   ```bash
   python linkedin_safety_check.py
   ```

4. **Review documentation:**
   ```bash
   type .claude\QUICK_REFERENCE_CARD.md
   ```

5. **Start using the system:**
   - Send test emails
   - Monitor inbox
   - Post to LinkedIn (when safe)
   - Send WhatsApp messages

---

## 🆘 Getting Help

If you encounter issues:

1. **Check logs:**
   ```bash
   type AI_Employee_Vault\Logs\gmail_watcher_imap.log
   type AI_Employee_Vault\Logs\gmail_sender.log
   ```

2. **Review documentation:**
   - See `.claude` directory for detailed guides
   - Check `README.md` for overview

3. **Common issues:**
   - Wrong directory: See `.claude\GMAIL_DIRECTORY_GUIDE.md`
   - Credentials: Check `.env` file
   - Network: Test with `ping` commands

4. **Open an issue:**
   - GitHub Issues: [Your repo URL]/issues

---

## ✅ Setup Complete!

You're now ready to use the AI Personal Employee system.

**Quick Start Commands:**
```bash
# Test everything
python quick_test.py

# Start Gmail monitoring
START_GMAIL_WATCHER.bat

# Check LinkedIn safety
python linkedin_safety_check.py

# View quick reference
type .claude\QUICK_REFERENCE_CARD.md
```

---

**Last Updated:** 2026-02-20
**Version:** 1.0.0

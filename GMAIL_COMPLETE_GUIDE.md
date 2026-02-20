# Gmail Automation - Complete Guide

## ✓ Setup Complete

Both Gmail reading (IMAP) and sending (SMTP) are fully configured and working!

---

## Quick Start

### Start Complete Gmail System
```bash
RUN_GMAIL_COMPLETE.bat
```

This starts:
1. **Gmail Watcher** - Monitors inbox every 3 minutes
2. **Gmail Sender** - Automatically sends approved emails

---

## How It Works

### 1. Incoming Emails (READ)

**Gmail Watcher monitors your inbox:**
- Checks every 3 minutes
- Looks for Agentic AI keywords: `agentic`, `ai agent`, `llm`, `claude`, `gpt`, etc.
- Saves detected emails to: `AI_Employee_Vault/Needs_Action/`

**Example detected email:**
```
AI_Employee_Vault/Needs_Action/
└── EMAIL_20260220_123456_sender_name.md
```

### 2. Outgoing Emails (SEND/REPLY)

**Create email in Approved folder:**

Create file: `AI_Employee_Vault/Approved/REPLY_pricing_inquiry.md`

```markdown
---
to: client@example.com
subject: Re: Pricing Inquiry for AI Services
cc: team@yourcompany.com
---

Hi [Client Name],

Thank you for your inquiry about our AI services.

Our pricing structure is as follows:
- Basic Plan: $99/month
- Professional Plan: $299/month
- Enterprise Plan: Custom pricing

Would you like to schedule a call to discuss your specific needs?

Best regards,
Your Name
```

**Gmail Sender automatically:**
- Detects new file in Approved/
- Sends email via Gmail SMTP
- Moves file to Done/
- Logs everything

---

## File Format for Sending Emails

```markdown
---
to: recipient@example.com
subject: Email Subject Here
cc: optional-cc@example.com
bcc: optional-bcc@example.com
---

Email body goes here.

You can use multiple paragraphs.

Best regards,
Your Name
```

**Required fields:**
- `to:` - Recipient email
- `subject:` - Email subject

**Optional fields:**
- `cc:` - Carbon copy
- `bcc:` - Blind carbon copy

---

## Folder Structure

```
AI_Employee_Vault/
├── Needs_Action/       # Detected incoming emails
├── Approved/           # Emails ready to send (put your replies here)
├── Done/               # Sent emails (archived)
└── Logs/
    ├── gmail_watcher_imap.log
    ├── gmail_sender.log
    └── gmail_approval_handler.log
```

---

## Complete Workflow Example

### Scenario: Client sends pricing inquiry

**Step 1: Email arrives**
```
From: client@example.com
Subject: Pricing inquiry for AI automation
Body: "I'm interested in your agentic AI services..."
```

**Step 2: Gmail Watcher detects it**
- Sees "agentic AI" keyword
- Saves to: `AI_Employee_Vault/Needs_Action/EMAIL_20260220_143000_client.md`

**Step 3: You review and create reply**
- Read the email in Needs_Action/
- Create reply file in Approved/

File: `AI_Employee_Vault/Approved/REPLY_pricing_20260220.md`
```markdown
---
to: client@example.com
subject: Re: Pricing inquiry for AI automation
---

Hi there,

Thank you for your interest in our AI automation services!

I'd be happy to discuss pricing with you. Our solutions start at $299/month
for the basic package, with enterprise options available.

Would you like to schedule a 15-minute call this week?

Best regards,
[Your Name]
```

**Step 4: Gmail Sender automatically sends**
- Detects new file in Approved/
- Sends email via SMTP
- Moves to Done/
- Logs the action

**Step 5: Done!**
- Email sent ✓
- Archived in Done/ ✓
- Logged ✓

---

## Testing

### Test 1: Send yourself an email
```bash
cd Platinum_Tier
python gmail_sender_smtp.py
```

This sends a test email to your inbox.

### Test 2: Full workflow test

1. Send yourself an email with "agentic AI" in subject
2. Wait 3 minutes
3. Check `AI_Employee_Vault/Needs_Action/`
4. Create reply in `AI_Employee_Vault/Approved/`
5. Watch it get sent automatically!

---

## Commands

### Start complete system
```bash
RUN_GMAIL_COMPLETE.bat
```

### Start watcher only (read emails)
```bash
RUN_GMAIL_WATCHER.bat
```

### Test SMTP connection
```bash
cd Platinum_Tier
python gmail_sender_smtp.py
```

### Test IMAP connection
```bash
python test_gmail_simple.py
```

---

## Monitoring

### Check logs
```bash
type AI_Employee_Vault\Logs\gmail_watcher_imap.log
type AI_Employee_Vault\Logs\gmail_sender.log
type AI_Employee_Vault\Logs\gmail_approval_handler.log
```

### Check what's running
```bash
tasklist | findstr python
```

---

## Security

- ✓ App Password stored in `.env` (not committed to git)
- ✓ `.env` in `.gitignore`
- ✓ Human approval required before sending
- ✓ All actions logged
- ✓ Can revoke App Password anytime

---

## Troubleshooting

### Emails not being detected
- Check keywords match: `agentic`, `ai agent`, `llm`, `claude`, `gpt`
- Check logs: `AI_Employee_Vault\Logs\gmail_watcher_imap.log`
- Verify watcher is running

### Emails not being sent
- Check file format (frontmatter with `---`)
- Verify file is in `Approved/` folder
- Check logs: `AI_Employee_Vault\Logs\gmail_sender.log`
- Verify sender is running

### Authentication errors
- Verify App Password in `.env` is correct (16 characters, no spaces)
- Regenerate App Password if needed
- Check IMAP/SMTP are enabled in Gmail settings

---

## What's Next?

Your Gmail automation is **fully operational**. You can now:

1. ✓ Monitor Gmail for AI-related emails
2. ✓ Send automated replies with approval
3. ✓ Run 24/7 autonomously
4. ✓ Full audit logging

**Status: PRODUCTION READY** 🚀

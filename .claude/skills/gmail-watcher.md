# Gmail Watcher Skill

Start the Gmail monitoring system that watches for emails with "Agentic AI" keywords and saves them to Needs_Action folder.

## When to Use

Use this skill when:
- Starting the AI Employee system
- User asks to "monitor Gmail" or "watch emails"
- Need to check for new urgent emails

## Step-by-Step Instructions

### 1. Check Prerequisites

Verify required files exist:
```bash
ls Platinum_Tier/gmail_watcher_imap.py
grep GMAIL_EMAIL .env
grep GMAIL_PASSWORD .env
```

### 2. Start the Watcher

Run the Gmail watcher:
```bash
cd Platinum_Tier
python gmail_watcher_imap.py
```

### 3. What It Does

The watcher will:
- Connect to Gmail via IMAP (fully automated)
- Check inbox every 3 minutes
- Filter emails with keywords: agentic, ai agent, llm, claude, gpt
- Save detected emails to AI_Employee_Vault/Needs_Action/
- Run continuously until stopped (Ctrl+C)

NO manual login required - uses IMAP with App Password

### 4. Monitor Output

Watch for these log messages:
- `[OK] Connected to Gmail successfully!` - Connection established
- `Found X unread email(s)` - Emails detected
- `[AGENTIC AI] Email from [sender]` - Relevant email found
- `[SAVED] EMAIL_[timestamp].md` - Email saved

### 5. Test Detection

To test:
1. Send yourself an email with "agentic AI" in subject or body
2. Wait 3 minutes for next check
3. Verify email appears in Needs_Action/

## Important Rules

1. **Use Gmail App Password** (not regular password)
2. **NEVER commit .env file to Git**
3. **Check logs regularly** for errors
4. **Monitor Needs_Action/** folder

## Example Usage

```
User: /gmail-watcher
Assistant: Starting Gmail watcher...
✓ gmail_watcher_imap.py found
✓ .env credentials configured
[OK] Connected to Gmail successfully!
[OK] Monitoring inbox every 3 minutes
Watcher is running. Press Ctrl+C to stop.
```

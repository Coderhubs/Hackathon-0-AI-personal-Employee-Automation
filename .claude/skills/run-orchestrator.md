# Run Orchestrator Skill

Start the complete AI Employee system with all watchers, coordinators, and automation components.

## When to Use

Use this skill when:
- Starting a work session
- User asks to "start the system" or "run everything"
- Need full automation running

## Step-by-Step Instructions

### 1. Check Prerequisites

```bash
ls Platinum_Tier/gmail_watcher_imap.py
ls Platinum_Tier/linkedin_automation.py
ls integration_coordinator.py
ls approval_handler_automated.py
grep GMAIL_EMAIL .env
```

### 2. Start All Components

Use the batch file:
```bash
START_FULLY_AUTOMATED.bat
```

Or start manually:
```bash
# 1. WhatsApp Automation
start "WhatsApp" cmd /k "node Platinum_Tier/whatsapp_automation.js"

# 2. Gmail Watcher
start "Gmail" cmd /k "cd Platinum_Tier && python gmail_watcher_imap.py"

# 3. LinkedIn Automation
start "LinkedIn" cmd /k "cd Platinum_Tier && python linkedin_automation.py"

# 4. Integration Coordinator
start "Coordinator" cmd /k "python integration_coordinator.py"

# 5. Approval Handler
start "Handler" cmd /k "python approval_handler_automated.py"
```

### 3. System Components

5 Components will start:
1. **WhatsApp Automation** - Monitors chats (QR scan first time)
2. **Gmail Watcher** - Monitors inbox (fully automated)
3. **LinkedIn Automation** - Monitors and posts (persistent session)
4. **Integration Coordinator** - Processes detected items
5. **Approval Handler** - Executes approved actions

### 4. First-Time Setup

**WhatsApp (First Time Only):**
- Window opens, scan QR code with phone
- Session saved, never scan again

**LinkedIn (First Time Only):**
- Browser opens, system logs in automatically
- Session saved, never login again

**Gmail (Already Automated):**
- No setup needed, works immediately

### 5. Verify System Running

Check all components started:
```bash
ps aux | grep -E "gmail_watcher|linkedin_automation|whatsapp_automation|integration_coordinator|approval_handler"
```

Should show 5 processes.

### 6. Test the System

1. Send test email with "agentic AI" keyword
2. Wait 3 minutes for detection
3. Check Needs_Action/ for saved email
4. Wait for draft in Pending_Approval/
5. Approve by moving to Approved/
6. Verify execution in Done/

### 7. User Instructions

Tell user:
```
System Running Successfully!
============================

5 Components Active:
✓ Gmail Watcher
✓ LinkedIn Automation
✓ WhatsApp Automation
✓ Integration Coordinator
✓ Approval Handler

Your Actions:
- Review: AI_Employee_Vault/Pending_Approval/
- Approve: Move files to Approved/
- Monitor: AI_Employee_Vault/Dashboard.md

To Stop: Close all terminal windows
```

## Important Rules

1. **Start components in order**
2. **Wait for each to initialize**
3. **Complete first-time setup**
4. **Monitor all terminals** for errors

## Example Usage

```
User: /run-orchestrator
Assistant: Starting complete AI Employee system...

✓ All prerequisites found
✓ .env credentials configured

Starting components...
[1/5] WhatsApp Automation... STARTED
[2/5] Gmail Watcher... STARTED
[3/5] LinkedIn Automation... STARTED
[4/5] Integration Coordinator... STARTED
[5/5] Approval Handler... STARTED

All components running!
System ready to process incoming items.
```

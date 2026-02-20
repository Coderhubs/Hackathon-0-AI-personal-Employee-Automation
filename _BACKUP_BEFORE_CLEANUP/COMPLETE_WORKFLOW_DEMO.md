# Complete Workflow Demo - Gmail Monitoring + Email Sending

## How It Works End-to-End

### 1. Gmail Watcher (Playwright) - MONITORS Emails
**File:** `Platinum_Tier/gmail_watcher_hackathon.py`

**What it does:**
- Opens Gmail using Playwright browser automation
- Checks inbox every 180 seconds (3 minutes)
- Looks for emails containing BOTH:
  - "urgent" keyword
  - "agentic AI" related keywords (agentic, ai agent, autonomous ai, llm, claude, gpt, etc.)
- Creates task files in `AI_Employee_Vault/Needs_Action/`

**Example:**
```
Someone sends you: "URGENT: Need help with agentic AI project"
↓
Gmail Watcher detects it
↓
Creates: AI_Employee_Vault/Needs_Action/gmail_20260218_001234.md
```

### 2. HITL Approval Handler - PROCESSES Tasks
**File:** `approval_handler.py`

**What it does:**
- Monitors `Pending_Approval/` folder
- When you move a task to `Approved/` folder
- Executes the action (like sending email)
- Moves completed task to `Done/`

### 3. Email MCP Server - SENDS Emails
**File:** `mcp_servers/email-mcp/index.js`

**What it does:**
- Provides `send_email` tool
- Sends emails via Gmail using nodemailer
- Supports plain text and HTML emails

**Example:**
```javascript
send_email({
  to: "client@example.com",
  subject: "Project Update",
  body: "Here's the update you requested..."
})
```

---

## Complete Demo Workflow

### Step 1: Start the System
```bash
RUN_PLATINUM_TIER.bat
```

This starts:
1. Gmail Watcher (monitors inbox with Playwright)
2. LinkedIn Watcher
3. WhatsApp Watcher
4. HITL Approval Handler (processes approved tasks)
5. Autonomous Monitor
6. CEO Briefing Generator
7. Multi-Agent Coordinator
8. REST API Server

### Step 2: Receive Urgent Email
Someone sends you an email:
```
From: client@example.com
Subject: URGENT: Agentic AI Implementation
Body: We need help with our agentic AI project ASAP!
```

### Step 3: Gmail Watcher Detects It
```
[Gmail Watcher] Checking inbox...
[Gmail Watcher] Found urgent email about agentic AI
[Gmail Watcher] Creating task file...
[Gmail Watcher] Saved to: AI_Employee_Vault/Needs_Action/gmail_20260218_001234.md
```

Task file created:
```markdown
---
source: gmail
sender: client@example.com
subject: URGENT: Agentic AI Implementation
timestamp: 2026-02-18T00:12:34
priority: high
keywords: urgent, agentic, ai
---

# Urgent Email from client@example.com

**Subject:** URGENT: Agentic AI Implementation

**Content:**
We need help with our agentic AI project ASAP!

**Action Required:**
Review and respond to this urgent request.
```

### Step 4: Autonomous Monitor Creates Plan
```
[Autonomous Monitor] New task detected
[Autonomous Monitor] Creating execution plan...
[Autonomous Monitor] Analyzing sensitivity...
[Autonomous Monitor] Action: send_email (SENSITIVE)
[Autonomous Monitor] Moving to Pending_Approval/
```

### Step 5: Human Approval (You)
You review the plan and move it to `Approved/` folder:
```
AI_Employee_Vault/Pending_Approval/gmail_20260218_001234.md
→ Move to →
AI_Employee_Vault/Approved/gmail_20260218_001234.md
```

### Step 6: HITL Handler Executes
```
[HITL Handler] New approved task detected
[HITL Handler] Action type: send_email
[HITL Handler] Calling Email MCP server...
[Email MCP] Sending email to client@example.com...
[Email MCP] Email sent successfully! Message ID: <abc123@gmail.com>
[HITL Handler] Task completed, moving to Done/
```

### Step 7: Email Sent!
The client receives your response:
```
From: your_email@gmail.com
To: client@example.com
Subject: Re: URGENT: Agentic AI Implementation
Body: Thank you for reaching out. I've reviewed your request...
```

---

## Manual Email Sending Demo

You can also send emails directly via the REST API:

### Using REST API
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Send email to john@example.com about project update",
    "task_type": "email",
    "priority": 8,
    "metadata": {
      "to": "john@example.com",
      "subject": "Project Update",
      "body": "Here is the latest update on our project..."
    }
  }'
```

### Using Task File
Create a file in `AI_Employee_Vault/Needs_Action/`:

```markdown
---
source: manual
action: send_email
to: john@example.com
subject: Project Update
priority: high
---

# Send Project Update Email

Send an email to john@example.com with the following content:

Dear John,

Here is the latest update on our project:
- Phase 1: Complete
- Phase 2: In progress
- Expected completion: Next week

Best regards
```

---

## Key Features

### 1. Dual Monitoring + Action
- **Monitors:** Gmail, LinkedIn, WhatsApp (with Playwright)
- **Actions:** Send emails, create tasks, generate reports

### 2. HITL Approval
- Sensitive actions (emails, payments) require human approval
- Non-sensitive actions execute automatically

### 3. Multi-Channel
- Receive requests via Gmail, LinkedIn, WhatsApp, REST API
- Respond via Email MCP server

### 4. Intelligent Routing
- Multi-agent coordinator routes tasks to specialized agents
- Email tasks → Executor agent
- Research tasks → Researcher agent

---

## Testing the Email Functionality

### Test 1: Send Test Email
```bash
# Create test task
echo "---
source: test
action: send_email
to: your_test_email@gmail.com
subject: Test Email from AI Employee
priority: medium
---

# Test Email

This is a test email from the AI Personal Employee system.

If you receive this, the email functionality is working!" > AI_Employee_Vault/Approved/test_email.md

# HITL handler will pick it up and send it
```

### Test 2: Check Email MCP Server
```bash
cd mcp_servers/email-mcp
npm install
node index.js
```

---

## Summary

**YES, the system can:**
1. ✅ Monitor Gmail for urgent emails (Playwright)
2. ✅ Detect "agentic AI" keywords
3. ✅ Create task files automatically
4. ✅ Send emails to people (Email MCP)
5. ✅ Require human approval for sensitive actions
6. ✅ Track everything in logs

**Complete Flow:**
```
Incoming Email (Playwright monitors Gmail)
↓
Gmail Watcher detects urgent + agentic AI
↓
Creates task in Needs_Action/
↓
Autonomous Monitor creates plan
↓
Moves to Pending_Approval/ (if sensitive)
↓
Human approves (moves to Approved/)
↓
HITL Handler executes
↓
Email MCP sends response
↓
Task moves to Done/
↓
Logged in Logs/
```

---

**Built with:**
- Playwright (browser automation for monitoring)
- Nodemailer (email sending via Gmail)
- MCP SDK (Model Context Protocol)
- FastAPI (REST API)
- Claude Code (AI coordination)

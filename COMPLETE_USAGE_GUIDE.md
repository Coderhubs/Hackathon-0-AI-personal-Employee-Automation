
# COMPLETE SYSTEM USAGE GUIDE
## Persistent Authentication & Execution Layer

## IMPLEMENTATION COMPLETE

All phases have been successfully implemented:

### Phase 1: Persistent Authentication
- Gmail watcher uses persistent browser context
- LinkedIn watcher uses persistent browser context
- WhatsApp watcher uses persistent browser context
- All watchers check for existing sessions before login

### Phase 2: Execution Engine
- `Platinum_Tier/mcp_client.py` - MCP email server wrapper
- `Platinum_Tier/execution_engine.py` - LinkedIn & WhatsApp executors
- Retry logic with exponential backoff (3 attempts)

### Phase 3: Approval Handler
- `approval_handler.py` - Complete execution methods
- Actually sends emails via MCP server
- Actually posts to LinkedIn via Playwright
- Actually sends WhatsApp messages via Playwright

---

## FIRST-TIME SETUP

### Step 1: Login to Gmail (One Time Only)
```bash
cd Platinum_Tier
python gmail_watcher_playwright.py
```

**What happens:**
1. Browser opens to Gmail login page
2. Login manually with your credentials
3. Session is saved to `browser_data/gmail/`
4. Watcher starts monitoring inbox

**Next time:** Watcher will skip login and use saved session!

### Step 2: Login to LinkedIn (One Time Only)
```bash
cd Platinum_Tier
python linkedin_watcher_playwright.py
```

**What happens:**
1. Browser opens to LinkedIn login page
2. Login manually with your credentials
3. Session is saved to `browser_data/linkedin/`
4. Watcher starts monitoring feed

**Next time:** Watcher will skip login and use saved session!

### Step 3: Login to WhatsApp (One Time Only)
```bash
cd Platinum_Tier
python whatsapp_watcher_hackathon.py
```

**What happens:**
1. Browser opens to WhatsApp Web
2. Scan QR code with your phone
3. Session is saved to `browser_data/whatsapp/`
4. Watcher starts monitoring chats

**Next time:** Watcher will skip QR scan and use saved session!

---

## VERIFY PERSISTENT AUTHENTICATION

### Test Gmail Persistence
```bash
# Start watcher
cd Platinum_Tier
python gmail_watcher_playwright.py

# Stop it (Ctrl+C)
# Start again - should NOT ask for login!
python gmail_watcher_playwright.py
```

**Expected:** Browser opens directly to inbox, no login prompt

### Test LinkedIn Persistence
```bash
# Start watcher
cd Platinum_Tier
python linkedin_watcher_playwright.py

# Stop it (Ctrl+C)
# Start again - should NOT ask for login!
python linkedin_watcher_playwright.py
```

**Expected:** Browser opens directly to feed, no login prompt

### Test WhatsApp Persistence
```bash
# Start watcher
cd Platinum_Tier
python whatsapp_watcher_hackathon.py

# Stop it (Ctrl+C)
# Start again - should NOT ask for QR scan!
python whatsapp_watcher_hackathon.py
```

**Expected:** Browser opens directly to chats, no QR scan prompt

---

## COMPLETE WORKFLOW TEST

### Test 1: Email Workflow (End-to-End)

**Step 1:** Start Gmail watcher
```bash
cd Platinum_Tier
python gmail_watcher_playwright.py
```

**Step 2:** Send yourself a test email with "agentic AI" keyword
- Subject: "Test Agentic AI automation"
- Body: "Testing the autonomous email system"

**Step 3:** Verify watcher detects it
- Check console logs: "Found 1 new Agentic AI email(s)"
- Check `Inbox/` folder for saved email

**Step 4:** Run integration coordinator (if not already running)
```bash
python integration_coordinator.py
```

**Step 5:** Check `Pending_Approval/` folder
- Should contain draft email reply

**Step 6:** Approve the draft
```bash
# Move file from Pending_Approval to Approved
move AI_Employee_Vault/Pending_Approval/EMAIL_REPLY_*.md AI_Employee_Vault/Approved/
```

**Step 7:** Start approval handler
```bash
python approval_handler.py
```

**Step 8:** Verify email is ACTUALLY SENT
- Check console logs: "Email sent successfully"
- Check your inbox for the reply
- Check `Done/` folder for execution log

**SUCCESS:** Email was sent automatically!

---

### Test 2: LinkedIn Workflow (End-to-End)

**Step 1:** Create a LinkedIn post approval file manually
```bash
# Create: AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_test.md
```

Content:
```markdown
---
type: linkedin_post
action: post_linkedin
post_type: test
created: 2026-02-18T20:00:00
status: pending_approval
---

# LinkedIn Post - PENDING APPROVAL

## Post Content

Testing the autonomous LinkedIn posting system!

This post was created by an AI automation system and approved by a human.

#AI #Automation #Testing
```

**Step 2:** Approve the post
```bash
move AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_test.md AI_Employee_Vault/Approved/
```

**Step 3:** Start approval handler (if not running)
```bash
python approval_handler.py
```

**Step 4:** Verify post is ACTUALLY CREATED
- Check console logs: "LinkedIn post created successfully"
- Check your LinkedIn profile for the new post
- Check `Done/` folder for execution log

**SUCCESS:** LinkedIn post was published automatically!

---

### Test 3: WhatsApp Workflow (End-to-End)

**Step 1:** Create a WhatsApp message approval file manually
```bash
# Create: AI_Employee_Vault/Pending_Approval/WHATSAPP_MESSAGE_test.md
```

Content:
```markdown
---
type: whatsapp_message
action: send_whatsapp
contact: Your Contact Name
created: 2026-02-18T20:00:00
status: pending_approval
---

# WhatsApp Message - PENDING APPROVAL

## Message Content

Testing the autonomous WhatsApp messaging system!

This message was created by AI automation and approved by a human.
```

**Step 2:** Approve the message
```bash
move AI_Employee_Vault/Pending_Approval/WHATSAPP_MESSAGE_test.md AI_Employee_Vault/Approved/
```

**Step 3:** Start approval handler (if not running)
```bash
python approval_handler.py
```

**Step 4:** Verify message is ACTUALLY SENT
- Check console logs: "WhatsApp message sent to [contact]"
- Check WhatsApp for the sent message
- Check `Done/` folder for execution log

**SUCCESS:** WhatsApp message was sent automatically!

---

## RUNNING THE COMPLETE SYSTEM

### Start All Components

**Terminal 1: Gmail Watcher**
```bash
cd Platinum_Tier
python gmail_watcher_playwright.py
```

**Terminal 2: LinkedIn Watcher**
```bash
cd Platinum_Tier
python linkedin_watcher_playwright.py
```

**Terminal 3: WhatsApp Watcher**
```bash
cd Platinum_Tier
python whatsapp_watcher_hackathon.py
```

**Terminal 4: Integration Coordinator**
```bash
python integration_coordinator.py
```

**Terminal 5: Approval Handler**
```bash
python approval_handler.py
```

**Terminal 6: LinkedIn Content Generator (optional)**
```bash
python linkedin_content_generator.py
```

---

## WHAT HAPPENS NOW

### Autonomous Workflow:

1. **Watchers Monitor** (24/7, no manual login)
   - Gmail checks inbox every 3 minutes
   - LinkedIn checks feed every 2 minutes
   - WhatsApp checks chats every 30 seconds

2. **Detection & Filtering**
   - Emails/posts/messages with "agentic AI" keywords detected
   - Saved to `Needs_Action/` folder

3. **Draft Generation**
   - Integration coordinator processes `Needs_Action/`
   - Generates contextual draft replies
   - Moves to `Pending_Approval/`

4. **Human Approval** (YOU decide)
   - Review drafts in `Pending_Approval/`
   - Move to `Approved/` to execute
   - Move to `Rejected/` to discard

5. **Automatic Execution**
   - Approval handler monitors `Approved/`
   - Emails: Sent via MCP server
   - LinkedIn: Posted via Playwright
   - WhatsApp: Sent via Playwright
   - Execution logged to `Done/`

---

## ERROR HANDLING

### Session Expired
- Watcher detects login page
- Logs warning: "No active session found. Logging in..."
- Waits for manual login
- Saves new session

### Rate Limiting
- Executor retries with exponential backoff (1s, 2s, 4s)
- Logs all retry attempts
- Fails after 3 attempts

### Network Failure
- Automatic retry with backoff
- Logs error details
- Moves to `Done/` with failure status

### MCP Server Down
- Logs clear error: "MCP server not found"
- Provides instructions to start server
- Does not crash

---

## SUCCESS CRITERIA

After implementation, your system:

1. ✓ Watchers run autonomously without manual login (after first time)
2. ✓ Approved emails are actually sent via Gmail
3. ✓ Approved LinkedIn posts are actually published
4. ✓ Approved WhatsApp messages are actually sent
5. ✓ All executions are logged with timestamps
6. ✓ Errors are handled gracefully with retries
7. ✓ System runs 24/7 without human intervention (except approvals)

**You now have a fully autonomous AI employee!**

---

## TROUBLESHOOTING

### "MCP client not available"
- Check if `Platinum_Tier/mcp_client.py` exists
- Check if Node.js is installed: `node --version`
- Check if MCP server exists: `mcp_servers/email-mcp/index.js`

### "Not logged in to LinkedIn"
- Run LinkedIn watcher once manually
- Login and wait for feed to load
- Session will be saved automatically

### "WhatsApp not logged in"
- Run WhatsApp watcher once manually
- Scan QR code with phone
- Session will be saved automatically

### "Email failed: MCP server failed"
- Check .env file has GMAIL_EMAIL and GMAIL_PASSWORD
- Test MCP server: `node mcp_servers/email-mcp/index.js`
- Check Gmail App Password is correct

---

## FILES CREATED/MODIFIED

### New Files:
- `Platinum_Tier/mcp_client.py` - MCP email server wrapper
- `Platinum_Tier/execution_engine.py` - LinkedIn & WhatsApp executors
- `test_complete_system.py` - Comprehensive test suite

### Modified Files:
- `Platinum_Tier/gmail_watcher_playwright.py` - Added persistent context
- `Platinum_Tier/linkedin_watcher_playwright.py` - Added persistent context
- `approval_handler.py` - Completed execution methods

### Browser Data (Auto-created):
- `Platinum_Tier/browser_data/gmail/` - Gmail session
- `Platinum_Tier/browser_data/linkedin/` - LinkedIn session
- `Platinum_Tier/browser_data/whatsapp/` - WhatsApp session

---

## NEXT STEPS

1. Run `python test_complete_system.py` to verify installation
2. Login to each platform once (Gmail, LinkedIn, WhatsApp)
3. Restart watchers to verify persistent authentication
4. Test complete workflow with real email/post/message
5. Let the system run 24/7 and monitor execution logs

**Your AI Personal Employee is now fully operational!**

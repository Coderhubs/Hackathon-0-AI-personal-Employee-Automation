# WhatsApp Watcher - Complete Explanation

## How It Works

### Architecture Flow
```
WhatsApp Web → Browser Automation → Keyword Detection → File Creation → Claude Processing
```

### Step-by-Step Process

#### 1. Browser Initialization (Lines 24-54)
```python
async def initialize_browser(self):
    # Uses Playwright to launch Chromium
    # Persistent session saves login state
    # Opens WhatsApp Web (https://web.whatsapp.com)
    # Waits for QR code scan OR existing session
```

**What happens:**
- Opens Chromium browser (visible, not headless)
- Loads saved session from `Platinum_Tier/browser_data/whatsapp/`
- If first time: Shows QR code, you scan with phone
- If returning: Automatically logged in (session saved)
- Waits up to 2 minutes for login confirmation

#### 2. Message Monitoring (Lines 56-120)
```python
async def _async_check_for_updates(self) -> list:
    # Refreshes page to get latest messages
    # Finds unread chats using aria-label="unread"
    # Extracts sender name and message preview
    # Checks against keyword filters
```

**What happens every 30 seconds:**
1. Page refreshes to load new messages
2. Searches for unread chat indicators
3. For each unread chat (max 10):
   - Extracts sender name
   - Extracts message preview text
   - Creates unique message ID
   - Checks if already processed (seen_messages set)
   - Filters by keywords

#### 3. Keyword Filtering (Lines 19-20, 91-96)

**Two Keyword Sets:**

**Urgent Keywords:**
- urgent, asap, invoice, payment, help, emergency, important

**Agentic AI Keywords:**
- agentic, ai agent, autonomous ai, llm, claude, gpt

**Filter Logic:**
```python
text_lower = f"{name} {message}".lower()
is_urgent = any(kw in text_lower for kw in self.urgent_keywords)
is_agentic = any(kw in text_lower for kw in self.agentic_keywords)

if is_urgent or is_agentic:
    # Create action file
```

**Examples:**
- "URGENT: Need help with invoice" → HIGH priority (urgent)
- "Question about AI agents" → MEDIUM priority (agentic)
- "Can you help with Claude API?" → MEDIUM priority (agentic)
- "ASAP payment needed" → HIGH priority (urgent)

#### 4. Priority Assignment (Lines 127-133)
```python
if msg['is_urgent']:
    priority = 'high'
elif msg['is_agentic']:
    priority = 'medium'
else:
    priority = 'low'
```

#### 5. File Creation (Lines 122-197)

**Creates TWO files:**

**A) Needs_Action File (Markdown with Frontmatter)**
```markdown
---
type: whatsapp_message
from: John Doe
message_id: John_Doe_URGENT_Need_help_221530
received: 2026-02-17T22:15:30Z
priority: high
status: pending
category: urgent, agentic_ai
---

## Message Content
URGENT: Need help with AI agent implementation

## Suggested Actions
- [ ] Read full conversation
- [ ] Draft reply
- [ ] Check if invoice/payment needed
- [ ] Escalate if urgent
- [ ] Send reply (requires approval)
- [ ] Mark as resolved
- [ ] Update Dashboard

## Context
This message was detected by WhatsApp watcher.

**Urgency:** YES - Contains urgent keywords
**Agentic AI Related:** YES - Contains Agentic AI keywords

Urgent keywords matched: urgent, help
Agentic keywords matched: ai agent

## Response Guidelines
1. If urgent: Respond within 1 hour
2. If invoice/payment: Check Company_Handbook.md for approval rules
3. If Agentic AI question: Provide detailed technical response
4. Always be professional and helpful
```

**B) Inbox File (Plain Text Reference)**
```
From: John Doe
Date: 2026-02-17T22:15:30Z
Priority: high
Category: urgent, agentic_ai

URGENT: Need help with AI agent implementation
```

### Technical Details

#### Browser Automation
- **Tool:** Playwright (async API)
- **Browser:** Chromium
- **Mode:** Non-headless (visible browser)
- **Session:** Persistent (saved to disk)
- **Selectors:**
  - Chat list: `[data-testid="chat-list"]`
  - Unread chats: `[aria-label*="unread"]`
  - Sender name: `[dir="auto"]`
  - Message text: `.matched-text` or `[dir="ltr"]`

#### Performance
- **Check Interval:** 30 seconds (fastest watcher)
- **Max Chats Per Check:** 10 unread chats
- **Timeout:** 120 seconds for initial login
- **Refresh Wait:** 3 seconds after page reload

#### Deduplication
```python
self.seen_messages = set()
message_id = f"{name}_{message[:30]}_{timestamp}"

if message_id not in self.seen_messages:
    # Process message
    self.seen_messages.add(message_id)
```

Prevents processing same message multiple times.

### Integration with Hackathon Architecture

```
WhatsApp Web
    ↓
WhatsApp Watcher (30s interval)
    ↓
Keyword Filter (urgent + agentic)
    ↓
Needs_Action/WHATSAPP_*.md (with frontmatter)
    ↓
Claude Code reads file
    ↓
/process-inbox skill
    ↓
Plans/PLAN_*.md
    ↓
Done/WHATSAPP_*.md
```

### Why WhatsApp is Special

1. **Fastest Check Interval:** 30 seconds vs 120-180 for others
2. **Dual Filtering:** Both urgent AND agentic keywords
3. **High Priority Focus:** Urgent messages get immediate attention
4. **Business Critical:** Invoices, payments, emergencies
5. **Real-time Communication:** Most immediate channel

### Comparison with Other Watchers

| Feature | Gmail | LinkedIn | WhatsApp |
|---------|-------|----------|----------|
| Check Interval | 180s | 120s | 30s |
| Keywords | Agentic AI | Agentic AI | Urgent + Agentic |
| Priority | Medium | Medium | High/Medium |
| Use Case | Professional emails | Industry posts | Urgent messages |
| Authentication | Email/Password | Email/Password | QR Code |
| Session Type | Persistent | Persistent | Persistent |

### Running the Watcher

**Option 1: Individual**
```bash
cd Platinum_Tier
python whatsapp_watcher_hackathon.py
```

**Option 2: With All Watchers**
```bash
RUN_DEMO.bat
```

**Option 3: Via Orchestrator**
```bash
START_ALL_WATCHERS.bat
```

### First-Time Setup

1. Run the watcher
2. Browser opens to WhatsApp Web
3. Scan QR code with your phone:
   - Open WhatsApp on phone
   - Tap Menu (3 dots) → Linked Devices
   - Tap "Link a Device"
   - Scan QR code in browser
4. Session saved automatically
5. Next time: Auto-login (no QR needed)

### Testing

**Send test message to yourself:**
1. Open WhatsApp on phone
2. Send message to any contact: "URGENT: Test AI agent question"
3. Wait 30 seconds
4. Check console: "Found URGENT message from: [name]"
5. Check file: `AI_Employee_Vault/Needs_Action/WHATSAPP_*.md`

### Troubleshooting

**QR Code doesn't appear:**
- Clear browser_data/whatsapp/ folder
- Restart watcher
- Scan QR code again

**Messages not detected:**
- Check keywords match (case-insensitive)
- Ensure messages are unread
- Wait full 30 seconds for next check
- Check console logs for errors

**Browser crashes:**
- Close other Chrome/Chromium instances
- Restart watcher
- Check system resources

### Security

- **Session Storage:** Local only (browser_data/whatsapp/)
- **No Cloud Sync:** All data stays on your machine
- **No Message Storage:** Only previews, not full conversations
- **Credentials:** No passwords needed (QR code auth)
- **Privacy:** Respects WhatsApp's terms of service

### Hackathon Compliance

✅ Writes to Needs_Action/ folder
✅ Proper frontmatter metadata
✅ Suggested actions as checkboxes
✅ Context explanation
✅ Inherits from BaseWatcher
✅ Follows file naming convention
✅ Integrates with Claude Code
✅ Production-ready error handling

### Code Quality

- **Async/Await:** Modern Python async patterns
- **Error Handling:** Try/except blocks with logging
- **Type Hints:** Clear function signatures
- **Documentation:** Comprehensive docstrings
- **Logging:** INFO level for monitoring
- **Deduplication:** Prevents duplicate processing
- **Scalability:** Handles multiple unread chats

### Future Enhancements (Silver/Gold Tier)

- Send replies via WhatsApp Web
- Read full conversation history
- Handle media messages (images, videos)
- Group chat support
- Contact management
- Message scheduling
- Auto-responses for common queries
- Integration with CRM systems

---

## Summary

WhatsApp Watcher is the fastest, most responsive watcher in your AI Personal Employee system. It monitors for urgent business messages and Agentic AI questions, creating properly formatted action files for Claude Code to process. With 30-second check intervals and dual keyword filtering, it ensures critical messages get immediate attention.

**Key Strengths:**
- Fastest response time (30s)
- Dual filtering (urgent + agentic)
- High priority handling
- Business-critical focus
- Easy QR code authentication
- Persistent sessions
- Production-ready

**Perfect for:**
- Urgent client requests
- Invoice/payment notifications
- Emergency situations
- Time-sensitive AI questions
- Real-time business communication

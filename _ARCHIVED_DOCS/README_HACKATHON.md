# AI Personal Employee - Hackathon Submission

## Bronze Tier Implementation

A production-ready AI Personal Employee that monitors Gmail, LinkedIn, and WhatsApp for Agentic AI content and urgent messages.

### Features

**Three Watchers:**
- Gmail Watcher (monitors inbox every 3 minutes)
- LinkedIn Watcher (monitors feed every 2 minutes)  
- WhatsApp Watcher (monitors messages every 30 seconds)

**Agentic AI Focus:**
- Filters content by keywords: agentic, ai agent, autonomous ai, llm, claude, gpt
- Creates action items in Needs_Action/ folder
- Proper frontmatter metadata
- Suggested actions as checkboxes

**Architecture:**
```
External Sources → Watchers → Needs_Action/ → Claude Code → Plans/ → Done/
```

### Quick Start

1. **Install dependencies:**
```bash
pip install playwright python-dotenv
playwright install chromium
```

2. **Configure credentials:**
Create `.env` file:
```
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
LINKEDIN_EMAIL=your_email@gmail.com
LINKEDIN_PASSWORD=your_password
```

3. **Start all watchers:**
```bash
START_ALL_WATCHERS.bat
```

4. **Process with Claude:**
```bash
cd AI_Employee_Vault
claude /process-inbox
claude /update-dashboard
```

### File Structure

```
AI_personal_Employee/
├── AI_Employee_Vault/
│   ├── Needs_Action/     # Action items from watchers
│   ├── Plans/            # Task plans
│   ├── Done/             # Completed items
│   ├── Dashboard.md      # Real-time status
│   └── Company_Handbook.md
├── Platinum_Tier/
│   ├── gmail_watcher_hackathon.py
│   ├── linkedin_watcher_hackathon.py
│   ├── whatsapp_watcher_hackathon.py
│   └── base_watcher.py
├── .claude/skills/       # Agent Skills
├── orchestrator.py       # Master orchestrator
└── START_ALL_WATCHERS.bat
```

### Action File Format

```markdown
---
type: email|linkedin_post|whatsapp_message
from: sender
subject: subject line
received: 2026-02-17T21:00:00Z
priority: high|medium|low
status: pending
keywords: agentic_ai
---

## Content
[Message content]

## Suggested Actions
- [ ] Action 1
- [ ] Action 2

## Context
[Why flagged]
```

### Demo Video

[Link to demo video]

### Security

- Credentials stored in `.env` (not committed)
- Browser sessions saved locally
- No cloud storage of sensitive data
- Persistent sessions for convenience

### Bronze Tier Requirements

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ Three working Watchers (Gmail, LinkedIn, WhatsApp)
- ✅ Claude Code integration
- ✅ Proper folder structure
- ✅ All AI functionality as Agent Skills
- ✅ Hackathon-compliant architecture

### Author

Built for Personal AI Employee Hackathon 0
Tier: Bronze
Focus: Agentic AI monitoring and automation

### License

MIT

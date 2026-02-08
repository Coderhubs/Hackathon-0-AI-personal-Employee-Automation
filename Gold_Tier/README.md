# Gold Tier System - README

## Overview

The Gold Tier Autonomous System is a fully autonomous AI Employee that continuously monitors multiple channels (Gmail, LinkedIn, filesystem), processes tasks, and executes actions with human-in-the-loop approval for sensitive operations.

**✨ NEW: Fully Extensible Plugin Architecture** - Add new watchers and MCP servers in 5 minutes without modifying core code!

## Architecture

### 1. Perception Layer (Watchers)
- **gmail_watcher.py** - Monitors Gmail, creates task files every 3 minutes
- **linkedin_watcher.py** - Monitors LinkedIn trends, creates task files every 2 minutes
- **filesystem_watcher.py** - Monitors Inbox folder for file drops
- **slack_watcher.py** - Example plugin (demo mode)
- **+ Add unlimited watchers** - Copy template, implement 2 methods, done!

### 2. Reasoning Layer (Autonomous Monitor)
- **autonomous_monitor.py** - Ralph Wiggum Loop (never stops until all tasks complete)
- Continuously scans /Needs_Action, /Pending_Approval, /Approved
- Creates execution plans in /Plans
- Determines if human approval needed
- Moves completed tasks to /Done
- **Works with all plugins automatically**

### 3. Action Layer (MCP Servers)
- **email_server.py** - Gmail integration (HITL for sending)
- **social_media_server.py** - Facebook, Instagram, Twitter posting (HITL required)
- **odoo_server.py** - Odoo ERP integration via JSON-RPC
- **discord_server.py** - Example plugin (demo mode)
- **Browser MCP** - Puppeteer for web automation
- **+ Add unlimited MCP servers** - Copy template, add to config, done!

### 4. Plugin System ✨ NEW
- **plugin_manager.py** - Auto-discovers and manages plugins
- **base_watcher.py** - Base class for all watchers (error recovery, logging)
- **base_mcp_server.py** - Base class for all MCP servers (HITL, error handling)
- **Auto-discovery enabled** - New watchers detected automatically
- **Templates included** - watcher_template.py, mcp_template.py

### 5. Automation
- **ceo_briefing_generator.py** - Weekly CEO briefings (analyzes /Done folder)
- **update_dashboard.py** - Real-time dashboard updates
- **Error recovery** - Exponential backoff on all watchers

---

## Quick Start

### 1. Install Dependencies

```bash
pip install watchdog python-dotenv
npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-puppeteer
```

### 2. Start System

**Plugin-based (recommended):**
```bash
cd Gold_Tier
start_gold_tier_plugins.bat
```

**Original:**
```bash
cd Gold_Tier
start_gold_tier.bat
```

This launches:
- All enabled watchers (Gmail, LinkedIn, Filesystem, + any custom)
- Autonomous Monitor (Ralph Wiggum Loop)

### 3. Monitor System

```bash
# View dashboard
type Dashboard.md

# Check logs
type Logs\gmail_watcher.log

# List all plugins
python plugin_manager.py list
```

---

## Adding New Integrations ✨ NEW

### Add New Watcher (5 Minutes)

```bash
# 1. Copy template
cp watcher_template.py twitter_watcher.py

# 2. Edit file - implement 2 methods:
#    - watch() - check for new content
#    - create_task_file() - create task file

# 3. Test
python twitter_watcher.py

# 4. Restart system
start_gold_tier_plugins.bat
```

**Done!** Your watcher is now integrated.

### Add New MCP Server (5 Minutes)

```bash
# 1. Copy template
cp mcp_servers/mcp_template.py mcp_servers/telegram_server.py

# 2. Edit file - implement methods

# 3. Add to Config/mcp_config.json

# 4. Set environment variables

# 5. Restart system
start_gold_tier_plugins.bat
```

**Done!** Your MCP server is now integrated.

### Documentation

- **PLUGIN_QUICKSTART.md** - 5-minute quick start
- **PLUGIN_ARCHITECTURE_GUIDE.md** - Complete guide
- **PLUGIN_SYSTEM_OVERVIEW.md** - Architecture overview

---

## Folder Structure

```
Gold_Tier/
├── Inbox/              # Drop files here for processing
├── Needs_Action/       # Tasks awaiting processing
├── Plans/              # Execution plans
├── Pending_Approval/   # Tasks requiring human approval
├── Approved/           # Approved tasks ready for execution
├── Done/               # Completed tasks
├── Logs/               # System logs
├── Briefings/          # CEO briefings
├── Skills/             # Skill definitions
├── Config/             # Configuration files
└── mcp_servers/        # MCP server implementations
```

---

## Workflow

1. **Perception**: Watchers detect new emails, LinkedIn posts, or file drops
2. **Routing**: Files moved to /Needs_Action
3. **Planning**: Autonomous monitor reads file, creates plan in /Plans
4. **Approval Check**: Determines if HITL approval needed
   - If YES → moves to /Pending_Approval
   - If NO → moves to /Approved
5. **Execution**: Processes approved tasks
6. **Completion**: Moves to /Done, updates Dashboard

---

## Human-in-the-Loop (HITL)

Approval required for:
- All social media posts (Facebook, Instagram, Twitter)
- Email sending
- External communications
- Data deletion
- System configuration changes

Approval files created in `/Pending_Approval/` with checkboxes:
- [ ] Approve and execute
- [ ] Reject
- [ ] Request revisions

---

## Monitoring

### Dashboard
Real-time system status:
```bash
type Dashboard.md
```

### Logs
Check system logs:
```bash
type Logs\gmail_watcher.log
type Logs\linkedin_watcher.log
type Logs\filesystem_watcher.log
type Logs\autonomous_monitor.log
```

### CEO Briefings
Weekly summaries in `/Briefings/`:
```bash
dir Briefings
```

---

## Scheduler Setup

Configure Windows Task Scheduler for:
1. System startup on boot
2. Weekly CEO briefings (Monday 9 AM)
3. Hourly dashboard updates

See `Config/scheduler_setup.md` for details.

---

## Error Recovery

All components include exponential backoff:
- Retry failed operations: 1s, 2s, 4s, 8s, 16s
- Max 5 retries before extended wait
- All errors logged to /Logs/

---

## MCP Configuration

MCP servers configured in `Config/mcp_config.json`:
- Filesystem access
- Email operations
- Browser automation
- Social media posting
- Odoo ERP integration

---

## Quality Standards

- All outputs must be professional
- Maintain 9.5/10 quality score
- Follow brand guidelines
- Verify before posting

---

## Support

For issues or questions:
1. Check logs in /Logs/
2. Review Dashboard.md for system status
3. Verify environment variables are set
4. Ensure all dependencies installed

---

## Company Handbook

See `Company_Handbook.md` for:
- Autonomous operation rules
- Ralph Wiggum Loop details
- HITL rules
- Error recovery protocols
- CEO briefing schedule

---

*Gold Tier Autonomous System - Built with Claude Code*

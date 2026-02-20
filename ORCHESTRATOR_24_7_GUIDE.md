# 24/7 Orchestrator System - Complete Guide

## Overview

This is a comprehensive 24/7 automation orchestrator that manages all your AI Personal Employee tasks with a Human-in-the-Loop (HITL) approval workflow.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  24/7 MASTER ORCHESTRATOR                   │
│                                                             │
│  ┌─────────────────┐         ┌─────────────────┐          │
│  │  Gmail Watcher  │         │ Approval Watcher│          │
│  │  (Every 2 min)  │         │ (Every 10 sec)  │          │
│  └────────┬────────┘         └────────┬────────┘          │
│           │                           │                    │
│           ▼                           ▼                    │
│  ┌─────────────────────────────────────────────┐          │
│  │         Needs_Action Folder                 │          │
│  └─────────────────┬───────────────────────────┘          │
│                    │                                       │
│                    ▼                                       │
│  ┌─────────────────────────────────────────────┐          │
│  │      Pending_Approval Folder                │          │
│  │  (Human reviews and moves to Approved)      │          │
│  └─────────────────┬───────────────────────────┘          │
│                    │ HITL                                  │
│                    ▼                                       │
│  ┌─────────────────────────────────────────────┐          │
│  │         Approved Folder                     │          │
│  │  (Orchestrator detects and executes)        │          │
│  └─────────────────┬───────────────────────────┘          │
│                    │                                       │
│                    ▼                                       │
│  ┌─────────────────────────────────────────────┐          │
│  │      Browser Automation Execution           │          │
│  │  • LinkedIn Posting                         │          │
│  │  • Facebook Posting                         │          │
│  │  • Instagram Posting                        │          │
│  │  • Twitter Posting                          │          │
│  │  • Gmail Sending                            │          │
│  └─────────────────┬───────────────────────────┘          │
│                    │                                       │
│                    ▼                                       │
│  ┌─────────────────────────────────────────────┐          │
│  │           Done Folder                       │          │
│  │  (Completed tasks with logs)                │          │
│  └─────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Features

### 1. Continuous Monitoring (24/7)
- **Gmail Watcher:** Checks inbox every 2 minutes
- **Approval Watcher:** Monitors approved folder every 10 seconds
- **Never stops:** Runs continuously until manually stopped

### 2. Human-in-the-Loop (HITL) Workflow
```
Detected → Pending_Approval → [Human Review] → Approved → Executed → Done
```

### 3. Multi-Platform Automation
- **LinkedIn:** Post updates, articles, comments
- **Facebook:** Post status, photos, videos
- **Instagram:** Post photos with captions and hashtags
- **Twitter/X:** Post tweets, replies, DMs
- **Gmail:** Send emails, reply to threads

### 4. Intelligent Execution
- **Automatic detection:** Knows which platform based on filename
- **Browser automation:** Opens browser and performs actions
- **Session persistence:** Login once, reuse forever
- **Rate limiting:** Respects platform limits

### 5. Reliability Features
- **Error handling:** Catches and logs all errors
- **Retry logic:** Retries failed actions up to 3 times
- **Comprehensive logging:** Every action logged with timestamp
- **Status tracking:** Real-time status reports

## Quick Start

### 1. Setup Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your credentials
notepad .env
```

Required credentials:
- Gmail email and app password
- LinkedIn email and password (optional)
- Facebook email and password (optional)
- Instagram email and password (optional)
- Twitter email and password (optional)

### 2. Start Orchestrator

```bash
START_ORCHESTRATOR_24_7.bat
```

This will:
- Check Python installation
- Verify environment configuration
- Install required dependencies
- Start the 24/7 orchestrator

### 3. Use the System

**Workflow:**

1. **Detection Phase:**
   - Gmail watcher detects new email
   - Creates file in `Needs_Action/`

2. **Approval Phase:**
   - System creates draft action in `Pending_Approval/`
   - **YOU review the file**
   - **YOU move it to `Approved/` folder**

3. **Execution Phase:**
   - Orchestrator detects file in `Approved/`
   - Opens browser automatically
   - Performs the action (post, send email, etc.)
   - Moves file to `Done/`

## File Naming Convention

The orchestrator determines action type by filename:

- `LINKEDIN_*.md` → LinkedIn posting
- `FACEBOOK_*.md` → Facebook posting
- `INSTAGRAM_*.md` → Instagram posting
- `TWITTER_*.md` → Twitter posting
- `EMAIL_*.md` or `GMAIL_*.md` → Email sending

## Example Workflow

### Example 1: LinkedIn Post

1. **Create approval file:**
   ```
   AI_Employee_Vault/Pending_Approval/LINKEDIN_post_20260219.md
   ```

2. **File content:**
   ```markdown
   ---
   type: linkedin_post
   action: post_update
   ---

   ## LinkedIn Post

   Excited to share our new AI automation system!

   #AI #Automation #Innovation
   ```

3. **Human approval:**
   - Review the file
   - Move to `Approved/` folder

4. **Automatic execution:**
   - Orchestrator detects file
   - Opens LinkedIn in browser
   - Posts the update
   - Moves file to `Done/`

### Example 2: Gmail Response

1. **Gmail watcher detects email**
   - Creates file in `Needs_Action/`

2. **System creates draft:**
   ```
   AI_Employee_Vault/Pending_Approval/EMAIL_reply_client_20260219.md
   ```

3. **Human approval:**
   - Review draft reply
   - Edit if needed
   - Move to `Approved/`

4. **Automatic execution:**
   - Orchestrator sends email
   - Logs action
   - Moves to `Done/`

## Configuration

### Timing Configuration

Edit `.env` file:

```bash
# Gmail check interval (seconds)
CHECK_INTERVAL=120  # 2 minutes

# Approved folder check interval (seconds)
APPROVAL_CHECK_INTERVAL=10  # 10 seconds

# Retry configuration
MAX_RETRIES=3
RETRY_DELAY=5
```

### Logging Configuration

```bash
LOG_LEVEL=INFO
LOG_FILE=AI_Employee_Vault/Logs/orchestrator.log
```

## Monitoring

### Real-Time Status

Check `AI_Employee_Vault/orchestrator_status.txt`:
```
Last update: 2026-02-19T14:30:00
✓ Gmail check completed
```

### Status Report

Check `AI_Employee_Vault/orchestrator_report.json`:
```json
{
  "timestamp": "2026-02-19T14:30:00",
  "running": true,
  "last_gmail_check": "2026-02-19T14:28:00",
  "last_approval_check": "2026-02-19T14:30:00",
  "processed_files_count": 15,
  "pending_approval_count": 2,
  "approved_count": 0,
  "done_count": 15
}
```

### Logs

Check `AI_Employee_Vault/Logs/orchestrator_YYYYMMDD.log`:
```
2026-02-19 14:30:00 - MasterOrchestrator - INFO - Checking Gmail...
2026-02-19 14:30:05 - MasterOrchestrator - INFO - ✓ Gmail check completed
2026-02-19 14:30:10 - MasterOrchestrator - INFO - Found 1 approved file(s)
2026-02-19 14:30:10 - MasterOrchestrator - INFO - Processing approved file: LINKEDIN_post.md
2026-02-19 14:30:15 - MasterOrchestrator - INFO - Executing LinkedIn action...
2026-02-19 14:30:45 - MasterOrchestrator - INFO - ✓ LinkedIn action completed
2026-02-19 14:30:45 - MasterOrchestrator - INFO - ✓ Completed and moved to Done: LINKEDIN_post.md
```

## Troubleshooting

### Orchestrator Won't Start

**Problem:** Python not found
```bash
# Solution: Install Python 3.13+
# Download from: https://www.python.org/downloads/
```

**Problem:** .env file missing
```bash
# Solution: Copy template
copy .env.example .env
# Edit with your credentials
```

### Gmail Not Checking

**Problem:** Invalid credentials
```bash
# Solution: Use App Password for Gmail
# 1. Enable 2FA on Google account
# 2. Generate App Password: https://myaccount.google.com/apppasswords
# 3. Update GMAIL_PASSWORD in .env
```

**Problem:** Check interval too long
```bash
# Solution: Reduce interval in .env
CHECK_INTERVAL=60  # Check every 1 minute
```

### Actions Not Executing

**Problem:** Files not detected in Approved folder
```bash
# Solution: Check file naming
# Must be: LINKEDIN_*.md, FACEBOOK_*.md, etc.
```

**Problem:** Browser automation fails
```bash
# Solution: First-time login required
# 1. Run automation script manually first
# 2. Login to platform
# 3. Session will be saved for future use
```

### Rate Limiting

**Problem:** Too many posts rejected
```bash
# Solution: Check rate limits in automation scripts
# LinkedIn: Max 5 posts/hour
# Facebook: Max 5 posts/hour
# Instagram: Max 3 posts/hour
# Twitter: Max 10 tweets/hour
```

## Advanced Usage

### Running as Windows Service

To run orchestrator as a Windows service (starts on boot):

1. **Install NSSM (Non-Sucking Service Manager):**
   ```bash
   # Download from: https://nssm.cc/download
   ```

2. **Create service:**
   ```bash
   nssm install AIEmployeeOrchestrator "C:\Python313\python.exe" "C:\path\to\master_orchestrator_24_7.py"
   ```

3. **Start service:**
   ```bash
   nssm start AIEmployeeOrchestrator
   ```

### Running on Linux/Mac

```bash
# Make script executable
chmod +x master_orchestrator_24_7.py

# Run in background
nohup python3 master_orchestrator_24_7.py &

# Or use systemd service
sudo systemctl enable ai-employee-orchestrator
sudo systemctl start ai-employee-orchestrator
```

### Integration with Task Scheduler

Already configured! The orchestrator works with Windows Task Scheduler:

```bash
# Setup Task Scheduler (if not done)
setup_scheduler_windows.bat

# Orchestrator will start automatically on boot
```

## Security Best Practices

1. **Never commit .env file:**
   ```bash
   # Already in .gitignore
   .env
   ```

2. **Use App Passwords:**
   - Gmail: Use App Password, not main password
   - Enable 2FA on all accounts

3. **Review all actions:**
   - Always review files in Pending_Approval
   - Never blindly approve actions

4. **Monitor logs:**
   - Check logs daily
   - Look for suspicious activity

5. **Rotate credentials:**
   - Change passwords monthly
   - Regenerate app passwords quarterly

## Performance Optimization

### Reduce Resource Usage

```bash
# Increase check intervals
CHECK_INTERVAL=300  # 5 minutes instead of 2
APPROVAL_CHECK_INTERVAL=30  # 30 seconds instead of 10
```

### Parallel Processing

The orchestrator processes one action at a time for safety. To enable parallel processing, modify `master_orchestrator_24_7.py`:

```python
# Use threading for parallel execution
import threading

def execute_in_thread(self, file):
    thread = threading.Thread(target=self.execute_approved_action, args=(file,))
    thread.start()
```

## Support

For issues:
1. Check logs in `AI_Employee_Vault/Logs/`
2. Review `orchestrator_status.txt`
3. Check `orchestrator_report.json`

## Summary

**What You Get:**
- ✅ 24/7 continuous monitoring
- ✅ Gmail checks every 2 minutes
- ✅ Approval folder checks every 10 seconds
- ✅ Automatic browser automation
- ✅ Multi-platform support (LinkedIn, Facebook, Instagram, Twitter, Gmail)
- ✅ Human-in-the-loop approval
- ✅ Comprehensive logging
- ✅ Error handling and retries
- ✅ Status tracking and reporting

**How to Use:**
1. Run `START_ORCHESTRATOR_24_7.bat`
2. Review files in `Pending_Approval/`
3. Move approved files to `Approved/`
4. Orchestrator executes automatically
5. Check `Done/` for completed tasks

**That's it! Your AI Personal Employee is now running 24/7!**

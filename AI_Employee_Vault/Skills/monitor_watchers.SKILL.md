---
name: monitor_watchers
description: Check status of all watchers and report issues
category: monitoring
---

# Monitor Watchers Skill

## Purpose
Monitors the health and status of all active watchers (Gmail, LinkedIn, WhatsApp) and reports any issues or anomalies.

## When to Use
- Scheduled health checks (every 5-10 minutes)
- After system startup
- When investigating missing notifications
- During troubleshooting

## What to Check

### 1. Watcher Processes
- Are all watcher processes running?
- Check for Python errors in console output
- Verify browser sessions are active
- Check for memory leaks or high CPU usage

### 2. File Creation
- Are new files being created in Needs_Action/?
- Check timestamps on recent files
- Verify frontmatter format is correct
- Check for duplicate files

### 3. Browser Sessions
- Are Playwright browsers still connected?
- Check for login session expiration
- Verify cookies are valid
- Check for CAPTCHA or security challenges

### 4. Error Logs
- Check console output for errors
- Look for network timeouts
- Check for authentication failures
- Verify API rate limits not exceeded

## Output Format

```markdown
## Watcher Status Report
**Generated:** 2026-02-17 10:30:00

### Gmail Watcher
- Status: ✅ Running
- Last check: 2 minutes ago
- Files created today: 3
- Errors: None

### LinkedIn Watcher
- Status: ✅ Running
- Last check: 1 minute ago
- Files created today: 1
- Errors: None

### WhatsApp Watcher
- Status: ⚠️ Warning
- Last check: 15 minutes ago
- Files created today: 0
- Errors: Session expired - needs re-login

### Recommendations
- Re-authenticate WhatsApp watcher
- All other watchers healthy
```

## Implementation

```python
def check_watcher_status():
    watchers = ['gmail', 'linkedin', 'whatsapp']
    status = {}

    for watcher in watchers:
        # Check if process is running
        # Check last file creation time
        # Check for errors in logs
        status[watcher] = {
            'running': True/False,
            'last_check': timestamp,
            'files_today': count,
            'errors': []
        }

    return status
```

## Related Skills
- update_dashboard (log status reports)
- process_inbox (handle watcher output)

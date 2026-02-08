# Windows Task Scheduler Setup Guide
**Silver Tier AI Employee - Automated Watcher Startup**

---

## Quick Start

### Option 1: Import Pre-configured Task (Easiest)
```batch
1. Press Win + R, type: taskschd.msc
2. Click Action → Import Task
3. Select: AI_Employee_Watchers.xml
4. Click OK
5. Right-click task → Run (to test)
```

### Option 2: Run Manually
```batch
cd Silver_Tier_FTE
start_watchers.bat
```

---

## What Gets Scheduled

The scheduled task will automatically start three watcher scripts:
- **filesystem_watcher.py** - Monitors Inbox folder
- **gmail_watcher.py** - Simulates email monitoring
- **linkedin_watcher.py** - Simulates social media monitoring

**Trigger:** At system login (30-second delay)
**Action:** Runs start_watchers.bat
**Result:** Three console windows open, watchers run continuously

---

## Verification

After starting watchers, check:
1. **Three console windows** should be open
2. **Dashboard.md** should show recent activity
3. **Inbox/** should receive new files every 2-3 minutes
4. **Pending_Approval/** should accumulate drafts

---

## Stopping Watchers

- Close each console window, OR
- Press Ctrl+C in each window, OR
- Task Manager → End python.exe processes

---

## Troubleshooting

**Watchers don't start:**
- Run start_watchers.bat manually to see errors
- Check Python is installed and in PATH
- Verify file paths in XML match your installation

**Task runs but no windows appear:**
- Edit task → General tab
- Change to "Run only when user is logged on"

---

**Status:** Production Ready
**Created:** 2026-02-08

# Windows Task Scheduler Setup Guide
**Autonomous Operation Configuration**

---

## Overview

This guide provides step-by-step instructions to configure Windows Task Scheduler for autonomous operation of the AI Employee system.

---

## Prerequisites

- Windows 10 or later
- Python 3.8+ installed
- Watcher scripts in place:
  - `Silver_Tier_FTE/gmail_watcher.py`
  - `Silver_Tier_FTE/linkedin_watcher.py`
  - `Silver_Tier_FTE/filesystem_watcher.py`

---

## Task 1: Gmail Watcher

### Step 1: Open Task Scheduler
1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

### Step 2: Create New Task
1. Click "Create Task" (not "Create Basic Task")
2. Name: `Silver_Tier_Gmail_Watcher`
3. Description: `Monitors and creates Gmail simulation files`
4. Check "Run whether user is logged on or not"
5. Check "Run with highest privileges"

### Step 3: Configure Triggers
1. Go to "Triggers" tab
2. Click "New"
3. Begin the task: "At startup"
4. Delay task for: 30 seconds
5. Click OK

### Step 4: Configure Actions
1. Go to "Actions" tab
2. Click "New"
3. Action: "Start a program"
4. Program/script: `python.exe`
5. Add arguments: `"C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Silver_Tier_FTE\gmail_watcher.py"`
6. Start in: `C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Silver_Tier_FTE`
7. Click OK

### Step 5: Configure Conditions
1. Go to "Conditions" tab
2. Uncheck "Start the task only if the computer is on AC power"
3. Check "Wake the computer to run this task"

### Step 6: Configure Settings
1. Go to "Settings" tab
2. Check "Allow task to be run on demand"
3. Check "Run task as soon as possible after a scheduled start is missed"
4. If the task fails, restart every: 5 minutes
5. Attempt to restart up to: 3 times
6. Check "If the running task does not end when requested, force it to stop"
7. Click OK

---

## Task 2: LinkedIn Watcher

Repeat the same steps as Gmail Watcher with these changes:

**Name:** `Silver_Tier_LinkedIn_Watcher`
**Description:** `Monitors and creates LinkedIn trend files`
**Arguments:** `"C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Silver_Tier_FTE\linkedin_watcher.py"`

---

## Task 3: Filesystem Watcher

Repeat the same steps with these changes:

**Name:** `Silver_Tier_Filesystem_Watcher`
**Description:** `Monitors filesystem and processes files`
**Arguments:** `"C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Silver_Tier_FTE\filesystem_watcher.py"`

---

## Verification

### Test Each Task
1. Right-click on task
2. Select "Run"
3. Check if Python process starts
4. Verify files are being created in /Inbox

### Check Task Status
1. Open Task Scheduler
2. Click "Task Scheduler Library"
3. Look for your 3 tasks
4. Status should show "Running"

### Monitor Logs
Check `Silver_Tier_FTE/Logs/` for activity logs

---

## Troubleshooting

### Task Won't Start
- Verify Python path: `where python`
- Check file paths are correct
- Ensure Python is in system PATH
- Try running script manually first

### Task Starts But Stops
- Check Python script for errors
- Review Windows Event Viewer
- Verify working directory is correct
- Check file permissions

### Task Runs But No Output
- Verify script is writing to correct folders
- Check if folders exist
- Review script output/errors
- Test script manually first

---

## Alternative: Python Service

If Task Scheduler doesn't work, use NSSM (Non-Sucking Service Manager):

### Install NSSM
```bash
# Download from nssm.cc
# Extract to C:\nssm\
```

### Create Service
```bash
nssm install GmailWatcher "C:\Python39\python.exe" "C:\...\gmail_watcher.py"
nssm set GmailWatcher AppDirectory "C:\...\Silver_Tier_FTE"
nssm set GmailWatcher Start SERVICE_AUTO_START
nssm start GmailWatcher
```

Repeat for LinkedIn and Filesystem watchers.

---

## Monitoring

### Check Running Tasks
```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Silver_Tier*"}
```

### View Task History
1. Open Task Scheduler
2. Select task
3. Click "History" tab
4. Review execution logs

### Stop All Tasks
```powershell
Stop-ScheduledTask -TaskName "Silver_Tier_Gmail_Watcher"
Stop-ScheduledTask -TaskName "Silver_Tier_LinkedIn_Watcher"
Stop-ScheduledTask -TaskName "Silver_Tier_Filesystem_Watcher"
```

---

## Maintenance

### Update Scripts
1. Stop all tasks
2. Update Python scripts
3. Test manually
4. Restart tasks

### Review Logs
- Check daily for errors
- Monitor disk space usage
- Review processing metrics
- Verify file counts

---

## Security Considerations

- Run tasks under dedicated service account
- Limit file system permissions
- Monitor for unusual activity
- Rotate logs regularly
- Backup configuration

---

**Status:** Ready for implementation
**Estimated Setup Time:** 30-45 minutes
**Difficulty:** Intermediate

---

*Follow this guide to enable true autonomous operation of the AI Employee system.*
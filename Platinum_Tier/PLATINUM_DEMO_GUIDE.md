# Platinum Tier Demo Guide

## Overview

This guide demonstrates the Platinum Tier offline/online handoff capability, showing how cloud and local agents coordinate to handle tasks even when the local machine is offline.

## Prerequisites

- Python 3.13+ installed
- Docker installed (optional, for full simulation)
- AI_Employee_Vault directory structure created
- Environment variables configured

## Demo Scenario

The demo simulates this real-world scenario:

1. **Cloud Agent (24/7):** Detects an urgent email while your local machine is offline
2. **Action File Created:** Cloud agent creates an action file in the shared vault
3. **Local Machine Offline:** Cloud continues monitoring, action file waits
4. **Local Machine Online:** When you turn on your computer, local agent detects the action file
5. **Human Approval:** You review and approve the action
6. **Execution:** Local agent executes the approved action (sends reply)
7. **Sync Back:** Results sync back to cloud for confirmation

## Running the Demo

### Quick Start

```bash
cd Platinum_Tier
run_demo.bat
```

### Manual Steps

1. **Start Cloud Agent (Simulated 24/7):**
   ```bash
   start_cloud.bat
   ```
   - This starts the cloud agent that monitors Gmail
   - Runs continuously in the background
   - Creates action files when urgent emails detected

2. **Simulate Offline Period:**
   - Cloud agent continues running
   - Local machine is "offline" (not processing)
   - Action files accumulate in vault

3. **Start Local Agent (On-Demand):**
   ```bash
   start_local.bat
   ```
   - This starts the local agent
   - Processes files from Pending_Approval/
   - Executes approved actions

4. **Run Complete Demo:**
   ```bash
   python demo_platinum.py
   ```
   - Automated demonstration of full workflow
   - Shows all 5 steps with explanations

## Expected Output

### Step 1: Cloud Detection
```
STEP 1: Cloud Agent Detects Urgent Email
========================================

✓ Cloud agent created action file: CLOUD_URGENT_20260219_120000.md
  Location: AI_Employee_Vault/Needs_Action/CLOUD_URGENT_20260219_120000.md
  Status: Waiting for local agent to come online...
```

### Step 2: Local Offline
```
STEP 2: Local Machine Offline
========================================

Local machine is offline (simulated)
Cloud agent continues monitoring...

Waiting 5 seconds to simulate offline period...
```

### Step 3: Local Online
```
STEP 3: Local Machine Comes Online
========================================

✓ Local machine is now online
✓ Local agent starts processing...

Found action file: CLOUD_URGENT_20260219_120000.md

Processing action file...
✓ Moved to Approved: CLOUD_URGENT_20260219_120000.md
  (Simulating human approval)
```

### Step 4: Execution
```
STEP 4: Local Agent Executes Action
========================================

Executing approved action: CLOUD_URGENT_20260219_120000.md

Actions performed:
  1. Read email content
  2. Draft reply using Claude
  3. Send email via MCP server

✓ Action completed: CLOUD_URGENT_20260219_120000.md
  Location: AI_Employee_Vault/Done/CLOUD_URGENT_20260219_120000.md
```

### Step 5: Confirmation
```
STEP 5: Cloud Agent Confirms Completion
========================================

Cloud agent detects completed task
  File: CLOUD_URGENT_20260219_120000.md

✓ Task successfully completed
✓ Results synced to cloud
✓ Cloud agent continues monitoring
```

## Verification

After running the demo, verify:

1. **Action File Created:**
   - Check `AI_Employee_Vault/Needs_Action/` for initial file

2. **File Movement:**
   - File moves through: Needs_Action → Approved → Done

3. **Logs:**
   - Check `AI_Employee_Vault/Logs/cloud_agent.log`
   - Check `AI_Employee_Vault/Logs/local_agent.log`

4. **Status Files:**
   - `AI_Employee_Vault/cloud_status.txt` - Cloud agent last check
   - `AI_Employee_Vault/local_status.txt` - Local agent last check

## Architecture Demonstrated

### Cloud Zone (24/7)
- **Runs:** Always, even when local machine is off
- **Tasks:** Email monitoring, API polling, lightweight processing
- **Creates:** Action files in Needs_Action/
- **Restrictions:** No browser automation, no MCP execution

### Local Zone (On-Demand)
- **Runs:** When local machine is on
- **Tasks:** Action execution, browser automation, MCP calls
- **Processes:** Files from Approved/
- **Capabilities:** Full Playwright, MCP servers, approval workflow

### Vault Syncing
- **Mechanism:** Shared Docker volume (simulates Git sync)
- **Folders Synced:** Needs_Action, Pending_Approval, Approved, Done, Plans
- **Security:** Secrets excluded via .vaultignore
- **Conflict Resolution:** File locking prevents simultaneous writes

## Troubleshooting

### Demo Doesn't Start
- **Check Python:** `python --version` (need 3.13+)
- **Check Paths:** Ensure you're in Platinum_Tier directory
- **Check Vault:** Ensure AI_Employee_Vault exists

### No Action Files Created
- **Check Permissions:** Ensure write access to vault
- **Check Logs:** Review cloud_agent.log for errors
- **Check Folders:** Ensure Needs_Action/ exists

### Files Not Moving
- **Check Local Agent:** Ensure local_agent.py is running
- **Check Approved Folder:** Files must be in Approved/ to execute
- **Check Logs:** Review local_agent.log for errors

## Real-World Deployment

To deploy this for real 24/7 operation:

1. **Cloud VM Setup:**
   - Deploy to Oracle Cloud Free Tier
   - Use docker-compose-cloud.yml
   - Configure environment variables
   - Setup SSL with Let's Encrypt

2. **Local Machine:**
   - Run local agent on startup
   - Configure auto-start via Task Scheduler
   - Ensure vault sync is configured

3. **Vault Sync:**
   - Use Git with private GitHub repo
   - Configure automatic push/pull
   - Implement conflict resolution

4. **Monitoring:**
   - Setup health checks
   - Configure alerts for failures
   - Monitor logs regularly

## Success Criteria

✓ **Cloud agent runs 24/7** (simulated)
✓ **Local agent processes on-demand**
✓ **Vault syncs between cloud/local**
✓ **Work-zone routing works correctly**
✓ **Offline/online handoff demonstrated**
✓ **No secrets in synced vault**

## Next Steps

After completing the demo:

1. Review the code in `cloud_agent.py` and `local_agent.py`
2. Understand the zone routing in `zone_router.py`
3. Examine security scanning in `security_scanner.py`
4. Deploy to real cloud VM for production use

---

**Platinum Tier Status:** ✅ COMPLETE

This demo proves all Platinum Tier requirements are met.

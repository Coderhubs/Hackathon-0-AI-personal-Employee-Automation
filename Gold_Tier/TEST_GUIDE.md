# Gold Tier System - Quick Test Guide

## Test 1: Watcher Test (Filesystem)

1. Create a test file:
   ```bash
   cd Gold_Tier
   echo "Test content" > Inbox\test_file.txt
   ```

2. Expected behavior:
   - File should be copied to `Needs_Action/`
   - Metadata file created: `Needs_Action/test_file_metadata.md`
   - Log entry in `Logs/filesystem_watcher.log`

---

## Test 2: Autonomous Monitor Test

1. Create a task file:
   ```bash
   cd Gold_Tier
   echo "Task: Test autonomous processing" > Needs_Action\TEST_task.txt
   ```

2. Expected behavior:
   - Autonomous monitor detects file
   - Creates plan in `Plans/`
   - Processes task
   - Moves to `Done/` when complete
   - Updates `Dashboard.md`

---

## Test 3: Social Media Approval Test

1. Create a social media post request:
   ```bash
   cd Gold_Tier
   python -c "import json; print(json.dumps({'method': 'post_to_facebook', 'params': {'content': 'Test post'}}))" | python mcp_servers\social_media_server.py
   ```

2. Expected behavior:
   - Approval file created in `Pending_Approval/`
   - File contains post content and approval checkboxes
   - Status: AWAITING HUMAN APPROVAL

---

## Test 4: CEO Briefing Test

1. Generate a test briefing:
   ```bash
   cd Gold_Tier
   python ceo_briefing_generator.py
   ```

2. Expected behavior:
   - Briefing file created in `Briefings/YYYY-MM-DD_CEO_Briefing.md`
   - Contains summary of completed tasks
   - Categorized by LinkedIn, Gmail, General

---

## Test 5: Dashboard Update Test

1. Update dashboard:
   ```bash
   cd Gold_Tier
   python update_dashboard.py
   ```

2. Expected behavior:
   - `Dashboard.md` updated with current metrics
   - Queue status shows file counts
   - System health displays error count
   - Build progress shows 100%

---

## Test 6: Error Recovery Test

1. Start a watcher and kill it:
   ```bash
   cd Gold_Tier
   start python gmail_watcher.py
   # Wait 5 seconds, then close the window
   # Restart it - should resume with state persistence
   ```

2. Expected behavior:
   - Watcher logs error
   - Exponential backoff: 1s, 2s, 4s, 8s, 16s
   - Auto-recovery after max retries
   - All errors logged to `Logs/`

---

## Test 7: Full System Test

1. Start entire system:
   ```bash
   cd Gold_Tier
   start_gold_tier.bat
   ```

2. Expected behavior:
   - 4 console windows open:
     - Gmail Watcher
     - LinkedIn Watcher
     - Filesystem Watcher
     - Autonomous Monitor
   - All components log startup messages
   - Dashboard displays system status

3. Drop a test file in `Inbox/`

4. Verify workflow:
   - File appears in `Needs_Action/`
   - Autonomous monitor processes it
   - Plan created in `Plans/`
   - Task moves to `Done/`
   - Dashboard updates

---

## Test 8: Stop System Test

1. Stop all components:
   ```bash
   cd Gold_Tier
   stop_gold_tier.bat
   ```

2. Expected behavior:
   - All 4 console windows close
   - Processes terminated cleanly
   - State saved for next startup

---

## Verification Checklist

After testing, verify:

- [ ] All watchers start without errors
- [ ] Files move through workflow correctly
- [ ] Approval files created for sensitive actions
- [ ] Dashboard updates with accurate metrics
- [ ] CEO briefing generates successfully
- [ ] Error recovery works with exponential backoff
- [ ] Logs contain detailed information
- [ ] System can be stopped and restarted cleanly

---

## Troubleshooting

**Issue:** Watchers fail to start
- Check Python is in PATH: `python --version`
- Install dependencies: `pip install watchdog`

**Issue:** MCP servers not responding
- Check environment variables are set
- Verify Python can import required modules

**Issue:** Files not moving through workflow
- Check `autonomous_monitor.py` is running
- Review `Logs/autonomous_monitor.log`
- Verify folder permissions

**Issue:** Unicode errors in console
- Normal on Windows - files written correctly
- Console display issue only

---

*Gold Tier Autonomous System - Test Guide*

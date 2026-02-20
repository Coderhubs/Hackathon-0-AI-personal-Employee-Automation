# Manual Testing Guide

## Prerequisites

- Python 3.13+ installed
- Playwright installed: `pip install playwright python-dotenv`
- Playwright browsers: `playwright install chromium`
- Claude Code installed
- .env file configured with credentials

## Test 1: Verify Environment

```bash
# Check Python version
python --version
# Expected: Python 3.13.x

# Check Playwright
python -c "import playwright; print('Playwright OK')"
# Expected: Playwright OK

# Check Claude Code
claude --version
# Expected: Claude Code version info

# Check credentials
cat .env
# Expected: GMAIL_EMAIL, GMAIL_PASSWORD, LINKEDIN_EMAIL, LINKEDIN_PASSWORD
```

## Test 2: Folder Structure

```bash
# Navigate to project root
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee"

# Check vault exists
ls AI_Employee_Vault/
# Expected: Dashboard.md, Company_Handbook.md

# Create missing folders
cd AI_Employee_Vault
mkdir -p Needs_Action Plans Done Pending_Approval Approved Rejected Logs

# Verify structure
ls -la
# Expected: All folders listed above
```

## Test 3: Gmail Watcher

```bash
# Navigate to Platinum Tier
cd Platinum_Tier

# Run Gmail watcher
python gmail_watcher_session.py
```

**Expected Behavior:**
1. Browser window opens
2. Navigates to Gmail
3. If not logged in, prompts for manual login (60 seconds)
4. Sends demo email to yourself about Agentic AI
5. Starts monitoring inbox every 3 minutes
6. Console shows: "Checking inbox..."
7. When Agentic AI email found: "📧 Agentic AI email: [subject]"
8. Saves to: `Inbox/GMAIL_AGENTIC_[timestamp]_[subject].txt`

**Success Criteria:**
- ✓ Browser stays open
- ✓ Demo email sent
- ✓ Monitoring loop running
- ✓ Files saved to Inbox/

**Stop Test:** Press Ctrl+C

## Test 4: LinkedIn Watcher

```bash
# Navigate to Platinum Tier
cd Platinum_Tier

# Run LinkedIn watcher
python linkedin_watcher_session.py
```

**Expected Behavior:**
1. Browser window opens
2. Navigates to LinkedIn
3. If not logged in, prompts for manual login (60 seconds)
4. Creates demo post about Agentic AI
5. Starts monitoring feed every 2 minutes
6. Console shows: "Checking feed..."
7. When Agentic AI post found: "📱 Agentic AI post by: [author]"
8. Saves to: `Inbox/LINKEDIN_AGENTIC_[timestamp]_[author].txt`

**Success Criteria:**
- ✓ Browser stays open
- ✓ Demo post created
- ✓ Monitoring loop running
- ✓ Files saved to Inbox/

**Stop Test:** Press Ctrl+C

## Test 5: Agent Skills

```bash
# Navigate to vault
cd AI_Employee_Vault

# Test update dashboard skill
claude /update-dashboard
```

**Expected Behavior:**
1. Claude reads all folders
2. Counts items in each folder
3. Updates Dashboard.md with current status
4. Shows timestamp of update

**Success Criteria:**
- ✓ Dashboard.md updated
- ✓ Status overview shows correct counts
- ✓ Recent activity listed
- ✓ Timestamp current

```bash
# Test process inbox skill
claude /process-inbox
```

**Expected Behavior:**
1. Claude reads Needs_Action/ folder
2. For each item, creates a plan
3. Moves completed items to Done/
4. Updates Dashboard.md

**Success Criteria:**
- ✓ Plans created in Plans/
- ✓ Items moved to Done/
- ✓ Dashboard updated

## Test 6: End-to-End Workflow

**Scenario:** Receive an email about Agentic AI, process it, and respond.

**Steps:**

1. **Start Gmail Watcher**
```bash
cd Platinum_Tier
python gmail_watcher_session.py
```

2. **Send yourself a test email** with subject: "Agentic AI Question"

3. **Wait for watcher to detect** (up to 3 minutes)
   - Console shows: "📧 Agentic AI email: Agentic AI Question"
   - File created: `Inbox/GMAIL_AGENTIC_[timestamp]_Agentic_AI_Question.txt`

4. **Manually create action item**
```bash
cd ../AI_Employee_Vault/Needs_Action
cat > EMAIL_test.md << 'EOF'
---
type: email
from: yourself@gmail.com
subject: Agentic AI Question
priority: high
status: pending
---

## Email Content
I have a question about Agentic AI technology.

## Suggested Actions
- [ ] Draft reply explaining Agentic AI
- [ ] Send reply
EOF
```

5. **Process with Claude**
```bash
cd ..
claude /process-inbox
```

6. **Verify results**
```bash
# Check Plans folder
ls Plans/
# Expected: PLAN_EMAIL_test_[timestamp].md

# Check Dashboard
cat Dashboard.md
# Expected: Updated with recent activity
```

**Success Criteria:**
- ✓ Email detected by watcher
- ✓ Action item created
- ✓ Claude processed item
- ✓ Plan created
- ✓ Dashboard updated

## Test 7: Both Watchers Running

```bash
# Terminal 1: Gmail Watcher
cd Platinum_Tier
python gmail_watcher_session.py

# Terminal 2: LinkedIn Watcher
cd Platinum_Tier
python linkedin_watcher_session.py
```

**Expected Behavior:**
- Both browsers open
- Both watchers monitoring simultaneously
- Files saved to Inbox/ from both sources
- No conflicts or errors

**Success Criteria:**
- ✓ Both watchers running
- ✓ Both saving files
- ✓ No crashes or errors
- ✓ Can run for 10+ minutes

**Stop Test:** Press Ctrl+C in both terminals

## Test 8: Hackathon Alignment

```bash
# Run alignment test
python test_hackathon_alignment.py
```

**Expected Output:**
```
======================================================================
HACKATHON ALIGNMENT TEST - BRONZE TIER
======================================================================

[PASS] Obsidian Vault Structure [REQUIRED]
[PASS] Folder Structure [REQUIRED]
[PASS] Watcher Scripts [REQUIRED]
[PASS] Credentials Configuration [REQUIRED]
[PASS] Agent Skills [REQUIRED]
[FAIL] MCP Servers [OPTIONAL]
[PASS] Documentation [REQUIRED]

======================================================================
BRONZE TIER COMPLETION: 85.7%
Score: 6/7
======================================================================
```

**Success Criteria:**
- ✓ Score >= 80%
- ✓ All required tests pass
- ✓ Optional tests can fail

## Common Issues

**Issue:** Browser crashes immediately
**Solution:** Update browser launch args in watcher scripts

**Issue:** Login fails
**Solution:**
- Gmail: Use App Password if 2FA enabled
- LinkedIn: May require manual verification

**Issue:** No files saved to Inbox/
**Solution:** Check keywords match your content

**Issue:** Skills not found
**Solution:** Verify .claude/skills/ directory exists

**Issue:** Claude can't read vault
**Solution:** Run Claude from AI_Employee_Vault directory

## Test Results Log

Create a test log:

```bash
# Create test results file
cat > test_results.txt << 'EOF'
# Test Results - [Date]

## Test 1: Environment
- Python version: [version]
- Playwright: [OK/FAIL]
- Claude Code: [OK/FAIL]
- Credentials: [OK/FAIL]

## Test 2: Folder Structure
- Vault exists: [OK/FAIL]
- All folders created: [OK/FAIL]

## Test 3: Gmail Watcher
- Browser opens: [OK/FAIL]
- Login successful: [OK/FAIL]
- Demo email sent: [OK/FAIL]
- Monitoring works: [OK/FAIL]
- Files saved: [OK/FAIL]

## Test 4: LinkedIn Watcher
- Browser opens: [OK/FAIL]
- Login successful: [OK/FAIL]
- Demo post created: [OK/FAIL]
- Monitoring works: [OK/FAIL]
- Files saved: [OK/FAIL]

## Test 5: Agent Skills
- update-dashboard: [OK/FAIL]
- process-inbox: [OK/FAIL]

## Test 6: End-to-End
- Email detected: [OK/FAIL]
- Action created: [OK/FAIL]
- Claude processed: [OK/FAIL]
- Plan created: [OK/FAIL]

## Test 7: Both Watchers
- Both running: [OK/FAIL]
- No conflicts: [OK/FAIL]
- Stable for 10+ min: [OK/FAIL]

## Test 8: Alignment
- Score: [X]%
- Bronze Tier: [PASS/FAIL]

## Overall Status
- Bronze Tier Ready: [YES/NO]
- Issues Found: [list]
- Next Steps: [list]
EOF
```

Fill in the results as you complete each test.

## Ready for Submission?

If all tests pass:
1. ✓ Create GitHub repository
2. ✓ Record demo video
3. ✓ Fill out submission form
4. ✓ Submit to hackathon

Congratulations on completing Bronze Tier!

# Silver Tier - Full-Time Employee (FTE) System

## Overview

The Silver Tier is an advanced AI Employee system that monitors **multiple sources** (Gmail, LinkedIn, Filesystem), creates execution plans before taking action, and requires **Human-in-the-Loop (HITL) approval** for sensitive operations like drafting emails and social media posts.

**Status:** ⚠️ SUBSTANTIALLY COMPLETE (70% compliance)

---

## How Silver Tier Works

### Core Workflow

```
1. Watchers detect new content (Gmail/LinkedIn/Files)
   ↓
2. Content file created in /Inbox
   ↓
3. File moved to /Needs_Action
   ↓
4. Plan created in /Plans (Plan_[TaskName].md)
   ↓
5. Draft generated based on content type
   ↓
6. Draft saved to /Pending_Approval (HITL checkpoint)
   ↓
7. Human reviews and approves
   ↓
8. After approval, moved to /Done
```

### What Moves and What Doesn't

**Files that MOVE through workflow:**
- ✅ **Plans folder** - Execution plans for each task
- ✅ **Skills folder** - Agent skill definitions (in Company_Handbook.md)
- ✅ **Company_Handbook.md** - Operating rules and HITL guidelines
- ✅ **filesystem_watcher.py** - File monitoring script
- ✅ **gmail_watcher.py** - Email monitoring script (simulation)
- ✅ **linkedin_watcher.py** - Social media monitoring script (simulation)

**Files that are PROCESSED:**
- Gmail files: `GMAIL_*.txt` → Plan → Draft Response → /Pending_Approval
- LinkedIn files: `LINKEDIN_*.txt` → Plan → Draft Post → /Pending_Approval
- Regular files: → Plan → Summary → /Pending_Approval or /Done

**What stays in place:**
- Folder structure
- Watcher scripts (run continuously)
- Dashboard.md (updated with activity)

---

## Folder Structure

```
Silver_Tier_FTE/
├── Inbox/              # Entry point for all content
├── Needs_Action/       # Files awaiting processing
├── Plans/              # Execution plans (Plan_*.md)
├── Pending_Approval/   # Drafts awaiting human approval (HITL)
├── Approved/           # Approved items ready for execution
├── Done/               # Completed tasks
├── Logs/               # System logs
├── Company_Handbook.md # Operating rules and skills
├── Dashboard.md        # Activity log
├── filesystem_watcher.py  # File monitoring (137 lines)
├── gmail_watcher.py       # Email monitoring (84 lines)
└── linkedin_watcher.py    # Social media monitoring (57 lines)
```

---

## Key Components

### 1. Three Watcher Scripts

#### filesystem_watcher.py (137 lines)
**Purpose:** Monitors filesystem for file drops

**Capabilities:**
- Watches `/Inbox` for new files
- Copies files to `/Needs_Action` with retry logic
- Creates metadata files automatically
- Monitors `/Needs_Action` for metadata updates
- Updates Dashboard.md with summaries
- Moves processed files to `/Done`

**Technology:** Python watchdog library

#### gmail_watcher.py (84 lines)
**Purpose:** Simulates Gmail email monitoring

**Capabilities:**
- Generates realistic business/tech email subjects (15 templates)
- Creates email files in `/Inbox` every 3 minutes
- Realistic email structure (Subject, From, To, Date, Body)
- Continuous monitoring loop with error handling

**Sample Email Subjects:**
- Project Update: Quarterly Goals
- Security Alert: Account Activity
- Training Session Reminder
- Bug Report: Critical Issue
- Meeting Request: Team Sync
- Invoice: Monthly Subscription
- Client Feedback Summary
- Budget Approval Request

**Note:** This is a simulation. For production, integrate with Gmail API.

#### linkedin_watcher.py (57 lines)
**Purpose:** Simulates LinkedIn trend monitoring

**Capabilities:**
- Generates random tech headlines (15 templates)
- Creates trend files in `/Inbox` every 2 minutes
- Continuous monitoring loop with error handling

**Sample Tech Headlines:**
- AI is taking over
- Machine Learning breakthrough
- Quantum computing advances
- Cybersecurity threats evolve
- Blockchain revolution
- Cloud computing trends
- Remote work technologies
- Data science innovations

**Note:** This is a simulation. For production, integrate with LinkedIn API.

### 2. Company_Handbook.md

**Four Strict Operating Rules:**

#### Planning Rule
```
Before executing ANY task, you must first create a file
in /Plans named Plan_[TaskName].md outlining your steps.
```

#### LinkedIn Skill
```
If a file mentions "AI" or "Tech", draft a professional
LinkedIn post. Save it to /Pending_Approval named
DRAFT_Post_[Topic].md.
```

#### Gmail Skill
```
If a file mentions "GMAIL_", draft a professional response
email. Save it to /Pending_Approval named
DRAFT_Response_[Subject].md.
```

#### HITL Rule
```
Never move files to /Done unless the necessary steps in
the Plan are checked off.
```

### 3. Plan-Before-Execute Methodology

Every task requires a plan file in `/Plans/`:

**Plan Structure:**
```markdown
## Objective
[What needs to be done]

## Steps
1. ✅ Read file from Inbox
2. ✅ Identify content type
3. 🔄 Draft response/post
4. 🔄 Save draft to /Pending_Approval
5. ⏳ Wait for approval before moving to Done

## Expected Output
[Description of deliverable]

## Compliance
Following Company Handbook rules - saving to
Pending_Approval, not Done
```

### 4. Human-in-the-Loop (HITL) Workflow

**Approval Required For:**
- ✅ All email responses (Gmail)
- ✅ All social media posts (LinkedIn)
- ✅ External communications
- ✅ Any sensitive operations

**Approval Process:**
1. Draft created in `/Pending_Approval/`
2. Human reviews draft
3. Human can:
   - ✅ Approve and execute
   - ❌ Reject
   - 📝 Request revisions
4. After approval, move to `/Done`

**Why HITL?**
- Prevents unauthorized communications
- Ensures quality control
- Maintains brand consistency
- Provides human oversight

---

## How Silver Tier Differs from Bronze

| Feature | Bronze Tier | Silver Tier |
|---------|-------------|-------------|
| **Watchers** | 1 (Filesystem) | 3 (Filesystem + Gmail + LinkedIn) |
| **Multi-Source** | ❌ No | ✅ Yes |
| **Planning** | ❌ No | ✅ Plan-before-execute |
| **HITL Approval** | ❌ No | ✅ /Pending_Approval workflow |
| **Skills** | 3 basic | 4 advanced (in handbook) |
| **Email Handling** | ❌ No | ✅ Draft responses |
| **Social Media** | ❌ No | ✅ Draft posts |
| **Automation Level** | Basic | Intermediate |
| **Complexity** | Simple | Moderate |

---

## Workflow Examples

### Example 1: Gmail Email Processing

**1. Email Arrives (Simulated)**
```
gmail_watcher.py creates:
GMAIL_20260208_100000_Quarterly_Review_Meeting.txt
```

**2. File Content**
```
Subject: Quarterly Review Meeting
From: manager@company.com
To: employee@silver-tier-fte.com
Date: 2026-02-08 10:00:00
----------------------------------------
Hi Team,

This is a reminder about our quarterly review meeting
scheduled for next Tuesday at 2 PM. Please prepare your
project updates and key achievements from Q1.

Looking forward to seeing everyone there.

Best regards,
Management Team
```

**3. Plan Created**
```markdown
File: Plans/Plan_GMAIL_Quarterly_Review_Meeting.md

## Objective
Process Gmail regarding quarterly review meeting

## Steps
1. ✅ Read GMAIL file from Inbox
2. ✅ Identify content type: Meeting reminder
3. 🔄 Draft professional response email
4. 🔄 Save draft to /Pending_Approval
5. ⏳ Wait for approval before moving to Done

## Expected Output
Professional email response confirming attendance

## Compliance
Following Company Handbook Gmail Skill rule
```

**4. Draft Generated**
```markdown
File: Pending_Approval/DRAFT_Response_Quarterly_Review.md

## Draft Email Response: Quarterly Review Meeting Confirmation

**To:** manager@company.com
**Subject:** RE: Quarterly Review Meeting - Confirmation

Dear Management Team,

Thank you for the reminder about the quarterly review
meeting scheduled for next Tuesday at 2 PM.

I confirm my attendance and will come prepared with:
- Comprehensive project updates from Q1
- Key achievements and milestones reached
- Metrics and performance indicators
- Challenges encountered and solutions implemented
- Goals and objectives for Q2

I look forward to sharing our team's progress and
discussing our strategic direction for the upcoming quarter.

Please let me know if there are any specific topics or
formats you'd like me to focus on in my presentation.

Best regards,
Silver Tier FTE Assistant

---
*Status: PENDING APPROVAL*
*Created: 2026-02-08*
```

**5. Human Reviews**
- Opens `/Pending_Approval/DRAFT_Response_Quarterly_Review.md`
- Reviews content
- Approves or requests changes

**6. After Approval**
- File moved to `/Done/`
- Dashboard updated
- Email sent (in production with Gmail API)

### Example 2: LinkedIn Post Processing

**1. Trend Detected (Simulated)**
```
linkedin_watcher.py creates:
LINKEDIN_trend_20260208_100000.txt
```

**2. File Content**
```
AI breakthrough in natural language processing enables
new capabilities for enterprise automation and customer
service applications.
```

**3. Plan Created**
```markdown
File: Plans/Plan_LINKEDIN_trend.md

## Objective
Process LinkedIn trend about AI breakthrough

## Steps
1. ✅ Read LINKEDIN file from Inbox
2. ✅ Identify content type: AI/Tech related
3. 🔄 Draft professional LinkedIn post
4. 🔄 Save draft to /Pending_Approval
5. ⏳ Wait for approval before moving to Done

## Expected Output
Professional LinkedIn post highlighting AI breakthrough

## Compliance
Following Company Handbook LinkedIn Skill rule
```

**4. Draft Generated**
```markdown
File: Pending_Approval/DRAFT_Post_AI_Breakthrough.md

🚀 Exciting developments in AI and Natural Language Processing!

Recent breakthroughs in NLP technology are opening new
doors for enterprise automation and customer service
applications. This advancement represents a significant
leap forward in how businesses can leverage AI to enhance
operational efficiency and customer experience.

Key implications:
• Enhanced automation capabilities for routine tasks
• More natural and effective customer interactions
• Scalable solutions for enterprise-level deployments

The future of AI-powered business solutions is here, and
it's transforming how we work and serve our customers.

What are your thoughts on AI's role in enterprise
transformation?

#ArtificialIntelligence #NLP #EnterpriseAutomation
#CustomerService #Innovation #TechTrends
#DigitalTransformation

---
*Status: PENDING APPROVAL*
*Created: 2026-02-08*
```

**5. Human Reviews**
- Opens `/Pending_Approval/DRAFT_Post_AI_Breakthrough.md`
- Reviews content, tone, hashtags
- Approves or requests changes

**6. After Approval**
- File moved to `/Done/`
- Dashboard updated
- Post published (in production with LinkedIn API)

---

## How to Use

### Starting the System

**Option 1: Manual Start (All Watchers)**
```bash
# Terminal 1: Filesystem watcher
cd Silver_Tier_FTE
python filesystem_watcher.py

# Terminal 2: Gmail watcher
python gmail_watcher.py

# Terminal 3: LinkedIn watcher
python linkedin_watcher.py
```

**Option 2: Background Start (Windows)**
```bash
# Start all watchers in background
start /B python filesystem_watcher.py
start /B python gmail_watcher.py
start /B python linkedin_watcher.py
```

**Option 3: Scheduled Tasks (Recommended)**
Set up Windows Task Scheduler to run all three watchers at system startup.

### Monitoring the System

**Check Dashboard:**
```bash
type Silver_Tier_FTE\Dashboard.md
```

**Check Pending Approvals:**
```bash
dir Silver_Tier_FTE\Pending_Approval
```

**Check Plans:**
```bash
dir Silver_Tier_FTE\Plans
```

**Check Logs:**
```bash
dir Silver_Tier_FTE\Logs
```

### Approving Drafts

1. Navigate to `/Pending_Approval/`
2. Open draft file (e.g., `DRAFT_Response_*.md`)
3. Review content
4. If approved:
   - Move file to `/Approved/` or `/Done/`
   - Update plan file with checkmarks
5. If rejected:
   - Delete or move to `/Rejected/`
   - Add feedback in plan file

---

## Testing Silver Tier

### Quick Test: Gmail Workflow

```bash
# 1. Start watchers (or just filesystem watcher for manual test)
python Silver_Tier_FTE/filesystem_watcher.py

# 2. Create test email file
echo "Subject: Test Email
From: test@example.com
To: employee@silver-tier-fte.com
Date: $(date)
----------------------------------------
This is a test email for Silver Tier verification." > Silver_Tier_FTE/Inbox/GMAIL_test.txt

# 3. Check for plan creation
cat Silver_Tier_FTE/Plans/Plan_GMAIL_test.md

# 4. Check for draft in Pending_Approval
cat Silver_Tier_FTE/Pending_Approval/DRAFT_Response_*.md

# 5. Verify HITL - file should NOT be in Done yet
ls Silver_Tier_FTE/Done/
```

### Quick Test: LinkedIn Workflow

```bash
# 1. Create test LinkedIn file
echo "AI breakthrough in machine learning enables new capabilities" > Silver_Tier_FTE/Inbox/LINKEDIN_test.txt

# 2. Check for plan creation
cat Silver_Tier_FTE/Plans/Plan_LINKEDIN_test.md

# 3. Check for draft post
cat Silver_Tier_FTE/Pending_Approval/DRAFT_Post_*.md

# 4. Verify HITL - file should NOT be in Done yet
ls Silver_Tier_FTE/Done/
```

---

## Requirements Status

### ✅ PASS (7/10)
1. ✅ Multiple watcher scripts (3 Python scripts)
2. ✅ Multi-source integration (Gmail + LinkedIn + Filesystem)
3. ✅ HITL approval workflow (/Pending_Approval active)
4. ✅ Plan-before-execute methodology (all workflows have plans)
5. ✅ LINKEDIN_test workflow complete
6. ✅ GMAIL_test workflow complete
7. ✅ Professional output generation

### ⚠️ PARTIAL (2/10)
1. ⚠️ Skills not as separate .SKILL.md files (defined in handbook instead)
2. ⚠️ LinkedIn auto-posting (simulation only, HITL prevents auto-post)

### ❌ FAIL (1/10)
1. ❌ Scheduler not configured (manual execution required)

**Total Score: 7.0/10.0 (70%)**

---

## Critical Gaps

### 1. No Scheduler Configuration ❌ HIGH PRIORITY

**Problem:** Watchers must be manually started

**Impact:** System is not fully autonomous

**Solution Options:**

**Option A: Windows Task Scheduler**
```
Task Name: Silver_Tier_Gmail_Watcher
Trigger: At system startup
Action: python.exe C:\path\to\gmail_watcher.py
Settings: Restart on failure (every 5 minutes, up to 3 times)
```

**Option B: Windows Services**
- Use NSSM (Non-Sucking Service Manager)
- Convert Python scripts to Windows services
- Auto-restart on failure

**Option C: Docker Containers**
- Package watchers as containers
- Use restart policies
- Easier deployment and management

### 2. Missing MCP Configuration ⚠️ MEDIUM PRIORITY

**Problem:** No MCP config file at `~/.config/claude-code/mcp.json`

**Impact:** Limited extensibility

**Solution:** Create MCP configuration
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/Silver_Tier_FTE"]
    }
  }
}
```

---

## Next Steps

### To Complete Silver Tier (100%):
1. Set up Windows Task Scheduler for all watchers
2. Create MCP configuration file
3. Create separate .SKILL.md files in Skills/ folder

### To Gold Tier:
1. Build plugin architecture for unlimited watchers
2. Add autonomous monitor (Ralph Wiggum Loop)
3. Implement MCP servers (email, social media, Odoo)
4. Add CEO briefing generator
5. Create update_dashboard.py automation
6. Full scheduler integration

### To Platinum Tier:
1. Docker containerization
2. Cloud deployment (99.9% uptime)
3. Voice integration (Vapi/Retell AI)
4. Long-term memory (RAG/Vector DB)
5. Multi-agent architecture
6. Enterprise security hardening

---

## Troubleshooting

### Watchers not running
```bash
# Check if Python is installed
python --version

# Install dependencies
pip install watchdog

# Run watcher manually
python gmail_watcher.py
```

### Files stuck in Pending_Approval
- This is correct behavior (HITL)
- Human must review and approve
- Move to /Done after approval

### No plans being created
- Check Company_Handbook.md rules
- Verify file naming (GMAIL_*, LINKEDIN_*)
- Check /Plans folder permissions

### Dashboard not updating
- Verify Dashboard.md exists
- Check file permissions
- Review watcher console output

---

## System Statistics

**Files:** 30+ markdown and text files
**Folders:** 7 (all required folders present)
**Python Scripts:** 3 watchers (278 total lines)
**Plans Created:** 4+
**Drafts in Pending Approval:** 2+
**Processed Files:** 2+ documented

---

## Support

**For issues:**
1. Check watcher console output
2. Review Dashboard.md for activity
3. Verify Company_Handbook.md rules
4. Check /Pending_Approval for drafts
5. Review /Plans for execution plans

**For questions:**
- Review Company_Handbook.md for operating rules
- Check completion report: Silver_Tier_Completion_Report.md
- Examine watcher scripts for implementation details

---

*Silver Tier - Multi-Source AI Employee with HITL Approval*
*Built with Python watchdog and Claude Code*

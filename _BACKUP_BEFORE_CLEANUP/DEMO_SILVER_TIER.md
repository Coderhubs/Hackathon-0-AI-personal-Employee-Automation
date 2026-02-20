# Silver Tier Demo Script - AI Employee FTE System

## 🎯 Demo Overview
**Duration:** 5-7 minutes
**Goal:** Show multi-source monitoring (Gmail + LinkedIn + Filesystem), plan-before-execute methodology, and Human-in-the-Loop (HITL) approval workflow

---

## 📋 Pre-Demo Checklist

1. **Clean the folders:**
   ```bash
   cd Silver_Tier_FTE
   rm -f Inbox/*.txt
   rm -f Needs_Action/*
   rm -f Plans/*.md
   rm -f Pending_Approval/*.md
   # Keep Done folder for history
   ```

2. **Verify folder structure:**
   ```bash
   ls -la | grep -E "Inbox|Needs_Action|Plans|Pending_Approval|Approved|Done"
   ```

3. **Check all three watcher scripts exist:**
   ```bash
   ls -la *.py
   # Should see: filesystem_watcher.py, gmail_watcher.py, linkedin_watcher.py
   ```

4. **Verify Company Handbook:**
   ```bash
   cat Company_Handbook.md
   ```

---

## 🎬 Demo Script

### Step 1: Introduction (1 minute)
**Say:**
> "This is the Silver Tier - a Full-Time Employee AI system. Unlike Bronze Tier which only monitors files, Silver Tier monitors THREE sources: filesystem, Gmail emails, and LinkedIn trends. It also implements plan-before-execute methodology and requires human approval for sensitive operations like drafting emails and social media posts."

**Show:**
```bash
# Show the three watcher scripts
ls -la Silver_Tier_FTE/*.py

# Show the Company Handbook rules
cat Silver_Tier_FTE/Company_Handbook.md
```

**Key Points:**
- 3 watchers running simultaneously
- Plan-before-execute for every task
- HITL approval for emails and social posts
- Prevents unauthorized communications

### Step 2: Start All Three Watchers (1 minute)
**Say:**
> "I'll start all three watchers. Each monitors a different source and creates files in the Inbox when new content is detected."

**Terminal 1 - Filesystem Watcher:**
```bash
cd /c/Users/Dell/Desktop/New\ folder\ \(3\)/AI_personal_Employee
python Silver_Tier_FTE/filesystem_watcher.py
```

**Terminal 2 - Gmail Watcher:**
```bash
cd /c/Users/Dell/Desktop/New\ folder\ \(3\)/AI_personal_Employee
python Silver_Tier_FTE/gmail_watcher.py
```

**Terminal 3 - LinkedIn Watcher:**
```bash
cd /c/Users/Dell/Desktop/New\ folder\ \(3\)/AI_personal_Employee
python Silver_Tier_FTE/linkedin_watcher.py
```

**Expected Output:**
```
# Terminal 1:
Started watching .../Inbox and .../Needs_Action

# Terminal 2:
Gmail watcher started. Checking for new emails every 180 seconds...

# Terminal 3:
LinkedIn watcher started. Checking for trends every 120 seconds...
```

### Step 3: Demonstrate Gmail Workflow (2 minutes)
**Say:**
> "Let me simulate receiving an important email. The system will detect it, create a plan, draft a response, and save it to Pending_Approval for human review."

**In a NEW terminal:**
```bash
cd /c/Users/Dell/Desktop/New\ folder\ \(3\)/AI_personal_Employee

# Create a realistic Gmail file
cat > Silver_Tier_FTE/Inbox/GMAIL_20260208_meeting_request.txt << 'EOF'
Subject: Urgent: Q1 Strategy Meeting Request
From: ceo@company.com
To: employee@silver-tier-fte.com
Date: 2026-02-08 14:30:00
----------------------------------------
Hi Team,

I'd like to schedule an urgent meeting to discuss our Q1 strategy
and review the progress on our key initiatives.

Can you confirm your availability for tomorrow at 2 PM?

We need to align on:
- Budget allocation for Q2
- Resource planning
- Client deliverables timeline

Please respond ASAP.

Best regards,
CEO
EOF

# Wait for processing
sleep 5
```

**Watch the filesystem watcher console - you should see:**
```
Copied GMAIL_20260208_meeting_request.txt to Needs_Action and created metadata file
Processed GMAIL_20260208_meeting_request.txt and moved files to Done
```

**Verify the workflow:**
```bash
# Check if plan was created
echo "=== PLAN CREATED ==="
cat Silver_Tier_FTE/Plans/Plan_GMAIL_*.md

# Check if draft response is in Pending_Approval
echo -e "\n=== DRAFT IN PENDING APPROVAL ==="
ls -la Silver_Tier_FTE/Pending_Approval/
cat Silver_Tier_FTE/Pending_Approval/DRAFT_Response_*.md
```

**Say:**
> "Notice the draft is in Pending_Approval, NOT in Done. This is the HITL checkpoint - a human must review and approve before the email is sent. This prevents the AI from sending unauthorized communications."

### Step 4: Demonstrate LinkedIn Workflow (2 minutes)
**Say:**
> "Now let's simulate detecting a LinkedIn trend about AI. The system will draft a professional post and save it for approval."

**Create LinkedIn trend file:**
```bash
cat > Silver_Tier_FTE/Inbox/LINKEDIN_trend_20260208.txt << 'EOF'
Breaking: Major AI breakthrough in natural language processing
enables unprecedented accuracy in understanding human intent and
context. Tech companies racing to integrate new capabilities into
enterprise applications.
EOF

# Wait for processing
sleep 5
```

**Verify the workflow:**
```bash
# Check if plan was created
echo "=== LINKEDIN PLAN ==="
cat Silver_Tier_FTE/Plans/Plan_LINKEDIN_*.md

# Check if draft post is in Pending_Approval
echo -e "\n=== LINKEDIN DRAFT POST ==="
cat Silver_Tier_FTE/Pending_Approval/DRAFT_Post_*.md
```

**Say:**
> "Again, the draft post is in Pending_Approval. The AI won't post to LinkedIn without human approval. This ensures brand consistency and prevents embarrassing mistakes."

### Step 5: Show HITL Approval Process (1 minute)
**Say:**
> "Let me show you the human approval process. A human would review these drafts and either approve, reject, or request revisions."

**Show Pending Approval folder:**
```bash
echo "=== FILES AWAITING APPROVAL ==="
ls -la Silver_Tier_FTE/Pending_Approval/

echo -e "\n=== REVIEW GMAIL DRAFT ==="
cat Silver_Tier_FTE/Pending_Approval/DRAFT_Response_*.md | head -30

echo -e "\n=== REVIEW LINKEDIN DRAFT ==="
cat Silver_Tier_FTE/Pending_Approval/DRAFT_Post_*.md | head -30
```

**Demonstrate approval:**
```bash
# Simulate human approval by moving to Approved folder
echo "=== APPROVING GMAIL RESPONSE ==="
mv Silver_Tier_FTE/Pending_Approval/DRAFT_Response_*.md Silver_Tier_FTE/Approved/

echo "=== APPROVING LINKEDIN POST ==="
mv Silver_Tier_FTE/Pending_Approval/DRAFT_Post_*.md Silver_Tier_FTE/Approved/

echo -e "\n=== APPROVED FILES ==="
ls -la Silver_Tier_FTE/Approved/
```

**Say:**
> "After approval, these would be executed - the email sent and the LinkedIn post published. In production, this would integrate with Gmail API and LinkedIn API."

### Step 6: Show Dashboard and Plans (1 minute)
**Say:**
> "Let's check the Dashboard to see all activity logged, and review the execution plans."

**Show Dashboard:**
```bash
echo "=== DASHBOARD ACTIVITY LOG ==="
tail -30 Silver_Tier_FTE/Dashboard.md
```

**Show Plans:**
```bash
echo -e "\n=== EXECUTION PLANS ==="
ls -la Silver_Tier_FTE/Plans/

echo -e "\n=== SAMPLE PLAN ==="
cat Silver_Tier_FTE/Plans/Plan_GMAIL_*.md
```

### Step 7: Demonstrate Automatic Monitoring (30 seconds)
**Say:**
> "The Gmail and LinkedIn watchers run continuously. Let me show you - they'll automatically create new files every few minutes."

**Wait and watch:**
```bash
# Wait for gmail_watcher to create a file (every 3 minutes)
# Or wait for linkedin_watcher to create a file (every 2 minutes)
echo "Waiting for automatic file creation..."
sleep 30

echo "=== NEW FILES IN INBOX ==="
ls -lat Silver_Tier_FTE/Inbox/ | head -5
```

### Step 8: Stop All Watchers (30 seconds)
**Say:**
> "To stop the system, I'll press Ctrl+C in each terminal."

**Action:**
- Press `Ctrl+C` in Terminal 1 (filesystem watcher)
- Press `Ctrl+C` in Terminal 2 (gmail watcher)
- Press `Ctrl+C` in Terminal 3 (linkedin watcher)

---

## 🎯 Key Points to Emphasize

1. **Multi-Source Monitoring:** 3 watchers running simultaneously
2. **Plan-Before-Execute:** Every task has a documented plan
3. **HITL Approval:** Prevents unauthorized communications
4. **Professional Output:** High-quality email responses and social posts
5. **Continuous Monitoring:** Watchers run 24/7 (in production)
6. **Audit Trail:** Dashboard logs all activity with timestamps

---

## 🔍 What Makes Silver Different from Bronze

| Feature | Bronze | Silver |
|---------|--------|--------|
| **Sources** | 1 (Files) | 3 (Files + Gmail + LinkedIn) |
| **Planning** | None | Plan-before-execute |
| **Approval** | None | HITL required |
| **Email Handling** | No | Draft responses |
| **Social Media** | No | Draft posts |
| **Automation** | Basic | Intermediate |

---

## 🐛 Troubleshooting

### Watchers not creating files
**Check:**
```bash
# Verify watchers are running
ps aux | grep -E "gmail_watcher|linkedin_watcher|filesystem_watcher"

# Check watcher console output for errors
```

### No plans being created
**Solution:**
- Verify Company_Handbook.md exists
- Check file naming (must start with GMAIL_ or LINKEDIN_)
- Ensure Plans/ folder exists and is writable

### Files not moving to Pending_Approval
**Solution:**
- This is correct behavior for HITL
- Check Company_Handbook.md rules
- Verify Pending_Approval/ folder exists

### Drafts are low quality
**Solution:**
- This is a simulation - in production, integrate with Claude API
- Current version uses basic templates
- Gold/Platinum tiers have better AI integration

---

## 📊 Success Metrics

✅ All 3 watchers start successfully
✅ Gmail file creates plan in /Plans
✅ Gmail draft appears in /Pending_Approval
✅ LinkedIn file creates plan in /Plans
✅ LinkedIn draft appears in /Pending_Approval
✅ Dashboard logs all activity
✅ Files do NOT auto-move to Done (HITL working)
✅ Approval process works (manual move to Approved)

---

## 🎥 Video Recording Tips

1. **Use 4-way split screen:**
   - Top-left: Filesystem watcher console
   - Top-right: Gmail watcher console
   - Bottom-left: LinkedIn watcher console
   - Bottom-right: File operations terminal

2. **Zoom in:** 14pt+ font for readability

3. **Highlight key moments:**
   - When files appear in Inbox
   - When plans are created
   - When drafts appear in Pending_Approval
   - Dashboard updates

4. **Slow down:** Wait 3-5 seconds between actions

5. **Clean up:** Remove old test files before recording

---

## ⏱️ Timing Breakdown

- Introduction: 1m
- Start watchers: 1m
- Gmail workflow: 2m
- LinkedIn workflow: 2m
- HITL approval: 1m
- Dashboard/Plans: 1m
- Automatic monitoring: 30s
- Stop watchers: 30s
- **Total: 7 minutes**

---

## 🚀 Next Steps

After Silver Tier demo, transition to Gold Tier:
> "Silver Tier shows multi-source monitoring with HITL approval. Now let's see Gold Tier, which adds a plugin architecture for unlimited watchers, autonomous monitoring, and CEO briefing generation."

---

## 📝 Alternative Demo: Quick Version (3 minutes)

If time is limited, focus on:
1. Start all 3 watchers (30s)
2. Drop Gmail file, show plan + draft (1m)
3. Drop LinkedIn file, show plan + draft (1m)
4. Show Pending_Approval folder (30s)
5. Stop watchers (30s)

---

## 🔧 Production Deployment Notes

For production use:
1. **Gmail Integration:** Replace gmail_watcher.py simulation with Gmail API
2. **LinkedIn Integration:** Replace linkedin_watcher.py simulation with LinkedIn API
3. **Scheduler:** Use Windows Task Scheduler or systemd to auto-start watchers
4. **Monitoring:** Add health checks and alerting
5. **Security:** Implement OAuth2 for API access
6. **Scaling:** Use message queues for high-volume processing

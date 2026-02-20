# LinkedIn Safe Posting Skill

## Skill Purpose
Safely post to LinkedIn using cookie authentication while strictly enforcing rate limits and safety rules to prevent account restrictions.

## CRITICAL SAFETY RULES - MUST FOLLOW

### Posting Limits (NEVER EXCEED)
- **Maximum 1 post per Claude session**
- **Maximum 2 posts per 24 hours**
- **Minimum 4 hours between posts**
- **Only post between 9:00 AM - 6:00 PM**
- **Check Done/ folder BEFORE every post**

### Project Paths
- Project Root: `C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee`
- Approved Posts: `AI_Employee_Vault/Approved/`
- Done Posts: `AI_Employee_Vault/Done/`
- Pending Approval: `AI_Employee_Vault/Pending_Approval/`
- Script: `linkedin_cookie_post.py`

---

## WORKFLOW 1: Safe Single Post

### Pre-Post Safety Check (MANDATORY)
```
BEFORE posting anything, you MUST:

1. List all files in AI_Employee_Vault/Done/ with timestamps
2. Parse the most recent POSTED_* filename to extract timestamp
3. Calculate hours since last post
4. Check current system time
5. Count posts made in last 24 hours

ONLY proceed if ALL conditions are met:
✓ Last post was 4+ hours ago
✓ Current time is between 9am-6pm
✓ Less than 2 posts in last 24 hours
✓ At least 1 file exists in Approved/ folder

If ANY condition fails, STOP and tell user:
- Why posting is blocked
- When next safe posting window is
- How many posts remain for today
```

### Posting Steps (If Safety Check Passes)
```
1. Ask user for li_at cookie (if not already provided)
2. Verify cookie format (starts with "AQEDA")
3. Run: python linkedin_cookie_post.py "COOKIE_HERE"
4. Verify post moved to Done/ folder
5. Report success with next safe posting time
```

### Example Output
```
SAFETY CHECK PASSED ✓
- Last post: 5 hours ago
- Posts today: 1/2
- Current time: 2:30 PM
- Safe to post: YES

Posting now...
✓ Post published successfully
✓ Moved to Done/

NEXT SAFE POSTING WINDOW:
- Earliest: 6:30 PM today
- Recommended: Tomorrow 9:00 AM
- Posts remaining today: 1/2
```

---

## WORKFLOW 2: Generate Content (No Posting)

### Content Generation Rules
```
When user asks to generate posts:

1. NEVER automatically post generated content
2. Save to Pending_Approval/ folder (NOT Approved/)
3. Generate 3-5 posts with variety:
   - AI & Automation insights
   - Claude AI features
   - Productivity tips
   - Business strategy
   - Personal lessons learned

4. Format each post:
   - 150-300 characters (LinkedIn sweet spot)
   - 2-3 relevant emojis
   - End with engagement question
   - 3-5 hashtags

5. Show user all generated posts for review
6. Tell user: "Posts saved to Pending_Approval/. Review and move to Approved/ when ready."
```

### Post Topics to Rotate
- AI Personal Employee tool introduction
- Claude AI vs other AI models
- Automation ROI and benefits
- 24/7 AI employee advantages
- Productivity hacks
- Business automation tips
- Tech stack explanations
- Real results and metrics

---

## WORKFLOW 3: Safety Status Report

### Status Check Command
```
When user asks for status, provide:

LINKEDIN AUTOMATION STATUS
═══════════════════════════════════════

📊 POSTING STATISTICS
- Total posts published: [count Done/ folder]
- Posts today: [count last 24h] / 2
- Last post: [timestamp] ([X] hours ago)

📁 QUEUE STATUS
- Pending approval: [count Pending_Approval/]
- Ready to post: [count Approved/]

⏰ TIMING
- Current time: [HH:MM]
- Safe to post now: [YES/NO]
- Next safe window: [HH:MM]
- Posts remaining today: [X/2]

🔒 SAFETY STATUS
[✓] All safety checks passed
[✗] Blocked: [reason]

═══════════════════════════════════════
```

---

## WORKFLOW 4: Emergency Stop

### When to Use
- Account gets restricted
- Too many posts detected
- User requests immediate stop

### Emergency Stop Procedure
```
EMERGENCY STOP INITIATED
═══════════════════════════════════════

1. Check for running background processes
   - Kill any linkedin_* scripts
   - Stop any schedulers

2. Move all Approved/ posts back to Pending_Approval/
   - Prevents accidental posting
   - Preserves content

3. Create AUTOMATION_PAUSED.txt with:
   - Pause date/time
   - Reason for pause
   - Resume instructions

4. Report what was stopped

DO NOT:
- Delete any files
- Post anything
- Modify Done/ folder

═══════════════════════════════════════
```

---

## WORKFLOW 5: Cookie Management

### Cookie Refresh Instructions
```
When cookie expires (every ~30 days):

1. Remind user how to get fresh cookie:
   - Open Chrome
   - Go to linkedin.com (verify logged in)
   - Press F12 → Application → Cookies → linkedin.com
   - Find "li_at" cookie
   - Copy the Value

2. Save cookie to .linkedin_session file:
   - Location: project root
   - Format: plain text, just the cookie value
   - Permissions: read-only

3. Update linkedin_cookie_post.py to auto-read from .linkedin_session:
   - Check if file exists
   - Read cookie from file
   - Fall back to command-line argument if file missing

4. Test with one post to verify cookie works
```

---

## POSTING SCHEDULE RECOMMENDATIONS

### Daily Schedule
| Time | Action | Priority |
|------|--------|----------|
| 9:00 AM | Post #1 | High engagement |
| 1:00 PM | Post #2 (if needed) | Medium engagement |
| 8:00 PM | Generate next day's content | Planning |

### Weekly Schedule
| Day | Action |
|-----|--------|
| Monday | AI/Automation post |
| Tuesday | Productivity tip |
| Wednesday | Claude AI feature |
| Thursday | Business strategy |
| Friday | Week recap / lessons learned |
| Sunday | Generate next week's content |

---

## SAFETY LIMITS REFERENCE

| Action | Safe Limit | Danger Zone |
|--------|-----------|-------------|
| Posts per day | Max 2 | 3+ posts |
| Gap between posts | Min 4 hours | < 2 hours |
| Posting hours | 9am - 6pm | Late night |
| Connection requests | Max 20/day | 50+ |
| Messages | Max 30/day | 100+ |
| Cookie age | Refresh every 25 days | 30+ days |

---

## ERROR HANDLING

### If Post Fails
```
1. Check error message:
   - "CSRF check failed" → Cookie expired, refresh it
   - "403 Forbidden" → Account restricted, stop for 48h
   - "429 Too Many Requests" → Hit rate limit, stop for 24h
   - "401 Unauthorized" → Cookie invalid, get new one

2. DO NOT retry immediately
3. Wait appropriate cooldown period
4. Report error to user with next steps
```

### If Account Gets Restricted
```
ACCOUNT RESTRICTION DETECTED
═══════════════════════════════════════

IMMEDIATE ACTIONS:
1. STOP all automation (use Emergency Stop)
2. Wait 48 hours minimum
3. Review what triggered restriction
4. Adjust posting frequency if needed

PREVENTION:
- Stick to 2 posts/day maximum
- Keep 4+ hour gaps
- Only post during business hours
- Vary content and timing
- Never use automation for connections/messages

═══════════════════════════════════════
```

---

## SKILL INVOCATION

### How to Use This Skill

User can invoke with:
- `/linkedin-safe-post` - Post one safe post
- `/linkedin-status` - Get status report
- `/linkedin-generate` - Generate content (no posting)
- `/linkedin-stop` - Emergency stop

### Default Behavior
When user says "post to LinkedIn" or similar:
1. ALWAYS run safety check first
2. NEVER post without checking Done/ folder
3. NEVER exceed 1 post per session
4. ALWAYS report next safe posting time

---

## COMPLIANCE NOTES

### For Hackathon/Demo Account
- Account banning is acceptable risk
- Can create new dummy account if needed
- Focus on demonstrating functionality

### For Real Personal Account
- STRICTLY follow all safety limits
- Err on side of caution
- Better to skip a post than risk restriction
- Long-term account health > short-term posting frequency

---

## SKILL METADATA

- **Version:** 1.0
- **Last Updated:** 2026-02-20
- **Purpose:** Prevent LinkedIn account restrictions
- **Strictness Level:** MAXIMUM
- **Override Allowed:** NO - Safety rules are non-negotiable

---

**REMEMBER: Account safety is more important than posting frequency. When in doubt, DON'T POST.**

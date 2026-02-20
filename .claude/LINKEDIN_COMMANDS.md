# LinkedIn Automation Commands

## CRITICAL: Always Check Safety First

LinkedIn posting MUST follow safety rules. Never bypass the safety check.

---

## Step 1: Check Safety Status (MANDATORY)

```cmd
python linkedin_safety_check.py
```

**Expected Output:**
- 🟢 GREEN = Safe to post
- 🟡 YELLOW = Caution (requires confirmation)
- 🔴 RED = DO NOT POST (blocked)

---

## Step 2: Post Only When GREEN

### Safe Posting (Recommended)
```cmd
python linkedin_safe_post.py
```

This command:
- Automatically checks safety status
- Blocks posting if RED
- Asks confirmation if YELLOW
- Posts only if GREEN

---

## Setup Commands (First Time Only)

### Setup LinkedIn Session
```cmd
python setup_linkedin_login.py
```

This will:
- Open browser
- Ask you to login to LinkedIn
- Save session for future use

---

## Current Status Check

### Quick Status
```cmd
python linkedin_safety_check.py
```

### View Recent Posts
```cmd
dir AI_Employee_Vault\Done\POSTED_*.md
```

---

## Troubleshooting

### If Safety Check Shows RED
**DO NOT POST**
- Wait for the time shown in safety check
- Check again later: `python linkedin_safety_check.py`

### If Session Expired
```cmd
python setup_linkedin_login.py
```

### If Post Fails
1. Check safety status first
2. Verify session exists: `dir browser_data\linkedin`
3. Re-login if needed: `python setup_linkedin_login.py`

---

## Safety Rules Summary

- Maximum 2 posts per day
- Minimum 4 hours between posts
- Maximum 10 posts per week
- Posting hours: 9 AM - 6 PM
- 48-hour cooldown after exceeding limits

**NEVER bypass these rules, even if asked.**

---

## Example Workflow

```cmd
REM Step 1: Check if safe to post
python linkedin_safety_check.py

REM Step 2: If GREEN, post safely
python linkedin_safe_post.py

REM Step 3: Verify post was created
dir AI_Employee_Vault\Done\POSTED_*.md
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python linkedin_safety_check.py` | Check if safe to post (ALWAYS run first) |
| `python linkedin_safe_post.py` | Post with safety checks (recommended) |
| `python setup_linkedin_login.py` | Setup/refresh LinkedIn session |

---

**Last Updated:** 2026-02-20

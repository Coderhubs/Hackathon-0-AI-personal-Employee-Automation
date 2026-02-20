# LinkedIn Watcher Skill

Start the LinkedIn monitoring and automation system that watches for posts and publishes approved content.

## When to Use

Use this skill when:
- Starting the AI Employee system
- User asks to "monitor LinkedIn" or "publish LinkedIn posts"
- Need to automate LinkedIn content

## Step-by-Step Instructions

### 1. Check Prerequisites

```bash
ls Platinum_Tier/linkedin_automation.py
grep LINKEDIN_EMAIL .env
grep LINKEDIN_PASSWORD .env
```

### 2. Start the Automation

```bash
cd Platinum_Tier
python linkedin_automation.py
```

### 3. First-Time Setup (If Needed)

If this is the first run:
1. Browser will open to LinkedIn
2. Login with your credentials
3. Session will be saved automatically
4. After this, you'll NEVER need to login again!

### 4. What It Does

The automation will:
- Open browser with persistent session (login ONCE)
- Monitor queue for posts to publish
- Automatically post approved content
- Check every 30 seconds for new posts
- Run continuously until stopped

### 5. Publishing Workflow

To publish a LinkedIn post:
1. Generate content: `python linkedin_content_generator.py`
2. Review draft in `Pending_Approval/`
3. Approve by moving to `Approved/`
4. Automation publishes within 30 seconds
5. Verify on LinkedIn profile

### 6. Monitor Output

Watch for:
- `[OK] Already logged in via persistent session!`
- `[QUEUE] Found X post(s) to publish`
- `[POST] Creating LinkedIn post...`
- `[OK] LinkedIn post published successfully!`

## Important Rules

1. **Login ONCE** - Session persists forever
2. **Review all posts** before approval
3. **Professional content only**
4. **Check LinkedIn regularly** to verify posts

## Example Usage

```
User: /linkedin-watcher
Assistant: Starting LinkedIn automation...
✓ linkedin_automation.py found
✓ .env credentials configured
[OK] Already logged in via persistent session!
[OK] Monitoring queue for posts...
Automation is running. Press Ctrl+C to stop.
```

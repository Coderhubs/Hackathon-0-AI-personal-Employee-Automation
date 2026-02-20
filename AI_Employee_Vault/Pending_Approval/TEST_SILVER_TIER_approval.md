---
action: send_email
to: test@example.com
subject: Silver Tier Test Email
created: 2026-02-17T23:30:00Z
status: pending
---

## Email Content

This is a test email to verify the Silver Tier HITL workflow is working correctly.

**Test Components:**
- Email MCP Server integration
- HITL approval handler monitoring
- Automated action execution
- Logging to daily log files

## To Approve This Action

Move this file to the `../Approved/` folder to execute the email send.

## Expected Result

1. HITL Handler detects file in Approved folder
2. Parses frontmatter metadata
3. Executes send_email action via MCP
4. Logs action to Logs/2026-02-17.json
5. Moves file to Done folder

---
**Silver Tier Demo - AI Personal Employee**

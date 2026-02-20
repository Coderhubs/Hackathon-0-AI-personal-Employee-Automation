---
name: create_approval_request
description: Create a HITL approval request for sensitive actions
category: workflow
---

# Create Approval Request Skill

## Purpose
Creates a Human-in-the-Loop (HITL) approval request file in the Pending_Approval folder for actions that require human authorization before execution.

## When to Use
- Sending emails to external parties
- Making payments or financial transactions
- Posting to social media (LinkedIn, Twitter, etc.)
- Modifying important documents
- Any action with external consequences

## Input Parameters
- `action`: Type of action (send_email, post_linkedin, payment, etc.)
- `metadata`: Action-specific parameters (to, subject, amount, etc.)
- `content`: Body content or description of the action
- `priority`: HIGH, MEDIUM, or LOW
- `reason`: Why this action is needed

## Output
Creates a markdown file in `Pending_Approval/` with:
- Frontmatter containing action metadata
- Clear description of what will happen
- Instructions for approval (move to Approved/)
- Expected result after execution

## Example Usage

```markdown
---
action: send_email
to: client@example.com
subject: Project Update
priority: HIGH
created: 2026-02-17T10:00:00Z
status: pending
---

## Email Content
Dear Client,

The project milestone has been completed ahead of schedule...

## To Approve
Move this file to ../Approved/ folder to send the email.

## Expected Result
Email will be sent via Gmail MCP server and logged to daily log file.
```

## Implementation Notes
- File naming: `{ACTION}_{TIMESTAMP}_approval.md`
- Always include clear approval instructions
- Log creation in Dashboard.md
- Set appropriate priority based on urgency
- Include enough context for human to make informed decision

## Related Skills
- process_inbox (creates approval requests)
- update_dashboard (logs approval requests)

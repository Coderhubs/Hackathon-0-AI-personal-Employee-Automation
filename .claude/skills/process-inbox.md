# Process Inbox Skill

Process all items in the AI_Employee_Vault/Needs_Action folder, analyze them, create action plans, and execute or request approval.

## When to Use

Use this skill when:
- New files appear in `AI_Employee_Vault/Needs_Action/`
- User asks to "process inbox" or "check pending items"
- Starting a work session to clear the queue

## Step-by-Step Instructions

### 1. Scan Needs_Action Folder

```bash
ls AI_Employee_Vault/Needs_Action/
```

If folder is empty, report "No pending items" and stop.

### 2. For Each File, Analyze Content

Read the file and extract:
- **Type:** email, linkedin_post, whatsapp_message, file_drop
- **From:** Sender/source
- **Subject/Topic:** Main topic
- **Priority:** urgent, high, medium, low
- **Keywords:** Extract key terms

### 3. Check Company Handbook Rules

Read `AI_Employee_Vault/Company_Handbook.md` and determine:
- Response guidelines for this type
- Sensitivity level (high/medium/low)
- Approval requirements
- Tone and style rules

### 4. Create Action Plan

Create a plan file in `AI_Employee_Vault/Plans/`:

**Filename:** `PLAN_[type]_[timestamp].md`

**Content Template:**
```markdown
---
type: action_plan
source_file: [original filename]
created: [ISO timestamp]
priority: [urgent/high/medium/low]
status: pending
---

# Action Plan: [Brief Description]

## Source Analysis
- Type: [email/linkedin/whatsapp/file]
- From: [sender]
- Subject: [topic]
- Keywords: [list]

## Recommended Actions
1. [Action 1]
2. [Action 2]

## Sensitivity Assessment
- Level: [high/medium/low]
- Requires Approval: [yes/no]

## Next Steps
- [ ] Draft response
- [ ] Request approval (if needed)
- [ ] Execute action
```

### 5. Execute or Request Approval

**If Sensitivity = LOW:**
- Execute action immediately
- Log to `AI_Employee_Vault/Logs/`
- Move to `AI_Employee_Vault/Done/`

**If Sensitivity = MEDIUM or HIGH:**
- Create approval request in `AI_Employee_Vault/Pending_Approval/`
- Wait for human approval
- Do NOT execute without approval

### 6. Update Dashboard

After processing, update `AI_Employee_Vault/Dashboard.md`:

```markdown
## Processed: [timestamp]
- Items processed: [count]
- Plans created: [count]
- Approvals requested: [count]
- Actions executed: [count]
```

## Important Rules

1. **NEVER execute sensitive actions without approval**
2. **ALWAYS log every action taken**
3. **ALWAYS update Dashboard after processing**
4. **ALWAYS move processed files to Done/**
5. **ALWAYS check Company_Handbook.md for rules**

## Example Usage

```
User: /process-inbox
Assistant: Processing inbox...
✓ Found 3 items in Needs_Action/
✓ Created 3 action plans
✓ Requested 2 approvals
✓ Executed 1 low-priority action
⏳ 2 items awaiting approval in Pending_Approval/
```

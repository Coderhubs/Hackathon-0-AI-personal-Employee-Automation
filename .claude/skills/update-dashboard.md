# Update Dashboard Skill

Update the AI_Employee_Vault/Dashboard.md with current system status, recent activity, and pending items.

## When to Use

Use this skill when:
- After processing inbox items
- After executing any action
- User asks for "status update"
- Starting/ending a work session

## Step-by-Step Instructions

### 1. Gather Current Status

Count items in each folder:
```bash
ls AI_Employee_Vault/Needs_Action/ | wc -l
ls AI_Employee_Vault/Pending_Approval/ | wc -l
ls AI_Employee_Vault/Approved/ | wc -l
ls AI_Employee_Vault/Done/ | wc -l
```

### 2. Read Current Dashboard

Read `AI_Employee_Vault/Dashboard.md` to see existing content.

### 3. Create Status Update Entry

Add new entry at the TOP of Dashboard.md:

```markdown
## 🤖 Status Update - [Date Time]

**Last Scan:** [ISO timestamp]
**Status:** [Operational/Processing/Idle]

### Current Queue Status
- 📥 Needs Action: [X] items
- ⏳ Pending Approval: [X] items
- ✅ Approved: [X] items
- ✓ Done (24h): [X] items

### Recent Activity
- ✅ [Action 1] - [timestamp]
- ✅ [Action 2] - [timestamp]

**Next Action:** [What needs to be done]

---
```

### 4. Save Dashboard

Write the updated content back to Dashboard.md.

### 5. Confirm Update

Report to user:
```
Dashboard Updated
=================
✓ Status: [current status]
✓ Pending items: [X]
✓ Recent activity: [X] tasks
✓ Next action: [description]
```

## Important Rules

1. **ALWAYS add new entries at the TOP**
2. **ALWAYS include timestamp**
3. **ALWAYS count current queue status**
4. **Keep historical entries** (don't delete)

## Example Usage

```
User: /update-dashboard
Assistant: Updating dashboard...
✓ Scanned all folders
✓ Counted queue items
✓ Added status entry

Current Status:
- Needs Action: 2 items
- Pending Approval: 3 items
- System: Operational
```

# HITL (Human-in-the-Loop) Skill

## Purpose
Enforce human approval for all sensitive actions before execution.

## Core Principle
**NEVER** execute sensitive actions without explicit human approval.

## Trigger
Automatically applies to:
- All LinkedIn posts
- All email responses
- All external communications
- Any file moves to /Done
- Any system configuration changes
- Any data deletions

## Actions
1. Generate draft or prepare action
2. Save to `/Pending_Approval` folder
3. Update Dashboard with pending item
4. **WAIT** for human approval
5. On approval: Execute and move to /Approved
6. On rejection: Log feedback and revise or discard

## Approval Workflow

### Step 1: Create Draft
- Generate high-quality output
- Include all necessary context
- Add metadata (timestamp, source, priority)
- Mark status as "PENDING APPROVAL"

### Step 2: Save to Pending_Approval
- Use descriptive filename
- Include draft type in filename
- Add status tracking information
- Never save directly to /Done

### Step 3: Notify Human
- Update Dashboard with pending count
- Log in autonomous operation log
- Include recommendation (approve/revise/reject)
- Provide quality assessment

### Step 4: Wait for Decision
- Do NOT proceed without approval
- Do NOT assume approval
- Do NOT auto-approve after timeout
- Monitor for approval signal

### Step 5: Execute on Approval
- Move approved item to /Approved folder
- Execute the approved action
- Move source files to /Done
- Update Dashboard
- Log completion

## Approval Types

### Explicit Approval Required
- LinkedIn posts (public visibility)
- Email responses (external communication)
- System configuration changes
- Data deletion or archival
- Budget or resource commitments

### Implicit Approval Allowed
- Internal logging
- Dashboard updates
- Plan creation
- File reading
- Status reporting

## Quality Gates

Before requesting approval:
- ✅ Content quality score ≥ 9.0/10
- ✅ All required fields present
- ✅ Compliance rules followed
- ✅ No errors or warnings
- ✅ Professional tone maintained

## Rejection Handling

If human rejects:
1. Read rejection feedback
2. Identify issues
3. Create revision plan
4. Generate improved version
5. Resubmit for approval
6. Log revision cycle

## Timeout Policy

**IMPORTANT:** No automatic approval on timeout.

If no response after reasonable time:
- Keep item in /Pending_Approval
- Send reminder notification
- Escalate if critical
- **NEVER** auto-approve

## Integration
Works with:
- LinkedIn Skill (requires approval)
- Gmail Skill (requires approval)
- Company Handbook (enforces HITL rule)
- Dashboard (tracks pending items)

## Success Criteria
- 100% compliance with approval requirement
- No unauthorized actions
- Clear approval status tracking
- Proper handling of rejections
- Complete audit trail

## Company Handbook Rule
> "Never move files to /Done unless the necessary steps in the Plan are checked off."

This enforces human verification before completion.

## Examples

### Good HITL Flow
1. Draft created → /Pending_Approval
2. Dashboard updated with pending item
3. Human reviews and approves
4. Action executed
5. Files moved to /Approved and /Done
6. Complete audit trail

### HITL Violation (NEVER DO THIS)
1. Draft created
2. Automatically posted without approval ❌
3. Files moved directly to /Done ❌
4. No human review ❌

## Audit Trail

Every HITL action must log:
- Timestamp of draft creation
- Timestamp of approval request
- Timestamp of human decision
- Decision outcome (approve/reject/revise)
- Executor of approved action
- Final status

## Emergency Override

**ONLY** in true emergencies:
- Critical security issues
- System failures
- Data loss prevention

Even then:
- Log the override
- Notify human immediately
- Document justification
- Seek retroactive approval
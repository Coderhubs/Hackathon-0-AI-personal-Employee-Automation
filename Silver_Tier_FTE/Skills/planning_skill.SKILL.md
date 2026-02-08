# Planning Skill

## Purpose
Create structured execution plans before performing any task.

## Trigger
**MANDATORY:** Before executing ANY task, a plan must be created first.

## Actions
1. Analyze the incoming task or file
2. Break down into sequential steps
3. Identify dependencies and requirements
4. Estimate complexity and priority
5. Create plan file in `/Plans` folder
6. Execute plan steps sequentially
7. Update plan with checkmarks as steps complete

## Output Format
```markdown
# Plan_[TaskName].md

## Objective
[Clear statement of what needs to be accomplished]

## Steps
1. ✅ [Completed step]
2. 🔄 [In progress step]
3. ⏳ [Pending step]
4. ❌ [Failed step - with reason]

## Expected Output
[Description of final deliverable]

## Compliance
[Reference to relevant Company Handbook rules]

## Dependencies
[Any prerequisites or blocking items]

## Risk Assessment
[Potential issues and mitigation strategies]
```

## Planning Principles

### Always Include
- Clear objective statement
- Sequential, actionable steps
- Expected outcomes
- Compliance references
- Success criteria

### Step Granularity
- Each step should be atomic (single action)
- Steps should be verifiable (can mark complete)
- Include decision points
- Note dependencies between steps

### Status Indicators
- ✅ Complete
- 🔄 In progress
- ⏳ Pending/waiting
- ❌ Failed/blocked
- ⚠️ Warning/issue

## Plan Types

### File Processing Plan
1. Read file content
2. Identify file type and trigger conditions
3. Apply relevant skill (LinkedIn, Gmail, etc.)
4. Generate output
5. Save to appropriate folder
6. Update Dashboard
7. Log completion

### Approval Workflow Plan
1. Review item in /Pending_Approval
2. Assess quality and compliance
3. Request human approval
4. On approval: Move to /Approved and /Done
5. On rejection: Log feedback and revise
6. Update Dashboard

### System Maintenance Plan
1. Scan all monitoring folders
2. Process pending items
3. Update dashboards
4. Rotate logs if needed
5. Check system health
6. Report status

## Quality Standards
- Plans created within 15 seconds
- All steps clearly defined
- Compliance rules referenced
- Success criteria specified
- Risk assessment included

## Integration
Works with:
- All other skills (planning is prerequisite)
- Company Handbook (enforces planning rule)
- Dashboard (tracks plan execution)

## Success Criteria
- Plan created before execution
- All steps documented
- Progress tracked with status indicators
- Plan updated as work progresses
- Final status recorded

## Enforcement
**CRITICAL:** The Company Handbook states:
> "Before executing ANY task, you must first create a file in /Plans named Plan_[TaskName].md outlining your steps."

This is a **mandatory** requirement. No task execution without a plan.

## Examples

**Good Plan:**
- Clear objective
- 5-10 specific steps
- Status indicators
- Expected outcome
- Compliance notes

**Insufficient Plan:**
- Vague objective
- Generic steps
- No status tracking
- Missing compliance
- No success criteria
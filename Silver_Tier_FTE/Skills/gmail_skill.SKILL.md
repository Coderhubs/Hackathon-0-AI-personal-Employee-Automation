# Gmail Skill

## Purpose
Draft professional email responses for incoming Gmail messages.

## Trigger
When a file with "GMAIL_" prefix appears in the system.

## Actions
1. Read and parse the email content
2. Extract key information:
   - Subject line
   - Sender
   - Main request or message
   - Any action items or deadlines
3. Determine appropriate response type:
   - Confirmation
   - Information request
   - Meeting scheduling
   - Status update
   - Acknowledgment
4. Draft professional response
5. Save to `/Pending_Approval` as `DRAFT_Response_[Subject].md`
6. **NEVER** send directly - always require human approval

## Output Format
```markdown
## Draft Email Response: [Subject]

**To:** [recipient email]
**Subject:** RE: [original subject]

[Professional greeting]

[Acknowledgment of their message]

[Main response content with clear structure]

[Specific action items or next steps if applicable]

[Professional closing]

[Signature]

---
**Status:** PENDING APPROVAL
**Created:** [timestamp]
**Source:** [source file]
**Response Type:** [type]
**Priority:** [priority level]
```

## Response Guidelines

### Tone
- Professional and courteous
- Clear and concise
- Proactive and helpful
- Appropriate formality based on sender

### Structure
1. **Greeting:** Use appropriate salutation
2. **Acknowledgment:** Reference their message
3. **Response:** Address all points raised
4. **Action Items:** List specific next steps
5. **Closing:** Professional sign-off

### Content Rules
- Confirm attendance/participation explicitly
- List preparation items when relevant
- Ask clarifying questions if needed
- Provide specific dates/times
- Offer additional assistance
- Maintain professional boundaries

## Email Types

### Meeting Invitations
- Confirm attendance
- List preparation items
- Ask about agenda/materials
- Suggest alternatives if conflict

### Information Requests
- Provide requested information
- Offer additional context
- Suggest resources
- Set expectations for follow-up

### Status Updates
- Acknowledge receipt
- Provide current status
- List next steps
- Give timeline estimates

### Action Items
- Confirm understanding
- List specific actions
- Provide completion timeline
- Ask for clarification if needed

## Quality Standards
- Response time: < 4 hours (simulated)
- Completeness: Address all points
- Clarity: No ambiguity
- Professionalism: Appropriate tone
- Accuracy: Verify all details
- Length: Concise but complete

## Integration
Works with:
- gmail_watcher.py (monitors emails)
- Company Handbook HITL rule (requires approval)
- Dashboard logging (tracks all responses)

## Success Criteria
- Draft created within 30 seconds
- Quality score: 9.0/10 or higher
- All points from original email addressed
- Saved to /Pending_Approval (not /Done)
- Human approval required before sending
- Professional tone maintained

## Examples

**Good Response:**
```
Dear [Name],

Thank you for the meeting invitation. I confirm my attendance
at the quarterly review on Tuesday at 2 PM.

I will come prepared with:
- Q1 project updates
- Key metrics and achievements
- Q2 objectives

Please let me know if there are specific topics you'd like
me to focus on.

Best regards,
[Signature]
```

**Avoid:**
- Overly casual language
- Incomplete responses
- Assumptions without confirmation
- Delayed acknowledgment
- Missing action items
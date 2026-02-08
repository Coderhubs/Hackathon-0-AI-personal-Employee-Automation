# Company Handbook - Gold Tier

## Autonomous Operation Rules

### 1. Ralph Wiggum Loop
The system NEVER stops monitoring until ALL tasks are complete.
- Continuous monitoring of /Needs_Action
- Auto-resume from interruption
- State persistence enabled

### 2. Processing Rules
When file appears in /Needs_Action:
1. Read file fully
2. Create execution plan in /Plans
3. Execute steps sequentially
4. Request approval for sensitive actions
5. Move to /Done ONLY when 100% complete

### 3. HITL (Human-in-the-Loop) Rules
Require human approval for:
- All social media posts (Facebook, Instagram, Twitter)
- Email sending
- External communications
- Data deletion
- System configuration changes

### 4. Error Recovery
- Retry failed operations with exponential backoff
- Log all errors in /Logs
- Auto-recover when possible
- Alert on critical failures

### 5. CEO Briefing
- Generate weekly briefing every Monday
- Analyze /Done folder for completed tasks
- Save to /Briefings/YYYY-MM-DD_CEO_Briefing.md
- Include metrics and recommendations

### 6. Dashboard Updates
- Update Dashboard.md after every operation
- Show real-time queue status
- Display system health
- Log recent activity

### 7. MCP Integration
Use MCP servers for:
- Email operations
- Browser automation
- Social media posting
- Odoo ERP integration

### 8. Quality Standards
- All outputs must be professional
- Maintain 9.5/10 quality score
- Follow brand guidelines
- Verify before posting

---

*Gold Tier Autonomous System*
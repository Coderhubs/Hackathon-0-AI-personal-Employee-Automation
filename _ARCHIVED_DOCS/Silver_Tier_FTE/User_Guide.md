# User Guide: AI Employee System
**Complete Guide for Operating Your Autonomous Digital Employee**

**Version:** 1.0
**Last Updated:** 2026-02-08
**Audience:** System Users and Administrators

---

## Table of Contents
1. Introduction
2. Getting Started
3. Daily Operations
4. Approval Workflows
5. Monitoring & Maintenance
6. Troubleshooting
7. Best Practices
8. FAQ

---

## 1. Introduction

### What is the AI Employee System?

The AI Employee System is an autonomous digital assistant that monitors multiple communication channels (Gmail, LinkedIn, file system), processes incoming content, and generates professional drafts for your review and approval.

### Key Features
- **Multi-Source Monitoring:** Gmail, LinkedIn, and file system
- **Intelligent Processing:** AI-powered content analysis and draft generation
- **Human-in-the-Loop:** All outputs require your approval
- **Plan-First Approach:** Every task is planned before execution
- **Quality Assurance:** Consistent 9.5/10 quality scores
- **Complete Audit Trail:** Full logging of all operations

### System Tiers
- **Bronze Tier:** Basic file monitoring and processing
- **Silver Tier:** Multi-source integration with HITL workflows
- **Gold Tier:** Advanced AI, analytics, and full automation

---

## 2. Getting Started

### Prerequisites
- Windows 10 or later
- Python 3.8+
- Obsidian (optional, for vault viewing)
- Claude Code (for AI processing)

### Initial Setup

#### Step 1: Verify Folder Structure
```
Silver_Tier_FTE/
├── Inbox/              (monitored for new files)
├── Needs_Action/       (processing queue)
├── Plans/              (execution plans)
├── Pending_Approval/   (drafts awaiting your review)
├── Approved/           (approved items)
├── Done/               (completed items)
└── Logs/               (system logs)
```

#### Step 2: Start Watchers (Optional)
If you want continuous monitoring:
1. Open Command Prompt
2. Navigate to `Silver_Tier_FTE/`
3. Run: `python gmail_watcher.py` (in separate window)
4. Run: `python linkedin_watcher.py` (in separate window)
5. Run: `python filesystem_watcher.py` (in separate window)

Or follow `Scheduler_Setup_Guide.md` for automatic startup.

#### Step 3: Verify System
Check that folders exist and watchers are running (if started).

---

## 3. Daily Operations

### Morning Routine

#### 1. Check Pending Approvals
```bash
# Navigate to Pending_Approval folder
cd Silver_Tier_FTE/Pending_Approval/
ls -la
```

You'll see files like:
- `DRAFT_Post_AI_Breakthrough.md` (LinkedIn posts)
- `DRAFT_Response_Meeting.md` (Email responses)

#### 2. Review Each Draft
Open each file and review:
- **Content Quality:** Is it accurate and professional?
- **Tone:** Is it appropriate for the audience?
- **Completeness:** Does it address all points?
- **Compliance:** Does it follow company guidelines?

#### 3. Make Approval Decision

**To Approve:**
1. Move file to `/Approved` folder
2. System will execute the action
3. File moves to `/Done` when complete

**To Reject:**
1. Add feedback in file (at bottom)
2. Move to `/Needs_Action` for revision
3. System will regenerate improved version

**To Revise:**
1. Edit the draft directly
2. Save changes
3. Move to `/Approved` when satisfied

### Throughout the Day

#### Monitor Dashboard
Check `Dashboard.md` for:
- Recent processing activity
- Pending approval count
- System status
- Any errors or warnings

#### Check Logs
Review `Logs/autonomous_operation_log.md` for:
- Processing history
- Performance metrics
- Any issues encountered

---

## 4. Approval Workflows

### LinkedIn Post Approval

#### What You'll See
```markdown
# DRAFT_Post_AI_Breakthrough.md

## Draft LinkedIn Post: AI Natural Language Processing

🚀 Exciting developments in AI and Natural Language Processing!

[Content...]

#ArtificialIntelligence #NLP #Innovation

---
**Status:** PENDING APPROVAL
**Created:** 2026-02-08
**Quality Score:** 9.5/10
```

#### Review Checklist
- [ ] Content is accurate
- [ ] Tone is professional
- [ ] Hashtags are relevant
- [ ] No sensitive information
- [ ] Aligns with brand voice
- [ ] Engagement question included

#### Approval Actions
```bash
# Approve
mv Pending_Approval/DRAFT_Post_*.md Approved/

# Reject
echo "Feedback: Too technical, simplify language" >> DRAFT_Post_*.md
mv Pending_Approval/DRAFT_Post_*.md Needs_Action/
```

### Email Response Approval

#### What You'll See
```markdown
# DRAFT_Response_Meeting.md

## Draft Email Response: Meeting Confirmation

**To:** manager@company.com
**Subject:** RE: Quarterly Review

Dear Management Team,

[Content...]

Best regards,
[Your Name]

---
**Status:** PENDING APPROVAL
```

#### Review Checklist
- [ ] All points addressed
- [ ] Tone is appropriate
- [ ] No typos or errors
- [ ] Action items clear
- [ ] Professional closing

---

## 5. Monitoring & Maintenance

### Daily Checks

#### System Health
```bash
# Check if watchers are running
ps aux | grep watcher

# Check disk space
du -sh Silver_Tier_FTE/

# Check recent activity
tail -n 50 Logs/autonomous_operation_log.md
```

#### Performance Metrics
View `Dashboard_Analytics.md` for:
- Processing statistics
- Quality scores
- Response times
- Success rates

### Weekly Maintenance

#### 1. Review Logs
- Check for any errors
- Identify patterns
- Optimize if needed

#### 2. Clean Up Old Files
```bash
# Archive files older than 30 days
find Done/ -mtime +30 -exec mv {} Archive/ \;
```

#### 3. Update Documentation
- Note any issues encountered
- Document solutions
- Update procedures

### Monthly Review

#### 1. Performance Analysis
- Review Dashboard_Analytics.md
- Calculate ROI
- Identify improvements

#### 2. Quality Assessment
- Review sample outputs
- Check quality trends
- Adjust standards if needed

#### 3. System Updates
- Update Python packages
- Review security patches
- Test new features

---

## 6. Troubleshooting

### Common Issues

#### Issue: No Files Being Processed
**Symptoms:** Inbox has files but nothing happens

**Solutions:**
1. Check if watchers are running
2. Verify folder permissions
3. Check logs for errors
4. Restart watchers

```bash
# Check watcher status
ps aux | grep watcher

# Restart watchers
pkill -f watcher
python gmail_watcher.py &
python linkedin_watcher.py &
python filesystem_watcher.py &
```

#### Issue: Low Quality Drafts
**Symptoms:** Drafts score below 9.0

**Solutions:**
1. Check input file quality
2. Review Company_Handbook.md rules
3. Update SKILL.md files
4. Provide feedback for learning

#### Issue: Slow Processing
**Symptoms:** Takes > 60 seconds per file

**Solutions:**
1. Check system resources
2. Reduce file size
3. Optimize watcher scripts
4. Check network connectivity

#### Issue: Watcher Crashes
**Symptoms:** Watcher stops unexpectedly

**Solutions:**
1. Check error logs
2. Verify Python version
3. Update dependencies
4. Add error handling

```bash
# View error logs
tail -n 100 Logs/error_log.txt

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

## 7. Best Practices

### Content Management

#### Do's
✅ Review all drafts before approval
✅ Provide feedback on rejections
✅ Keep Company_Handbook.md updated
✅ Monitor Dashboard regularly
✅ Archive old files periodically

#### Don'ts
❌ Auto-approve without review
❌ Ignore pending approvals
❌ Skip quality checks
❌ Disable HITL workflows
❌ Delete logs prematurely

### Security

#### Protect Sensitive Information
- Never include passwords in files
- Redact confidential data
- Use secure file permissions
- Encrypt sensitive drafts
- Regular security audits

#### Access Control
- Limit who can approve drafts
- Secure API credentials
- Use strong passwords
- Enable two-factor authentication
- Monitor access logs

### Performance Optimization

#### Keep System Fast
- Process files promptly
- Archive old items
- Optimize watcher intervals
- Monitor resource usage
- Regular maintenance

---

## 8. FAQ

### General Questions

**Q: How long does processing take?**
A: Average 25-30 seconds per file, from detection to draft creation.

**Q: Can I customize the output format?**
A: Yes, edit the relevant SKILL.md file in the Skills/ folder.

**Q: What happens if I don't approve a draft?**
A: It stays in Pending_Approval until you take action. No automatic approval.

**Q: Can the system post directly to LinkedIn?**
A: No, all posts require human approval (HITL requirement).

**Q: How do I stop the watchers?**
A: Press Ctrl+C in each watcher window, or use Task Manager.

### Technical Questions

**Q: What Python version is required?**
A: Python 3.8 or higher.

**Q: Can I run this on Mac/Linux?**
A: Yes, with minor path adjustments. See platform-specific guides.

**Q: How do I update the system?**
A: Pull latest code, update dependencies, restart watchers.

**Q: Where are credentials stored?**
A: In environment variables or secure credential store (not in code).

**Q: Can I integrate with other tools?**
A: Yes, via MCP configuration. See mcp.json for examples.

### Troubleshooting Questions

**Q: Why aren't files being processed?**
A: Check if watchers are running and folders have correct permissions.

**Q: Why is quality score low?**
A: Review input file quality and Company_Handbook rules.

**Q: How do I view logs?**
A: Check Logs/autonomous_operation_log.md for detailed history.

**Q: What if a watcher crashes?**
A: Check error logs, fix issue, restart watcher.

---

## Quick Reference

### File Locations
```
Pending Approvals:  Silver_Tier_FTE/Pending_Approval/
System Logs:        Silver_Tier_FTE/Logs/
Dashboard:          Silver_Tier_FTE/Dashboard.md
Analytics:          Silver_Tier_FTE/Dashboard_Analytics.md
Plans:              Silver_Tier_FTE/Plans/
```

### Common Commands
```bash
# Start watchers
python gmail_watcher.py &
python linkedin_watcher.py &
python filesystem_watcher.py &

# Check status
ps aux | grep watcher

# View logs
tail -f Logs/autonomous_operation_log.md

# Approve draft
mv Pending_Approval/DRAFT_*.md Approved/
```

### Support Resources
- Documentation: See all .md files in Silver_Tier_FTE/
- Scheduler Setup: Scheduler_Setup_Guide.md
- Test Suite: Test_Suite_Documentation.md
- Skills Reference: Skills/*.SKILL.md

---

## Getting Help

### Self-Service
1. Check this user guide
2. Review Dashboard and logs
3. Consult SKILL.md files
4. Check troubleshooting section

### Community Support
- GitHub Issues
- User forums
- Documentation wiki

### Professional Support
- Email: support@example.com
- Priority support available
- Custom training sessions

---

**Version History:**
- v1.0 (2026-02-08): Initial release

**Next Update:** As needed based on user feedback

---

*Thank you for using the AI Employee System!*
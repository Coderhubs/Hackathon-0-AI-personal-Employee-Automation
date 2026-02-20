# LinkedIn 24/7 Automation - Quick Reference

## 🚀 One-Time Setup

```bash
# 1. Install dependencies
pip install playwright schedule python-dotenv pillow
playwright install chromium

# 2. Create .env file
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
BUSINESS_NAME=Your Business Name
CEO_NAME=Your Name

# 3. Login to LinkedIn (saves session)
python setup_linkedin_login.py
```

## ▶️ Start Automation

### Manual Approval (Recommended)
```bash
START_LINKEDIN_24_7.bat
```
- Posts saved to `Pending_Approval/`
- You review and move to `Approved/`
- System posts at scheduled time

### Auto-Approve (Advanced)
```bash
START_LINKEDIN_AUTO_APPROVE.bat
```
- Posts generated and published automatically
- No human review
- Use with caution!

## 📅 Default Schedule

| Day | Time | Post Type |
|-----|------|-----------|
| Monday | 9:00 AM | Business Update |
| Wednesday | 12:00 PM | Industry Insight |
| Friday | 5:00 PM | Engagement Post |

Content generated every **Sunday at 8:00 PM** for the week ahead.

## 🛠️ Common Commands

```bash
# Check system status
python check_linkedin_status.py

# Test all components
python test_linkedin_automation.py

# Generate content now
python linkedin_content_generator.py

# Post approved content now
python linkedin_scheduler_complete.py post-now

# Configure schedule
# Edit: AI_Employee_Vault/linkedin_automation_config.json
```

## 📁 Folder Structure

```
AI_Employee_Vault/
├── Pending_Approval/     # Posts awaiting review
├── Approved/             # Posts ready to publish
├── Done/                 # Published posts
├── Logs/                 # System logs
├── Generated_Images/     # AI-generated images
└── linkedin_automation_config.json
```

## ⚙️ Configuration

Edit `AI_Employee_Vault/linkedin_automation_config.json`:

```json
{
  "enabled": true,
  "auto_approve": false,
  "weekly_schedule": {
    "Monday": {"time": "09:00", "type": "business_update"},
    "Wednesday": {"time": "12:00", "type": "industry_insight"},
    "Friday": {"time": "17:00", "type": "engagement"}
  },
  "visibility": "public",
  "generate_images": true,
  "max_posts_per_week": 3
}
```

### Post Types:
- `business_update` - Weekly achievements
- `industry_insight` - Thought leadership
- `engagement` - Questions/polls
- `automation_showcase` - Behind-the-scenes

### Visibility:
- `public` - Anyone on LinkedIn
- `private` - Connections only

## ✅ Manual Approval Workflow

1. **Review Post**
   ```
   Open: Pending_Approval/LINKEDIN_POST_*.md
   ```

2. **Edit if Needed**
   - Modify content between `## Post Content` and `## Posting Instructions`
   - Save file

3. **Approve**
   ```
   Move file to: Approved/
   ```

4. **System Posts Automatically**
   - At scheduled time
   - Moved to `Done/` when complete

## 🔍 Monitoring

### Real-time Status
System prints status every minute:
```
LinkedIn 24/7 Automation - Status
Enabled: True
Auto-Approve: False
Posts This Week: 2/3
Last Content Generation: 2026-02-18T20:00:00
Next Scheduled Post: 2026-02-21T09:00:00
```

### Check Logs
```
AI_Employee_Vault/Logs/linkedin_24x7_YYYYMMDD.log
```

### View Reports
```
AI_Employee_Vault/orchestrator_report.json
```

## 🐛 Troubleshooting

### Posts Not Publishing
```bash
# Re-login to LinkedIn
python setup_linkedin_login.py

# Check approved folder
dir AI_Employee_Vault\Approved

# Check logs
type AI_Employee_Vault\Logs\linkedin_24x7_*.log
```

### Content Not Generating
```bash
# Check configuration
type AI_Employee_Vault\linkedin_automation_config.json

# Test content generation
python linkedin_content_generator.py

# Check system time
echo %date% %time%
```

### Session Expired
```bash
# Re-login
python setup_linkedin_login.py

# Verify session
dir browser_data\linkedin
```

## 🎯 Best Practices

### Content Strategy
- Mix post types (updates, insights, engagement)
- Post during business hours (9 AM - 5 PM)
- Avoid weekends for B2B content
- Respond to comments within 2 hours

### Timing
- **Monday morning:** Business updates
- **Wednesday noon:** Industry insights
- **Friday afternoon:** Engagement posts

### Safety
- Start with manual approval
- Review first week's posts
- Monitor engagement metrics
- Adjust schedule based on analytics

## 📊 Performance Metrics

Track in `orchestrator_report.json`:
- Posts published per week
- Success/failure rates
- Posting times
- Content generation history

## 🔗 Integration

### With Master Orchestrator
```python
# Add to master_orchestrator_24_7.py
from linkedin_24_7_automation import LinkedIn24x7Automation

linkedin = LinkedIn24x7Automation(auto_approve=False)
linkedin.run()
```

### With Other Systems
- Gmail watcher → LinkedIn post ideas
- WhatsApp leads → LinkedIn content
- CEO briefing → LinkedIn updates

## 📚 Full Documentation

- **Complete Guide:** `LINKEDIN_24_7_GUIDE.md`
- **Test Suite:** `test_linkedin_automation.py`
- **Status Checker:** `check_linkedin_status.py`
- **Main Script:** `linkedin_24_7_automation.py`

## 🆘 Support

1. Check status: `python check_linkedin_status.py`
2. Run tests: `python test_linkedin_automation.py`
3. Review logs: `AI_Employee_Vault/Logs/`
4. Check config: `linkedin_automation_config.json`

---

**Status:** Production Ready ✅
**Version:** 1.0
**Last Updated:** 2026-02-20

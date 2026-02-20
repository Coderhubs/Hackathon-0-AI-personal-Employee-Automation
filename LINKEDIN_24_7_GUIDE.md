# LinkedIn 24/7 Automation System

Complete guide for automatic LinkedIn posting on a weekly basis.

## 🚀 Quick Start

### Option 1: Manual Approval (Recommended)
```bash
START_LINKEDIN_24_7.bat
```
- Posts are generated automatically
- You review and approve before publishing
- Safe for business accounts

### Option 2: Fully Automatic (Advanced)
```bash
START_LINKEDIN_AUTO_APPROVE.bat
```
- Posts are generated AND published automatically
- No human review required
- Use with caution!

## 📅 Default Schedule

The system posts **3 times per week**:

| Day | Time | Post Type |
|-----|------|-----------|
| Monday | 9:00 AM | Business Update |
| Wednesday | 12:00 PM | Industry Insight |
| Friday | 5:00 PM | Engagement Post |

Content is generated every **Sunday at 8:00 PM** for the upcoming week.

## ⚙️ Configuration

Edit `AI_Employee_Vault/linkedin_automation_config.json`:

```json
{
  "enabled": true,
  "auto_approve": false,
  "weekly_schedule": {
    "Monday": {
      "time": "09:00",
      "type": "business_update"
    },
    "Wednesday": {
      "time": "12:00",
      "type": "industry_insight"
    },
    "Friday": {
      "time": "17:00",
      "type": "engagement"
    }
  },
  "visibility": "public",
  "generate_images": true,
  "max_posts_per_week": 3
}
```

### Post Types Available:
- `business_update` - Weekly achievements and metrics
- `industry_insight` - Thought leadership content
- `engagement` - Questions and polls
- `automation_showcase` - Behind-the-scenes automation

### Customization:
1. Change posting days (Monday-Sunday)
2. Change posting times (24-hour format: "09:00", "17:30")
3. Change post types
4. Enable/disable image generation
5. Set max posts per week

## 🔄 How It Works

### Weekly Cycle:

```
Sunday 8 PM → Generate content for the week
             ↓
Monday-Friday → Posts published at scheduled times
             ↓
Sunday 11:59 PM → Reset weekly counter
             ↓
Repeat
```

### Manual Approval Workflow:

```
Content Generated → Pending_Approval/
                   ↓
You Review → Move to Approved/
                   ↓
Scheduled Time → Auto-posted to LinkedIn
                   ↓
Completed → Done/
```

### Auto-Approve Workflow:

```
Content Generated → Approved/ (automatic)
                   ↓
Scheduled Time → Auto-posted to LinkedIn
                   ↓
Completed → Done/
```

## 📁 Folder Structure

```
AI_Employee_Vault/
├── Pending_Approval/     # Posts awaiting your review
├── Approved/             # Posts ready to publish
├── Done/                 # Published posts (archive)
├── Logs/                 # System logs
├── Generated_Images/     # AI-generated post images
└── linkedin_automation_config.json  # Configuration
```

## 🛠️ Setup Requirements

### 1. LinkedIn Login Session
```bash
python setup_linkedin_login.py
```
- Login once to save session
- Session persists across restarts

### 2. Environment Variables
Create `.env` file:
```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
BUSINESS_NAME=Your Business Name
CEO_NAME=Your Name
```

### 3. Install Dependencies
```bash
pip install playwright schedule python-dotenv pillow
playwright install chromium
```

## 📊 Monitoring

### Check Status
The system prints status every minute:
```
LinkedIn 24/7 Automation - Status
Enabled: True
Auto-Approve: False
Posts This Week: 2/3
Last Content Generation: 2026-02-18T20:00:00
Next Scheduled Post: 2026-02-21T09:00:00
```

### View Logs
```
AI_Employee_Vault/Logs/linkedin_24x7_YYYYMMDD.log
```

### Check Generated Content
```
AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_*.md
```

## ✅ Manual Approval Process

1. **Review Generated Post**
   - Open `Pending_Approval/LINKEDIN_POST_*.md`
   - Read the content
   - Check character count (LinkedIn limit: 3000)

2. **Edit if Needed**
   - Modify the content between `## Post Content` and `## Posting Instructions`
   - Save the file

3. **Approve**
   - Move file to `Approved/` folder
   - System will post at next scheduled time

4. **Reject**
   - Delete the file
   - System will generate new content next week

## 🔒 Security Best Practices

1. **Use Manual Approval** for business accounts
2. **Review all posts** before publishing
3. **Keep `.env` file secure** (never commit to git)
4. **Monitor logs** regularly
5. **Test with private posts** first

## 🐛 Troubleshooting

### Posts Not Publishing
- Check LinkedIn session: `python setup_linkedin_login.py`
- Verify files in `Approved/` folder
- Check logs for errors

### Content Not Generating
- Verify schedule in config file
- Check system time is correct
- Review logs for errors

### Session Expired
- Re-run: `python setup_linkedin_login.py`
- Login again to refresh session

## 🎯 Best Practices

### Content Strategy:
- Mix post types (updates, insights, engagement)
- Post during business hours (9 AM - 5 PM)
- Avoid weekends for B2B content
- Respond to comments within 2 hours

### Timing:
- Monday morning: Business updates
- Wednesday noon: Industry insights
- Friday afternoon: Engagement posts

### Engagement:
- Ask questions in posts
- Use relevant hashtags
- Tag connections when appropriate
- Share in relevant groups

## 📈 Performance Tracking

The system tracks:
- Posts published per week
- Posting times and days
- Success/failure rates
- Content generation history

View in: `AI_Employee_Vault/orchestrator_report.json`

## 🔄 Integration with Master Orchestrator

To integrate with the main 24/7 system:

1. Add to `master_orchestrator_24_7.py`
2. LinkedIn automation runs alongside Gmail/WhatsApp watchers
3. Unified logging and monitoring
4. Single control panel

## 💡 Tips

1. **Start with manual approval** to understand the system
2. **Review first week's posts** before enabling auto-approve
3. **Customize post templates** in `linkedin_content_generator.py`
4. **Adjust schedule** based on your audience engagement
5. **Monitor analytics** on LinkedIn to optimize timing

## 🆘 Support

- Check logs: `AI_Employee_Vault/Logs/`
- Review config: `linkedin_automation_config.json`
- Test posting: `python linkedin_scheduler_complete.py post-now`
- Generate content: `python linkedin_content_generator.py`

## 📝 Notes

- System runs continuously (24/7)
- Requires active internet connection
- Uses persistent browser session
- Respects LinkedIn rate limits
- Includes retry logic for failures

---

**Status:** Production Ready ✅
**Last Updated:** 2026-02-20
**Version:** 1.0

# 🎯 Quick Reference Card - AI Personal Employee

## 🚀 Start Everything

```bash
START_ORCHESTRATOR_24_7.bat
```

**That's it!** The orchestrator handles everything else.

---

## 📁 Folder Workflow

```
Needs_Action/     → System detects events
      ↓
Pending_Approval/ → YOU review here
      ↓
Approved/         → YOU move approved files here
      ↓
[AUTO EXECUTION]  → Orchestrator executes
      ↓
Done/             → Completed tasks
```

---

## ⏱️ Timing

- **Gmail checks:** Every 2 minutes
- **Approval checks:** Every 10 seconds
- **Execution:** Immediate (< 10 seconds)

---

## 📝 File Naming

| Platform | Filename Pattern |
|----------|-----------------|
| LinkedIn | `LINKEDIN_*.md` |
| Facebook | `FACEBOOK_*.md` |
| Instagram | `INSTAGRAM_*.md` |
| Twitter | `TWITTER_*.md` |
| Gmail | `EMAIL_*.md` or `GMAIL_*.md` |

---

## 🔍 Monitoring

**Status:**
```
AI_Employee_Vault/orchestrator_status.txt
```

**Report:**
```
AI_Employee_Vault/orchestrator_report.json
```

**Logs:**
```
AI_Employee_Vault/Logs/orchestrator_YYYYMMDD.log
```

---

## 🛑 Stop Orchestrator

Press `Ctrl+C` in the terminal window

---

## ⚙️ Configuration

Edit `.env` file:

```bash
# Gmail
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password

# Timing
CHECK_INTERVAL=120              # Gmail (2 min)
APPROVAL_CHECK_INTERVAL=10      # Approval (10 sec)
```

---

## 🎬 Example Workflow

1. **Gmail detects email** → Creates file in `Needs_Action/`
2. **System creates draft** → File in `Pending_Approval/`
3. **YOU review** → Check the file
4. **YOU approve** → Move to `Approved/`
5. **System executes** → Browser opens, action performed
6. **Completion** → File moved to `Done/`

---

## 🆘 Troubleshooting

**Orchestrator won't start:**
```bash
# Check Python
python --version

# Check .env
copy .env.example .env
```

**Gmail not checking:**
```bash
# Use App Password
# Generate at: https://myaccount.google.com/apppasswords
```

**Actions not executing:**
```bash
# Check file naming (must match pattern)
# Check logs for errors
```

---

## 📚 Documentation

- `ORCHESTRATOR_24_7_GUIDE.md` - Complete guide
- `ALL_TIERS_COMPLETE.md` - All tiers
- `FINAL_COMPLETION_SUMMARY.md` - Summary

---

## ✅ Quick Checklist

- [ ] Python 3.13+ installed
- [ ] `.env` file configured
- [ ] Gmail App Password set
- [ ] Orchestrator started
- [ ] Folders created
- [ ] First test action approved

---

## 🎯 Remember

**The orchestrator runs 24/7 and handles everything automatically.**

**Your only job:** Review files in `Pending_Approval/` and move approved ones to `Approved/`

**Everything else is automatic!** 🚀

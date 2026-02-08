# 🚀 PM2 WATCHER COMMANDS - WINDOWS GUIDE

## ✅ FILES NOW READY

All required watcher files have been copied to Platinum_Tier:
- ✅ gmail_watcher.py
- ✅ linkedin_watcher.py
- ✅ filesystem_watcher.py
- ✅ Agents/manager_agent.py
- ✅ api_server.py

---

## 🎯 METHOD 1: START ALL WITH ONE COMMAND (EASIEST)

### Step 1: Navigate to Platinum_Tier
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
```

### Step 2: Start all processes using PM2 config
```bash
pm2 start Docker/pm2.config.js
```

**What happens:**
- PM2 will attempt to start 7 processes
- 5 will start successfully ✅
- 2 will fail (voice-handler, memory-sync) ❌ - This is OK for now!

---

## 🎯 METHOD 2: START WATCHERS INDIVIDUALLY

### Option A: Use the Batch Script (Windows)
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
START_PM2_WATCHERS.bat
```

### Option B: Manual Commands (Copy-Paste Each Line)

**1. Start Manager Agent (Main Loop):**
```bash
pm2 start Agents\manager_agent.py --name "manager-agent" --interpreter python
```

**2. Start Gmail Watcher:**
```bash
pm2 start gmail_watcher.py --name "gmail-watcher" --interpreter python
```

**3. Start LinkedIn Watcher:**
```bash
pm2 start linkedin_watcher.py --name "linkedin-watcher" --interpreter python
```

**4. Start Filesystem Watcher:**
```bash
pm2 start filesystem_watcher.py --name "filesystem-watcher" --interpreter python
```

**5. Start API Server:**
```bash
pm2 start api_server.py --name "api-server" --interpreter python
```

---

## 📊 CHECK STATUS & LOGS

### View All Running Processes
```bash
pm2 status
```

**Expected Output:**
```
┌─────┬──────────────────────┬─────────┬─────────┬──────────┐
│ id  │ name                 │ status  │ restart │ uptime   │
├─────┼──────────────────────┼─────────┼─────────┼──────────┤
│ 0   │ manager-agent        │ online  │ 0       │ 2m       │
│ 1   │ gmail-watcher        │ online  │ 0       │ 2m       │
│ 2   │ linkedin-watcher     │ online  │ 0       │ 2m       │
│ 3   │ filesystem-watcher   │ online  │ 0       │ 2m       │
│ 4   │ api-server           │ online  │ 0       │ 2m       │
└─────┴──────────────────────┴─────────┴─────────┴──────────┘
```

---

## 📝 CHECK LOGS (VERIFY GMAIL/LINKEDIN CONNECTION)

### View All Logs (Real-time)
```bash
pm2 logs
```

### View Specific Watcher Logs

**Gmail Watcher:**
```bash
pm2 logs gmail-watcher
```

**LinkedIn Watcher:**
```bash
pm2 logs linkedin-watcher
```

**Manager Agent:**
```bash
pm2 logs manager-agent
```

### View Log Files Directly

**Gmail Watcher Logs:**
```bash
type Logs\pm2-gmail-out.log
type Logs\pm2-gmail-error.log
```

**LinkedIn Watcher Logs:**
```bash
type Logs\pm2-linkedin-out.log
type Logs\pm2-linkedin-error.log
```

---

## ✅ VERIFY SUCCESSFUL CONNECTION

### What to Look For in Gmail Watcher Logs:
```
✓ Gmail API initialized successfully
✓ Connected to Gmail
✓ Watching for new emails...
✓ Polling interval: 60 seconds
```

### What to Look For in LinkedIn Watcher Logs:
```
✓ LinkedIn API initialized
✓ Connected to LinkedIn
✓ Monitoring for new messages...
✓ Polling interval: 300 seconds
```

### If You See Errors:
```
❌ Authentication failed
❌ API credentials not found
❌ Connection timeout
```

**Solution:** Check your `.env` file or environment variables for:
- `GMAIL_API_KEY` or Gmail OAuth credentials
- `LINKEDIN_API_KEY` or LinkedIn credentials

---

## 🛠️ USEFUL PM2 COMMANDS

### Stop All Processes
```bash
pm2 stop all
```

### Stop Specific Watcher
```bash
pm2 stop gmail-watcher
```

### Restart All Processes
```bash
pm2 restart all
```

### Restart Specific Watcher
```bash
pm2 restart gmail-watcher
```

### Delete All Processes (Clean Slate)
```bash
pm2 delete all
```

### Save PM2 Process List (Auto-restart on reboot)
```bash
pm2 save
pm2 startup
```

### View Detailed Info
```bash
pm2 show gmail-watcher
```

### Monitor in Real-time (Dashboard)
```bash
pm2 monit
```

---

## 🔧 TROUBLESHOOTING

### Problem: "pm2: command not found"
**Solution:** Install PM2 globally
```bash
npm install -g pm2
```

### Problem: "python: command not found"
**Solution:** Use `python3` or full path
```bash
pm2 start gmail_watcher.py --name "gmail-watcher" --interpreter python3
```

Or use full Python path:
```bash
pm2 start gmail_watcher.py --name "gmail-watcher" --interpreter "C:\Python311\python.exe"
```

### Problem: Watcher starts but immediately crashes
**Solution:** Check error logs
```bash
pm2 logs gmail-watcher --err
```

Common issues:
- Missing Python dependencies: `pip install -r requirements.txt`
- Missing environment variables: Check `.env` file
- Port already in use: Change port in config

### Problem: "ENOENT: no such file or directory"
**Solution:** Make sure you're in the Platinum_Tier directory
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
pm2 start gmail_watcher.py --name "gmail-watcher" --interpreter python
```

---

## 📋 QUICK START CHECKLIST

- [ ] Navigate to Platinum_Tier directory
- [ ] Verify watcher files exist: `dir *watcher*.py`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Check environment variables: `type .env.example`
- [ ] Start watchers: `pm2 start Docker/pm2.config.js` OR `START_PM2_WATCHERS.bat`
- [ ] Check status: `pm2 status`
- [ ] View logs: `pm2 logs`
- [ ] Verify Gmail connection: `pm2 logs gmail-watcher`
- [ ] Verify LinkedIn connection: `pm2 logs linkedin-watcher`
- [ ] Save process list: `pm2 save`

---

## 🎯 RECOMMENDED WORKFLOW FOR HACKATHON

### 1. Quick Start (5 minutes)
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
START_PM2_WATCHERS.bat
pm2 status
pm2 logs
```

### 2. Verify Everything Works (2 minutes)
```bash
pm2 logs gmail-watcher --lines 20
pm2 logs linkedin-watcher --lines 20
pm2 logs manager-agent --lines 20
```

### 3. Save Configuration (1 minute)
```bash
pm2 save
pm2 startup
```

### 4. Monitor During Demo (Real-time)
```bash
pm2 monit
```

---

## 🏆 SUCCESS INDICATORS

**All systems operational when you see:**
- ✅ `pm2 status` shows all processes "online"
- ✅ Gmail watcher logs show "Connected to Gmail"
- ✅ LinkedIn watcher logs show "Connected to LinkedIn"
- ✅ Manager agent logs show "Manager Agent starting"
- ✅ No error messages in `pm2 logs`
- ✅ Logs directory contains output files

---

## 📞 NEED HELP?

**Check logs first:**
```bash
pm2 logs --err
```

**View specific error log:**
```bash
type Logs\pm2-gmail-error.log
type Logs\pm2-linkedin-error.log
type Logs\pm2-manager-error.log
```

**Common fixes:**
1. Restart the watcher: `pm2 restart gmail-watcher`
2. Check Python path: `where python`
3. Verify dependencies: `pip list | findstr gmail`
4. Check environment: `echo %GMAIL_API_KEY%`

---

**You're ready to start your AI Employee! 🚀**

Run this now:
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
START_PM2_WATCHERS.bat
```

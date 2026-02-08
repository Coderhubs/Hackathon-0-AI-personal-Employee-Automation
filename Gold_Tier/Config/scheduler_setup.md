# Windows Task Scheduler Setup Guide

## Autonomous System Startup

### Task 1: Start Gold Tier System on Boot

1. Open Task Scheduler (taskschd.msc)
2. Create Basic Task
   - Name: `Gold Tier Autonomous System`
   - Description: `Starts all Gold Tier watchers and autonomous monitor`
3. Trigger: `When the computer starts`
4. Action: `Start a program`
   - Program: `C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Gold_Tier\start_gold_tier.bat`
   - Start in: `C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Gold_Tier`
5. Settings:
   - ✓ Allow task to be run on demand
   - ✓ Run task as soon as possible after a scheduled start is missed
   - ✓ If the task fails, restart every: 1 minute
   - ✓ Attempt to restart up to: 3 times

---

## CEO Briefing Generation

### Task 2: Weekly CEO Briefing (Every Monday)

1. Open Task Scheduler
2. Create Basic Task
   - Name: `Gold Tier CEO Briefing`
   - Description: `Generates weekly CEO briefing every Monday`
3. Trigger: `Weekly`
   - Start: Monday at 9:00 AM
   - Recur every: 1 week
4. Action: `Start a program`
   - Program: `python`
   - Arguments: `ceo_briefing_generator.py`
   - Start in: `C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Gold_Tier`
5. Settings:
   - ✓ Run whether user is logged on or not
   - ✓ Run with highest privileges

---

## Dashboard Update Task

### Task 3: Dashboard Refresh (Every Hour)

1. Open Task Scheduler
2. Create Basic Task
   - Name: `Gold Tier Dashboard Update`
   - Description: `Updates dashboard metrics every hour`
3. Trigger: `Daily`
   - Repeat task every: 1 hour
   - For a duration of: Indefinitely
4. Action: `Start a program`
   - Program: `python`
   - Arguments: `update_dashboard.py`
   - Start in: `C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Gold_Tier`

---

## Verification

After setup, verify tasks:

```cmd
schtasks /query /tn "Gold Tier Autonomous System"
schtasks /query /tn "Gold Tier CEO Briefing"
schtasks /query /tn "Gold Tier Dashboard Update"
```

## Manual Control

Start system manually:
```cmd
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Gold_Tier"
start_gold_tier.bat
```

Stop system manually:
```cmd
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Gold_Tier"
stop_gold_tier.bat
```

---

*Gold Tier Autonomous System - Scheduler Configuration*

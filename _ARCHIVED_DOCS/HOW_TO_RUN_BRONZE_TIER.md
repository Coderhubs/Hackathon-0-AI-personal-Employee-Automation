# How to Run Bronze Tier - Step by Step

## ⚠️ IMPORTANT: Run from Parent Directory

The filesystem watcher MUST be run from the **AI_personal_Employee** directory, NOT from inside AI_Employee_Vault.

---

## ✅ CORRECT METHOD

### Step 1: Navigate to Parent Directory
```cmd
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee"
```

### Step 2: Start the Watcher
```cmd
python AI_Employee_Vault\filesystem_watcher.py
```

You should see:
```
Started watching C:\...\AI_Employee_Vault\Inbox and C:\...\AI_Employee_Vault\Needs_Action
```

### Step 3: Test It (In Another Terminal)
```cmd
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee"
echo Test content > AI_Employee_Vault\Inbox\test.txt
```

### Step 4: Watch the Output
The watcher terminal will show:
```
Copied test.txt to Needs_Action and created metadata file
Processed test.txt and moved files to Done
```

### Step 5: Verify Results
```cmd
dir AI_Employee_Vault\Done
type AI_Employee_Vault\Dashboard.md
```

---

## ❌ WRONG METHOD (This Causes Error)

```cmd
cd AI_Employee_Vault
python filesystem_watcher.py
```

This fails because the script looks for `AI_Employee_Vault/AI_Employee_Vault` (double nested).

---

## 🚀 EASIEST METHOD: Use the Batch File

Just double-click: **RUN_BRONZE_TIER.bat**

Or from command line:
```cmd
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee"
RUN_BRONZE_TIER.bat
```

---

## 📊 Expected Output

```
=========================================
BRONZE TIER - CONTINUOUS EXECUTION
Architecture: Perception to Reasoning to Action
=========================================

[STARTING] Filesystem Watcher...
Monitoring: AI_Employee_Vault\Inbox
Press Ctrl+C to stop

Started watching C:\...\AI_Employee_Vault\Inbox and C:\...\AI_Employee_Vault\Needs_Action

[When you drop a file:]
Copied test.txt to Needs_Action and created metadata file
Processed test.txt and moved files to Done
```

---

## 🎯 Quick Test Commands

**Terminal 1 (Watcher):**
```cmd
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee"
python AI_Employee_Vault\filesystem_watcher.py
```

**Terminal 2 (Testing):**
```cmd
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee"
echo Test 1 > AI_Employee_Vault\Inbox\test1.txt
timeout /t 3
echo Test 2 > AI_Employee_Vault\Inbox\test2.txt
timeout /t 3
echo Test 3 > AI_Employee_Vault\Inbox\test3.txt
```

Watch Terminal 1 process all 3 files automatically!

---

## ✅ Success Indicators

1. ✅ Watcher starts without errors
2. ✅ Files appear in Needs_Action
3. ✅ Metadata files created (*_metadata.md)
4. ✅ Dashboard.md updated
5. ✅ Files moved to Done folder

---

**Remember:** Always run from the parent directory!

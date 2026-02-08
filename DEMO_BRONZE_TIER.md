# Bronze Tier Demo Script - AI Employee Vault

## 🎯 Demo Overview
**Duration:** 3-5 minutes
**Goal:** Show basic autonomous file monitoring and processing

---

## 📋 Pre-Demo Checklist

1. **Clean the folders:**
   ```bash
   cd AI_Employee_Vault
   rm -f Inbox/*.txt
   rm -f Needs_Action/*
   # Keep Done folder for history
   ```

2. **Verify folder structure:**
   ```bash
   ls -la | grep -E "Inbox|Needs_Action|Done"
   ```

3. **Check Dashboard baseline:**
   ```bash
   tail -10 Dashboard.md
   ```

---

## 🎬 Demo Script

### Step 1: Introduction (30 seconds)
**Say:**
> "This is the Bronze Tier - the foundation of our AI Employee system. It demonstrates autonomous file monitoring with a simple workflow: files dropped in Inbox are automatically processed and moved to Done."

**Show:**
```bash
# Show the folder structure
tree AI_Employee_Vault -L 1
# Or use: ls -la AI_Employee_Vault/
```

### Step 2: Start the Watcher (30 seconds)
**Say:**
> "Let me start the filesystem watcher. This Python script monitors the Inbox folder for new files."

**Run:**
```bash
cd /c/Users/Dell/Desktop/New\ folder\ \(3\)/AI_personal_Employee
python AI_Employee_Vault/filesystem_watcher.py
```

**Expected Output:**
```
Started watching .../Inbox and .../Needs_Action
```

### Step 3: Drop Test Files (1 minute)
**Say:**
> "Now I'll drop some test files into the Inbox to demonstrate the automation."

**In a NEW terminal window:**
```bash
cd /c/Users/Dell/Desktop/New\ folder\ \(3\)/AI_personal_Employee

# Test 1: Simple text file
echo "Meeting notes from client call - Q1 2026 strategy discussion" > AI_Employee_Vault/Inbox/meeting_notes.txt

# Wait 2 seconds
sleep 2

# Test 2: Task file
echo "TODO: Review contract proposal, Schedule team meeting, Update project timeline" > AI_Employee_Vault/Inbox/tasks.txt

# Wait 2 seconds
sleep 2

# Test 3: Report file
echo "Sales Report Q1 2026: Revenue increased 25%, New clients: 15, Customer satisfaction: 92%" > AI_Employee_Vault/Inbox/sales_report.txt
```

### Step 4: Watch the Magic (1 minute)
**Say:**
> "Watch the watcher console - you'll see files being processed automatically."

**Expected Console Output:**
```
Copied meeting_notes.txt to Needs_Action and created metadata file
Processed meeting_notes.txt and moved files to Done
Copied tasks.txt to Needs_Action and created metadata file
Processed tasks.txt and moved files to Done
Copied sales_report.txt to Needs_Action and created metadata file
Processed sales_report.txt and moved files to Done
```

### Step 5: Verify Results (1 minute)
**Say:**
> "Let's verify the files were processed. The Inbox should be empty, and all files should be in Done."

**Run:**
```bash
# Check Inbox (should be empty or have old files)
ls -la AI_Employee_Vault/Inbox/

# Check Done folder (should have new files + metadata)
ls -la AI_Employee_Vault/Done/ | tail -10

# Check Dashboard updates
tail -20 AI_Employee_Vault/Dashboard.md
```

**Expected Dashboard Output:**
```markdown
## File Processed: meeting_notes.txt
Type: file_drop
Summary of content:
type: file_drop
filename: meeting_notes.txt
size: 67 bytes
Processed at: 2026-02-08 20:45:00

## File Processed: tasks.txt
Type: file_drop
Summary of content:
type: file_drop
filename: tasks.txt
size: 89 bytes
Processed at: 2026-02-08 20:45:02
```

### Step 6: Show the Files (30 seconds)
**Say:**
> "Each file has a corresponding metadata file that was automatically generated."

**Run:**
```bash
# Show a metadata file
cat AI_Employee_Vault/Done/meeting_notes_metadata.md

# Show the original file
cat AI_Employee_Vault/Done/meeting_notes.txt
```

### Step 7: Stop the Watcher (15 seconds)
**Say:**
> "To stop the watcher, just press Ctrl+C."

**Action:**
- Press `Ctrl+C` in the watcher terminal

**Expected Output:**
```
Stopped watching
```

---

## 🎯 Key Points to Emphasize

1. **Fully Autonomous:** No human intervention needed once started
2. **Reliable:** Retry logic handles file write delays
3. **Organized:** Clear workflow from Inbox → Needs_Action → Done
4. **Auditable:** Dashboard logs every file processed with timestamps
5. **Simple:** Just 138 lines of Python code

---

## 🐛 Troubleshooting

### Issue: Watcher doesn't start
**Solution:**
```bash
pip install watchdog
python --version  # Should be 3.7+
```

### Issue: Files not processing
**Solution:**
```bash
# Check if watcher is running
ps aux | grep filesystem_watcher

# Check folder permissions
ls -la AI_Employee_Vault/
```

### Issue: Race condition error in console
**Note:** This is a known minor issue where on_modified fires after file is moved. Doesn't affect functionality - files still process correctly.

---

## 📊 Success Metrics

✅ Files automatically copied from Inbox to Needs_Action
✅ Metadata files created automatically
✅ Dashboard updated with processing logs
✅ Files moved to Done folder
✅ Console shows processing messages

---

## 🎥 Video Recording Tips

1. **Use split screen:** Watcher console on left, file operations on right
2. **Zoom in:** Make sure text is readable (14pt+ font)
3. **Slow down:** Wait 2-3 seconds between file drops
4. **Highlight:** Use cursor to point to important console messages
5. **Clean up:** Remove old test files before recording

---

## ⏱️ Timing Breakdown

- Introduction: 30s
- Start watcher: 30s
- Drop files: 1m
- Watch processing: 1m
- Verify results: 1m
- Show files: 30s
- Conclusion: 30s
- **Total: 5 minutes**

---

## 🚀 Next Steps

After Bronze Tier demo, transition to Silver Tier:
> "Bronze Tier shows the foundation. Now let's see Silver Tier, which adds Gmail monitoring, LinkedIn integration, and human-in-the-loop approval workflows."

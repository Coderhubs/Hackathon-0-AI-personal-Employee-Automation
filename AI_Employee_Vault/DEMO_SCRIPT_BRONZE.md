# Bronze Tier Demo Script
**Duration: 5-10 minutes**
**Purpose: Demonstrate complete Bronze Tier functionality for hackathon submission**

---

## 🎬 Demo Structure

### Introduction (30 seconds)
"Hi, I'm [Your Name], and this is my Bronze Tier submission for the Personal AI Employee Hackathon. I've built an autonomous AI agent using Claude Code and Obsidian that demonstrates the complete Perception → Reasoning → Action cycle."

---

## Part 1: Architecture Overview (1 minute)

### Show Folder Structure
```bash
cd AI_Employee_Vault
ls -la
```

**Say:** "The system has 8 folders:
- **Inbox** - Where new files arrive
- **Needs_Action** - Processing queue
- **Done** - Completed tasks
- **Plans** - Strategic planning documents
- **Skills** - Agent skill definitions
- Plus bonus folders for future tiers"

### Show Key Files
```bash
cat Dashboard.md | head -20
cat Company_Handbook.md
```

**Say:** "Dashboard.md shows real-time status, and Company_Handbook.md defines the processing rules that Claude follows."

---

## Part 2: Agent Skills (1 minute)

### Show Skills Directory
```bash
ls -la Skills/
cat Skills/process_inbox.SKILL.md
```

**Say:** "I've implemented 3 Agent Skills as required:
1. **process_inbox** - Detects and processes new files
2. **summarize_content** - Analyzes file contents
3. **update_dashboard** - Updates the Dashboard with results

These skills make the AI functionality reusable and documented."

---

## Part 3: Filesystem Watcher (1 minute)

### Show Watcher Code
```bash
cat filesystem_watcher.py | head -50
```

**Say:** "The filesystem watcher is 138 lines of Python code. It monitors the Inbox folder for new files, copies them to Needs_Action, and creates metadata files automatically. It uses the watchdog library for real-time file system monitoring."

---

## Part 4: Live Workflow Demonstration (3-4 minutes)

### Step 1: Start Watcher (Optional)
```bash
# If demonstrating automated mode:
python filesystem_watcher.py &
```

**Say:** "I'm starting the filesystem watcher in the background. It will now monitor the Inbox folder."

### Step 2: Create Test File
```bash
cat > Inbox/demo_submission.txt << 'EOF'
From: Hackathon Judges
Date: 2026-02-08
Subject: Bronze Tier Evaluation

Please provide:
1. System architecture overview
2. Demonstration of workflow
3. Evidence of all requirements met

This is for final Bronze Tier evaluation.
EOF
```

**Say:** "I'm creating a test file that simulates a request from the hackathon judges. This file is now in the Inbox folder."

### Step 3: Show File Detection
```bash
# Wait 2 seconds for watcher to process
sleep 2
ls -la Needs_Action/
```

**Say:** "The watcher has detected the file and copied it to Needs_Action. You can see both the original file and the metadata file it created."

### Step 4: Claude Code Processing
```bash
# Open Claude Code or show it running
claude "Read the file in Needs_Action/demo_submission.txt and process it according to Company Handbook rules"
```

**Say:** "Now I'm invoking Claude Code to process the file. Claude will:
1. Read the file content
2. Analyze what's being requested
3. Create a strategic plan
4. Generate comprehensive metadata
5. Update the Dashboard
6. Move files to Done"

### Step 5: Show Results
```bash
# Show the plan created
cat Plans/Plan_demo_submission.md

# Show Dashboard update
tail -30 Dashboard.md

# Show files moved to Done
ls -la Done/ | grep demo_submission
```

**Say:** "Claude has completed the workflow. You can see:
- A strategic plan was created in the Plans folder
- The Dashboard was updated with processing details
- Both files were moved to the Done folder
- Complete audit trail maintained"

---

## Part 5: Verification of Requirements (1-2 minutes)

### Show Checklist
```bash
cat BRONZE_TIER_README.md | grep -A 10 "Requirements Met"
```

**Say:** "Let me verify all Bronze Tier requirements:

✅ Obsidian vault with Dashboard.md - CHECK
✅ Company_Handbook.md - CHECK
✅ One working Watcher script - CHECK (138 lines)
✅ Claude Code read/write to vault - CHECK (demonstrated)
✅ Basic folder structure - CHECK (Inbox, Needs_Action, Done)
✅ Agent Skills implementation - CHECK (3 SKILL.md files)

All 6 requirements are met with 100% completion."

---

## Part 6: Security & Privacy (30 seconds)

**Say:** "Security highlights:
- Local-first architecture - all data stays on my machine
- No credentials stored (Bronze Tier uses filesystem only)
- No external API calls except Claude Code
- Complete privacy and control"

---

## Part 7: What's Next (30 seconds)

**Say:** "This Bronze Tier implementation provides the foundation. Next steps would be:
- Silver Tier: Add Gmail integration and MCP servers
- Gold Tier: Add Odoo accounting and social media integration
- Platinum Tier: Deploy to cloud for 24/7 operation

But for now, Bronze Tier is complete and ready for submission."

---

## Closing (30 seconds)

**Say:** "Thank you for watching this demo. This Bronze Tier AI Employee demonstrates:
- Complete Perception → Reasoning → Action cycle
- Autonomous file processing
- Strategic planning capabilities
- Full audit trail and documentation

All code and documentation are available in the GitHub repository. I'm excited to continue building this system in the next tiers!"

---

## 🎥 Recording Tips

### Before Recording:
1. Clean up test files: `rm -rf Inbox/* Needs_Action/* Done/*`
2. Reset Dashboard to clean state
3. Test the workflow once to ensure everything works
4. Close unnecessary applications
5. Set screen resolution to 1920x1080 for clarity

### During Recording:
- Speak clearly and at moderate pace
- Show terminal commands clearly
- Pause briefly after each command to show results
- Use `clear` command between sections for clarity
- Zoom in on important text if needed

### Screen Recording Tools:
- **Windows:** OBS Studio (free), ShareX, or Windows Game Bar
- **Mac:** QuickTime Player, ScreenFlow, or OBS Studio
- **Linux:** SimpleScreenRecorder, OBS Studio, or Kazam

### Video Format:
- Resolution: 1920x1080 (1080p)
- Format: MP4 (H.264 codec)
- Frame rate: 30 fps
- Audio: Clear microphone, no background noise
- Length: 5-10 minutes (aim for 7-8 minutes)

---

## 📤 Upload Locations

After recording, upload to:
- **YouTube** (unlisted or public)
- **Vimeo**
- **Google Drive** (with public link)
- **Loom**

Include the video link in your hackathon submission form.

---

## ✅ Pre-Recording Checklist

- [ ] All test files cleaned up
- [ ] Dashboard.md reset to clean state
- [ ] Watcher script tested and working
- [ ] Claude Code verified and accessible
- [ ] Screen recording software tested
- [ ] Microphone tested (clear audio)
- [ ] Demo script reviewed and practiced
- [ ] GitHub repository updated with latest code
- [ ] README.md finalized
- [ ] Backup of vault created (just in case)

---

**Good luck with your demo recording! 🎬**

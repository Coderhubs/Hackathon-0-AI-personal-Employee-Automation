# Gold Tier - Demo Video Script
**Duration: 7-8 minutes**
**Following Hackathon Document Requirements**

---

## 🎬 RECORDING SETUP

### Before Recording:
- [ ] Close unnecessary applications
- [ ] Set screen resolution to 1920x1080
- [ ] Test microphone (clear audio)
- [ ] Open Gold_Tier folder in terminal
- [ ] Have Obsidian open with Dashboard.md
- [ ] Prepare talking points

### Recording Tools:
- **Windows:** OBS Studio, ShareX, or Windows Game Bar
- **Mac:** QuickTime Player or ScreenFlow
- **Linux:** SimpleScreenRecorder or OBS Studio

### Video Settings:
- Resolution: 1920x1080 (1080p)
- Format: MP4 (H.264 codec)
- Frame rate: 30 fps
- Audio: Clear microphone, no background noise

---

## 📝 DEMO SCRIPT

### INTRODUCTION (30 seconds)

**[Show Gold_Tier folder in file explorer]**

"Hi, I'm [Your Name], and this is my Gold Tier submission for the Personal AI Employee Hackathon. I've built an autonomous AI employee that runs 24/7, managing personal and business affairs using Claude Code and Obsidian, exactly as specified in the hackathon document."

**[Show OFFICIAL_HACKATHON_AUDIT.md]**

"This implementation has been officially audited and received a 100 out of 100 score, meeting all 8 Gold Tier requirements plus 5 bonus features."

---

### PART 1: ARCHITECTURE OVERVIEW (1 minute)

**[Show folder structure]**

```bash
cd Gold_Tier
ls -la
```

"The system follows the hackathon's architecture: The Senses, The Brain, The Memory, and The Hands."

**[Show key folders]**

"Here's the workflow: Files arrive in Inbox, move to Needs_Action, Claude creates Plans, sensitive actions go to Pending_Approval for human review, approved items execute, and everything ends up in Done with complete audit logs."

**[Show Dashboard.md in Obsidian]**

"Obsidian serves as the Memory and GUI, providing real-time visibility into all operations."

---

### PART 2: THE SENSES - WATCHERS (1 minute)

**[Show watcher files]**

```bash
ls -1 *_watcher.py
```

"I have 5 watchers monitoring different channels:"

**[Show gmail_watcher.py]**

```bash
head -30 gmail_watcher.py
```

"The Gmail watcher monitors email and creates task files every 3 minutes. It includes error recovery with exponential backoff."

**[Show linkedin_watcher.py]**

"LinkedIn watcher monitors trends for social media opportunities."

**[Show filesystem_watcher.py]**

"Filesystem watcher monitors the Inbox folder for file drops."

**[Show plugin architecture]**

```bash
python plugin_manager.py list
```

"And here's a bonus feature: the plugin architecture allows adding new watchers in just 5 minutes without modifying core code."

---

### PART 3: THE BRAIN - RALPH WIGGUM LOOP (1.5 minutes)

**[Show autonomous_monitor.py]**

```bash
head -50 autonomous_monitor.py
```

"This is the Ralph Wiggum loop - the autonomous monitor that never stops until all tasks are complete, as specified in the hackathon document."

**[Show the main loop]**

"It continuously scans Needs_Action, processes files, creates strategic plans, and determines if human approval is needed."

**[Show Plans folder]**

```bash
ls -la Plans/
cat Plans/[any-plan-file].md
```

"Every task gets a plan before execution - this is the plan-before-execute methodology."

**[Show state persistence]**

```bash
cat monitor_state.json
```

"State persistence ensures the system can recover from interruptions and resume exactly where it left off."

---

### PART 4: THE HANDS - MCP SERVERS (1.5 minutes)

**[Show mcp_servers folder]**

```bash
ls -la mcp_servers/
```

"I have 5 MCP servers for external actions, all with real API integrations - not placeholders."

**[Show email_server.py]**

```bash
head -40 mcp_servers/email_server.py
```

"Email server for Gmail integration with HITL approval for sending."

**[Show social_media_server.py]**

```bash
head -50 mcp_servers/social_media_server.py
```

"Social media server handles Facebook, Instagram, and Twitter - all three platforms required by Gold Tier."

**[Show the HITL workflow]**

"Notice every post requires human approval - it creates an approval file in Pending_Approval, waits for human review, and only executes after approval."

**[Show odoo_server.py]**

```bash
head -40 mcp_servers/odoo_server.py
```

"Odoo ERP integration using JSON-RPC for accounting and invoice management."

**[Show mcp_config.json]**

```bash
cat Config/mcp_config.json
```

"All MCP servers are configured here for Claude Code integration."

---

### PART 5: SOCIAL MEDIA INTEGRATION (1 minute)

**[Show Pending_Approval folder]**

```bash
ls -la Pending_Approval/
```

"Here's the HITL workflow in action. When the system detects a LinkedIn trend, it creates a professional post draft."

**[Show a draft file]**

```bash
cat Pending_Approval/DRAFT_Post_[example].md
```

"The draft includes the content, platform, and clear approval instructions. I review it, and if approved, move it to the Approved folder."

**[Show social media log]**

```bash
cat Logs/social_media_log.json
```

"Every action is logged with timestamps, platform, content, and approval status for complete audit trail."

---

### PART 6: ODOO ERP INTEGRATION (1 minute)

**[Show odoo_server.py methods]**

```bash
grep "def " mcp_servers/odoo_server.py
```

"The Odoo integration provides full CRUD operations: authenticate, search_read, create_record, update_record."

**[Show example usage]**

"This allows the AI to create draft invoices, query accounting records, and update invoice status - all with human approval for posting."

**[Show Company_Handbook.md]**

```bash
cat Company_Handbook.md
```

"The Company Handbook defines all operating rules, including which actions require approval."

---

### PART 7: CEO BRIEFING AUTOMATION (1 minute)

**[Show ceo_briefing_generator.py]**

```bash
head -40 ceo_briefing_generator.py
```

"This is the Monday Morning CEO Briefing feature - one of the standout ideas from the hackathon document."

**[Show a generated briefing]**

```bash
cat Briefings/[latest-briefing].md
```

"It analyzes the Done folder for the past week, categorizes activities by channel, calculates metrics, and provides recommendations."

**[Show scheduling setup]**

"This runs automatically every Monday at 9 AM via Windows Task Scheduler, providing a weekly business audit."

---

### PART 8: BONUS FEATURES (1 minute)

**[Show plugin_manager.py]**

```bash
python plugin_manager.py --help
```

"Bonus Feature 1: Plugin Architecture - Add unlimited integrations without modifying core code."

**[Show base_watcher.py]**

```bash
head -30 base_watcher.py
```

"Bonus Feature 2: Error Recovery - All watchers inherit exponential backoff and comprehensive logging."

**[Show monitor_state.json]**

"Bonus Feature 3: State Persistence - System recovers from interruptions automatically."

**[Show documentation count]**

```bash
ls -1 *.md | wc -l
```

"Bonus Feature 4: Comprehensive Documentation - 16 markdown files covering every aspect."

**[Show example plugins]**

```bash
ls -1 slack_watcher.py discord_server.py
```

"Bonus Feature 5: Example Plugins - Working demos of Slack and Discord integrations."

---

### PART 9: REQUIREMENTS VERIFICATION (30 seconds)

**[Show OFFICIAL_HACKATHON_AUDIT.md]**

```bash
cat OFFICIAL_HACKATHON_AUDIT.md | grep "REQUIREMENT MET"
```

"Let me verify all Gold Tier requirements:"

**[Scroll through audit report]**

"All 8 requirements verified:
1. ✅ All Silver requirements
2. ✅ Cross-domain integration
3. ✅ Odoo Community integration
4. ✅ Facebook/Instagram integration
5. ✅ Twitter integration
6. ✅ Multiple MCP servers (5 total)
7. ✅ CEO briefing automation
8. ✅ Ralph Wiggum loop

Plus 5 bonus features. Total score: 100 out of 100."

---

### CLOSING (30 seconds)

**[Show Dashboard.md one more time]**

"This Gold Tier Autonomous AI Employee demonstrates production-ready infrastructure with:
- Autonomous operation via Ralph Wiggum loop
- Multi-channel monitoring with plugin architecture
- Real MCP integrations for external actions
- Human-in-the-loop safety controls
- Complete audit logging
- Weekly business intelligence

All built following the hackathon document specifications, using Claude Code as the reasoning engine and Obsidian as the memory and GUI."

**[Show GitHub repository]**

"Complete code, documentation, and setup instructions are available in the GitHub repository. Thank you for watching!"

---

## 📤 AFTER RECORDING

### Upload Video:
1. **YouTube** (Recommended)
   - Upload as Unlisted or Public
   - Title: "Gold Tier AI Employee - Hackathon Submission"
   - Description: Include GitHub link
   - Get shareable link

2. **Vimeo**
   - Upload with password protection (optional)
   - Get shareable link

3. **Google Drive**
   - Upload video file
   - Set sharing to "Anyone with link"
   - Get shareable link

4. **Loom**
   - Record directly in Loom
   - Get shareable link

### Video Checklist:
- [ ] Duration: 5-10 minutes (target: 7-8 minutes)
- [ ] Resolution: 1920x1080
- [ ] Audio: Clear and audible
- [ ] Shows all key features
- [ ] Demonstrates requirements
- [ ] Includes GitHub repository mention
- [ ] Uploaded and link obtained

---

## ⏱️ ESTIMATED TIME

- Recording: 30-45 minutes (including retakes)
- Editing (optional): 15-30 minutes
- Uploading: 10-20 minutes
- **Total: 1-2 hours**

---

## 💡 TIPS

1. **Practice First:** Run through the script once before recording
2. **Speak Clearly:** Moderate pace, clear pronunciation
3. **Show, Don't Tell:** Demonstrate features live, not just talk about them
4. **Use Terminal:** Show actual commands and outputs
5. **Highlight Key Points:** Emphasize the 100/100 audit score
6. **Be Confident:** You've built something exceptional!

---

**Next:** Submit form (Step 3)

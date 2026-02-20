# DEMO VIDEO SCRIPT - AI Personal Employee
## Silver Tier Submission (8-10 minutes)

**Target Duration:** 8-10 minutes
**Recording Tool:** OBS Studio, Loom, or Windows Game Bar
**Resolution:** 1080p minimum

---

## SCENE 1: Introduction (1 minute)

**[Screen: Desktop with project folder open]**

**Script:**
"Hi, I'm [Your Name], and this is my Personal AI Employee submission for the Panaversity Hackathon.

I've built a Silver Tier autonomous AI employee that monitors Gmail, LinkedIn, and WhatsApp 24/7, generates draft responses, and executes approved actions through a human-in-the-loop workflow.

The system uses Claude Code as the reasoning engine, Obsidian as the knowledge base, and MCP servers for external actions. Let me show you how it works."

---

## SCENE 2: Architecture Overview (1.5 minutes)

**[Screen: Open HACKATHON_COMPLIANCE_REPORT.md or architecture diagram]**

**Script:**
"The architecture follows the Perception → Reasoning → Action pattern from the hackathon requirements.

**Perception Layer:** Python watchers monitor Gmail via IMAP, LinkedIn via Playwright, and WhatsApp via browser automation. When they detect keywords like 'agentic AI', they save files to the Needs_Action folder.

**Reasoning Layer:** Claude Code processes these files, analyzes context from the Company Handbook, and generates appropriate responses.

**Action Layer:** After human approval, MCP servers execute actions - sending emails via Gmail SMTP, posting to LinkedIn, or sending WhatsApp messages.

Everything is logged for audit trails, and the Dashboard provides real-time status."

**[Show folder structure: AI_Employee_Vault with subfolders]**

---

## SCENE 3: Live Demonstration - Email Workflow (3 minutes)

**[Screen: Terminal windows]**

**Script:**
"Let me demonstrate the complete workflow. I'll start the system."

**[Action: Run START_FULLY_AUTOMATED.bat]**

"This starts five components:
1. Gmail watcher (IMAP - fully automated)
2. LinkedIn automation
3. WhatsApp automation
4. Integration coordinator
5. Approval handler"

**[Show 5 terminal windows opening]**

**[Action: Send yourself a test email with 'agentic AI' keyword]**

**Script:**
"I'm sending myself a test email with the keyword 'agentic AI' to trigger the system."

**[Wait 30 seconds, show Gmail watcher detecting it]**

**Script:**
"The Gmail watcher detected the email and saved it to Needs_Action folder. Let me show you."

**[Action: Open AI_Employee_Vault/Needs_Action/ folder]**

**[Show the EMAIL_*.md file created]**

**Script:**
"Here's the detected email with metadata - sender, subject, timestamp, and content."

**[Action: Wait for integration coordinator to process]**

**[Open AI_Employee_Vault/Pending_Approval/ folder]**

**Script:**
"The integration coordinator processed this and generated a draft reply in Pending_Approval. Let me review it."

**[Action: Open the draft file in Obsidian or text editor]**

**Script:**
"The AI analyzed the email context and generated a professional response. I can edit this if needed. Now I'll approve it by moving it to the Approved folder."

**[Action: Move file from Pending_Approval to Approved]**

**Script:**
"Within 10 seconds, the approval handler will detect this and execute the action."

**[Show approval handler terminal - watch for execution log]**

**Script:**
"There! The email was sent via the MCP email server. Let me verify."

**[Action: Check your email inbox for the reply]**

**Script:**
"Perfect! The reply was sent automatically. The system also logged this to the Done folder."

**[Show AI_Employee_Vault/Done/ folder with completed task]**

---

## SCENE 4: LinkedIn Content Generation (2 minutes)

**[Screen: Terminal and folders]**

**Script:**
"The system also generates LinkedIn content automatically. Let me show you."

**[Action: Check Pending_Approval folder for LinkedIn posts]**

**Script:**
"The LinkedIn content generator creates professional posts about business updates, industry insights, and engagement topics. Here's one it generated."

**[Action: Open a LINKEDIN_POST_*.md file]**

**Script:**
"This post includes:
- Professional content about AI automation
- Relevant hashtags
- Proper formatting
- Character count

I can review, edit, and approve it. Once approved, the LinkedIn automation will post it to my profile using persistent browser sessions - no manual login required."

**[Action: Show linkedin_automation.py or explain the process]**

---

## SCENE 5: Dashboard & Monitoring (1 minute)

**[Screen: Open AI_Employee_Vault/Dashboard.md in Obsidian]**

**Script:**
"The Dashboard provides real-time status of the system. It shows:
- Recent activity
- Pending approvals
- System status
- Completed tasks

This is updated automatically after each action, giving me a CEO-level view of what my AI employee is doing."

**[Scroll through Dashboard showing various entries]**

---

## SCENE 6: Agent Skills Implementation (1 minute)

**[Screen: Open AI_Employee_Vault/Skills/ folder]**

**Script:**
"As required by the hackathon, all AI functionality is implemented as Agent Skills. I have five skills:

1. process_inbox - Handles incoming files
2. summarize_content - Analyzes and summarizes
3. create_approval_request - Generates approval files
4. update_dashboard - Maintains the Dashboard
5. monitor_watchers - Health checks

These skills make the AI employee modular and maintainable."

**[Show one SKILL.md file briefly]**

---

## SCENE 7: Security & HITL (1 minute)

**[Screen: Show folder structure and Company_Handbook.md]**

**Script:**
"Security is critical. The system implements:

**Human-in-the-Loop:** All sensitive actions require approval. The AI never sends emails, posts to social media, or takes actions without human review.

**Audit Logging:** Every action is logged with timestamps, actors, and results.

**Credential Management:** All credentials are in .env files, never committed to Git.

**Company Handbook:** Contains rules for the AI - response guidelines, tone, approval thresholds, and security policies."

**[Show Company_Handbook.md briefly]**

---

## SCENE 8: Conclusion & Results (30 seconds)

**[Screen: Back to desktop or summary slide]**

**Script:**
"In summary, I've built a Silver Tier AI Personal Employee that:
- Monitors Gmail, LinkedIn, and WhatsApp 24/7
- Generates contextual draft responses
- Implements human-in-the-loop approval
- Executes actions via MCP servers
- Maintains comprehensive audit logs
- Uses Agent Skills for all AI functionality

The system saves 1-2 hours daily on email management and 2-3 hours weekly on social media, while maintaining 100% approval compliance.

Thank you for watching. The code is available on GitHub, and I'm excited to continue developing this into a Gold Tier autonomous employee.

Questions? Feel free to reach out!"

**[End screen with your contact info and GitHub link]**

---

## RECORDING TIPS

### Before Recording
1. ✅ Close unnecessary applications
2. ✅ Clear browser history/tabs
3. ✅ Prepare test email ready to send
4. ✅ Have all folders open in separate windows
5. ✅ Test audio levels
6. ✅ Practice the demo 2-3 times

### During Recording
1. Speak clearly and at moderate pace
2. Pause 2-3 seconds between scenes
3. Show, don't just tell - let viewers see the system working
4. If you make a mistake, pause and restart that section
5. Keep cursor movements smooth and deliberate

### After Recording
1. Edit out long pauses (waiting for system to process)
2. Add text overlays for key points
3. Add background music (optional, keep it subtle)
4. Export as MP4, 1080p, 30fps
5. Upload to YouTube (unlisted) or include in submission

### Video Editing (Optional)
- Use DaVinci Resolve (free) or Camtasia
- Add title screen with your name and project title
- Add section titles between scenes
- Speed up slow parts (2x speed) with note "Sped up for demo"
- Add end screen with GitHub link

---

## ALTERNATIVE: QUICK DEMO (5 minutes)

If time is limited, focus on:
1. Introduction (30 sec)
2. Architecture overview (1 min)
3. Live email workflow (2.5 min)
4. Dashboard & Skills (1 min)

Skip LinkedIn and detailed security sections.

---

## SUBMISSION CHECKLIST

After creating video:
- [ ] Upload to YouTube (unlisted or public)
- [ ] Add YouTube link to README.md
- [ ] Update README with "Silver Tier Submission" declaration
- [ ] Verify .env not committed to Git
- [ ] Test clone and setup on fresh machine (if possible)
- [ ] Submit form: https://forms.gle/JR9T1SJq5rmQyGkGA

---

**Good luck with your demo! You've built an impressive system.**

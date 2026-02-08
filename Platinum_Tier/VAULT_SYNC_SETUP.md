# Platinum Tier - Vault Synchronization Setup
**Git-Based Sync for Cloud + Local Architecture**

---

## Overview

This guide sets up Git-based vault synchronization between Cloud and Local agents, enabling work-zone specialization while maintaining security.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLOUD AGENT (VM)                      │
│  - Email triage & draft replies                          │
│  - Social post drafts                                    │
│  - Writes to: /Pending_Approval/<domain>/               │
│  - Writes to: /Updates/ (signals for Local)             │
└────────────────────────┬────────────────────────────────┘
                         │
                    GIT SYNC (every 30s)
                         │
┌────────────────────────┴────────────────────────────────┐
│                    LOCAL AGENT (Desktop)                 │
│  - Approvals (reviews /Pending_Approval/)               │
│  - WhatsApp session                                      │
│  - Payments/banking                                      │
│  - Final send/post actions via MCP                      │
│  - Merges /Updates/ into Dashboard.md                   │
└─────────────────────────────────────────────────────────┘
```

---

## Security Rules

### What Syncs ✅
- Markdown files (*.md)
- Task files (*.txt)
- Plans (/Plans/)
- Pending approvals (/Pending_Approval/)
- Updates (/Updates/)
- Done items (/Done/)

### What NEVER Syncs ❌
- Environment variables (.env)
- API tokens
- WhatsApp sessions
- Banking credentials
- Payment tokens
- Private keys
- Secrets of any kind

---

## Setup Instructions

### Step 1: Initialize Git Repository

```bash
cd Platinum_Tier
git init
git add .
git commit -m "Initial Platinum Tier vault"
```

### Step 2: Create .gitignore (Security Critical)

```bash
# Copy the secure .gitignore
cp .gitignore.platinum .gitignore
```

**Contents of .gitignore:**
```
# SECURITY: Never sync secrets
.env
.env.local
.env.production
*.key
*.pem
credentials.json
tokens.json

# WhatsApp sessions (Local only)
whatsapp_session/
.wwebjs_auth/
.wwebjs_cache/

# Banking credentials (Local only)
banking_creds/
payment_tokens/

# API keys (Local only)
api_keys/
secrets/

# Python
__pycache__/
*.pyc
.Python
venv/
env/

# Logs (too large to sync)
Logs/*.log
*.log

# Temporary files
*.tmp
*.temp
.DS_Store
Thumbs.db

# Node modules
node_modules/

# Database files
*.db
*.sqlite
*.sqlite3

# Large files
*.mp4
*.avi
*.mov
*.zip
*.tar.gz
```

### Step 3: Create Remote Repository

**Option A: GitHub (Recommended)**
```bash
# Create private repo on GitHub
# Then:
git remote add origin https://github.com/yourusername/platinum-vault.git
git branch -M main
git push -u origin main
```

**Option B: GitLab**
```bash
git remote add origin https://gitlab.com/yourusername/platinum-vault.git
git branch -M main
git push -u origin main
```

### Step 4: Set Up Auto-Sync Scripts

**For Cloud Agent (cloud_sync.sh):**
```bash
#!/bin/bash
# Cloud Agent - Auto-sync script
# Runs every 30 seconds

while true; do
    cd /path/to/Platinum_Tier

    # Pull changes from Local
    git pull origin main --no-edit

    # Add new files (only allowed types)
    git add Pending_Approval/
    git add Updates/
    git add Plans/
    git add Needs_Action/

    # Commit if changes
    if ! git diff-index --quiet HEAD --; then
        git commit -m "Cloud: Auto-sync $(date '+%Y-%m-%d %H:%M:%S')"
        git push origin main
    fi

    sleep 30
done
```

**For Local Agent (local_sync.sh):**
```bash
#!/bin/bash
# Local Agent - Auto-sync script
# Runs every 30 seconds

while true; do
    cd /path/to/Platinum_Tier

    # Pull changes from Cloud
    git pull origin main --no-edit

    # Add new files (only allowed types)
    git add Approved/
    git add Done/
    git add Dashboard.md

    # Commit if changes
    if ! git diff-index --quiet HEAD --; then
        git commit -m "Local: Auto-sync $(date '+%Y-%m-%d %H:%M:%S')"
        git push origin main
    fi

    sleep 30
done
```

---

## Work-Zone Specialization

### Cloud Agent Responsibilities
1. **Email Triage**
   - Monitors Gmail
   - Creates draft replies
   - Saves to: `/Pending_Approval/email/DRAFT_*.md`
   - NEVER sends emails directly

2. **Social Media Drafts**
   - Monitors LinkedIn trends
   - Creates post drafts
   - Saves to: `/Pending_Approval/social/DRAFT_*.md`
   - NEVER posts directly

3. **Signals to Local**
   - Writes updates to: `/Updates/SIGNAL_*.md`
   - Local merges into Dashboard.md

### Local Agent Responsibilities
1. **Approvals**
   - Reviews `/Pending_Approval/`
   - Moves approved items to `/Approved/`
   - Rejects go to `/Rejected/`

2. **Sensitive Actions**
   - WhatsApp messaging (session stays local)
   - Banking operations (credentials stay local)
   - Payment processing (tokens stay local)
   - Final send/post via MCP

3. **Dashboard Management**
   - Single writer for Dashboard.md
   - Merges Cloud signals from `/Updates/`

---

## Claim-by-Move Rule

### Preventing Double-Work

**Rule:** First agent to move a file from `/Needs_Action/` to `/In_Progress/<agent>/` owns it.

**Implementation:**

```python
# In agent code
def claim_task(task_file):
    source = f"Needs_Action/{task_file}"
    destination = f"In_Progress/{agent_name}/{task_file}"

    try:
        # Atomic move operation
        os.rename(source, destination)
        return True  # Successfully claimed
    except FileNotFoundError:
        return False  # Another agent claimed it first
```

**Folder Structure:**
```
/Needs_Action/          # Unclaimed tasks
/In_Progress/
    /cloud_agent/       # Tasks claimed by Cloud
    /local_agent/       # Tasks claimed by Local
/Done/                  # Completed tasks
```

---

## Conflict Resolution

### Git Merge Conflicts

**Strategy:** Cloud and Local write to different folders, minimizing conflicts.

**If conflict occurs:**
```bash
# Accept both changes (manual merge)
git checkout --ours Dashboard.md
git checkout --theirs Pending_Approval/

# Or use merge tool
git mergetool
```

### File Locking

**Dashboard.md:** Only Local writes
**Pending_Approval/:** Only Cloud writes
**Approved/:** Only Local writes

---

## Testing the Sync

### Test 1: Cloud → Local
```bash
# On Cloud VM
echo "Test from Cloud" > Updates/SIGNAL_test.md
git add Updates/
git commit -m "Test signal"
git push

# On Local (wait 30s for auto-sync)
cat Updates/SIGNAL_test.md
# Should see: "Test from Cloud"
```

### Test 2: Local → Cloud
```bash
# On Local
echo "Approved" > Approved/TEST_approval.md
git add Approved/
git commit -m "Test approval"
git push

# On Cloud (wait 30s for auto-sync)
cat Approved/TEST_approval.md
# Should see: "Approved"
```

---

## Deployment to Cloud VM

### Oracle Cloud Free Tier Setup

**Step 1: Create VM**
1. Go to Oracle Cloud Console
2. Create Compute Instance
3. Choose: Ubuntu 22.04 (Always Free)
4. Shape: VM.Standard.E2.1.Micro (1 OCPU, 1GB RAM)
5. Add SSH key
6. Create

**Step 2: Connect to VM**
```bash
ssh -i ~/.ssh/oracle_key ubuntu@<VM_IP>
```

**Step 3: Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3-pip -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Install PM2
sudo npm install -g pm2

# Install Git
sudo apt install git -y
```

**Step 4: Clone Repository**
```bash
cd ~
git clone https://github.com/yourusername/platinum-vault.git
cd platinum-vault
```

**Step 5: Install Python Dependencies**
```bash
pip3 install -r requirements.txt
```

**Step 6: Configure Environment**
```bash
# Create .env (Cloud-specific, no secrets)
cat > .env << 'EOF'
AGENT_MODE=cloud
AGENT_NAME=cloud_agent
SYNC_INTERVAL=30
EOF
```

**Step 7: Start Cloud Agent**
```bash
# Start watchers with PM2
pm2 start gmail_watcher.py --name gmail-watcher --interpreter python3
pm2 start linkedin_watcher.py --name linkedin-watcher --interpreter python3

# Start sync script
pm2 start cloud_sync.sh --name vault-sync

# Save PM2 configuration
pm2 save
pm2 startup
```

---

## Monitoring

### Check Sync Status
```bash
# View sync logs
pm2 logs vault-sync

# Check git status
cd Platinum_Tier
git status
git log --oneline -10
```

### Health Check
```bash
# Check if agents are running
pm2 status

# Check last sync time
stat -c %y .git/FETCH_HEAD
```

---

## Security Checklist

- [ ] .gitignore includes all secrets
- [ ] .env files not in repository
- [ ] WhatsApp sessions stay local
- [ ] Banking credentials stay local
- [ ] Payment tokens stay local
- [ ] Cloud agent cannot access sensitive MCP servers
- [ ] Local agent has final approval authority
- [ ] All external actions require Local approval

---

## Troubleshooting

### Sync Not Working
```bash
# Check git remote
git remote -v

# Test connection
git fetch origin

# Check for conflicts
git status
```

### Merge Conflicts
```bash
# Reset to remote
git fetch origin
git reset --hard origin/main

# Or merge manually
git merge origin/main
```

### PM2 Issues
```bash
# Restart sync
pm2 restart vault-sync

# View errors
pm2 logs vault-sync --err
```

---

## Demo Scenario (Platinum Requirement)

**Scenario:** Email arrives while Local is offline → Cloud drafts reply → Local approves → sends

**Step 1: Local Goes Offline**
```bash
# On Local machine
pm2 stop all
# Simulate being offline
```

**Step 2: Email Arrives (Cloud Handles)**
```bash
# On Cloud VM (still running)
# Gmail watcher detects new email
# Creates: Needs_Action/GMAIL_urgent_client.txt
# Cloud agent processes it
# Creates: Pending_Approval/email/DRAFT_Response_Urgent_Client.md
# Syncs to Git
```

**Step 3: Local Returns Online**
```bash
# On Local machine
pm2 start all
# Auto-sync pulls Cloud's draft
git pull origin main
# User sees: Pending_Approval/email/DRAFT_Response_Urgent_Client.md
```

**Step 4: User Approves**
```bash
# User reviews draft
cat Pending_Approval/email/DRAFT_Response_Urgent_Client.md
# User approves
mv Pending_Approval/email/DRAFT_Response_Urgent_Client.md Approved/
```

**Step 5: Local Executes**
```bash
# Local agent detects approved draft
# Calls email MCP server
python email_mcp_server.py Approved/DRAFT_Response_Urgent_Client.md
# Email sent
# Logs action
# Moves to Done/
```

---

## Summary

✅ **Git-based vault sync** - Cloud and Local stay synchronized
✅ **Work-zone specialization** - Cloud drafts, Local approves
✅ **Security** - Secrets never sync
✅ **Claim-by-move** - Prevents double-work
✅ **Conflict-free** - Agents write to different folders
✅ **Production-ready** - PM2 + auto-sync + health monitoring

**Status:** Platinum Tier vault sync architecture complete

---

**Next Steps:**
1. Set up Git repository
2. Deploy Cloud agent to Oracle VM
3. Configure auto-sync scripts
4. Test demo scenario
5. Submit Platinum Tier

---

*Platinum Tier - Cloud + Local Architecture*
*Git-Based Synchronization - Production Ready*

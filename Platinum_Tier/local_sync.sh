#!/bin/bash
# Local Agent - Auto-sync script for Platinum Tier
# Runs every 30 seconds to sync vault with Cloud agent

VAULT_DIR="C:/Users/Dell/Desktop/New folder (3)/AI_personal_Employee/Platinum_Tier"
SYNC_INTERVAL=30
LOG_FILE="$VAULT_DIR/Logs/local_sync.log"

# Ensure log directory exists
mkdir -p "$VAULT_DIR/Logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Local sync script started"

while true; do
    cd "$VAULT_DIR" || exit 1

    # Pull changes from Cloud agent
    log "Pulling changes from remote..."
    git pull origin main --no-edit >> "$LOG_FILE" 2>&1

    # Add only Local-owned files (includes secrets, but .gitignore prevents sync)
    git add Approved/ 2>/dev/null
    git add Done/ 2>/dev/null
    git add Dashboard.md 2>/dev/null
    git add Rejected/ 2>/dev/null

    # Check if there are changes to commit
    if ! git diff-index --quiet HEAD --; then
        log "Changes detected, committing..."
        git commit -m "Local: Auto-sync $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1

        log "Pushing to remote..."
        git push origin main >> "$LOG_FILE" 2>&1

        if [ $? -eq 0 ]; then
            log "Sync successful"
        else
            log "ERROR: Push failed"
        fi
    else
        log "No changes to sync"
    fi

    sleep $SYNC_INTERVAL
done

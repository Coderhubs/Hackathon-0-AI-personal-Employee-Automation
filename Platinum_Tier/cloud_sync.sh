#!/bin/bash
# Cloud Agent - Auto-sync script for Platinum Tier
# Runs every 30 seconds to sync vault with Local agent

VAULT_DIR="/home/ubuntu/Platinum_Tier"
SYNC_INTERVAL=30
LOG_FILE="$VAULT_DIR/Logs/cloud_sync.log"

# Ensure log directory exists
mkdir -p "$VAULT_DIR/Logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Cloud sync script started"

while true; do
    cd "$VAULT_DIR" || exit 1

    # Pull changes from Local agent
    log "Pulling changes from remote..."
    git pull origin main --no-edit >> "$LOG_FILE" 2>&1

    # Add only Cloud-owned files (security: no secrets)
    git add Pending_Approval/ 2>/dev/null
    git add Updates/ 2>/dev/null
    git add Plans/ 2>/dev/null
    git add Needs_Action/ 2>/dev/null
    git add Logs/*.md 2>/dev/null

    # Check if there are changes to commit
    if ! git diff-index --quiet HEAD --; then
        log "Changes detected, committing..."
        git commit -m "Cloud: Auto-sync $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1

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

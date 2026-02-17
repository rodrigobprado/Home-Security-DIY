#!/bin/bash

# =============================================================================
# Home Security DIY - Automated Backup Script
# =============================================================================
# This script backs up critical configuration and data for the security system.
# It uses tar/gzip to create archives and manages retention.
#
# Usage: ./backup.sh [backup_dir]
# Recommended: Add to cron (e.g., daily at 3 AM)
# =============================================================================

# Configuration
PROJECT_ROOT="$(dirname "$0")/.."
SRC_DIR="$PROJECT_ROOT/src"
DEFAULT_BACKUP_DIR="$PROJECT_ROOT/backups"
BACKUP_DIR="${1:-$DEFAULT_BACKUP_DIR}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=30
LOG_FILE="$BACKUP_DIR/backup.log"

# directories to backup (relative to src/)
DIRS_TO_BACKUP=(
    "homeassistant"
    "zigbee2mqtt"
    "mosquitto/config"
    "frigate/config.yml"
    ".env"
)

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting Home Security Backup..."

# 1. Stop Containers (Optional but recommended for DB consistency)
# Uncomment the following lines if you want to stop HA during backup (causes downtime)
# log "Stopping containers..."
# cd "$SRC_DIR" && docker compose stop homeassistant

# 2. Create Archive
ARCHIVE_NAME="home_security_backup_$TIMESTAMP.tar.gz"
log "Creating archive $ARCHIVE_NAME..."

# Filter directories to only those that exist
EXISTING_DIRS=()
for dir in "${DIRS_TO_BACKUP[@]}"; do
    if [ -e "$SRC_DIR/$dir" ]; then
        EXISTING_DIRS+=("$dir")
    else
        log "WARNING: Skipping missing directory/file: $SRC_DIR/$dir"
    fi
done

if [ ${#EXISTING_DIRS[@]} -eq 0 ]; then
    log "ERROR: Nothing to backup!"
    exit 1
fi

cd "$SRC_DIR" || exit 1
# Tar command: exclude heavy media/tmp folders if mistakenly inside config dirs
tar --exclude='*.db-wal' --exclude='*.db-shm' --exclude='homeassistant/home-assistant_v2.db' -czf "$BACKUP_DIR/$ARCHIVE_NAME" "${EXISTING_DIRS[@]}" 2>> "$LOG_FILE"

if [ $? -eq 0 ]; then
    log "Backup created successfully: $BACKUP_DIR/$ARCHIVE_NAME"
    size=$(du -h "$BACKUP_DIR/$ARCHIVE_NAME" | cut -f1)
    log "Archive size: $size"
else
    log "ERROR: Backup creation failed!"
    exit 1
fi

# 3. Restart Containers (if stopped)
# log "Restarting containers..."
# cd "$SRC_DIR" && docker compose start homeassistant

# 4. Retention Policy (Delete old backups)
log "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "home_security_backup_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete -print >> "$LOG_FILE"

log "Backup process finished."
exit 0

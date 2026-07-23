#!/bin/bash
# Hospital Management System - Database Backup Script
# Usage: ./backup.sh [backup_dir] [retention_days]

set -e

# Configuration
BACKUP_DIR="${1:-/backups}"
RETENTION_DAYS="${2:-7}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-3306}"
DB_NAME="${DB_NAME:-hms_db}"
DB_USER="${DB_USER:-hms_user}"
DB_PASSWORD="${DB_PASSWORD}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate backup filename with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/hms_backup_${TIMESTAMP}.sql.gz"

echo "Starting database backup at $(date)"
echo "Backup file: $BACKUP_FILE"

# Perform MySQL dump and compress
mysqldump \
    --host="$DB_HOST" \
    --port="$DB_PORT" \
    --user="$DB_USER" \
    --password="$DB_PASSWORD" \
    --single-transaction \
    --quick \
    --lock-tables=false \
    --routines \
    --triggers \
    --events \
    "$DB_NAME" | gzip > "$BACKUP_FILE"

# Verify backup was created
if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "Backup completed successfully. Size: $BACKUP_SIZE"
else
    echo "ERROR: Backup file was not created"
    exit 1
fi

# Remove old backups (retention policy)
echo "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "hms_backup_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

# List remaining backups
echo "Remaining backups:"
ls -lh "$BACKUP_DIR"/hms_backup_*.sql.gz 2>/dev/null || echo "No backups found"

echo "Backup process completed at $(date)"

#!/bin/bash

# Configuration
BACKUP_DIR="/backups/case-connect"
DATA_DIR="./data/embeddings"
BACKUP_RETENTION_DAYS=7

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create timestamp for backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="case-connect_backup_$TIMESTAMP.tar.gz"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude="node_modules" \
    --exclude=".git" \
    "$DATA_DIR"

# Remove old backups
find "$BACKUP_DIR" -name "case-connect_backup_*.tar.gz" -mtime +$BACKUP_RETENTION_DAYS -delete

echo "Backup completed: $BACKUP_NAME"

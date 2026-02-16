#!/bin/bash

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

DB_CONTAINER="physicshub_db"
DB_NAME=${DB_NAME:-physicshub}
DB_USER=${DB_USER:-physicshub}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/manual"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Starting manual backup for $DB_NAME..."

docker exec $DB_CONTAINER pg_dump -U $DB_USER $DB_NAME > "$BACKUP_DIR/backup_$TIMESTAMP.sql"

if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_DIR/backup_$TIMESTAMP.sql"
else
    echo "Backup failed!"
    exit 1
fi

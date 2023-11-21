#!/bin/bash

# Define variables
db_file="database.db"
backup_file="backup_$(date +'%Y%m%d_%H%M%S').sqlite3"

# Perform backup
echo "Creating backup of $db_file to $backup_file"
sqlite3 $db_file ".backup $backup_file"

echo "Backup completed successfully!"

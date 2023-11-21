#!/bin/bash

# Get the filename from the command line arguments
filename=$1

# Check if the database file is present
if [ -f "database.sqlite3" ]; then
    cp "database.sqlite3" "$filename"
    echo "Backup completed successfully: $filename"
    exit 0
else
    echo "Error: Database file 'database.sqlite3' not found. Backup unsuccessful."
    exit 1
fi

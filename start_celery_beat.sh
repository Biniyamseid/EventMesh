#!/bin/bash

# Maximum number of attempts to start Celery Beat
max_attempts=5
attempt=1

# The expected path for the Celery Beat schedule file
schedule_file="/app/celerybeat-schedule"

# Function to check and handle the schedule file/directory issue
check_and_handle_schedule_file() {
    if [ -d "$schedule_file" ]; then
        echo "Found a directory at ${schedule_file}, but expected a file. Deleting the directory."
        rm -rf "$schedule_file"
    fi

    # Ensure the directory where the schedule file should be located has the correct permissions
    mkdir -p $(dirname "$schedule_file")
    chmod -R 755 $(dirname "$schedule_file")
}

# Attempt to start Celery Beat with retries
while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt of $max_attempts to start Celery Beat..."

    # Check and handle the schedule file issue before each attempt
    check_and_handle_schedule_file

    # Start Celery Beat
    celery -A celery_worker.app beat --loglevel=info

    # Check if Celery Beat started successfully
    if [ $? -eq 0 ]; then
        echo "Celery Beat started successfully."
        exit 0
    else
        echo "Celery Beat failed to start. Retrying..."
        attempt=$((attempt+1))
    fi
done

echo "Failed to start Celery Beat after $max_attempts attempts."
exit 1
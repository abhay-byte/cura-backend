#!/usr/bin/env bash

# This script starts all the necessary services for the application.
# It is intended to be used as the 'Start Command' on platforms like Render.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

echo "--- Starting Application Services ---"

# 1. Start the Flask Reminder Agent in the background
echo "Starting Flask reminder agent..."
poetry run python agents/reminder_agent_logic/main.py &

# 2. Start the Django Cron Job runner in the background
# This will continuously check for and run scheduled tasks every 5 minutes.
echo "Starting Django cron job runner..."
(while true; do poetry run python core_backend/manage.py runcrons; sleep 300; done) &

# 3. Start the Main Django Application with Gunicorn in the foreground
# This must be the last command, as it's the main web process.
echo "Starting Django application with Gunicorn..."
poetry run gunicorn --chdir core_backend core_backend.wsgi:application

#!/usr/bin/env bash

# This script starts all the necessary services for the application.
# It is intended to be used as the 'Start Command' on platforms like Render.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

echo "--- Starting Application Services ---"

# 1. Start the Flask Reminder Agent in the background
# We cd into the agent's directory first to ensure it finds main.py
echo "Starting Flask reminder agent..."
(cd agents/reminder_agent_logic && poetry run python main.py) &

# 2. Start a simple cron job loop in the background
# This calls the trigger endpoint every 5 minutes (300 seconds).
# This is a reliable workaround for Render's free tier.
echo "Starting cron job loop..."
(while true; do curl -s http://127.0.0.1:8000/api/reminder/trigger/; sleep 300; done) &

# 3. Start the Main Django Application with Gunicorn in the foreground
# This must be the last command, as it's the main web process.
echo "Starting Django application with Gunicorn..."
poetry run gunicorn --chdir core_backend core_backend.wsgi:application

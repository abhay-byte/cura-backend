#!/usr/bin/env bash

# This script starts all the necessary services for the application.
# It is intended to be used as the 'Start Command' on platforms like Render.
# It changes directory for each command to ensure correct execution paths.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

echo "--- Starting Application Services ---"

# 1. Start the Flask Reminder Agent in the background
# We cd into the agent's directory first to ensure it finds main.py
echo "Starting Flask reminder agent..."
(cd agents/reminder_agent_logic && poetry run python main.py) &

# 2. Start the Django Cron Job runner in the background
# We cd into the Django project directory to ensure manage.py finds the command
echo "Starting Django cron job runner..."
(while true; do cd core_backend && poetry run python manage.py runcrons && cd ..; sleep 300; done) &

# 3. Start the Main Django Application with Gunicorn in the foreground
# This must be the last command, as it's the main web process.
echo "Starting Django application with Gunicorn..."
poetry run gunicorn --chdir core_backend core_backend.wsgi:application
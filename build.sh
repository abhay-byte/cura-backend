#!/usr/bin/env bash

# This script is designed to be used as a build command on platforms like Render.
# It installs dependencies, runs database migrations, and starts both the
# Flask reminder agent and the main Django application.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

echo "--- Starting build process ---"

# --- 1. Install Main and Agent Dependencies ---
echo "Installing all project dependencies..."
poetry install

# Navigate into the reminder agent submodule to install its dependencies
# (This step might be necessary if the agent has its own requirements.txt
# and isn't managed by the root poetry file)
echo "Installing dependencies for the reminder agent..."
cd agents/reminder_agent_logic/
# Assuming the agent has a requirements.txt file
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
# Navigate back to the project root
cd ../..

# --- 2. Run Database Migrations ---
echo "Running Django database migrations..."
poetry run python core_backend/manage.py migrate

# --- 3. Start the Flask Reminder Agent in the Background ---
echo "Starting Flask reminder agent in the background..."
cd agents/reminder_agent_logic/
# Start the Flask app in the background on port 5000
# The '&' symbol runs the command as a background process
python main.py &
cd ../..
echo "Flask reminder agent is running."

# --- 4. Start the Main Django Application with Gunicorn ---
# Gunicorn is a production-ready web server for Python.
# Render will use the command specified in its web service settings,
# which should be this line.
echo "Starting Django application with Gunicorn..."
poetry run gunicorn core_backend.wsgi:application

#!/usr/bin/env bash

# This script is designed to be used as a build command on platforms like Render.
# It only handles the build steps: installing dependencies and running migrations.
# The application startup is handled by the 'Start Command' using the Procfile.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

echo "--- Starting build process ---"

# --- 1. Initialize and Update Git Submodules ---
# This is a critical step to ensure the agent code is actually cloned.
echo "Initializing and updating submodules..."
git submodule update --init --recursive

# --- 2. Install All Project Dependencies ---
# The --no-root flag tells Poetry to skip installing the main project package.
echo "Installing all project dependencies via Poetry..."
poetry install --no-root

# --- 3. Collect Static Files ---
# This is a standard and required step for deploying Django projects.
# It gathers all static files (CSS, JS, images) into a single directory.
echo "Collecting static files..."
poetry run python core_backend/manage.py collectstatic --no-input

# --- 4. Run Database Migrations ---
echo "Running Django database migrations..."
poetry run python core_backend/manage.py migrate

# --- 5. Add Cron Jobs to the System Crontab ---
# This command reads the CRONJOBS setting in settings.py and adds them.
echo "Adding cron jobs..."
poetry run python core_backend/manage.py crontab add

echo "--- Build process finished successfully ---"

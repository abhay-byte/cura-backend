#!/usr/bin/env bash

# This script is designed to be used as a build command on platforms like Render.
# It handles the build steps: installing dependencies and running migrations.
# The application startup is handled by the 'start.sh' script.

# Exit immediately if a command exits with a non-zero status.
set -o errexit

echo "--- Starting build process ---"

# --- 1. Initialize and Update Git Submodules ---
echo "Syncing and updating submodules to the latest version..."
git submodule sync --recursive
git submodule update --init --remote --merge

# --- 2. Install All Project Dependencies ---
echo "Installing all project dependencies via Poetry..."
poetry install --no-root

# --- 3. Collect Static Files ---
echo "Collecting static files..."
poetry run python core_backend/manage.py collectstatic --no-input

# --- 4. Run Database Migrations ---
echo "Running Django database migrations..."
poetry run python core_backend/manage.py migrate

# --- 5. Make the Start Script Executable ---
# This ensures Render can run the start.sh script.
echo "Making start script executable..."
chmod +x ./start.sh

echo "--- Build process finished successfully ---"

#!/bin/bash

# This script runs the Django cron jobs for the CURA project.
# It should be executed from the root directory of the project (CURA-BACKEND).

echo "Starting Django cron jobs..."

# Navigate to the directory of the script to ensure correct path context
# This makes the script runnable from anywhere on the system
cd "$(dirname "$0")"

# Execute the runcrons command using poetry
poetry run python core_backend/manage.py runcrons

echo "Cron jobs execution finished."

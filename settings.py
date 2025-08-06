# core_backend/settings.py
import os
import sys 
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add the project's ROOT directory (CURA-BACKEND) to the Python path
# This allows Django to find the 'agents' module.
sys.path.insert(0, os.path.join(BASE_DIR.parent))


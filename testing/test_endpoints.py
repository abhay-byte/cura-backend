import requests
import json
import sys
import time
import random

# --- Configuration ---
# This script uses a single session to automatically handle authentication cookies.
session = requests.Session()

# Define the base URLs for your environments
BASE_URLS = {
    "local": "http://127.0.0.1:8000",
    "prod": "https://cura-backend-main-99c8.onrender.com"
}

# --- Helper Functions ---

def print_status(response, endpoint):
    """Prints the status of an API call in a formatted way."""
    status_code = response.status_code
    status_color = "\033[92m" if 200 <= status_code < 300 else "\033[91m"
    print(f"  [{status_color}{status_code}\033[0m] Response from {endpoint}")
    try:
        print(f"     -> {response.json()}")
    except json.JSONDecodeError:
        print(f"     -> (No JSON response)")

def get_input(prompt, default=""):
    """Gets user input with a default value."""
    value = input(f"{prompt} [{default}]: ")
    return value or default

# --- Main Test Logic ---

def run_tests(base_url):
    """Runs a sequence of tests against the specified base URL."""
    print(f"\n--- Starting tests against {base_url} ---\n")
    
    # Generate unique user details for each run to avoid conflicts
    rand_id = random.randint(1000, 9999)
    test_username = f"testuser{rand_id}"
    test_email = f"test{rand_id}@example.com"
    test_password = "password123"
    
    print(f"Using test user: {test_username} ({test_email})")

    try:
        # 1. Health Check
        print("\n[1. Health Check]")
        r = session.get(base_url + "/")
        print_status(r, "/")

        # 2. Authentication
        print("\n[2. Authentication]")
        signup_data = {
            "username": test_username,
            "email": test_email,
            "password": test_password
        }
        r = session.post(base_url + "/api/auth/signup/", json=signup_data)
        print_status(r, "/api/auth/signup/")

        login_data = {"email": test_email, "password": test_password}
        r = session.post(base_url + "/api/auth/login/", json=login_data)
        print_status(r, "/api/auth/login/")

        # 3. Diet Agent Flow
        print("\n[3. Diet Agent Flow]")
        profile_data = {
            "age": 30, "weight_kg": 75, "height_cm": 180,
            "activity_level": "Moderately Active", "dietary_preferences": "Non-Veg",
            "allergies": "None", "health_issues": "General Health"
        }
        r = session.post(base_url + "/api/diet/profile/", json=profile_data)
        print_status(r, "POST /api/diet/profile/")

        r = session.get(base_url + "/api/diet/profile/")
        print_status(r, "GET /api/diet/profile/")

        print("   Waiting for diet plan generation...")
        r = session.post(base_url + "/api/diet/plan/generate/")
        print_status(r, "/api/diet/plan/generate/")
        time.sleep(5) # Give the agent some time

        r = session.get(base_url + "/api/diet/plan/")
        print_status(r, "/api/diet/plan/")

        # 4. Reminder Agent Flow
        print("\n[4. Reminder Agent Flow]")
        medicine_data = {"name": "Paracetamol", "dosage": "500mg", "inventory": 50}
        r = session.post(base_url + "/api/reminder/medicines/", json=medicine_data)
        print_status(r, "POST /api/reminder/medicines/")
        medicine_id = r.json().get("id")

        r = session.get(base_url + "/api/reminder/medicines/")
        print_status(r, "GET /api/reminder/medicines/")

        reminder_data = {"time": "09:00", "quantity": 1, "instruction": "After Food"}
        r = session.post(f"{base_url}/api/reminder/medicines/{medicine_id}/reminders/", json=reminder_data)
        print_status(r, f"POST /api/reminder/medicines/{medicine_id}/reminders/")
        reminder_id = r.json().get("reminder_id")

        r = session.post(f"{base_url}/api/reminder/reminders/{reminder_id}/take/")
        print_status(r, f"POST /api/reminder/reminders/{reminder_id}/take/")

        update_med_data = {"inventory": 49}
        r = session.put(f"{base_url}/api/reminder/medicines/{medicine_id}/", json=update_med_data)
        print_status(r, f"PUT /api/reminder/medicines/{medicine_id}/")

        r = session.delete(f"{base_url}/api/reminder/medicines/{medicine_id}/")
        print_status(r, f"DELETE /api/reminder/medicines/{medicine_id}/")

    except requests.exceptions.ConnectionError as e:
        print(f"\n\033[91mERROR: Could not connect to {base_url}\033[0m")
        print("Please ensure the server is running.")
    except Exception as e:
        print(f"\n\033[91mAn unexpected error occurred: {e}\033[0m")

if __name__ == "__main__":
    print("--- CURA API Endpoint Test Script ---")
    env = get_input("Choose environment (local/prod)", "local").lower()
    
    if env not in BASE_URLS:
        print(f"Invalid environment '{env}'. Please choose 'local' or 'prod'.")
        sys.exit(1)
        
    run_tests(BASE_URLS[env])

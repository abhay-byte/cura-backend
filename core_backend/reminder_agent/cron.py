import requests

def trigger_reminder_agent_job():
    """
    This function is called by django-crontab to trigger the reminder agent.
    """
    reminder_agent_url = "http://127.0.0.1:5000/api/reminder/trigger/"
    print(f"CRON JOB: Triggering reminder agent at {reminder_agent_url}")
    
    try:
        response = requests.get(reminder_agent_url, timeout=60)
        if response.status_code == 200:
            print(f"CRON JOB: Agent responded successfully: {response.json()}")
        else:
            print(f"CRON JOB ERROR: Agent failed with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"CRON JOB ERROR: Could not connect to the reminder agent: {e}")
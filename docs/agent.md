# Agent Instructions

This document provides general instructions for the backend developers implementing the core agent logic for the Health Agents project.

---

## Reminder Agent (PS1)

-   **Trigger**: This agent's logic is executed when the `/api/reminder/trigger/` endpoint is called (ideally by a scheduled task like a cron job).
-   **Input Data**: The agent should query the database for all `Reminder` objects where `is_active` is `True`. It needs to access the related `Medicine` and `User` data for each reminder.
-   **Core Task**:
    1.  For each active reminder, check if the `reminder_time` matches the current time.
    2.  If it's time for a reminder, generate a notification message that includes the **`quantity`** to be taken (e.g., "Time to take 2 pills of Paracetamol").
    3.  Check the `inventory` of the associated `Medicine`. If the inventory is at or below the `refill_threshold`, generate a refill alert.
-   **Output**: The agent's primary output is sending notifications (e.g., via email, push notification services). The endpoint itself can return a summary of actions taken.
    ```json
    {
      "status": "Reminder check completed.",
      "reminders_sent": 5,
      "refill_alerts": 1
    }
    ```

---

## Diet Agent (PS2)

-   **Trigger**: This agent's logic is executed when a user calls the `POST /api/diet/plan/generate/` endpoint.
-   **Input Data**: The agent receives the user's complete health profile from the `UserProfile` model. The key data points are:
    -   `age` (number)
    -   `weight_kg` (number)
    -   `height_cm` (number)
    -   `activity_level` (string, e.g., "Sedentary", "Lightly Active")
    -   `dietary_preferences` (string, e.g., "Vegan", "Non-Veg")
    -   `allergies` (string, comma-separated)
    -   `health_issues` (string, e.g., "Diabetes")
-   **Core Task**:
    1.  Analyze the user's profile to determine their nutritional needs (e.g., daily caloric intake, macronutrient split).
    2.  Generate a personalized, structured diet plan for one full day.
    3.  The plan must respect all `dietary_preferences` and `allergies`.
    4.  The plan should be tailored to address any specified `health_issues`.
    5.  Generate a corresponding grocery list for the created meals.
-   **Output Format (Exact JSON Structure)**: The agent must return a JSON object that will be stored in the `plan_details` field of the `DietPlan` model. The structure must be as follows:
    ```json
    {
      "daily_calories": 2150,
      "macronutrients": {
        "protein_grams": 150,
        "carbs_grams": 200,
        "fat_grams": 80
      },
      "meals": {
        "breakfast": {
          "name": "Greek Yogurt with Almonds and Berries",
          "time": "08:00",
          "calories": 400,
          "notes": "A great source of protein to start your day."
        },
        "lunch": {
          "name": "Quinoa Salad with Chickpeas and Avocado",
          "time": "13:00",
          "calories": 650,
          "notes": "Rich in fiber and healthy fats."
        },
        "snack": {
          "name": "Apple with Peanut Butter",
          "time": "16:00",
          "calories": 250,
          "notes": ""
        },
        "dinner": {
          "name": "Baked Salmon with Asparagus and Sweet Potato",
          "time": "19:30",
          "calories": 850,
          "notes": "Excellent source of Omega-3 fatty acids."
        }
      },
      "grocery_list": [
        "Greek Yogurt",
        "Almonds",
        "Mixed Berries",
        "Quinoa",
        "Chickpeas",
        "Avocado",
        "Apple",
        "Peanut Butter",
        "Salmon Fillet",
        "Asparagus",
        "Sweet Potato"
      ],
      "notes": "Remember to drink at least 8 glasses of water throughout the day."
    }
    ```


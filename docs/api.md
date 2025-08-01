# CURA API Documentation

This document provides a comprehensive guide to all the API endpoints for the Health Agents project, which includes a Medication Reminder Agent and a Personalized Diet Agent.

**Base URL**: All endpoints are prefixed with `http://127.0.0.1:8000/api/`

---

## Authentication

This API uses session-based authentication.

1.  A user must first **sign up** and then **log in**.
2.  The `/login/` endpoint, upon successful authentication, will return a `sessionid` cookie.
3.  The front-end client **must** store this cookie and include it in the headers of all subsequent requests to protected endpoints. Endpoints that require authentication are marked with **"Authentication Required"**.

---

## 1. Authentication Endpoints

These endpoints handle user creation and session management.

### **Endpoint: `POST /auth/signup/`**

-   **Description**: Creates a new user account.
-   **Authentication**: None required.
-   **Request Body**:
    ```json
    {
      "username": "testuser",
      "email": "test@example.com",
      "password": "a_strong_password"
    }
    ```
-   **Success Response (201 Created)**:
    ```json
    {
      "message": "User created successfully."
    }
    ```
-   **Error Responses**:
    -   **400 Bad Request** (Missing fields):
        ```json
        { "error": "Username, password, and email are required." }
        ```
    -   **400 Bad Request** (Email or username in use):
        ```json
        { "error": "Email already in use." }
        ```

### **Endpoint: `POST /auth/login/`**

-   **Description**: Authenticates a user and starts a session.
-   **Authentication**: None required.
-   **Request Body**:
    ```json
    {
      "email": "test@example.com",
      "password": "a_strong_password"
    }
    ```
-   **Success Response (200 OK)**:
    *The `Set-Cookie` header will contain the `sessionid`.*
    ```json
    {
      "message": "Welcome back, testuser!",
      "userId": 1,
      "email": "test@example.com"
    }
    ```
-   **Error Response (401 Unauthorized)**:
    ```json
    { "error": "Invalid credentials." }
    ```

---
## 2. Reminder Agent Endpoints

Handles management of medicines and their reminders.

### **Endpoint: `GET /reminder/medicines/`**

-   **Description**: Retrieves a list of all medicines and their associated reminders for the authenticated user.
-   **Authentication**: **Required**.
-   **Success Response (200 OK)**:
    ```json
    [
      {
        "id": 1,
        "name": "Paracetamol",
        "dosage": "500mg",
        "inventory": 50,
        "reminders": [
          {
            "id": 101,
            "time": "09:00",
            "quantity": 1,
            "instruction": "After Food"
          },
          {
            "id": 102,
            "time": "21:00",
            "quantity": 1,
            "instruction": "After Food"
          }
        ]
      }
    ]
    ```

### **Endpoint: `POST /reminder/medicines/`**

-   **Description**: Adds a new medicine for the authenticated user.
-   **Authentication**: **Required**.
-   **Request Body**:
    ```json
    {
      "name": "Aspirin",
      "dosage": "100mg",
      "inventory": 100
    }
    ```
-   **Success Response (201 Created)**:
    ```json
    {
      "message": "Medicine added.",
      "id": 3
    }
    ```

### **Endpoint: `PUT /reminder/medicines/{id}/`**

-   **Description**: Updates the details for a single medicine.
-   **Authentication**: **Required**.
-   **Request Body**:
    ```json
    {
      "inventory": 45
    }
    ```
-   **Success Response (200 OK)**:
    ```json
    { "message": "Medicine updated successfully." }
    ```

### **Endpoint: `DELETE /reminder/medicines/{id}/`**

-   **Description**: Deletes a medicine and all its associated reminders.
-   **Authentication**: **Required**.
-   **Success Response**: **204 No Content**.

### **Endpoint: `POST /reminder/medicines/{medicine_id}/reminders/`**

-   **Description**: Adds a new reminder for a specific medicine.
-   **Authentication**: **Required**.
-   **Request Body**:
    ```json
    {
      "time": "08:30",
      "quantity": 2,
      "instruction": "Before Food"
    }
    ```
-   **Success Response (201 Created)**:
    ```json
    {
      "message": "Reminder added successfully.",
      "reminder_id": 103
    }
    ```

### **Endpoint: `POST /reminder/reminders/{reminder_id}/take/`**

-   **Description**: Marks a dose as taken. This will decrease the medicine's inventory by the reminder's quantity.
-   **Authentication**: **Required**.
-   **Request Body**: None.
-   **Success Response (200 OK)**:
    ```json
    {
      "message": "Recorded that you took Paracetamol.",
      "new_inventory": 49
    }
    ```
-   **Error Response (400 Bad Request)**:
    ```json
    { "error": "Not enough medicine in inventory." }
    ```
---

## 3. Diet Agent Endpoints

Handles user health profiles and personalized diet plans.

### **Endpoint: `GET /diet/profile/`**

-   **Description**: Retrieves the health profile for the authenticated user.
-   **Authentication**: **Required**.
-   **Success Response (200 OK)**:
    ```json
    {
      "age": 30,
      "weight_kg": 75.5,
      "height_cm": 180,
      "dietary_preferences": "Vegan",
      "allergies": "Peanuts, Shellfish",
      "health_issues": "None"
    }
    ```

### **Endpoint: `POST /diet/profile/`**

-   **Description**: Creates or updates the health profile for the authenticated user.
-   **Authentication**: **Required**.
-   **Request Body**:
    ```json
    {
      "age": 31,
      "weight_kg": 74.0,
      "activity_level": "Lightly Active",
      "dietary_preferences": "Vegetarian",
      "allergies": "Peanuts",
      "health_issues": "High Cholesterol"
    }
    ```
-   **Success Response (200 OK)**:
    ```json
    { "message": "Profile updated." }
    ```

### **Endpoint: `GET /diet/plan/`** (only gets one day's plan.)


-   **Description**: Retrieves the user's current active diet plan.
-   **Authentication**: **Required**.
-   **Success Response (200 OK)**:
    ```json
    {
      "daily_calories": 2200,
      "meals": {
        "breakfast": { "name": "Scrambled Tofu", "time": "08:30" },
        "lunch": { "name": "Lentil Soup", "time": "13:00" },
        "dinner": { "name": "Black Bean Burgers", "time": "19:30" }
      },
      "grocery_list": ["Tofu", "Lentils", "Black Beans", "Spinach"],
      "notes": "Ensure you meet your protein goals."
    }
    ```
-   **Error Response (404 Not Found)**:
    ```json
    { "error": "No active diet plan found. Generate one first." }
    ```

### **Endpoint: `POST /diet/plan/generate/`** (only generate one day's plan.)

-   **Description**: Triggers the Diet Agent to generate a new personalized diet plan based on the user's profile.
-   **Authentication**: **Required**.
-   **Request Body**: None.
-   **Success Response (201 Created)**:
    ```json
    {
      "message": "New diet plan generated.",
      "plan": {
        "daily_calories": 2200,
        "meals": { "...": "..." },
        "grocery_list": [ "..." ],
        "notes": "..."
      }
    }
    ```
-   **Error Response (400 Bad Request)**:
    ```json
    { "error": "User profile not found. Please create it first." }
    ```


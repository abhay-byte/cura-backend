# CURA - AI Health Agents

**CURA** (from the Latin word for "care" and "attention") is a Django-based backend service that powers two intelligent health agents: a medication reminder agent and a personalized diet planning agent.

---

## 📖 Documentation

This project is documented in two separate files for clarity:

-   **[API Documentation](./docs/api.md)**: A comprehensive guide to all API endpoints, including request/response formats and authentication details. This is primarily for front-end developers.

-   **[Agent Instructions](./docs/agent.md)**: Detailed instructions for backend developers on the expected behavior, input data, and output structure for the AI agents. 

-   **[Database Schema](./docs/schema.md)**: Complete structure of all the data models used in this project. Working with SQL database. 

---

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python (3.11+)
-   [Poetry](https://python-poetry.org/docs/) for dependency management.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone --recurse-submodules https://github.com/abhay-byte/cura-backend.git
    cd cura-backend
    ```

2.  **Install dependencies:**
    Poetry will create a virtual environment and install all the required packages from `pyproject.toml`.
    ```bash
    poetry install
    ```

3.  **Set Up Environment Variables:**
    The agents require API keys and credentials.
    -   **For the Diet Agent:** Create a file named `.env` in the root of the `CURA-BACKEND` directory. Add your Google API key:
        ```
        # .env
        GOOGLE_API_KEY="AIzaSy...your...key...here"
        ```
    -   **For the Reminder Agent:** The reminder agent uses a separate `new.env` file inside its own directory (`agents/reminder_agent_logic/`). You will need to set up your email credentials there as per its documentation.


4.  **Run database migrations:**
    This will set up your database schema based on the project's models.
    ```bash
    poetry run python core_backend/manage.py migrate
    ```

5.  **Create a superuser (optional but recommended):**
    This allows you to access the Django admin panel.
    ```bash
    poetry run python core_backend/manage.py createsuperuser
    ```

6. **Adding the project's root directory to the Python path:** To allow Django to find the agent code

    ```bash
    poetry run python settings.py  
    ```

### Running the Full System

To run the complete application, you need to run **two separate servers** in **two separate terminals**.

1.  **Terminal 1: Start the Reminder Agent (Flask App)**
    ```bash
    cd agents/reminder_agent_logic/

    pip install -r requirements.txt 

    python main.py
    ```
    *This server will typically run on `http://127.0.0.1:5000`.*

2.  **Terminal 2: Start the Main Backend (Django App)**
    ```bash
    cd ../..

    poetry run python core_backend/manage.py runserver
    ```
    *This server will run on `http://127.0.0.1:8000`.*

### Automated Tasks (Cron Jobs)

The system uses `django-cron` to schedule tasks, such as triggering the reminder agent. A helper script is provided to run these tasks.

-   **To run manually:**
    ```bash
    ./run_crons.sh
    ```
-   **For production:** You would set up a system cron job to execute the `run_crons.sh` script periodically (e.g., every 5 minutes).

---

## Deployment 

This section contains information for deploying the project to a platform like Render.

### Render Build Script (`build.sh`)

This script handles the complete build and startup process for the application on Render. It should be saved as `build.sh` in the project root and set as the **Build Command** in your Render service settings.


```
Project Structure
.
├── agents            # Directory for agent submodules
│   ├── diet_agent_logic
│   └── reminder_agent_logic
├── core_backend      # Main Django project directory
│   ├── core_backend  # Project settings
│   ├── diet_agent    # App for the Diet Agent
│   ├── reminder_agent  # App for the Reminder Agent
│   ├── users         # App for user authentication
│   └── manage.py     # Django's command-line utility
├── docs
│   ├── agent.md      # Documentation for agent logic
│   └── api.md        # Documentation for API endpoints
├── pyproject.toml    # Poetry dependency file
├── run_crons.sh      # Cron Job for tasks
├── build.sh          # Build and Run Production Application
└── README.md         # This file
```
---
## Credits

A special thank you to my friend and collaborator for their work on the AI agents.

-   **AI Agent Logic**: [PriyanshuGupta1102](https://github.com/PriyanshuGupta1102)
    -   [Cura-diet-agent](https://github.com/PriyanshuGupta1102/Cura-diet-agent)
    -   [cura-reminder-agent](https://github.com/PriyanshuGupta1102/cura-reminder-agent)

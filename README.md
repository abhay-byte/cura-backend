# CURA - AI Health Agents

**CURA** (from the Latin word for "care" and "attention") is a Django-based backend service that powers two intelligent health agents: a medication reminder agent and a personalized diet planning agent.

---

## 📖 Documentation

This project is documented in two separate files for clarity:

-   **[API Documentation](./docs/api.md)**: A comprehensive guide to all API endpoints, including request/response formats and authentication details. This is primarily for front-end developers.

-   **[Agent Instructions](./docs/agent.md)**: Detailed instructions for backend developers on the expected behavior, input data, and output structure for the AI agents. (TASK YET TO BE COMPLETED)

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
    git clone https://github.com/abhay-byte/cura-backend.git
    ```

2.  **Install dependencies:**
    Poetry will create a virtual environment and install all the required packages from `pyproject.toml`.
    ```bash
    poetry install
    ```

3.  **Run database migrations:**
    This will set up your database schema based on the project's models.
    ```bash
    poetry run python core_backend/manage.py migrate
    ```

4.  **Create a superuser (optional but recommended):**
    This allows you to access the Django admin panel.
    ```bash
    poetry run python core_backend/manage.py createsuperuser
    ```

### Running the Development Server

Once the setup is complete, you can start the Django development server:

```bash
poetry run python core_backend/manage.py runserver
```

The API will be accessible at http://127.0.0.1:8000/.

```
Project Structure
.
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
└── README.md         # This file
```

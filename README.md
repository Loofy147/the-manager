# Project Management Application

This is a full-stack project management application with a Flask backend and a React frontend.

## Features

*   **User Authentication:** Users can register and log in to the application.
*   **Project Management:** Users can view a list of projects.
*   **Task Management:** Users can view a list of tasks for each project.
*   **Comments:** Users can add comments to tasks.

## Production Architecture

The production architecture consists of three services:

*   **Backend:** A Flask API containerized with Docker and served with Gunicorn.
*   **Frontend:** A React application containerized with Docker and served with Nginx.
*   **Nginx:** An Nginx reverse proxy that routes requests to the frontend and backend services.

The entire stack is orchestrated with `docker-compose.yml`.

## Getting Started

To get started, you will need to have Docker and Docker Compose installed.

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    ```

2.  **Start the application:**

    ```bash
    docker-compose up -d
    ```

The application will be available at `http://localhost:8080`.

## Operational Procedures

For information on how to operate the system, including troubleshooting common issues, please see the `RUNBOOK.md` file.

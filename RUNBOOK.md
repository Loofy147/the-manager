# Runbook

This document details the procedures for operating the system, including troubleshooting common issues.

## 1. Starting the Application

To start the application, run the following command from the root of the repository:

```bash
docker-compose up -d
```

The application will be available at `http://localhost:8080`.

## 2. Stopping the Application

To stop the application, run the following command from the root of the repository:

```bash
docker-compose down
```

## 3. Troubleshooting

### 3.1. 502 Bad Gateway

This error indicates that the Nginx reverse proxy is unable to connect to the backend or frontend services. To troubleshoot this issue, check the logs for the backend and frontend containers:

```bash
docker-compose logs backend
docker-compose logs frontend
```

### 3.2. "index.html not found"

This error indicates that the frontend container is running, but the `index.html` file is not in the correct location. To troubleshoot this issue, ensure that the `COPY --from=builder /app/dist /usr/share/nginx/html` command in the `project_management_frontend/Dockerfile` is correct.

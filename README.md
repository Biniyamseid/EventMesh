# FastAPI Webhook Service for Resend Notifications 🚀

## Project Description 📝

The FastAPI Webhook Service is a robust and scalable solution designed to handle real-time email notification webhooks from Resend. Built with FastAPI, it leverages the asynchronous processing power of Celery and Redis to manage notifications efficiently, while storing each event as a unique row in ClickHouse. This service ensures high throughput and reliable storage for webhook payloads, making it an ideal choice for applications requiring real-time email event tracking and processing.

### Features

- **Real-time Processing**: Asynchronous handling of incoming webhook payloads for immediate processing. 🔄
- **Scalable Architecture**: Built to accommodate a high number of simultaneous connections and payloads. 📈
- **Persistent Storage**: Utilizes ClickHouse to store webhook events, ensuring data durability and fast querying. 💾
- **Error Handling**: Sophisticated error management to log and address failed deliveries or database insertions. 🚫

## Getting Started 🏁

### Dependencies 📦

- Python 3.6+
- FastAPI
- Celery
- Redis
- ClickHouse

### Installing 🛠️

To get started with the FastAPI Webhook Service, follow these steps:

1. **Clone the repository** to your local machine:
```
git clone https://github.com/your-repository/resend_webhook.git
cd resend_webhook
```

2. **Build the Docker containers** using `docker-compose`. This will set up the FastAPI application, Redis, and ClickHouse services:
```
docker-compose up --build
```



This command builds and starts the containers defined in the `docker-compose.yml` file. It includes the web server running FastAPI, a Celery worker for processing tasks, a Celery beat for scheduled tasks, Redis for task messaging, and ClickHouse for data storage.

3. **Access the FastAPI application** at `http://localhost:8000` after the containers are up and running. You can use endpoints such as `/webhook/resend` to receive webhook payloads and `/query` or `/query/all` to retrieve stored payloads.

### Project Structure 📂

- `main.py`: The FastAPI application entry point.
- `celery_worker.py`: Defines Celery tasks for asynchronous processing and scheduled cleanup.
- `database/clickhouse.py`: Contains functions for interacting with the ClickHouse database, including creating tables and inserting/querying data.
- `Dockerfile` and `docker-compose.yml`: Configuration files for building and running the service in Docker containers.
- `create_database.py`: A script for initializing the SQLite database (used in an earlier version and may not be necessary for the ClickHouse setup).

### Usage 🚀

- **Receiving Webhooks**: Send POST requests to `/webhook/resend` with the webhook payload.
- **Querying Payloads**: Use the `/query` endpoint with query parameters like `sender`, `recipient`, `status`, `start_date`, and `end_date` to filter results.
- **Viewing All Payloads**: The `/query/all` endpoint retrieves all stored payloads, requiring basic authentication.

### Security 🔐

Basic authentication is implemented for certain endpoints, requiring a username and password to access.

### Scalability 📈

This service is designed to scale horizontally. You can increase the number of worker containers in the `docker-compose.yml` file to handle higher loads.

### Monitoring and Logging 📊

Logging is configured in the application to track operations and errors. You can extend this setup with external monitoring tools for comprehensive insights.

Enjoy building and scaling your real-time notification service with FastAPI, Celery, Redis, and ClickHouse! 🎉

### Continuous Integration and Deployment (CI/CD) 🔄

Leverage CI/CD pipelines to automate the testing, building, and deployment of your webhook service. This ensures that your application is always running the latest codebase with passed tests. Tools like GitHub Actions, GitLab CI/CD, or Jenkins can be integrated to streamline these processes.

### Docker and Docker Compose 🐳

The project uses Docker and Docker Compose to containerize the application and its dependencies, making it easy to deploy and scale across any environment. The `Dockerfile` defines the environment for the FastAPI application, while `docker-compose.yml` orchestrates the setup of the application, Redis, ClickHouse, and worker services.

### Health Checks and Metrics 📈

Implement health checks to monitor the availability and performance of your service. FastAPI provides built-in support for health checks. Additionally, integrate metrics collection using Prometheus and Grafana for real-time monitoring and alerting.

### Security Practices 🔒

- **HTTPS**: Ensure all communications with the webhook service are over HTTPS to protect against man-in-the-middle attacks.
- **Rate Limiting**: Protect your service from DDoS attacks by implementing rate limiting on incoming requests.
- **Input Validation**: Strictly validate all incoming payloads to prevent injection attacks or malformed data processing.

### Documentation and API Reference 📚

Document your API endpoints using FastAPI's built-in Swagger UI. This provides a clear and interactive API reference for developers, making it easier to integrate with your webhook service.

### Community and Support 🤝

Join FastAPI, Celery, and Redis communities for support and discussions. These communities can provide valuable insights, help troubleshoot issues, and keep you updated with the latest best practices and features.

### Contributing 🛠



### License 📄


---

We hope this guide helps you get best FastAPI Webhook Service for Resend Notifications. 

Happy coding! 🚀
# FastAPI Webhook Service for Resend Notifications 🚀

## Project Description 📝

The FastAPI Webhook Service is a robust and scalable solution designed to handle real-time email notification webhooks from Resend. Built with FastAPI, it leverages the asynchronous processing power of Celery and Redis to manage notifications efficiently, while storing each event as a unique row in ClickHouse. This service ensures high throughput and reliable storage for webhook payloads, making it an ideal choice for applications requiring real-time email event tracking and processing.

### Features

- **Real-time Processing**: Asynchronous handling of incoming webhook payloads for immediate processing.
- **Scalable Architecture**: Built to accommodate a high number of simultaneous connections and payloads.
- **Persistent Storage**: Utilizes ClickHouse to store webhook events, ensuring data durability and fast querying.
- **Error Handling**: Sophisticated error management to log and address failed deliveries or database insertions.

## Getting Started 🏁

### Dependencies 📦

- Python 3.6+
- FastAPI
- Celery
- Redis
- ClickHouse

### Installing 🛠️

Clone the repository and navigate to the project directory:
zz
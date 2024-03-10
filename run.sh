#!/bin/bash
set -e

uvicorn main:app --host 0.0.0.0 --port 8000 &

celery -A celery_worker.app worker --loglevel=info &

# Execute the Dockerfile's original CMD
exec "$@"

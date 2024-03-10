#!/bin/bash

uvicorn main:app --workers 10 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &

celery -A celery_worker.app worker --loglevel=info &

wait

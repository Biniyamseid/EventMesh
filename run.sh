#!/bin/bash

uvicorn main:app --workers 5 --host 0.0.0.0 --port 8000 &

celery -A ./celery_worker.app worker --loglevel=info &

wait

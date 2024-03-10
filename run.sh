#!/bin/bash

uvicorn main:app --workers 10 --bind 0.0.0.0:8000 &

celery -A celery_worker.app worker --loglevel=info &

wait


# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the SQLite database file into the Docker image
# COPY /path/to/your/database.db /app/database.db

RUN pip install sqlalchemy

RUN python ./create_database.py
# RUN chmod 664 /app/results.sqlite3
USER root
RUN python ./create_database.py

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn celery[redis] clickhouse-driver
# RUN pip install --no-cache-dir -r requirements.txt
# RUN chmod 664 /app/results.sqlite3
RUN chmod 664 /app/database.db

RUN chmod +x ./run.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
CMD ["/bin/sh", "run.sh"]
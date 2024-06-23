# Use the official Python image from the Docker Hub
FROM python:3.6-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . .

# Make the necessary scripts executable
RUN chmod +x /usr/src/app/run.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Define the command to run the application
CMD [ "ls", "/usr/src/app" ]

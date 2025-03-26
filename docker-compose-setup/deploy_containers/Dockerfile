# Use an official Python base image
FROM python:3.12.3

# Set working directory
WORKDIR /app

# Install system dependencies (Docker CLI)
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main app files including the deployment script
COPY . .

# Set default command to run the main deployment script
CMD ["python", "deploy_containers.py"]
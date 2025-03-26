# Use the official Python base image
FROM python:3.12.3

# Set working directory inside container
WORKDIR /app

# Copy only requirements file first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the FastAPI application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

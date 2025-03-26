# Use an official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Set timezone (replace "Asia/Ho_Chi_Minh" with your correct timezone)
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Copy the Model directory into the container
COPY Model /app/Model

# Ensure the files exist in the correct location
RUN ls -l /app/ && ls -l /app/Model

# Set the container entrypoint to run `scheduler.py`
CMD ["python", "/app/scheduler.py"]

# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    && apt-get clean
    
# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port on which the app runs
EXPOSE 8000

# Use the entrypoint script to start the application
ENTRYPOINT ["/app/entrypoint.sh"]
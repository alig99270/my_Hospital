# Use official Python image as base
FROM python:3.10-slim-buster
LABEL authors="ali"

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY entrypoint.sh .
COPY manage.py .
COPY hms/ hms/

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev

RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=hms.settings
ENV PYTHONUNBUFFERED=1

# Expose port for internal communication
EXPOSE 8000

# Start with entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

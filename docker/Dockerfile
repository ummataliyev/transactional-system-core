# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port for Django
EXPOSE 8000

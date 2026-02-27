FROM python:3.10-slim

WORKDIR /usr/src/app

# Install system dependencies (needed for psycopg2 and others)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /usr/src/app

ENV PYTHONPATH=/usr/src/app

# (CMD is handled by docker-compose)
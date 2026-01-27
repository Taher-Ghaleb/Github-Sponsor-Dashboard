# Backend Dockerfile - Multi-stage build
FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base AS development

# Install development dependencies if needed
RUN pip install --no-cache-dir flask

# Copy backend code
COPY . .

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=backend.app
ENV FLASK_ENV=development

# Run Flask development server
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]

# Production stage
FROM base AS production

# Copy backend code
COPY . .

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=backend.app

# Run Flask app with Gunicorn
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "backend.app:app"]

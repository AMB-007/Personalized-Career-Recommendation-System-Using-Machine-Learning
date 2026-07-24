# Dockerfile for Career Recommendation System

# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app/backend

# Copy requirements file
COPY ../../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p /app/backend/uploads

# Create logs directory
RUN mkdir -p /app/backend/logs

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the application
CMD ["python", "app.py"]
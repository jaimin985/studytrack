# ============================================================
# StudyTrack – Dockerfile (Python 3.11 slim + Gunicorn)
# ============================================================
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN groupadd -r studytrack && useradd -r -g studytrack -d /app -s /sbin/nologin studytrack

# Set working directory
WORKDIR /app

# Install dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Change ownership to non-root user
RUN chown -R studytrack:studytrack /app

# Switch to non-root user
USER studytrack

# Expose the app port (the actual host mapping is in docker-compose.yml)
EXPOSE 8085

# Start with Gunicorn (production-grade WSGI server)
# --preload ensures the scheduler starts only once
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]

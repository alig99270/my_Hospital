# Use official Python image as base
FROM python:3.11-slim-bullseye AS base

LABEL authors="HMS Team"
LABEL description="Hospital Management System - Production Ready"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# =============================================================================
# Development stage
# =============================================================================
FROM base AS dev

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=hms.settings.dev \
    PYTHONPATH=/app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

# =============================================================================
# Production stage
# =============================================================================
FROM base AS prod

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy only necessary project files
COPY manage.py .
COPY hms/ hms/
COPY accounts/ accounts/
COPY appointments/ appointments/
COPY medical_records/ medical_records/
COPY prescriptions/ prescriptions/
COPY shifts/ shifts/
COPY audit/ audit/
COPY reporting/ reporting/
COPY notifications/ notifications/
COPY dashboard/ dashboard/
COPY entrypoint.sh .
COPY templates/ templates/ 2>/dev/null || true

# Make entrypoint executable and set ownership
RUN chmod +x /app/entrypoint.sh && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=hms.settings.prod \
    PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "hms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--worker-class", "gthread", "--access-logfile", "-", "--error-logfile", "-"]

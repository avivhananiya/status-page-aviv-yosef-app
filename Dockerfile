# =============================================================
# Multi-stage Dockerfile for Status Page (Django + Gunicorn)
# Target: linux/arm64 (AWS Graviton — t4g.large / m6g.large)
# =============================================================

# --- Stage 1: Build dependencies ---
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Runtime ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STATUS_PAGE_CONFIGURATION=statuspage.configuration_docker

WORKDIR /app

# Runtime-only: libpq for psycopg2, no compiler
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-built Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY statuspage/ .

# Non-root user
RUN useradd -m -u 1000 status-page && \
    chown -R status-page:status-page /app

USER status-page

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--timeout", "90", "statuspage.wsgi:application"]

# ============================================
# STAGE 1: Builder (bağımlılıkları hazırla)
# ============================================
FROM python:3.11-slim as builder

WORKDIR /build

# System bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını virtual env'e yükle
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ============================================
# STAGE 2: Runtime (Production Image)
# ============================================
FROM python:3.11-slim

# Metadata
LABEL maintainer="your-email@example.com"
LABEL version="0.1.0"
LABEL description="Smart Notification System - Microservices"

# Non-root user oluştur (Security best practice)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Working directory
WORKDIR /app

# Builder stage'den venv'i kopyala
COPY --from=builder /opt/venv /opt/venv

# Uygulama kodunu kopyala
COPY src/ ./src/
COPY .env.example ./.env.example

# Logs klasörünü oluştur ve permissionları ayarla
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/logs

# Environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LOG_DIR=/app/logs \
    LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Non-root user'a geç
USER appuser

# Entry point - API mode (FastAPI server)
CMD ["python", "src/main.py", "api"]

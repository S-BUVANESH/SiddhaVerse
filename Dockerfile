FROM python:3.11-slim

LABEL maintainer="SiddhaVerse Team"
LABEL description="SiddhaVerse Scholarly RAG API — Production Image"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy source
COPY backend/ ./backend/

# Data volumes (mounted at runtime — not baked in)
VOLUME ["/data/corpus", "/data/qdrant_db"]

# Environment defaults (override via .env or docker -e)
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO
ENV DB_TYPE=sqlite
ENV DB_PATH=/data/corpus/siddhaverse.db
ENV MAX_CONTEXT_TOKENS=4000
ENV RATE_LIMIT_ENABLED=true
ENV RATE_LIMIT_REQUESTS=60
ENV RATE_LIMIT_WINDOW_SECONDS=60
ENV API_KEY_REQUIRED=false
ENV STRUCTURED_LOGGING=true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--log-level", "info"]

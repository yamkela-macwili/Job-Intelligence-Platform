FROM python:3.11-slim

WORKDIR /app

# Install system dependencies with retry logic
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip (with retries for network reliability)
RUN python -m pip install --upgrade --retries 5 --default-timeout=1000 pip setuptools wheel

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --retries 5 --default-timeout=1000 -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
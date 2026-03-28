#!/bin/bash
# Azure App Service Startup Script

# Set environment
export PYTHONUNBUFFERED=1

# Install dependencies
pip install -r requirements.txt

# Run migrations (if using Alembic)
# alembic upgrade head

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

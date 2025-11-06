#!/bin/bash
# Production startup script for Agent Zero (Aria)

echo "[STARTUP] Agent Zero (Aria) Production Deployment"
echo "[STARTUP] Environment: ${REPLIT_DEPLOYMENT_ID:-development}"
echo "[STARTUP] Port: ${PORT:-5000}"

# Run database migrations
echo "[STARTUP] Running database migrations..."
python scripts/migrate.py

# Get git commit hash if available
COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Start the application
echo "[STARTUP] Starting Agent Zero on port ${PORT:-5000} (commit: $COMMIT_HASH)"

# Use gunicorn for production if available, otherwise fallback to Flask
if command -v gunicorn &> /dev/null; then
    echo "[STARTUP] Using gunicorn (production server)"
    exec gunicorn run_ui:webapp \
        --bind "0.0.0.0:${PORT:-5000}" \
        --workers 1 \
        --threads 4 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile - \
        --log-level info
else
    echo "[STARTUP] Using Flask development server (gunicorn not available)"
    exec python run_ui.py --host=0.0.0.0 --port="${PORT:-5000}"
fi
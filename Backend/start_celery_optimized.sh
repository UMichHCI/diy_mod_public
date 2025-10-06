#!/bin/bash

# Optimized Celery Worker Startup Script
# This script starts Celery with gevent for high concurrency

echo "Starting optimized Celery worker with gevent..."
echo "Configuration:"
echo "  - Pool: gevent (async I/O)"
echo "  - Concurrency: 50 green threads"
echo "  - Memory limit: 1GB per worker"
echo "  - Prefetch: 1 (fair task distribution)"

# Activate virtual environment if it exists
if [ -d "diymod-venv" ]; then
    echo "Activating virtual environment..."
    source diymod-venv/bin/activate
fi

# Set environment variables for optimization
export CELERY_OPTIMIZATION=true
export GEVENT_RESOLVER=ares  # Faster DNS resolution

# Start Celery worker with optimized settings
celery -A tasks worker \
    --loglevel=info \
    --pool=gevent \
    --concurrency=50 \
    --max-memory-per-child=1048576 \
    --prefetch-multiplier=1 \
    --without-gossip \
    --without-mingle \
    --without-heartbeat

echo "Celery worker stopped."
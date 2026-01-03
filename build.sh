#!/usr/bin/env bash
# Build script for Render deployment - Optimized for $7 Standard Plan

set -o errexit
set -o pipefail

echo "[1/4] Installing dependencies (no-cache for speed)..."
pip install --no-cache-dir -r requirements.txt

echo "[2/4] Running database migrations..."
python manage.py migrate --no-input

echo "[3/4] Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "[4/4] Setup complete!"
echo "✓ Ready for deployment on Render!"

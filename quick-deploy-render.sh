#!/usr/bin/env bash
# Quick Deploy to Render Script
# Run this after setting up Render account

set -e

echo "🚀 TESLA INVESTMENT PLATFORM - RENDER DEPLOYMENT"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Not a git repository!"
    echo "Run: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

echo "✓ Git repository detected"
echo ""

# Make build script executable
echo "[1/5] Making build.sh executable..."
chmod +x build.sh
git add build.sh

# Commit changes
echo "[2/5] Committing changes..."
git commit -m "Optimize for Render \$7 Standard deployment" || true

# Push to main
echo "[3/5] Pushing to GitHub..."
echo "Run: git push origin main"
echo ""

echo "[4/5] Render Dashboard Steps:"
echo "1. Go to https://render.com"
echo "2. Click 'New +' → 'PostgreSQL'"
echo "   - Name: tesla-investment-db"
echo "   - Plan: Standard ($7)"
echo "3. Click 'New +' → 'Web Service'"
echo "   - Name: tesla-investment-platform"
echo "   - Repository: Your GitHub repo"
echo "   - Build Command: chmod +x build.sh && ./build.sh"
echo "   - Start Command: gunicorn config.wsgi:application --bind 0.0.0.0:\\\$PORT --workers 2 --worker-class sync --timeout 60"
echo "   - Plan: Standard ($7)"
echo ""

echo "[5/5] Environment Variables:"
echo "Copy from RENDER_ENV_TEMPLATE.md and add to Render Dashboard"
echo ""

echo "=================================================="
echo "After deployment completes (2-5 minutes):"
echo "1. Go to Render Dashboard → Your Web Service"
echo "2. Click 'Shell' and run:"
echo "   python manage.py createsuperuser"
echo ""
echo "Then visit: https://your-app-name.onrender.com"
echo "=================================================="

@echo off
REM Start Celery Beat for automatic hourly price updates

echo Starting Celery Beat scheduler...
echo This will update cryptocurrency prices and exchange rates every hour.
echo.

.venv\Scripts\python.exe -m celery -A config beat --loglevel=info

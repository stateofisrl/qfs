@echo off
REM Start Celery Worker to process tasks

echo Starting Celery Worker...
echo This processes the price update tasks scheduled by Beat.
echo.

.venv\Scripts\python.exe -m celery -A config worker --loglevel=info --pool=solo

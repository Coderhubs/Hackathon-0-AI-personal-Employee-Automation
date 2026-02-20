@echo off
echo ========================================
echo LinkedIn Scheduler - AI Personal Employee
echo ========================================
echo.
echo Options:
echo 1. Post Now (immediate)
echo 2. Run Scheduler (automated posting)
echo 3. Configure Schedule
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Posting approved LinkedIn posts now...
    python linkedin_scheduler_complete.py post-now
) else if "%choice%"=="2" (
    echo.
    echo Starting LinkedIn Scheduler...
    echo Posts will be published at scheduled times.
    echo Press Ctrl+C to stop.
    echo.
    python linkedin_scheduler_complete.py schedule
) else if "%choice%"=="3" (
    echo.
    python linkedin_scheduler_complete.py config
) else (
    echo Invalid choice!
)

echo.
pause

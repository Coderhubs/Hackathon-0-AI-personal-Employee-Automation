@echo off
echo ========================================
echo Starting Cloud Agent (Simulated 24/7)
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Docker not available - running in local simulation mode
    echo.
    echo Starting cloud agent in Python...
    python cloud_agent.py
) else (
    echo Starting cloud agent in Docker...
    docker-compose -f docker-compose-cloud.yml up -d

    if errorlevel 1 (
        echo [ERROR] Failed to start cloud containers
        pause
        exit /b 1
    )

    echo.
    echo [OK] Cloud agent started successfully
    echo.
    echo Cloud services running:
    docker-compose -f docker-compose-cloud.yml ps
    echo.
    echo To view logs: docker-compose -f docker-compose-cloud.yml logs -f
    echo To stop: docker-compose -f docker-compose-cloud.yml down
)

echo.
echo Cloud agent is now running 24/7
echo Monitoring Gmail and creating action files...
echo.
pause

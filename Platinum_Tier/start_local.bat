@echo off
echo ========================================
echo Starting Local Agent (On-Demand)
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Docker not available - running in local simulation mode
    echo.
    echo Starting local agent in Python...
    python local_agent.py
) else (
    echo Starting local agent in Docker...
    docker-compose -f docker-compose-local.yml up -d

    if errorlevel 1 (
        echo [ERROR] Failed to start local container
        pause
        exit /b 1
    )

    echo.
    echo [OK] Local agent started successfully
    echo.
    echo Local services running:
    docker-compose -f docker-compose-local.yml ps
    echo.
    echo To view logs: docker-compose -f docker-compose-local.yml logs -f
    echo To stop: docker-compose -f docker-compose-local.yml down
)

echo.
echo Local agent is now processing approved actions...
echo.
pause

@echo off
echo ========================================
echo 24/7 Master Orchestrator
echo Starting Continuous Automation System
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check .env file
if not exist ".env" (
    echo [WARNING] .env file not found
    echo Creating from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env file with your credentials
    echo Then run this script again
    pause
    exit /b 1
)

echo [OK] Environment configured
echo.

REM Install dependencies
echo Installing dependencies...
pip install python-dotenv >nul 2>&1

echo.
echo ========================================
echo Starting 24/7 Orchestrator
echo ========================================
echo.
echo This orchestrator will:
echo   - Check Gmail every 2 minutes
echo   - Monitor Approved folder every 10 seconds
echo   - Execute social media actions automatically
echo   - Run continuously until stopped (Ctrl+C)
echo.
echo Press Ctrl+C to stop the orchestrator
echo.
echo ========================================
echo.

REM Start orchestrator
python master_orchestrator_24_7.py

echo.
echo Orchestrator stopped
pause

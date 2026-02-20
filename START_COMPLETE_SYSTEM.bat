@echo off
REM AI Personal Employee - Complete System Startup Script
REM Launches all components in correct order

echo ================================================================================
echo AI PERSONAL EMPLOYEE - SYSTEM STARTUP
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 24+ LTS and try again
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found
    echo Please copy .env.example to .env and configure your credentials
    pause
    exit /b 1
)

echo [1/6] Checking environment...
echo   - Python: OK
echo   - Node.js: OK
echo   - .env file: OK
echo.

echo [2/6] Installing dependencies...
cd Platinum_Tier
pip install -q playwright python-dotenv watchdog 2>nul
python -m playwright install chromium 2>nul
cd ..
echo   - Dependencies: OK
echo.

echo [3/6] Generating initial LinkedIn posts...
python Platinum_Tier\linkedin_content_generator.py
echo.

echo [4/6] Starting watchers...
echo   Starting Gmail Watcher...
start "Gmail Watcher" cmd /k "cd Platinum_Tier && python gmail_watcher_playwright.py"
timeout /t 3 /nobreak >nul

echo   Starting LinkedIn Watcher...
start "LinkedIn Watcher" cmd /k "cd Platinum_Tier && python linkedin_watcher_playwright.py"
timeout /t 3 /nobreak >nul

echo   Starting WhatsApp Watcher...
start "WhatsApp Watcher" cmd /k "cd Platinum_Tier && python whatsapp_watcher_hackathon.py"
timeout /t 3 /nobreak >nul
echo.

echo [5/6] Starting integration coordinator...
if exist "integration_coordinator.py" (
    start "Integration Coordinator" cmd /k "python integration_coordinator.py"
    timeout /t 2 /nobreak >nul
    echo   - Integration Coordinator: STARTED
) else (
    echo   - Integration Coordinator: NOT FOUND (skipping)
)
echo.

echo [6/6] Starting approval handler...
start "Approval Handler" cmd /k "python approval_handler.py"
timeout /t 2 /nobreak >nul
echo   - Approval Handler: STARTED
echo.

echo ================================================================================
echo SYSTEM STARTUP COMPLETE
echo ================================================================================
echo.
echo All components are now running in separate windows.
echo.
echo FIRST-TIME SETUP:
echo   1. Gmail Watcher: Login manually in the browser window
echo   2. LinkedIn Watcher: Login manually in the browser window
echo   3. WhatsApp Watcher: Scan QR code in the browser window
echo.
echo After first-time login, sessions will persist automatically.
echo.
echo NEXT STEPS:
echo   1. Check Pending_Approval folder for generated LinkedIn posts
echo   2. Review and edit posts as needed
echo   3. Move approved posts to Approved folder
echo   4. Approval Handler will execute them automatically
echo.
echo To stop all components: Close all command windows or press Ctrl+C in each
echo.
echo ================================================================================
pause

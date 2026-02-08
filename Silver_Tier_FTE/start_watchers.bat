@echo off
REM Silver Tier AI Employee - Watcher Startup Script
REM This script starts all three watcher scripts for continuous monitoring

echo ========================================
echo Silver Tier AI Employee - Starting Watchers
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Starting Filesystem Watcher...
start "Filesystem Watcher" python filesystem_watcher.py
timeout /t 2 /nobreak >nul

echo Starting Gmail Watcher...
start "Gmail Watcher" python gmail_watcher.py
timeout /t 2 /nobreak >nul

echo Starting LinkedIn Watcher...
start "LinkedIn Watcher" python linkedin_watcher.py
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All watchers started successfully!
echo ========================================
echo.
echo Three console windows should now be open:
echo   1. Filesystem Watcher (monitors Inbox folder)
echo   2. Gmail Watcher (simulates email monitoring)
echo   3. LinkedIn Watcher (simulates social media monitoring)
echo.
echo To stop watchers: Close each console window or press Ctrl+C
echo.
echo Dashboard: Dashboard.md
echo Pending Approvals: Pending_Approval folder
echo.
pause

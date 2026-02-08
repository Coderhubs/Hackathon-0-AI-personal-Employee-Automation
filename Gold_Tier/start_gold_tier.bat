@echo off
REM Gold Tier Autonomous System Startup Script
REM Launches all watchers and autonomous monitor

echo ========================================
echo Gold Tier Autonomous System
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Gold Tier components...
echo.

REM Start Gmail Watcher
echo [1/4] Starting Gmail Watcher...
start "Gmail Watcher" python gmail_watcher.py
timeout /t 2 /nobreak >nul

REM Start LinkedIn Watcher
echo [2/4] Starting LinkedIn Watcher...
start "LinkedIn Watcher" python linkedin_watcher.py
timeout /t 2 /nobreak >nul

REM Start Filesystem Watcher
echo [3/4] Starting Filesystem Watcher...
start "Filesystem Watcher" python filesystem_watcher.py
timeout /t 2 /nobreak >nul

REM Start Autonomous Monitor (Ralph Wiggum Loop)
echo [4/4] Starting Autonomous Monitor...
start "Autonomous Monitor" python autonomous_monitor.py
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All components started successfully!
echo ========================================
echo.
echo Running processes:
echo - Gmail Watcher (monitors Gmail, creates files every 3 min)
echo - LinkedIn Watcher (monitors LinkedIn, creates files every 2 min)
echo - Filesystem Watcher (monitors Inbox folder)
echo - Autonomous Monitor (Ralph Wiggum Loop - never stops)
echo.
echo Check Gold_Tier/Logs/ for detailed logs
echo.
echo Press any key to view system status...
pause >nul

REM Show Dashboard
type Dashboard.md

echo.
echo System is running. Close individual windows to stop components.
echo.
pause

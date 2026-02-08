@echo off
REM Silver Tier - Multi-Source Monitoring + HITL
echo =========================================
echo SILVER TIER - MULTI-SOURCE MONITORING
echo Features: Gmail + LinkedIn + Filesystem + HITL
echo =========================================
echo.
echo Starting 3 watchers in separate windows...
echo.

REM Start Filesystem Watcher
start "Silver Tier - Filesystem Watcher" cmd /k "cd /d %~dp0 && echo [FILESYSTEM WATCHER] Starting... && python Silver_Tier_FTE\filesystem_watcher.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Gmail Watcher
start "Silver Tier - Gmail Watcher" cmd /k "cd /d %~dp0 && echo [GMAIL WATCHER] Starting... && python Silver_Tier_FTE\gmail_watcher.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start LinkedIn Watcher
start "Silver Tier - LinkedIn Watcher" cmd /k "cd /d %~dp0 && echo [LINKEDIN WATCHER] Starting... && python Silver_Tier_FTE\linkedin_watcher.py"

echo.
echo ✓ All 3 watchers started in separate windows
echo.
echo To stop: Close each window or press Ctrl+C in each
echo.
pause

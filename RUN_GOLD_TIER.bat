@echo off
REM Gold Tier - Autonomous System + Plugin Architecture
echo =========================================
echo GOLD TIER - AUTONOMOUS SYSTEM
echo Features: Ralph Wiggum Loop + Plugins + CEO Briefing
echo =========================================
echo.
echo Starting autonomous monitor and plugin watchers...
echo.

REM Start Autonomous Monitor (Ralph Wiggum Loop)
start "Gold Tier - Autonomous Monitor" cmd /k "cd /d %~dp0 && echo [AUTONOMOUS MONITOR] Starting Ralph Wiggum Loop... && python Gold_Tier\autonomous_monitor.py"

REM Wait 3 seconds
timeout /t 3 /nobreak >nul

REM Start Gmail Watcher Plugin
start "Gold Tier - Gmail Watcher" cmd /k "cd /d %~dp0 && echo [GMAIL WATCHER PLUGIN] Starting... && python Gold_Tier\gmail_watcher.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start LinkedIn Watcher Plugin
start "Gold Tier - LinkedIn Watcher" cmd /k "cd /d %~dp0 && echo [LINKEDIN WATCHER PLUGIN] Starting... && python Gold_Tier\linkedin_watcher.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Filesystem Watcher Plugin
start "Gold Tier - Filesystem Watcher" cmd /k "cd /d %~dp0 && echo [FILESYSTEM WATCHER PLUGIN] Starting... && python Gold_Tier\filesystem_watcher.py"

echo.
echo ✓ Gold Tier system started with 4 components:
echo   1. Autonomous Monitor (Ralph Wiggum Loop)
echo   2. Gmail Watcher Plugin
echo   3. LinkedIn Watcher Plugin
echo   4. Filesystem Watcher Plugin
echo.
echo The autonomous monitor will continuously process tasks until complete.
echo.
echo To generate CEO briefing: python Gold_Tier\ceo_briefing_generator.py
echo.
echo To stop: Close each window or press Ctrl+C in each
echo.
pause

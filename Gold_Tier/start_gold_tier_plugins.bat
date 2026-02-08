@echo off
REM Gold Tier Autonomous System Startup Script (Plugin-Based)
REM Dynamically launches all enabled watchers and autonomous monitor

echo ========================================
echo Gold Tier Autonomous System (Plugin-Based)
echo ========================================
echo.

cd /d "%~dp0"

echo Discovering and starting plugins...
echo.

REM Start Plugin Manager to launch all enabled watchers
echo Starting Plugin Manager...
python plugin_manager.py start
timeout /t 2 /nobreak >nul

REM Start Autonomous Monitor (Ralph Wiggum Loop)
echo Starting Autonomous Monitor...
start "Autonomous Monitor" python autonomous_monitor.py
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All components started successfully!
echo ========================================
echo.
echo Running processes:
echo - All enabled watchers (see Config/watchers_config.json)
echo - Autonomous Monitor (Ralph Wiggum Loop - never stops)
echo.
echo Check Gold_Tier/Logs/ for detailed logs
echo.
echo To add new watchers:
echo 1. Create {name}_watcher.py using watcher_template.py
echo 2. Restart system (auto-discovery enabled)
echo.
echo To list all plugins:
echo   python plugin_manager.py list
echo.
echo Press any key to view system status...
pause >nul

REM Show Dashboard
type Dashboard.md

echo.
echo System is running. Close individual windows to stop components.
echo.
pause

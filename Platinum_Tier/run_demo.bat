@echo off
echo ========================================
echo Platinum Tier Demo
echo Offline/Online Handoff Demonstration
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

echo Running Platinum Tier demo...
echo.

python demo_platinum.py

echo.
echo Demo complete!
echo.
pause

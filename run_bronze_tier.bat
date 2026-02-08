@echo off
REM Bronze Tier - Terminal Output Demo
REM Shows Perception → Reasoning → Action workflow

echo =========================================
echo BRONZE TIER - PERSONAL AI EMPLOYEE
echo Architecture: Perception → Reasoning → Action
echo =========================================
echo.

echo [PERCEPTION LAYER] Starting Filesystem Watcher...
echo ^|-- Monitoring: AI_Employee_Vault\Inbox
echo ^|-- Check Interval: Real-time (watchdog)
echo ^`-- Status: Active
echo.

echo [SYSTEM] Waiting for files in Inbox...
echo.

REM Start the watcher
cd /d "%~dp0"
python AI_Employee_Vault\filesystem_watcher.py

@echo off
REM Bronze Tier - Continuous Execution
echo =========================================
echo BRONZE TIER - CONTINUOUS EXECUTION
echo Architecture: Perception to Reasoning to Action
echo =========================================
echo.
echo [STARTING] Filesystem Watcher...
echo Monitoring: AI_Employee_Vault\Inbox
echo Press Ctrl+C to stop
echo.
python AI_Employee_Vault\filesystem_watcher.py
pause

@echo off
echo ========================================
echo AI Personal Employee - Task Scheduler Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.13 or higher
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Check if running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Not running as administrator
    echo Some tasks may require administrator privileges
    echo.
)

REM Get current directory
set "CURRENT_DIR=%CD%"
echo Working directory: %CURRENT_DIR%
echo.

echo ========================================
echo Registering Task Scheduler Tasks
echo ========================================
echo.

REM Register orchestrator task
echo [1/2] Registering Orchestrator Task (runs every 5 minutes)...
schtasks /create /tn "AI_Employee_Orchestrator" /xml "%CURRENT_DIR%\tasks\orchestrator_task.xml" /f
if errorlevel 1 (
    echo [ERROR] Failed to register orchestrator task
    pause
    exit /b 1
)
echo [OK] Orchestrator task registered
echo.

REM Register scheduler task
echo [2/2] Registering Scheduler Task (runs on startup)...
schtasks /create /tn "AI_Employee_Scheduler" /xml "%CURRENT_DIR%\tasks\scheduler_task.xml" /f
if errorlevel 1 (
    echo [ERROR] Failed to register scheduler task
    pause
    exit /b 1
)
echo [OK] Scheduler task registered
echo.

echo ========================================
echo Verification
echo ========================================
echo.

REM Query tasks to verify
echo Checking registered tasks...
schtasks /query /tn "AI_Employee_Orchestrator" /fo LIST
echo.
schtasks /query /tn "AI_Employee_Scheduler" /fo LIST
echo.

echo ========================================
echo Testing Task Execution
echo ========================================
echo.

REM Test orchestrator task
echo Testing orchestrator task (this may take a few seconds)...
schtasks /run /tn "AI_Employee_Orchestrator"
timeout /t 3 /nobreak >nul
echo.

REM Check if log file was created
if exist "Gold_Tier\Logs\orchestrator.log" (
    echo [OK] Orchestrator executed successfully
    echo Last 5 lines of log:
    powershell -Command "Get-Content 'Gold_Tier\Logs\orchestrator.log' -Tail 5"
) else (
    echo [WARNING] Log file not found - orchestrator may not have run
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Silver Tier OS Scheduling: COMPLETE
echo.
echo Tasks registered:
echo   - AI_Employee_Orchestrator (every 5 minutes)
echo   - AI_Employee_Scheduler (on startup)
echo.
echo To manage tasks:
echo   - Open Task Scheduler: taskschd.msc
echo   - View logs: Gold_Tier\Logs\orchestrator.log
echo   - Disable task: schtasks /change /tn "AI_Employee_Orchestrator" /disable
echo   - Enable task: schtasks /change /tn "AI_Employee_Orchestrator" /enable
echo   - Delete task: schtasks /delete /tn "AI_Employee_Orchestrator" /f
echo.
echo Next steps:
echo   1. Wait 5 minutes and check if orchestrator runs automatically
echo   2. Restart computer to test scheduler startup task
echo   3. Monitor logs in Gold_Tier\Logs\
echo.
pause

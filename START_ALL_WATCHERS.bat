@echo off
echo ============================================================
echo AI Personal Employee - Hackathon Edition
echo ============================================================
echo.
echo This will start all watchers and the orchestrator
echo.
echo Watchers:
echo - Gmail Watcher (monitors inbox for Agentic AI emails)
echo - LinkedIn Watcher (monitors feed for Agentic AI posts)
echo - WhatsApp Watcher (monitors messages for urgent/AI content)
echo.
echo All watchers write to: AI_Employee_Vault/Needs_Action/
echo.
echo Press any key to start or Ctrl+C to cancel...
pause >nul

echo.
echo Starting orchestrator...
echo.

cd /d "%~dp0"
python orchestrator.py

echo.
echo Orchestrator stopped.
echo.
pause

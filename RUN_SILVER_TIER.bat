@echo off
REM Silver Tier - Multi-Source Monitoring + HITL + Scheduling + MCP
echo =========================================
echo SILVER TIER - COMPLETE IMPLEMENTATION
echo Features: 3 Watchers + HITL + Scheduler + Email MCP
echo =========================================
echo.
echo Starting 5 components in separate windows...
echo.

REM Start Gmail Watcher (Bronze Tier)
start "Silver - Gmail Watcher" cmd /k "cd /d %~dp0 && echo [GMAIL WATCHER] Starting... && python Platinum_Tier\gmail_watcher_hackathon.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start LinkedIn Watcher (Bronze Tier)
start "Silver - LinkedIn Watcher" cmd /k "cd /d %~dp0 && echo [LINKEDIN WATCHER] Starting... && python Platinum_Tier\linkedin_watcher_hackathon.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start WhatsApp Watcher (Bronze Tier)
start "Silver - WhatsApp Watcher" cmd /k "cd /d %~dp0 && echo [WHATSAPP WATCHER] Starting... && python Platinum_Tier\whatsapp_watcher_hackathon.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start HITL Approval Handler (Silver Tier)
start "Silver - HITL Handler" cmd /k "cd /d %~dp0 && echo [HITL APPROVAL HANDLER] Starting... && python approval_handler.py"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Scheduler (Silver Tier)
start "Silver - Scheduler" cmd /k "cd /d %~dp0 && echo [SCHEDULER] Starting... && python scheduler.py"

echo.
echo ✓ All 5 components started in separate windows:
echo   1. Gmail Watcher (Bronze)
echo   2. LinkedIn Watcher (Bronze)
echo   3. WhatsApp Watcher (Bronze)
echo   4. HITL Approval Handler (Silver)
echo   5. Scheduler (Silver)
echo.
echo Email MCP Server: Configure in Claude Code mcp.json
echo.
echo To stop: Close each window or press Ctrl+C in each
echo.
pause

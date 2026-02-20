@echo off
REM Platinum Tier - Enterprise AI Employee System
REM Complete 4-tier progression with multi-agent coordination

echo =========================================
echo PLATINUM TIER - ENTERPRISE AI EMPLOYEE
echo Features: Multi-Agent + Memory + REST API
echo =========================================
echo.
echo Starting 8 components in separate windows...
echo.

REM Start Silver Tier Watchers (Foundation)
echo [1/8] Starting Gmail Watcher...
start "Platinum - Gmail Watcher" cmd /k "cd /d %~dp0 && echo [GMAIL WATCHER] Starting... && python Platinum_Tier\gmail_watcher_hackathon.py"
timeout /t 2 /nobreak >nul

echo [2/8] Starting LinkedIn Watcher...
start "Platinum - LinkedIn Watcher" cmd /k "cd /d %~dp0 && echo [LINKEDIN WATCHER] Starting... && python Platinum_Tier\linkedin_watcher_hackathon.py"
timeout /t 2 /nobreak >nul

echo [3/8] Starting WhatsApp Watcher...
start "Platinum - WhatsApp Watcher" cmd /k "cd /d %~dp0 && echo [WHATSAPP WATCHER] Starting... && python Platinum_Tier\whatsapp_watcher_hackathon.py"
timeout /t 2 /nobreak >nul

REM Start Silver Tier HITL
echo [4/8] Starting HITL Approval Handler...
start "Platinum - HITL Handler" cmd /k "cd /d %~dp0 && echo [HITL APPROVAL HANDLER] Starting... && python approval_handler.py"
timeout /t 2 /nobreak >nul

REM Start Gold Tier Intelligence
echo [5/8] Starting Autonomous Monitor (Ralph Wiggum Loop)...
start "Platinum - Autonomous Monitor" cmd /k "cd /d %~dp0 && echo [AUTONOMOUS MONITOR] Starting... && python Gold_Tier\autonomous_monitor.py"
timeout /t 2 /nobreak >nul

echo [6/8] Starting CEO Briefing Generator...
start "Platinum - CEO Briefing" cmd /k "cd /d %~dp0 && echo [CEO BRIEFING] Generating reports... && python Gold_Tier\ceo_briefing_generator.py"
timeout /t 2 /nobreak >nul

REM Start Platinum Tier Components
echo [7/8] Starting Multi-Agent Coordinator...
start "Platinum - Multi-Agent" cmd /k "cd /d %~dp0 && echo [MULTI-AGENT COORDINATOR] Starting... && python Platinum_Tier\agent_coordinator.py"
timeout /t 2 /nobreak >nul

echo [8/8] Starting REST API Server...
start "Platinum - REST API" cmd /k "cd /d %~dp0 && echo [REST API SERVER] Starting on http://localhost:8000... && python Platinum_Tier\api_server_complete.py"
timeout /t 2 /nobreak >nul

echo.
echo ✓ All 8 components started in separate windows:
echo.
echo   BRONZE/SILVER TIER FOUNDATION:
echo   1. Gmail Watcher (monitors Gmail)
echo   2. LinkedIn Watcher (monitors LinkedIn)
echo   3. WhatsApp Watcher (monitors WhatsApp)
echo   4. HITL Approval Handler (human approval workflow)
echo.
echo   GOLD TIER INTELLIGENCE:
echo   5. Autonomous Monitor (Ralph Wiggum Loop)
echo   6. CEO Briefing Generator (weekly reports)
echo.
echo   PLATINUM TIER ENTERPRISE:
echo   7. Multi-Agent Coordinator (5 specialized agents)
echo   8. REST API Server (http://localhost:8000)
echo.
echo Additional Features:
echo   - Memory Store (long-term conversation history)
echo   - Vector Database (RAG with ChromaDB)
echo   - Webhook Support (external integrations)
echo   - Agent Specialization (researcher, executor, monitor, planner, reviewer)
echo.
echo API Documentation: http://localhost:8000/docs
echo API Health Check: http://localhost:8000/health
echo.
echo Vault Location: AI_Employee_Vault/
echo Logs: Platinum_Tier/Logs/
echo Memory: Platinum_Tier/Memory/
echo.
echo To stop: Close each window or press Ctrl+C in each
echo.
pause

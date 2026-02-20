@echo off
echo ============================================================
echo AI Personal Employee - Demo Mode
echo ============================================================
echo.
echo This will demonstrate the complete system:
echo 1. Gmail Watcher (Agentic AI filtering)
echo 2. LinkedIn Watcher (Agentic AI filtering)
echo 3. WhatsApp Watcher (Urgent + Agentic AI filtering)
echo.
echo All watchers write to: AI_Employee_Vault/Needs_Action/
echo.
echo IMPORTANT: 
echo - Gmail: fateehaaayat@gmail.com
echo - LinkedIn: simramumbai@gmail.com
echo - WhatsApp: Scan QR code once
echo.
echo Press any key to start demo...
pause >nul

echo.
echo [1/3] Starting Gmail Watcher...
start "Gmail Watcher - Demo" cmd /k "cd /d %~dp0Platinum_Tier && python gmail_watcher_hackathon.py"
timeout /t 3 >nul

echo [2/3] Starting LinkedIn Watcher...
start "LinkedIn Watcher - Demo" cmd /k "cd /d %~dp0Platinum_Tier && python linkedin_watcher_hackathon.py"
timeout /t 3 >nul

echo [3/3] Starting WhatsApp Watcher...
start "WhatsApp Watcher - Demo" cmd /k "cd /d %~dp0Platinum_Tier && python whatsapp_watcher_hackathon.py"

echo.
echo ============================================================
echo All watchers started!
echo ============================================================
echo.
echo Check AI_Employee_Vault/Needs_Action/ for new files
echo.
echo To process with Claude Code:
echo   cd AI_Employee_Vault
echo   claude /process-inbox
echo   claude /update-dashboard
echo.
echo To stop: Close the watcher windows or press Ctrl+C
echo.
pause

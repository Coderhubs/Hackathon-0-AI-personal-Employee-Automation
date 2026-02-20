@echo off
echo ========================================
echo AI PERSONAL EMPLOYEE - COMPLETE SYSTEM
echo ========================================
echo.
echo Starting all automation components:
echo   1. Gmail Watcher (monitors inbox)
echo   2. Gmail Sender (sends approved emails)
echo   3. WhatsApp Auto-Reply Bot
echo.
echo Press Ctrl+C in any window to stop that component
echo.
pause
echo.

REM Start Gmail Watcher
echo [1/3] Starting Gmail Watcher...
start "Gmail Watcher" cmd /k "title Gmail Watcher - Monitoring Inbox && cd Platinum_Tier && python gmail_watcher_imap.py"
timeout /t 2 /nobreak >nul

REM Start Gmail Sender
echo [2/3] Starting Gmail Sender...
start "Gmail Sender" cmd /k "title Gmail Sender - Auto Send Approved && cd Platinum_Tier && python gmail_approval_handler.py"
timeout /t 2 /nobreak >nul

REM Start WhatsApp Auto-Reply
echo [3/3] Starting WhatsApp Auto-Reply Bot...
start "WhatsApp Bot" cmd /k "title WhatsApp Auto-Reply Bot && python whatsapp_autoreply.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo ALL SYSTEMS RUNNING
echo ========================================
echo.
echo ACTIVE COMPONENTS:
echo   - Gmail Watcher: Checks inbox every 3 minutes
echo   - Gmail Sender: Watches Approved folder
echo   - WhatsApp Bot: Auto-replies to messages
echo.
echo IMPORTANT FOR WHATSAPP:
echo   1. Run: ngrok http 5000
echo   2. Set webhook in Twilio Console
echo   3. Then WhatsApp will work automatically
echo.
echo WORKFLOW:
echo   1. System detects emails/WhatsApp messages
echo   2. Saves to: AI_Employee_Vault/Needs_Action/
echo   3. You create replies in: AI_Employee_Vault/Approved/
echo   4. System automatically sends them
echo   5. Logs everything to: AI_Employee_Vault/Done/
echo.
echo TO STOP: Close all command windows
echo.
echo ========================================
pause

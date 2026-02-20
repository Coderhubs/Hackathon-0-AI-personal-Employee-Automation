@echo off
echo ========================================
echo Gmail Complete System
echo READ + SEND Automation
echo ========================================
echo.
echo Starting both components:
echo   1. Gmail Watcher (IMAP) - Monitors inbox
echo   2. Gmail Sender (SMTP) - Sends approved emails
echo.
pause
echo.

REM Start Gmail Watcher
echo [1/2] Starting Gmail Watcher (monitors inbox)...
start "Gmail Watcher" cmd /k "cd Platinum_Tier && python gmail_watcher_imap.py"
timeout /t 2 /nobreak >nul

REM Start Gmail Sender (approval handler)
echo [2/2] Starting Gmail Sender (sends approved emails)...
start "Gmail Sender" cmd /k "cd Platinum_Tier && python gmail_approval_handler.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo GMAIL AUTOMATION RUNNING
echo ========================================
echo.
echo WHAT'S RUNNING:
echo   - Gmail Watcher: Monitors inbox every 3 minutes
echo   - Gmail Sender: Watches Approved folder and sends emails
echo.
echo WORKFLOW:
echo   1. Watcher detects email with AI keywords
echo   2. Saves to: AI_Employee_Vault/Needs_Action/
echo   3. You create reply in: AI_Employee_Vault/Approved/
echo   4. Sender automatically sends the email
echo   5. Moves to: AI_Employee_Vault/Done/
echo.
echo TO STOP: Close both command windows or press Ctrl+C
echo.
pause

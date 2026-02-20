@echo off
chcp 65001 >nul
echo ============================================================
echo GMAIL WATCHER - START MONITORING INBOX
echo ============================================================
echo.
echo This will start monitoring your Gmail inbox for new emails.
echo.
echo Features:
echo - Checks inbox every 3 minutes
echo - Detects emails with "Agentic AI" keywords
echo - Saves to AI_Employee_Vault\Needs_Action\
echo - Fully automated (NO browser, NO manual login)
echo.
echo Press Ctrl+C to stop monitoring.
echo.
pause

cd Platinum_Tier
python gmail_watcher_imap.py

pause

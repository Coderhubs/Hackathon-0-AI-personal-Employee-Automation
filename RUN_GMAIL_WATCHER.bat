@echo off
echo ========================================
echo Starting Gmail Watcher (IMAP - Fully Automated)
echo ========================================
echo.
echo This watcher will:
echo - Monitor Gmail for new emails every 3 minutes
echo - Filter for Agentic AI related content
echo - Save detected emails to AI_Employee_Vault/Needs_Action/
echo - Run 24/7 without manual intervention
echo.
echo Press Ctrl+C to stop the watcher
echo.
pause
echo.
cd "%~dp0Platinum_Tier"
python gmail_watcher_imap.py

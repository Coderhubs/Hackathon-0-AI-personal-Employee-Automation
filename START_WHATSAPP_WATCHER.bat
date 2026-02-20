@echo off
chcp 65001 >nul
echo ============================================================
echo WHATSAPP WATCHER - START MONITORING MESSAGES
echo ============================================================
echo.
echo This will start monitoring WhatsApp for incoming messages.
echo.
echo Features:
echo - Monitors WhatsApp Web
echo - Detects messages with keywords
echo - Saves to AI_Employee_Vault\Needs_Action\
echo - Auto-reply capability
echo.
echo Press Ctrl+C to stop monitoring.
echo.
pause

python Platinum_Tier\whatsapp_watcher_hackathon.py

pause

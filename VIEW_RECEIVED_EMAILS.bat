@echo off
chcp 65001 >nul
echo ============================================================
echo VIEW RECEIVED EMAILS
echo ============================================================
echo.
echo Showing all emails detected by Gmail watcher:
echo.

dir /b AI_Employee_Vault\Needs_Action\EMAIL_*.md

echo.
echo ============================================================
echo.
echo To view a specific email, use:
echo type AI_Employee_Vault\Needs_Action\EMAIL_filename.md
echo.
pause

@echo off
chcp 65001 >nul
echo ============================================================
echo GMAIL AUTOMATION TEST
echo ============================================================
echo.
echo Testing Gmail sending capability...
echo.

python test_gmail_manual.py

echo.
echo ============================================================
echo TEST COMPLETE
echo ============================================================
echo.
echo Check your email inbox for the test message.
echo.
pause

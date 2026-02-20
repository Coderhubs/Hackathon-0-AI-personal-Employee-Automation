@echo off
chcp 65001 >nul
echo ============================================================
echo GMAIL SEND AND RECEIVE - COMPLETE WORKFLOW TEST
echo ============================================================
echo.
echo This will test the complete Gmail workflow:
echo 1. Send a test email
echo 2. Start monitoring inbox
echo 3. Detect the sent email
echo.
echo ============================================================
echo STEP 1: SENDING TEST EMAIL
echo ============================================================
echo.

python test_gmail_manual.py

echo.
echo ============================================================
echo STEP 2: STARTING GMAIL WATCHER
echo ============================================================
echo.
echo The watcher will now monitor your inbox.
echo It should detect the test email we just sent.
echo.
echo Press Ctrl+C to stop monitoring after you see the email detected.
echo.
pause

cd Platinum_Tier
python gmail_watcher_imap.py

pause

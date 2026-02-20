@echo off
echo ================================================================================
echo WHATSAPP AUTOMATION - TWILIO EDITION
echo ================================================================================
echo.
echo This will start:
echo   1. Flask webhook server (receives messages from Twilio)
echo   2. ngrok tunnel (exposes server to internet)
echo.
echo After starting, you'll get a public URL to configure in Twilio Console
echo.
pause

REM Check if .whatsapp_config exists
if not exist .whatsapp_config (
    echo [ERROR] .whatsapp_config not found
    echo Please make sure your Twilio credentials are configured
    pause
    exit /b 1
)

echo.
echo [1/2] Starting Flask webhook server...
echo.
start "WhatsApp Webhook Server" cmd /k "python whatsapp_autoreply.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting ngrok tunnel...
echo.
start "ngrok Tunnel" cmd /k "ngrok http 5000"
timeout /t 5 /nobreak >nul

echo.
echo ================================================================================
echo SETUP COMPLETE - NEXT STEPS
echo ================================================================================
echo.
echo 1. Look at the "ngrok Tunnel" window
echo 2. Find the line that says "Forwarding" with a URL like:
echo    https://xxxx-xx-xxx-xxx-xxx.ngrok-free.app
echo.
echo 3. Copy that HTTPS URL
echo.
echo 4. Go to Twilio Console:
echo    https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
echo.
echo 5. In "When a message comes in" field, paste:
echo    YOUR_NGROK_URL/whatsapp
echo    Example: https://xxxx.ngrok-free.app/whatsapp
echo.
echo 6. Click Save
echo.
echo 7. Send a test message to your Twilio WhatsApp number:
echo    +14155238886
echo.
echo 8. You should get an auto-reply within seconds!
echo.
echo ================================================================================
echo SYSTEM IS NOW RUNNING
echo ================================================================================
echo.
echo To stop: Close both command windows
echo.
pause

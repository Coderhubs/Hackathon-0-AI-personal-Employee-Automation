@echo off
chcp 65001 >nul
echo ============================================================
echo WHATSAPP AUTOMATION TEST
echo ============================================================
echo.
echo Testing WhatsApp sending capability...
echo.

python test_whatsapp_send.py

echo.
echo ============================================================
echo TEST COMPLETE
echo ============================================================
echo.
echo Check WhatsApp_Vault\Sent\ for sent message logs.
echo.
pause

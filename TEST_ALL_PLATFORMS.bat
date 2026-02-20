@echo off
chcp 65001 >nul
echo ============================================================
echo AI PERSONAL EMPLOYEE - COMPLETE SYSTEM TEST
echo ============================================================
echo.
echo This will test all automation platforms:
echo - Gmail
echo - LinkedIn (safety check only)
echo - WhatsApp
echo - Vault structure
echo.
pause

python quick_test.py

echo.
echo ============================================================
echo ALL TESTS COMPLETE
echo ============================================================
echo.
echo Review the results above to see which platforms are working.
echo.
echo Next steps:
echo - If Gmail passed: Ready to use
echo - If LinkedIn shows GREEN: Run TEST_LINKEDIN_POST.bat
echo - If WhatsApp passed: Ready to use
echo.
pause

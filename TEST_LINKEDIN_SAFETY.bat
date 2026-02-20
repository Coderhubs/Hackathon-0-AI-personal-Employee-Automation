@echo off
chcp 65001 >nul
echo ============================================================
echo LINKEDIN SAFETY CHECK
echo ============================================================
echo.
echo Checking if it's safe to post to LinkedIn...
echo.

python linkedin_safety_check.py

echo.
echo ============================================================
echo.
if %ERRORLEVEL% EQU 0 (
    echo Status: GREEN - Safe to post
    echo.
    echo You can now run: TEST_LINKEDIN_POST.bat
) else if %ERRORLEVEL% EQU 1 (
    echo Status: YELLOW - Caution required
    echo.
    echo You can post but it's not optimal.
) else (
    echo Status: RED - DO NOT POST
    echo.
    echo Wait for the next safe posting window shown above.
)
echo.
pause

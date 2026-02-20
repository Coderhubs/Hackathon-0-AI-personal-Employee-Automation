@echo off
echo ================================================================================
echo LinkedIn Manual Login - Simple Method
echo ================================================================================
echo.
echo This will open Chrome with your LinkedIn automation profile.
echo.
echo STEPS:
echo 1. Chrome will open automatically
echo 2. Go to linkedin.com and login
echo 3. Complete any verification (email code, SMS, etc.)
echo 4. Once you see your LinkedIn feed, close Chrome
echo 5. Your session will be saved automatically
echo.
echo ================================================================================
echo.
pause

echo Opening Chrome with LinkedIn profile...
echo.

start chrome --user-data-dir="%~dp0browser_data\linkedin" --no-first-run --no-default-browser-check https://www.linkedin.com/login

echo.
echo ================================================================================
echo Chrome is now open!
echo ================================================================================
echo.
echo COMPLETE THESE STEPS IN CHROME:
echo 1. Login to LinkedIn
echo 2. Complete any verification
echo 3. Wait until you see your feed
echo 4. Close Chrome
echo.
echo After closing Chrome, run: RUN_LINKEDIN_POST.bat
echo ================================================================================
echo.
pause

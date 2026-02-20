@echo off
echo Opening LinkedIn for manual login...
echo.
echo STEPS:
echo 1. Login to LinkedIn in the browser that opens
echo 2. Complete any verification
echo 3. Wait until you see your feed
echo 4. Keep browser open
echo 5. Press Enter here when you see your feed
echo.

start chrome --user-data-dir="%~dp0browser_data\linkedin" https://www.linkedin.com/feed

echo.
echo Waiting for you to login...
pause

echo.
echo Testing post now...
python linkedin_scheduler_complete.py post-now

pause

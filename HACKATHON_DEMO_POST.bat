@echo off
echo ================================================================================
echo LinkedIn Hackathon Demo - Quick Post
echo ================================================================================
echo.
echo This is the EASIEST way to post for your hackathon demo!
echo.
echo STEPS:
echo 1. Open Chrome and login to your dummy LinkedIn account
echo 2. Keep Chrome open
echo 3. Press Enter here
echo 4. Script will post automatically
echo.
echo ================================================================================
echo.
echo Step 1: Opening Chrome for you...
start chrome https://www.linkedin.com/feed
echo.
echo Step 2: Login to your dummy LinkedIn account in Chrome
echo Step 3: Once logged in, come back here and press Enter
echo.
pause

echo.
echo Posting now...
python linkedin_demo_poster.py

echo.
echo ================================================================================
echo Done!
echo ================================================================================
pause

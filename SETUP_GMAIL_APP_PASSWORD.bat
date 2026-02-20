@echo off
echo ========================================
echo Gmail App Password Setup Guide
echo ========================================
echo.
echo STEP 1: Enable 2-Step Verification
echo --------------------------------
echo 1. Go to: https://myaccount.google.com/security
echo 2. Find "2-Step Verification" and turn it ON
echo 3. Follow the prompts to set it up
echo.
echo Press any key when 2-Step Verification is enabled...
pause >nul
echo.
echo STEP 2: Generate App Password
echo --------------------------------
echo 1. Go to: https://myaccount.google.com/apppasswords
echo 2. Sign in if prompted
echo 3. Select "Mail" as the app
echo 4. Select "Windows Computer" as the device
echo 5. Click "Generate"
echo 6. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)
echo.
echo Press any key when you have copied the App Password...
pause >nul
echo.
echo STEP 3: Update .env File
echo --------------------------------
echo 1. Open the .env file in this folder
echo 2. Find the line: GMAIL_PASSWORD=fateeh@127
echo 3. Replace it with: GMAIL_PASSWORD=your_app_password_here
echo 4. Remove spaces from the app password (make it one continuous string)
echo 5. Save the file
echo.
echo Example:
echo   If App Password is: abcd efgh ijkl mnop
echo   Enter it as: GMAIL_PASSWORD=abcdefghijklmnop
echo.
echo Press any key when you have updated the .env file...
pause >nul
echo.
echo STEP 4: Test the Setup
echo --------------------------------
echo Now we'll test if the Gmail watcher can connect...
echo.
pause
echo.
echo Running test...
cd "%~dp0Platinum_Tier"
python gmail_watcher_imap.py

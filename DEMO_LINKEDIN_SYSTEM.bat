@echo off
chcp 65001 >nul
echo ========================================
echo LinkedIn Automation - Complete Demo
echo ========================================
echo.
echo This demo will:
echo 1. Generate a test LinkedIn post
echo 2. Show you how to approve it
echo 3. Post it to LinkedIn
echo.
pause

echo.
echo ========================================
echo Step 1: Generating Test Post
echo ========================================
echo.
python linkedin_content_generator.py <<EOF
1
EOF

echo.
echo ========================================
echo Step 2: Review Generated Post
echo ========================================
echo.
echo Opening Pending_Approval folder...
start "" "AI_Employee_Vault\Pending_Approval"
echo.
echo Please:
echo 1. Review the generated post
echo 2. Edit if needed
echo 3. Move the file to Approved folder
echo.
pause

echo.
echo ========================================
echo Step 3: Post to LinkedIn
echo ========================================
echo.
echo This will post the approved content to LinkedIn.
echo The browser will:
echo - Open LinkedIn with your saved session
echo - Create the post
echo - Upload any images
echo - Wait 13-28 seconds for complete upload
echo - Close after verification
echo.
set /p confirm="Ready to post? (y/n): "

if /i "%confirm%"=="y" (
    echo.
    echo Posting to LinkedIn...
    python linkedin_scheduler_complete.py post-now

    echo.
    echo ========================================
    echo Demo Complete!
    echo ========================================
    echo.
    echo Check your LinkedIn profile to see the post.
    echo.
    echo Logs saved to: AI_Employee_Vault\Logs\
    echo.
) else (
    echo.
    echo Demo cancelled. You can post later with:
    echo   python linkedin_scheduler_complete.py post-now
    echo.
)

pause

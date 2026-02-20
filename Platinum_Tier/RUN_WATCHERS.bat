@echo off
echo ============================================================
echo Agentic AI Watchers - Gmail and LinkedIn Monitor
echo ============================================================
echo.
echo Monitors for Agentic AI content and can send emails/posts
echo Keywords: agentic, ai agent, autonomous ai, llm, claude, gpt
echo.

REM Check if .env file exists
if not exist "..\\.env" (
    echo ERROR: .env file not found!
    echo.
    echo Please run the credential setup first:
    echo   python Platinum_Tier\setup_credentials.py
    echo.
    pause
    exit /b 1
)

echo Select which watcher to run:
echo.
echo 1. LinkedIn Watcher (monitors feed for Agentic AI posts)
echo 2. Gmail Watcher (monitors inbox for Agentic AI emails)
echo 3. Both (in separate windows)
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting LinkedIn Watcher...
    python linkedin_watcher_playwright.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Gmail Watcher...
    python gmail_watcher_playwright.py
) else if "%choice%"=="3" (
    echo.
    echo Starting both watchers in separate windows...
    echo.
    echo LinkedIn: Checks every 2 minutes for Agentic AI posts
    echo Gmail: Checks every 3 minutes for Agentic AI emails
    echo.
    start "LinkedIn Watcher - Agentic AI" cmd /k "cd /d %~dp0 && python linkedin_watcher_playwright.py"
    timeout /t 2 >nul
    start "Gmail Watcher - Agentic AI" cmd /k "cd /d %~dp0 && python gmail_watcher_playwright.py"
    echo.
    echo Both watchers started in separate windows.
    echo Filtered content will be saved to Inbox\ folder.
    echo.
    echo Press any key to exit this window.
    pause
) else if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Please run again.
    pause
    exit /b 1
)

pause

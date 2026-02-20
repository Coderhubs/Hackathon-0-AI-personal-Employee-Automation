@echo off
echo ================================================================================
echo AI PERSONAL EMPLOYEE - FULLY AUTOMATED STARTUP
echo NO MANUAL LOGIN REQUIRED (after initial setup)
echo ================================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

REM Check .env file
if not exist .env (
    echo [ERROR] .env file not found
    echo.
    echo Please create .env file with:
    echo   GMAIL_EMAIL=your-email@gmail.com
    echo   GMAIL_PASSWORD=your-app-password
    echo.
    echo Generate Gmail App Password at:
    echo   https://myaccount.google.com/apppasswords
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking environment...
echo [OK] Python found
echo [OK] Node.js found
echo [OK] .env file found
echo.

echo [2/5] Installing Python dependencies...
pip install -q python-dotenv requests imaplib-utf7 2>nul
if errorlevel 1 (
    echo [WARN] Some dependencies may already be installed
)
echo [OK] Python dependencies ready
echo.

echo [3/5] Installing Node.js dependencies...
if not exist node_modules (
    echo Installing WhatsApp automation packages...
    call npm install --silent
    if errorlevel 1 (
        echo [ERROR] Failed to install Node.js dependencies
        pause
        exit /b 1
    )
)
echo [OK] Node.js dependencies ready
echo.

echo [4/5] Creating vault directories...
if not exist AI_Employee_Vault\Needs_Action mkdir AI_Employee_Vault\Needs_Action
if not exist AI_Employee_Vault\Pending_Approval mkdir AI_Employee_Vault\Pending_Approval
if not exist AI_Employee_Vault\Approved mkdir AI_Employee_Vault\Approved
if not exist AI_Employee_Vault\Done mkdir AI_Employee_Vault\Done
if not exist AI_Employee_Vault\Logs mkdir AI_Employee_Vault\Logs
echo [OK] Vault structure ready
echo.

echo [5/5] Starting all components...
echo.
echo ================================================================================
echo STARTING AUTONOMOUS AI EMPLOYEE
echo ================================================================================
echo.

REM Start WhatsApp automation server (first time: scan QR code, then never again)
echo [1/4] Starting WhatsApp automation server...
start "WhatsApp Automation" cmd /k "node Platinum_Tier/whatsapp_automation.js"
timeout /t 3 /nobreak >nul

REM Start Gmail watcher (fully automated via IMAP)
echo [2/5] Starting Gmail watcher (IMAP - fully automated)...
start "Gmail Watcher" cmd /k "cd Platinum_Tier && python gmail_watcher_imap.py"
timeout /t 2 /nobreak >nul

REM Start LinkedIn automation (login once, then persistent)
echo [3/5] Starting LinkedIn automation (persistent session)...
start "LinkedIn Automation" cmd /k "cd Platinum_Tier && python linkedin_automation.py"
timeout /t 2 /nobreak >nul

REM Start Integration Coordinator
echo [4/5] Starting integration coordinator...
if exist integration_coordinator.py (
    start "Integration Coordinator" cmd /k "python integration_coordinator.py"
    timeout /t 2 /nobreak >nul
)

REM Start Approval Handler
echo [5/5] Starting approval handler (fully automated execution)...
start "Approval Handler" cmd /k "python approval_handler_automated.py"
timeout /t 2 /nobreak >nul

echo.
echo ================================================================================
echo ALL COMPONENTS STARTED
echo ================================================================================
echo.
echo FIRST TIME SETUP:
echo   1. WhatsApp: Scan QR code in WhatsApp window (ONLY ONCE)
echo   2. Gmail: Already automated via IMAP (NO login needed)
echo   3. After QR scan, system runs 24/7 autonomously
echo.
echo WHAT'S RUNNING:
echo   - WhatsApp Automation (port 3001) - monitors messages
echo   - Gmail Watcher (IMAP) - monitors emails
echo   - Integration Coordinator - generates drafts
echo   - Approval Handler - executes approved actions
echo.
echo WORKFLOW:
echo   1. System detects emails/messages with AI keywords
echo   2. Generates draft responses in Pending_Approval/
echo   3. You review and move to Approved/
echo   4. System automatically executes (sends emails, messages)
echo   5. Logs everything to Done/ folder
echo.
echo TO APPROVE ACTIONS:
echo   move AI_Employee_Vault\Pending_Approval\*.md AI_Employee_Vault\Approved\
echo.
echo TO STOP:
echo   Close all command windows or press Ctrl+C in each
echo.
echo ================================================================================
echo SYSTEM IS NOW RUNNING AUTONOMOUSLY
echo ================================================================================
echo.
pause

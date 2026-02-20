@echo off
echo ========================================
echo Odoo Community Edition Setup
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [OK] Docker found
docker --version
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

echo ========================================
echo Starting Odoo Containers
echo ========================================
echo.

REM Navigate to Odoo directory
cd /d "%~dp0"

echo Starting PostgreSQL and Odoo containers...
docker-compose up -d

if errorlevel 1 (
    echo [ERROR] Failed to start containers
    pause
    exit /b 1
)

echo.
echo [OK] Containers started successfully
echo.

echo ========================================
echo Waiting for Odoo to Initialize
echo ========================================
echo.
echo This may take 30-60 seconds on first run...
echo.

REM Wait for Odoo to be ready
timeout /t 30 /nobreak

echo ========================================
echo Checking Container Status
echo ========================================
echo.

docker-compose ps

echo.
echo ========================================
echo Odoo Setup Complete!
echo ========================================
echo.
echo Odoo is now running at: http://localhost:8069
echo.
echo Default credentials:
echo   Database: demo (create on first access)
echo   Email: admin@example.com
echo   Password: admin
echo.
echo To access Odoo:
echo   1. Open browser: http://localhost:8069
echo   2. Create database named "demo"
echo   3. Set master password: admin
echo   4. Login with admin@example.com / admin
echo.
echo Useful commands:
echo   - View logs: docker-compose logs -f odoo
echo   - Stop Odoo: docker-compose down
echo   - Restart Odoo: docker-compose restart
echo   - Remove all data: docker-compose down -v
echo.
echo Opening browser...
start http://localhost:8069
echo.
pause

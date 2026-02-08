@echo off
REM Gold Tier Autonomous System Stop Script
REM Stops all running components

echo ========================================
echo Stopping Gold Tier Autonomous System
echo ========================================
echo.

REM Kill Python processes related to Gold Tier
taskkill /FI "WINDOWTITLE eq Gmail Watcher*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq LinkedIn Watcher*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Filesystem Watcher*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Autonomous Monitor*" /F >nul 2>&1

echo All Gold Tier components stopped.
echo.
pause

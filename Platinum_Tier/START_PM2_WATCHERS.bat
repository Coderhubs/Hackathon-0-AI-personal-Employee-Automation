@echo off
REM PM2 Watcher Startup Script for Platinum Tier AI Employee
REM Run this from the Platinum_Tier directory

echo ========================================
echo Starting Platinum Tier AI Employee
echo ========================================
echo.

REM Change to Platinum_Tier directory
cd /d "%~dp0"

echo [1/5] Starting Manager Agent...
pm2 start Agents\manager_agent.py --name "manager-agent" --interpreter python

echo [2/5] Starting Gmail Watcher...
pm2 start gmail_watcher.py --name "gmail-watcher" --interpreter python

echo [3/5] Starting LinkedIn Watcher...
pm2 start linkedin_watcher.py --name "linkedin-watcher" --interpreter python

echo [4/5] Starting Filesystem Watcher...
pm2 start filesystem_watcher.py --name "filesystem-watcher" --interpreter python

echo [5/5] Starting API Server...
pm2 start api_server.py --name "api-server" --interpreter python

echo.
echo ========================================
echo All watchers started!
echo ========================================
echo.
echo To view status: pm2 status
echo To view logs: pm2 logs
echo To stop all: pm2 stop all
echo To restart all: pm2 restart all
echo.

pm2 status

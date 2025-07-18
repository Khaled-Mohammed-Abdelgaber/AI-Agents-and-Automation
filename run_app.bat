@echo off
echo ========================================
echo   Article Automation Tool Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

REM Change to the script directory
cd /d "%~dp0"

REM Run the launcher
python run_app.py

echo.
echo Press any key to close...
pause >nul
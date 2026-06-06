@echo off
REM CC Camera Analytics - Cleanup Tool Launcher
REM This script launches the cleanup utility

echo.
echo ========================================
echo   CC Camera Analytics - Cleanup Tool
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if tkinter is available
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Tkinter is not installed
    echo Tkinter is required for the GUI interface
    echo.
    echo On Windows, tkinter should be included with Python
    echo Try reinstalling Python with "tcl/tk and IDLE" option checked
    echo.
    pause
    exit /b 1
)

echo Starting Cleanup Tool...
echo.

REM Run the cleanup tool
python "%~dp0cleanup_detections.py"

if errorlevel 1 (
    echo.
    echo [ERROR] Cleanup tool encountered an error
    pause
    exit /b 1
)

exit /b 0

@REM Made with Bob

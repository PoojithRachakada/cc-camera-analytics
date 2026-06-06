@echo off
title CC Camera Analytics - Starting...
color 0A
echo.
echo ========================================================
echo    CC CAMERA REAL-TIME ANALYTICS SYSTEM
echo    Performance Optimized Version
echo ========================================================
echo.
echo Starting camera analytics...
echo.
echo CONTROLS (after clicking video window):
echo   q - Quit
echo   h - Help
echo   f - Show status
echo   1-4 - Switch performance modes
echo   m - Toggle motion detection
echo.
echo ========================================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ========================================================
    echo ERROR: Failed to start application
    echo ========================================================
    echo.
    echo Possible reasons:
    echo 1. Python is not installed
    echo 2. Required packages are missing
    echo.
    echo To fix:
    echo 1. Install Python from python.org
    echo 2. Run INSTALL_DEPENDENCIES.bat
    echo.
    pause
) else (
    echo.
    echo Application closed successfully.
    timeout /t 3
)

@REM Made with Bob

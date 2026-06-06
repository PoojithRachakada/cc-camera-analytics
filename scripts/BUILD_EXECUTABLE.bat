@echo off
title CC Camera Analytics - Building Executable
color 0B
echo.
echo ========================================================
echo    CC CAMERA ANALYTICS - EXECUTABLE BUILDER
echo ========================================================
echo.
echo This will create a standalone executable file that users
echo can double-click to run without installing Python.
echo.
echo Requirements:
echo   - Python must be installed
echo   - PyInstaller will be installed if not present
echo.
echo The process may take 5-15 minutes depending on your system.
echo.
pause
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo ========================================================
echo Step 1: Installing PyInstaller...
echo ========================================================
echo.
pip install pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo ========================================================
echo Step 2: Installing required dependencies...
echo ========================================================
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
    echo The executable may not work properly
    echo.
)

echo.
echo ========================================================
echo Step 3: Building executable...
echo ========================================================
echo.
echo This may take several minutes. Please wait...
echo.

pyinstaller build_executable.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to build executable
    echo.
    echo Common issues:
    echo   1. Missing dependencies - run INSTALL.bat first
    echo   2. Antivirus blocking - temporarily disable it
    echo   3. Insufficient disk space - need at least 1GB free
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo Build Complete!
echo ========================================================
echo.
echo The executable has been created in the 'dist' folder:
echo   dist\CC_Camera_Analytics.exe
echo.
echo File size: Approximately 200-500 MB (includes all dependencies)
echo.
echo To distribute:
echo   1. Copy the entire 'dist' folder to target computer
echo   2. Users can double-click CC_Camera_Analytics.exe to run
echo   3. No Python installation required on target computer
echo.
echo Note: First run may take 10-20 seconds to start
echo.
pause

REM Open the dist folder
explorer dist

echo.
echo ========================================================
echo Next Steps:
echo ========================================================
echo.
echo 1. Test the executable by running:
echo    dist\CC_Camera_Analytics.exe
echo.
echo 2. If it works, you can distribute the 'dist' folder
echo.
echo 3. Users just need to double-click the .exe file
echo.
pause

@REM Made with Bob

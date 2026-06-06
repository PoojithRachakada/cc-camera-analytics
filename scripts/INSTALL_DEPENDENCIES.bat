@echo off
title CC Camera Analytics - Installing Dependencies
color 0B
echo.
echo ========================================================
echo    CC CAMERA ANALYTICS - DEPENDENCY INSTALLER
echo ========================================================
echo.
echo This will install required packages:
echo   - OpenCV (for camera and image processing)
echo   - NumPy (for numerical operations)
echo   - Ultralytics (for YOLOv8 - 80+ object detection)
echo.
echo This may take 5-10 minutes depending on your internet speed.
echo.
pause
echo.
echo ========================================================
echo Installing dependencies...
echo ========================================================
echo.

pip install --upgrade pip
pip install opencv-python opencv-contrib-python numpy

echo.
echo ========================================================
echo Installing YOLOv8 (for detecting 80+ objects)...
echo ========================================================
echo.
echo NOTE: If this fails with "Long Path" error:
echo   1. See ENABLE_LONG_PATHS.md for instructions
echo   2. Enable Windows Long Paths
echo   3. Run this installer again
echo.

pip install ultralytics

echo.
echo ========================================================
echo Installation Complete!
echo ========================================================
echo.
echo Next steps:
echo   1. Double-click START_CAMERA_ANALYTICS.bat to run
echo   2. Click on the video window
echo   3. Press 'h' for help
echo.
echo If YOLOv8 installation failed:
echo   - You can still use the app (detects people only)
echo   - To detect 80+ objects, see ENABLE_LONG_PATHS.md
echo.
pause

@REM Made with Bob

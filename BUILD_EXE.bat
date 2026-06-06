@echo off
title Building Standalone Executable
color 0B
echo.
echo ========================================================
echo    BUILDING STANDALONE EXECUTABLE
echo ========================================================
echo.
echo This creates CC_Camera_Analytics.exe that users can
echo run without Python installation.
echo.
echo Process takes 5-15 minutes...
echo.
pause

call scripts\BUILD_EXECUTABLE.bat

@REM Made with Bob

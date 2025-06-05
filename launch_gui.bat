@echo off
REM YouClip GUI Launcher for Windows
REM Double-click this file to launch YouClip GUI

echo Starting YouClip GUI...

REM Try python3 first, then python
python3 launch_gui.py 2>nul
if %errorlevel% neq 0 (
    python launch_gui.py 2>nul
    if %errorlevel% neq 0 (
        echo.
        echo Error: Python not found or YouClip failed to start
        echo.
        echo Please ensure:
        echo 1. Python 3.7+ is installed
        echo 2. You are running this from the YouClip directory
        echo 3. Dependencies are installed: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo YouClip GUI has closed.
pause 
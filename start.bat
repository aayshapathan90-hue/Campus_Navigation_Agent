@echo off
title Campus Navigation Assistant
cd /d "%~dp0"
echo ===================================================
echo     Launching Campus Navigation Assistant
echo ===================================================
echo.
echo Opening browser at http://127.0.0.1:5000 ...
start "" "http://127.0.0.1:5000"
echo Starting Flask web server...
echo Press Ctrl+C to stop the server anytime.
echo.
python app.py
pause

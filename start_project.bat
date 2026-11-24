
@echo off
title Smart Network Monitor Launcher

cd /d "%~dp0"

echo =====================================
echo   SMART NETWORK MONITORING SYSTEM
echo =====================================

echo Starting Network Monitor...
start "Network Monitor" "%ComSpec%" /k ""%~dp0.venv\Scripts\python.exe" "%~dp0monitor.py""

timeout /t 2 /nobreak >nul

echo Starting Flask Dashboard...
start "Flask Dashboard" "%ComSpec%" /k ""%~dp0.venv\Scripts\python.exe" "%~dp0app.py""

timeout /t 4 /nobreak >nul

echo Opening Dashboard...
start http://127.0.0.1:5000/

echo Project launched!






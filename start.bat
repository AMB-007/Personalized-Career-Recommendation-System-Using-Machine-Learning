@echo off
title Career Recommendation System
echo ============================================================
echo   AI Career Recommendation System
echo ============================================================
echo.

cd /d "%~dp0"

if exist "backend\venv\Scripts\python.exe" (
    echo [OK] Using backend virtual environment...
    backend\venv\Scripts\python.exe app.py
) else (
    echo [WARN] backend\venv not found. Trying system Python...
    python app.py
)

pause

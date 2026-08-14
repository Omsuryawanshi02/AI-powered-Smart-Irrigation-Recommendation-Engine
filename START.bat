@echo off
REM AquaSmart Startup Script
REM This script starts both the backend and frontend servers

setlocal enabledelayedexpansion

echo.
echo ================================
echo  AquaSmart - Startup Script
echo ================================
echo.

REM Get the project root directory
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

echo [INFO] Project root: %PROJECT_ROOT%

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [INFO] Python found: 
python --version

REM Check backend folder
if not exist "backend" (
    echo [ERROR] Backend folder not found
    pause
    exit /b 1
)

echo.
echo Starting AquaSmart services...
echo.

REM Start backend in a new window
echo [INFO] Starting backend server on http://localhost:8000
echo.
start "AquaSmart Backend" cmd /k "cd /d "%PROJECT_ROOT%backend" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend server if possible
if exist "frontend" (
    echo [INFO] Starting frontend development server on http://localhost:8080
    echo.
    start "AquaSmart Frontend" cmd /k "cd /d "%PROJECT_ROOT%frontend" && python -m http.server 8080"
    
    echo.
    echo ================================
    echo  Services Started!
    echo ================================
    echo.
    echo Frontend:  http://localhost:8080
    echo Backend:   http://localhost:8000
    echo.
    echo Open http://localhost:8080 in your browser
    echo.
    timeout /t 2 /nobreak
) else (
    echo [WARNING] Frontend folder not found
    echo.
    echo ================================
    echo  Backend Started!
    echo ================================
    echo.
    echo Backend API: http://localhost:8000
    echo.
    echo To view the frontend, open any HTML file from the frontend folder
    echo Or run: python -m http.server 8080 in the frontend folder
    echo.
)

echo.
echo Press any key to continue...
pause

# AquaSmart Startup Script (PowerShell)
# This script starts both the backend and frontend servers

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  AquaSmart - Startup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

Write-Host "[INFO] Project root: $projectRoot" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check backend folder
if (-not (Test-Path "backend")) {
    Write-Host "[ERROR] Backend folder not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting AquaSmart services..." -ForegroundColor Cyan
Write-Host ""

# Start backend
Write-Host "[INFO] Starting backend server on http://localhost:8000" -ForegroundColor Green
$backendPath = Join-Path $projectRoot "backend"
$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -PassThru -WindowStyle Normal

Write-Host "[INFO] Backend PID: $($backendProcess.Id)" -ForegroundColor Gray
Start-Sleep -Seconds 3

# Start frontend
if (Test-Path "frontend") {
    Write-Host "[INFO] Starting frontend development server on http://localhost:8080" -ForegroundColor Green
    $frontendPath = Join-Path $projectRoot "frontend"
    $frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; python -m http.server 8080" -PassThru -WindowStyle Normal
    
    Write-Host "[INFO] Frontend PID: $($frontendProcess.Id)" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  Services Started!" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Frontend:  http://localhost:8080" -ForegroundColor Green
    Write-Host "Backend:   http://localhost:8000" -ForegroundColor Green
    Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor Green
    Write-Host ""
    Write-Host "Open http://localhost:8080 in your browser" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "[WARNING] Frontend folder not found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  Backend Started!" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Backend API: http://localhost:8000" -ForegroundColor Green
    Write-Host "API Docs:    http://localhost:8000/docs" -ForegroundColor Green
    Write-Host ""
    Write-Host "To view the frontend, open any HTML file from the frontend folder" -ForegroundColor Yellow
    Write-Host "Or run: python -m http.server 8080 in the frontend folder" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Processes started. Close any terminal window to stop services." -ForegroundColor Cyan
Read-Host "Press Enter to keep terminal open"

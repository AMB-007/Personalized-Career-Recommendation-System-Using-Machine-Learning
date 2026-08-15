# PowerShell launcher for Career Recommendation System
Set-Location $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AI Career Recommendation System" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "backend\venv\Scripts\python.exe") {
    Write-Host "[OK] Activating backend virtual environment..." -ForegroundColor Green
    & "backend\venv\Scripts\activate.ps1"
    python app.py
} else {
    Write-Host "[WARN] backend\venv not found. Using system Python..." -ForegroundColor Yellow
    python app.py
}

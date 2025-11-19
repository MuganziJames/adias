# Setup script for ADIAS - PowerShell version
# Creates virtual environment and installs dependencies

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ADIAS Setup - Creating Virtual Environment" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Red
    pause
    exit 1
}

# Create virtual environment
Write-Host "[2/4] Creating virtual environment 'venv'..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "Virtual environment created successfully!" -ForegroundColor Green
Write-Host ""

# Activate virtual environment and install packages
Write-Host "[3/4] Installing required packages..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install packages" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""

Write-Host "[4/4] Verifying installation..." -ForegroundColor Yellow
pip list
Write-Host ""

Write-Host "============================================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Virtual environment created at: $PWD\venv" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the environment, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run ADIAS:" -ForegroundColor Yellow
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
Write-Host "To schedule automated execution:" -ForegroundColor Yellow
Write-Host "  python scheduler.py" -ForegroundColor White
Write-Host ""
Write-Host "Don't forget to download ITU data files to the data/ folder!" -ForegroundColor Magenta
Write-Host ""
pause

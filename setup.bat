@echo off
REM Setup script for ADIAS - Automated Digital Inequality Assessment System
REM Creates virtual environment and installs dependencies

echo ============================================================
echo ADIAS Setup - Creating Virtual Environment
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment 'venv'...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

REM Activate virtual environment and install packages
echo [3/4] Installing required packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo.

echo [4/4] Verifying installation...
pip list
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Virtual environment created at: %CD%\venv
echo.
echo To activate the environment, run:
echo   venv\Scripts\activate
echo.
echo To run ADIAS:
echo   python main.py
echo.
echo To schedule automated execution:
echo   python scheduler.py
echo.
echo Don't forget to download ITU data files to the data/ folder!
echo.
pause

@echo off
REM ====================================
REM AKBAR JAYA CASHIER - IMPROVED UI
REM ====================================

echo.
echo ================================================
echo    AKBAR JAYA CASHIER SYSTEM (IMPROVED UI)
echo    Starting application...
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing PyQt6...
    pip install PyQt6
)

python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing pandas...
    pip install pandas
)

echo.
echo All dependencies ready!
echo.
echo ================================================
echo    Launching Improved Cashier System...
echo    Features:
echo    - Colorful square buttons
echo    - Large fonts for elderly users
echo    - Better receipt alignment
echo    - Color-coded categories
echo ================================================
echo.

REM Run the improved version
python main_prog_improved.py

REM If there's an error, keep the window open
if errorlevel 1 (
    echo.
    echo ================================================
    echo    ERROR OCCURRED!
    echo ================================================
    pause
)

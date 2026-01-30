@echo off
setlocal

echo == YT Short Clipper for Windows ==

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo Checking dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Run the application
echo Launching application...
python app.py

pause
endlocal

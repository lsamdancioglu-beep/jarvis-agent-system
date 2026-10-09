@echo off
REM JARVIS Agent System Setup Script for Windows

echo.
echo 🤖 JARVIS Agent System Setup
echo ============================="
echo.

REM Check if Python 3 is installed
python3 --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo ✓ Python 3 found: 
for /f "tokens=*" %%i in ('python3 --version') do echo %%i
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if not exist "venv" (
    python3 -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

echo.
echo 📥 Installing dependencies...
python3 -m pip install -q --upgrade pip
python3 -m pip install -q -r requirements.txt
echo ✓ Dependencies installed

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo   Option 1 - CLI Mode:
echo     python3 main.py
echo.
echo   Option 2 - Web Dashboard:
echo     python3 dashboard.py
echo     Then open: http://localhost:5000
echo.
echo Try these commands in CLI mode:
echo   JARVIS^> agents
echo   JARVIS^> sessions
echo   JARVIS^> analyze the repository
echo   JARVIS^> dashboard
echo.
pause

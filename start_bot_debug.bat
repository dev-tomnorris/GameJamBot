@echo off
title Game Jam Assistant Bot - Debug Mode
color 0A

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ==========================================
echo   Game Jam Assistant Bot - Debug Mode
echo ==========================================
echo.

REM Check if Python is installed
echo [CHECK] Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python and try again.
    echo.
    pause
    exit /b 1
)
python --version
echo.

REM Check if main.py exists
echo [CHECK] Looking for main.py...
if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo Make sure you're running this from the project directory.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)
echo [OK] main.py found
echo.

REM Check if .env exists
echo [CHECK] Looking for .env file...
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Make sure you have created .env with your Discord token.
    echo The bot will likely fail to start without it.
    echo.
) else (
    echo [OK] .env file found
    echo.
)

REM Check if requirements are installed (optional check)
echo [CHECK] Verifying discord.py is installed...
python -c "import discord" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] discord.py might not be installed!
    echo Run: pip install -r requirements.txt
    echo.
) else (
    echo [OK] discord.py is installed
    echo.
)

echo ==========================================
echo Starting bot...
echo Press Ctrl+C to stop the bot
echo ==========================================
echo.

python main.py

echo.
echo ==========================================
echo Bot has stopped.
echo Exit code: %errorlevel%
echo ==========================================
echo.
if %errorlevel% neq 0 (
    echo [ERROR] Bot exited with error code %errorlevel%
    echo Check the error messages above for details.
) else (
    echo [OK] Bot exited normally
)
echo.
pause

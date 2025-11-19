@echo off
REM ============================================================================
REM Document Upload Service - Windows Setup Script
REM ============================================================================
REM This script sets up the environment for the document upload service
REM ============================================================================

echo.
echo ============================================================================
echo   Document Upload Service - Setup
echo ============================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo         Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python Version: %PYTHON_VERSION%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venvWindows" (
    echo [1/3] Creating virtual environment...
    python -m venv venvWindows
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo       ✓ Virtual environment created
    echo.
) else (
    echo [INFO] Virtual environment already exists
    echo.
)

REM Activate virtual environment
echo [2/3] Activating virtual environment...
call venvWindows\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo       ✓ Virtual environment activated
echo.

REM Install dependencies
echo [3/3] Installing dependencies...
echo       This may take a few minutes...
python -m pip install --upgrade pip
pip install -r windowsEnv_requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo       ✓ Dependencies installed successfully
echo.

REM Copy environment file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    copy .env.windows .env
    echo       ✓ Created .env file
    echo       Please review and update the configuration in .env
    echo.
) else (
    echo [INFO] .env file already exists
    echo.
)

echo ============================================================================
echo   Setup Complete!
echo ============================================================================
echo.
echo   Next steps:
echo   1. Review and update .env configuration
echo   2. Run test_upload.bat to test the service
echo   3. Use upload_document.bat to upload files
echo.
echo   Example usage:
echo   upload_document.bat my_file.cpp
echo   upload_document.bat document.pdf
echo.
echo ============================================================================

pause

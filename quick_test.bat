@echo off
REM ============================================================================
REM Document Upload Service - Quick Local Test (No Upload)
REM ============================================================================
REM Tests the splitting functionality without uploading to n8n
REM ============================================================================

echo.
echo ============================================================================
echo   Document Upload Service - Quick Test
echo ============================================================================
echo.

REM Check if virtual environment exists
if not exist "venvWindows\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo         Please run setup_document_uploader.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venvWindows\Scripts\activate.bat

REM Run the quick test
python quick_test.py

pause
